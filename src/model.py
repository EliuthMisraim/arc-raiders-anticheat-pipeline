import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import skl2onnx
from skl2onnx.common.data_types import FloatTensorType
import onnx
import os

class AntiCheatModel:
    def __init__(self, n_estimators=100):
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        self.features = ['velocity', 'ping', 'packet_loss', 'vp_ratio', 'avg_velocity', 'std_velocity', 'windowed_ratio', 'acceleration', 'avg_acceleration', 'jitter']
        self.label = 'label'

    def train(self, data_path):
        df = pd.read_csv(data_path)
        X = df[self.features]
        y = df[self.label]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print(f"Training model on {len(X_train)} samples...")
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        print("Model Evaluation:")
        print(classification_report(y_test, y_pred))
        
        return self.model

    def export_onnx(self, model_path="anti_cheat_model.onnx"):
        initial_type = [('float_input', FloatTensorType([None, len(self.features)]))]
        onx = skl2onnx.convert_sklearn(self.model, initial_types=initial_type, target_opset=12)
        
        with open(model_path, "wb") as f:
            f.write(onx.SerializeToString())
        
        print(f"Model exported to {model_path}")
        return model_path

if __name__ == "__main__":
    # Quick test if data exists
    if os.path.exists("processed_telemetry.csv"):
        ac_model = AntiCheatModel()
        labels = ac_model.train("processed_telemetry.csv")
        ac_model.export_onnx()
    else:
        print("Data not found for training. Run pipeline.py first.")
