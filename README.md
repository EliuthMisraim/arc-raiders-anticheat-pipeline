# ARC Raiders: Real-Time Anti-Cheat System 🛡️🤖
### Data Scientist / Engineer Pipeline for Anomaly Detection

[![Repo Status](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/EliuthMisraim/arc-raiders-anticheat-pipeline)

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Apache Beam](https://img.shields.io/badge/Apache%20Beam-GCP%20Dataflow-orange.svg)
![ONNX](https://img.shields.io/badge/Model-ONNX%20Runtime-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

En un entorno competitivo como **ARC Raiders**, la integridad de la partida es el activo más valioso. Este repositorio contiene un pipeline avanzado de ingeniería de datos y ciencia de datos para identificar *cheaters* mediante el análisis de comportamiento server-side.

---

## 📖 Tabla de Contenidos
1. [🚀 Introducción](#introducción)
2. [🏗️ Arquitectura del Systema](#arquitectura-del-sistema)
3. [🛠️ Stack Tecnológico](#stack-tecnológico)
4. [⚙️ Pipeline de Datos y Características](#pipeline-de-datos)
5. [📥 Instalación y Uso](#instalación-y-uso)
6. [🔌 Guía de Integración (Go/Python)](#guía-de-integración)

---

## 🚀 Introducción

Este sistema está diseñado para detectar comportamientos anómalos sin depender de escaneos en el cliente. Se centra en la **física del movimiento** y la **frecuencia de red**.

### El Desafío: Lag vs. Cheat
La precisión es fundamental. Implementamos métricas avanzadas para distinguir entre un jugador con mala conexión y un atacante real:
- **VP_Ratio**: Velocity-to-Ping Ratio original.
- **Windowed Metrics**: Promedios y variaciones sobre ventanas de tiempo para filtrar picos de lag.
- **Jitter Detection**: Análisis de cambios bruscos de dirección y aceleración (característico de aimbots).

---

## 🏗️ Arquitectura del Sistema

El proyecto está organizado de manera modular para facilitar el testing y la producción:

```text
├── src/
│   ├── data_sim.py    # Generación de telemetría con perfiles físicos
│   ├── pipeline.py    # Procesamiento con Apache Beam (Feature Engineering)
│   ├── model.py       # Entrenamiento de Random Forest y exportación ONNX
│   └── inference.py   # Motor de inferencia listo para producción
├── tests/             # Suite de pruebas funcionales y de inferencia
├── INTEGRATION_GUIDE.md # Guía para desarrolladores de backend (Go/Python)
└── run_simulation.py  # Ejecutor end-to-end
```

---

## 🛠️ Stack Tecnológico

| Capa | Herramienta |
| :--- | :--- |
| **Ingeniería de Datos** | Apache Beam (DirectRunner/Dataflow) |
| **Ciencia de Datos** | Pandas, NumPy, Scikit-Learn |
| **Interoperabilidad** | ONNX Runtime, SKL2ONNX |
| **Testing** | Pytest |

---

## ⚙️ Pipeline de Datos y Características

### 1. Generación de Telemetría Realista
Simulamos perfiles con comportamiento físico:
* **Legit:** Movimientos suaves y velocidades consistentes.
* **Laggy:** Picos de velocidad y teletransportación debido a pérdida de paquetes.
* **Cheater (Aimbot/Speedhack):** Aceleraciones imposibles y cambios de dirección instantáneos (*Snapping*).

### 2. Ingeniería de Atributos (10 Features)
El pipeline calcula métricas críticas en ventanas de tiempo:
- **Spatial Features:** Seguimiento de coordenadas X, Y.
- **Acceleration:** Derivada de la velocidad respecto al tiempo.
- **Heading Jitter:** Desviación estándar de los cambios de ángulo de movimiento.
- **Windowed Ratio:** Normalización de velocidad media vs latencia media.

---

## 📥 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/EliuthMisraim/arc-raiders-anticheat-pipeline.git
   cd arc-raiders-anticheat-pipeline
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar Simulación Completa:**
   Este comando genera datos, procesa el pipeline, entrena el modelo y verifica la inferencia.
   ```bash
   python run_simulation.py
   ```

---

## 🔌 Guía de Integración

El modelo se exporta automáticamente como `anti_cheat_model.onnx`. Esto permite que el servidor del juego (escrito en **Go**) realice detecciones con latencia mínima.

Consulta la **[INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)** para ver ejemplos de código en Go y Python.
