from src.data_sim import generate_raw_events
from src.pipeline import run_pipeline
from src.model import AntiCheatModel
from src.inference import AntiCheatInference
import os

def main():
    print("=== ARC Raiders Anti-Cheat Simulation ===")
    
    # 1. Generate Telemetry
    print("\n1. Generating synthetic telemetry...")
    raw_data = generate_raw_events(n=5000)
    
    # 2. Run Processing Pipeline
    print("\n2. Running Apache Beam processing pipeline...")
    processed_file = run_pipeline(raw_data)
    
    # 3. Train and Export Model
    print("\n3. Training Random Forest model...")
    ac_model = AntiCheatModel()
    ac_model.train(processed_file)
    model_path = ac_model.export_onnx()
    
    # 4. End-to-End Test (Inference)
    print("\n4. Running functional inference test...")
    infer = AntiCheatInference(model_path)
    
    # Test cases: [velocity, ping, packet_loss, vp_ratio, avg_velocity, std_velocity, windowed_ratio, acceleration, avg_acceleration, jitter]
    test_cases = {
        "Legit Player": [5.0, 30.0, 0.1, 5.0/31.0, 5.0, 0.2, 5.0/31.0, 0.5, 0.4, 0.05],
        "Laggy Player": [25.0, 450.0, 5.0, 25.0/451.0, 20.0, 10.0, 20.0/401.0, 2.0, 1.5, 0.3],
        "Speedhacker": [55.0, 20.0, 0.05, 55.0/21.0, 54.0, 1.0, 54.0/21.0, 5.0, 4.5, 2.0]
    }
    
    print("\nResults:")
    import numpy as np
    simulation_results = {}
    for name, features in test_cases.items():
        pred, prob = infer.predict([features])
        # skl2onnx returns a list of dictionaries for probabilities if there are multiple classes
        if isinstance(prob[0], dict):
            prob_val = float(prob[0].get(pred[0], 0.0))
        else:
            prob_val = float(np.max(prob[0]))
            
        print(f"[{name}] Predicted: {pred[0]} (Confidence: {prob_val:.2f})")
        simulation_results[name] = {"prediction": str(pred[0]), "confidence": prob_val}
    
    import json
    with open("simulation_results.json", "w") as f:
        json.dump(simulation_results, f, indent=4)
    print("\nResults saved to simulation_results.json")

if __name__ == "__main__":
    main()
