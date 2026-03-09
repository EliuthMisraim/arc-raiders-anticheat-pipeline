# Anti-Cheat Integration Guide

This guide describes how to integrate the `anti_cheat_model.onnx` into your backend services.

## Model Overview

The model is a Random Forest classifier exported in ONNX format. It accepts a tensor of shape `[BatchSize, 10]` and returns predicted labels (`legit`, `laggy`, `cheater`) and their associated probabilities.

### Input Features (Requirement: Ordering is critical)

The input tensor must contain exactly 10 features in this order:

1.  `velocity`: Current move speed.
2.  `ping`: Latentcy in ms.
3.  `packet_loss`: % of lost packets.
4.  `vp_ratio`: `velocity / (ping + 1)`.
5.  `avg_velocity`: Mean velocity over the last window of events.
6.  `std_velocity`: Standard deviation of velocity over the window.
7.  `windowed_ratio`: `avg_velocity / (avg_ping + 1)`.
8.  `acceleration`: `(v2 - v1) / dt`.
9.  `avg_acceleration`: Mean acceleration over the window.
10. `jitter`: Standard deviation of movement heading changes.

## Integration in Go (Recommended for ARC Raiders Server)

Use the `onnxruntime-go` library.

```go
package main

import (
	"fmt"
	ort "github.com/yalue/onnxruntime_go"
)

func main() {
	// Initialize runtime
	ort.SetSharedLibraryPath("path/to/onnxruntime.dll")
	ort.InitializeRuntime()
	defer ort.DestroyRuntime()

	// Load model
	session, _ := ort.NewAdvancedSession("anti_cheat_model.onnx", 
        []string{"float_input"}, []string{"output_label", "output_probability"}, nil)
	defer session.Destroy()

	// Example Input: 10 features
	inputData := []float32{60.0, 20.0, 0.0, 2.85, 60.0, 0.0, 2.85, 5.0, 5.0, 0.5}
	inputTensor, _ := ort.NewTensor[float32](ort.NewShape(1, 10), inputData)
	defer inputTensor.Destroy()

	// Run Inference
	output, _ := session.Run([]ort.ArbitraryTensor{inputTensor})
	fmt.Printf("Detection Result: %v\n", output[0].GetData().([]string)[0])
}
```

## Integration in Python

```python
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("anti_cheat_model.onnx")
input_name = session.get_inputs()[0].name

# Shape (N, 10)
features = np.array([[60.0, 20.0, 0.05, 2.85, 60.0, 0.0, 2.85, 5.0, 4.0, 0.5]], dtype=np.float32)
preds, probs = session.run(None, {input_name: features})

print(f"Prediction: {preds[0]}")
```
