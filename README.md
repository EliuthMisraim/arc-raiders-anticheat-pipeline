# ARC Raiders: Real-Time Anti-Cheat System 🛡️🤖
### Data Scientist / Engineer Pipeline for Anomaly Detection

[![Repo Status](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/EliuthMisraim/arc-raiders-anticheat-pipeline)

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Apache Beam](https://img.shields.io/badge/Apache%20Beam-GCP%20Dataflow-orange.svg)
![ONNX](https://img.shields.io/badge/Model-ONNX%20Runtime-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

En un entorno competitivo como **ARC Raiders**, la integridad de la partida es el activo más valioso. Este repositorio contiene el pipeline completo de ingeniería de datos y ciencia de datos para identificar *cheaters* (Speedhacks) diferenciándolos de jugadores con problemas de red (*Lag*).

---

## 📖 Tabla de Contenidos
1. [🚀 Introducción](#introducción)
2. [🏗️ Arquitectura del Sistema](#arquitectura-del-sistema)
3. [🛠️ Stack Tecnológico](#stack-tecnológico)
4. [⚙️ Pipeline de Datos](#pipeline-de-datos)
5. [📥 Instalación y Uso](#instalación-y-uso)
6. [El Puente a Producción (Go)](#el-puente-a-producción-go)

---

## 🚀 Introducción

Este sistema no se basa en escaneo de archivos locales (Client-side), sino en el **Análisis de Comportamiento Server-Side**. 
El desafío principal es la **precisión**: ¿Cómo evitamos banear a un jugador que parece teletransportarse pero solo tiene una mala conexión? 

La respuesta está en nuestra métrica propietaria: el **VP_Ratio** (Velocity-to-Ping Ratio).

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue un flujo de datos moderno y desacoplado:



1.  **Ingesta:** Simulación de eventos de telemetría (velocidad, ping, pérdida de paquetes).
2.  **Procesamiento:** Pipeline con **Apache Beam** para Feature Engineering en tiempo real.
3.  **Modelado:** Clasificador Random Forest entrenado para distinguir perfiles maliciosos.
4.  **Interoperabilidad:** Exportación a **ONNX** para integración con microservicios en Go.

---

## 🛠️ Stack Tecnológico

| Capa | Herramienta |
| :--- | :--- |
| **Procesamiento** | Apache Beam |
| **Análisis** | Pandas, NumPy, Seaborn |
| **Machine Learning** | Scikit-Learn |
| **Interoperabilidad** | ONNX, SKL2ONNX |

---

## ⚙️ Pipeline de Datos

### 1. Generación de Telemetría
Simulamos tres tipos de perfiles de usuario basados en la física del motor de juego y la latencia de red:
* **Legit:** Comportamiento estándar.
* **Laggy:** Picos de velocidad debidos a alta latencia (Falsos Positivos comunes).
* **Cheater:** Velocidad extrema con baja latencia (Anomalía real).

### 2. Feature Engineering (Apache Beam)
Calculamos el ratio crítico para la toma de decisiones:
$VP\_Ratio = velocity / (ping + 1)$

### 3. Visualización y Análisis
El análisis exploratorio muestra que, mientras los jugadores con lag tienen velocidades altas, su **VP_Ratio** se mantiene bajo, permitiendo una separación clara de los atacantes reales.



---

## 📥 Instalación y Uso

Sigue estos pasos para replicar el entorno de desarrollo y ejecutar el pipeline de detección:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/EliuthMisraim/arc-raiders-anticheat-pipeline.git](https://github.com/EliuthMisraim/arc-raiders-anticheat-pipeline.git)
   cd arc-raiders-anticheat-pipeline

Instalar dependencias:

Bash
pip install apache-beam[gcp] skl2onnx onnxruntime scikit-learn seaborn pandas numpy
Ejecutar el pipeline:
Ejecuta el script principal o el notebook para generar el archivo anti_cheat_model.onnx.
