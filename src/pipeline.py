import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import pandas as pd
import numpy as np

class AntiCheatTransform(beam.DoFn):
    def process(self, element):
        """
        Base transformation: Cleaning and basic VP_Ratio.
        """
        v = element['velocity']
        p = element['ping']
        
        ratio = v / (p + 1)
        
        yield {
            'player_id': element['player_id'],
            'x': element['x'],
            'y': element['y'],
            'velocity': float(v),
            'ping': float(p),
            'packet_loss': float(element['packet_loss']),
            'vp_ratio': float(ratio),
            'label': element['label'],
            'timestamp': element['timestamp']
        }

class WindowedFeatures(beam.DoFn):
    def process(self, element):
        """
        Calculates windowed metrics: avg, std, and derivative features (acceleration, jitter).
        """
        player_id, events = element
        sorted_events = sorted(events, key=lambda x: x['timestamp'])
        
        velocities = []
        accelerations = []
        headings = []
        
        for i in range(len(sorted_events)):
            e = sorted_events[i]
            velocities.append(e['velocity'])
            
            if i > 0:
                prev = sorted_events[i-1]
                dt = max(e['timestamp'] - prev['timestamp'], 0.001)
                
                # Acceleration
                accel = abs(e['velocity'] - prev['velocity']) / dt
                accelerations.append(accel)
                
                # Heading Change (Jitter)
                dx = e['x'] - prev['x']
                dy = e['y'] - prev['y']
                heading = np.arctan2(dy, dx)
                headings.append(heading)
            else:
                accelerations.append(0.0)
                headings.append(0.0)

        # Calculate Heading Jitter (Standard deviation of heading changes)
        heading_changes = []
        for i in range(1, len(headings)):
            diff = abs(headings[i] - headings[i-1])
            if diff > np.pi: diff = 2*np.pi - diff # Wrap around
            heading_changes.append(diff)
            
        jitter = np.std(heading_changes) if heading_changes else 0.0
        avg_accel = np.mean(accelerations)
        
        avg_v = np.mean(velocities)
        std_v = np.std(velocities)
        avg_p = np.mean([e['ping'] for e in sorted_events])
        windowed_ratio = avg_v / (avg_p + 1)
        
        for i, e in enumerate(sorted_events):
            e['avg_velocity'] = float(avg_v)
            e['std_velocity'] = float(std_v)
            e['windowed_ratio'] = float(windowed_ratio)
            e['acceleration'] = float(accelerations[i])
            e['avg_acceleration'] = float(avg_accel)
            e['jitter'] = float(jitter)
            yield e

def run_pipeline(input_data, output_path="processed_telemetry.csv"):
    options = PipelineOptions(runner='DirectRunner')
    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | "CreateData" >> beam.Create(input_data)
            | "TransformFeatures" >> beam.ParDo(AntiCheatTransform())
            | "AddKeys" >> beam.Map(lambda x: (x['player_id'], x))
            | "GroupByPlayer" >> beam.GroupByKey()
            | "CalculateWindowed" >> beam.ParDo(WindowedFeatures())
            | "ToDataFrame" >> beam.combiners.ToList()
            | "SaveToCSV" >> beam.Map(lambda x: pd.DataFrame(x).to_csv(output_path, index=False))
        )
    return output_path

if __name__ == "__main__":
    from data_sim import generate_raw_events
    test_data = generate_raw_events(100)
    run_pipeline(test_data, "test_output.csv")
    print("Pipeline executed successfully. Output saved to test_output.csv")
