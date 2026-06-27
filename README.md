# frame-particle-tracking-otsu
Detección automática del centroide de una partícula en secuencias de video mediante umbralado Otsu y análisis de contornos. Guarda las coordenadas (x,y) por frame en archivos .dat.
# Particle centroid detection from video frames (Otsu + contour tracking)

Extrae de forma automática las coordenadas (x, y) del centroide de una partícula en una secuencia de imágenes (frames) usando umbralado automático de Otsu, filtro Gaussiano y selección del contorno más grande. Ideal para análisis de movimiento browniano, difusión o tracking de objetos aislados en microscopía.

---

## 🧠 ¿Qué hace el código?

1. **Carga** todos los archivos `frame_*.png` de una carpeta de entrada.
2. **Suaviza** cada imagen con un filtro Gaussiano para reducir el ruido de píxel.
3. **Aplica umbralado automático de Otsu** (con inversión binaria) para separar la partícula (oscura sobre fondo claro) del fondo.
4. **Encuentra el contorno más grande**, que se asume corresponde a la partícula de interés.
5. **Calcula el centroide** mediante momentos espaciales (cv2.moments).
6. **Guarda las coordenadas** en archivos `.dat` individuales por frame, con formato tabulado.

---

## 📦 Requisitos

- Python ≥ 3.7
- OpenCV (`cv2`)
- NumPy

Instalación rápida:

```bash
pip install opencv-python numpy
