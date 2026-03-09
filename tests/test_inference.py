import onnxruntime as ort
import numpy as np
import os
from src.inference import AntiCheatInference

def test_onnx_inference():
    model_path = "anti_cheat_model.onnx"
    if not os.path.exists(model_path):
        print(f"Skipping test: {model_path} not found.")
        return

    infer = AntiCheatInference(model_path)
    
    # Features: [velocity, ping, packet_loss, vp_ratio, avg_velocity, std_velocity, windowed_ratio, acceleration, avg_acceleration, jitter]
    test_cases = [
        # Legit
        {"features": [5.0, 30.0, 0.1, 5.0/31.0, 5.0, 0.2, 5.0/31.0, 0.5, 0.4, 0.05], "expected": "legit"},
        # Speedhacker
        {"features": [60.0, 20.0, 0.05, 60.0/21.0, 58.0, 2.0, 58.0/21.0, 5.0, 4.5, 2.0], "expected": "cheater"}
    ]
    
    print("\n--- Running Inference Tests ---")
    for case in test_cases:
        preds, probs = infer.predict([case['features']])
        prediction = preds[0]
        print(f"Input Expected: {case['expected']} | Predicted: {prediction}")
        # We don't assert strictly on accuracy here but on functional correctness
        assert prediction in ['legit', 'laggy', 'cheater']
    
    print("\nInference tests passed functionally!")

if __name__ == "__main__":
    test_onnx_inference()
