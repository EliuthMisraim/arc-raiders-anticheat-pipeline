import onnxruntime as ort
import numpy as np

class AntiCheatInference:
    def __init__(self, model_path="anti_cheat_model.onnx"):
        print(f"Loading ONNX model from {model_path}...")
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.label_name = self.session.get_outputs()[0].name
        self.probs_name = self.session.get_outputs()[1].name

    def predict(self, features):
        """
        features: numpy array or list of shape (N, 10)
        """
        if isinstance(features, list):
            if len(features[0]) < 10:
                print(f"Warning: Expected 10 features, got {len(features[0])}. Padding with zeros.")
                features = [f + [0.0] * (10 - len(f)) for f in features]
            features = np.array(features).astype(np.float32)
        
        preds, probs = self.session.run([self.label_name, self.probs_name], {self.input_name: features})
        return preds, probs

if __name__ == "__main__":
    import os
    if os.path.exists("anti_cheat_model.onnx"):
        infer = AntiCheatInference()
        # Features: [velocity, ping, packet_loss, vp_ratio, avg_velocity, std_velocity, windowed_ratio, acceleration, avg_acceleration, jitter]
        sample = [[60.0, 20.0, 0.05, 2.85, 60.0, 0.0, 2.85, 5.0, 4.0, 0.5]]
        prediction, confidence = infer.predict(sample)
        print(f"Prediction: {prediction}, Confidence: {confidence}")
    else:
        print("Model file not found. Run model.py first.")
