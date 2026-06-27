# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 13:45:00 2026

@author: mjorg
"""

import cv2
import numpy as np
import os
import glob

# ------------------------------------------------------------
# Parámetros (ajusta solo si Otsu no separa bien)
# ------------------------------------------------------------
gaussian_blur = 5        # tamaño del kernel gaussiano (debe ser impar, p. ej. 3,5,7)
# Puedes probar 7 si hay mucho ruido, 3 si la partícula es muy nítida.

carpeta_frames = r"C:\Users\mjorg\Desktop\memorias\M2\frames"
carpeta_resultados = r"C:\Users\mjorg\Desktop\memorias\M2\resultados"
os.makedirs(carpeta_resultados, exist_ok=True)

# Obtener lista de imágenes ordenadas
imagenes = sorted(glob.glob(os.path.join(carpeta_frames, "frame_*.png")))
print(f"Frames encontrados: {len(imagenes)}")

for idx, ruta_img in enumerate(imagenes):
    # Leer en escala de grises
    img = cv2.imread(ruta_img, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"No se pudo leer {ruta_img}")
        continue

    # 1) Suavizar con Gaussiana para eliminar ruido de píxel
    suave = cv2.GaussianBlur(img, (gaussian_blur, gaussian_blur), 0)

    # 2) Umbral automático (Otsu). Asume dos clases: fondo claro / partícula oscura
    _, mask = cv2.threshold(suave, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3) Quedarnos con la región más grande (la partícula)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M["m00"] > 0:
            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]
        else:
            cx, cy = np.nan, np.nan
    else:
        cx, cy = np.nan, np.nan

    # Guardar coordenadas (un archivo .dat por frame)
    nombre_base = os.path.splitext(os.path.basename(ruta_img))[0]
    archivo_salida = os.path.join(carpeta_resultados, nombre_base + ".dat")
    if not np.isnan(cx):
        np.savetxt(archivo_salida, np.array([[cx, cy]]), fmt="%.3f", delimiter="\t",
                   header="x\ty")
    else:
        np.savetxt(archivo_salida, np.array([[np.nan, np.nan]]), fmt="%.3f",
                   delimiter="\t", header="No detectada")

    if (idx+1) % 50 == 0:
        print(f"Procesados {idx+1}/{len(imagenes)}...")

print("¡Listo! Coordenadas guardadas en:", carpeta_resultados)