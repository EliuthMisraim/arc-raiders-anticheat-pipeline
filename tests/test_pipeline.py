import pytest
from src.data_sim import generate_raw_events
from src.pipeline import run_pipeline
import pandas as pd
import os

def test_pipeline_execution():
    """
    Tests that the pipeline runs and produces the expected columns.
    """
    test_data = generate_raw_events(n=10)
    output_path = "test_results.csv"
    
    if os.path.exists(output_path):
        os.remove(output_path)
        
    run_pipeline(test_data, output_path)
    
    assert os.path.exists(output_path)
    
    df = pd.read_csv(output_path)
    expected_cols = ['player_id', 'velocity', 'ping', 'packet_loss', 'vp_ratio', 
                     'label', 'timestamp', 'avg_velocity', 'std_velocity', 'windowed_ratio']
    
    for col in expected_cols:
        assert col in df.columns
    
    assert len(df) == 10

if __name__ == "__main__":
    test_pipeline_execution()
    print("Pipeline test passed!")
