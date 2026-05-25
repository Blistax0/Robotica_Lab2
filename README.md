# Laboratorio 2: Navegación reactiva con filtrado y fusión de sensores en Webots
**Integrantes**: Felipe Chávez Gonzalez - Sofía Mena Cortés - Kamila Leiva Morales

## Objetivo
El objetivo de este laboratorio es implementar un sistema básico de navegación reactiva en Webots para un robot móvil diferencial (e-punk), utilizando sensores de distancia y encoders de rueda.
Se aplica filtrado sobre las mediciones directas y se emplea un filtro Kalman para estimar la distancia frontal a los obtaculos y mejorar la toma de decisiones en tiempo real.

## Descripción
En este laboratorio se implementó el control de un robot móvil diferencial (e-puck) utilizando el simulador Webots y el lenguaje Python.

Se combinaron sensores de proximidad, encoders y técnicas de filtrado para permitir que el robot detecte obstáculos y navegue de forma autónoma en un espacion con obstáculos. Además se aplicó un filtro de Kalman para mejorar la estimación de proximidad frontal, reduciendo el efecto del ruido en las mediciones de los sensores.


