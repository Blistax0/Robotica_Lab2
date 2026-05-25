# Laboratorio 2: Navegación reactiva con filtrado y fusión de sensores en Webots
**Integrantes**: Felipe Chávez Gonzalez - Sofía Mena Cortés - Kamila Leiva Morales

## Objetivo
El objetivo de este laboratorio es implementar un sistema básico de navegación reactiva en Webots para un robot móvil diferencial (e-puck), utilizando sensores de distancia y encoders de rueda.
Se aplica filtrado sobre las mediciones directas y se emplea un filtro Kalman para estimar la distancia frontal a los obstaculos y mejorar la toma de decisiones en tiempo real.

## Descripción
En este laboratorio se implementó el control de un robot móvil diferencial (e-puck) utilizando el simulador Webots y el lenguaje Python.

Se combinaron sensores de proximidad, encoders y técnicas de filtrado para permitir que el robot detecte obstáculos y navegue de forma autónoma en un espacio con obstáculos. Además, se aplicó un filtro de Kalman para mejorar la estimación de proximidad frontal, reduciendo el efecto del ruido en las mediciones de los sensores.

## Implementación
Se utilizaron los siguientes componentes:
- ps0: frontal derecho
- ps7: frontal izquierdo
- ps5: lateral izquierdo
- ps2: lateral derecho
  
Estos sensores permitieron detectar obstáculos cercanos y decidir la dirección de movimiento del robot.

## Encoders
Se utilizaron encoders de ambas ruedas para estimar el desplazamiento del robot:
- left wheel sensor
- right wheel sensor

## Filtro simple
Antes de aplicar Kalman, se implementó un filtro exponencial con el objetivo de reducir parte del ruido presente en las lecturas de proximidad.

La ecuación utilizada fue:

$$f_k = \alpha x_k + (1 - \alpha) f_{k-1}$$ 

Este filtro permitió suavizar las variaciones bruscas presentes en las lecturas de proximidad.

## Filtro de Kalman
El filtro de Kalman fue utilizado para estimar la proximidad frontal al obstáculo combinando la información obtenida desde los sensores y los encoders del robot.

El algoritmo se dividió en dos etapas principales:

### Etapa de predicción
En esta etapa, el sistema estima el nuevo estado del robot utilizando el movimiento calculado a partir de los encoders. Esta predicción representa el valor esperado antes de considerar la nueva medición de los sensores.

$$\hat{x}_k^{-} = \hat{x}_{k-1} + \Delta x_k$$

### Etapa de corrección
Posteriormente, la predicción es corregida utilizando la medición real obtenida desde los sensores de proximidad. La corrección depende de la ganancia de Kalman, la cual determina cuánto confiar en la predicción o en la medición.

$$\hat{x}_k = \hat{x}_k^{-} + K_k (z_k - \hat{x}_k^{-})$$

Gracias a este proceso, se obtuvo una estimación más estable y menos sensible al ruido presente en las mediciones.


## Navegación Reactiva
La lógica de navegación implementada fue avanzar cuando no existen obstáculos cercanos, girar cuando se detecta un La navegación del robot fue implementada mediante una estrategia reactiva basada en sensores de proximidad.

El comportamiento principal del robot consistió en:
- Avanzar mientras el camino frontal estuviera despejado
- Detectar obstáculos mediante sensores frontales
- Decidir la dirección de giro utilizando sensores laterales
- Mantener temporalmente la dirección elegida para evitar oscilaciones entre izquierda y derecha

Durante las pruebas, se observó que tomar decisiones en cada iteración generaba cambios constantes de dirección, provocando que el robot quedara atrapado en ciclos de giro. Para solucionar esto, se implementó una memoria temporal de giro, permitiendo mantener la dirección seleccionada durante algunos ciclos antes de volver a evaluar el entorno.

Gracias a esta modificación, el movimiento del robot se volvió considerablemente más estable.

## Registro de Datos 
Durante la simulación se almacenaron los siguientes datos:
- Tiempo
- Señal cruda de proximidad
- Señal filtrada
- Señal estimada por Kalman

Los datos fueron exportados a un archivo CSV para posteriormente generar gráficos y comparar el comportamiento de cada señal.

## Gráficos

## Resultados obtenidos
Durante las pruebas realizadas, el robot logró desplazarse de manera autónoma evitando obstáculos en la mayoría de los escenarios probados. A medida que se fueron ajustando los parámetros del sistema, el comportamiento del robot se volvió más estable y menos propenso a quedarse atrapado en ciclos de decisión.

También se pudo observar claramente la diferencia entre las señales:

- La señal cruda presentaba bastante ruido y cambios bruscos.
- El filtro simple lograba suavizar parcialmente las mediciones.
- El filtro de Kalman entregaba una estimación mucho más estable.

En las pruebas iniciales, el robot tendía a quedar atrapado girando entre izquierda y derecha debido a cambios rápidos en las lecturas laterales. Este problema se redujo considerablemente al mantener temporalmente la dirección de giro seleccionada.

Además, se observó que las esquinas y obstáculos laterales representan situaciones más complejas para la navegación reactiva, especialmente cuando el robot no tiene visión directa frontal del objeto.

## Análisis 
Como grupo, consideramos que este laboratorio nos permitió entender de mejor manera cómo funcionan los sistemas de percepción y navegación en robótica móvil.

Uno de los aspectos que más nos llamó la atención fue la gran cantidad de ruido presente en las lecturas de sensores. En varios casos, pequeñas variaciones provocaban cambios importantes en el comportamiento del robot, especialmente al momento de decidir hacia qué lado girar.

Al implementar el filtro simple, notamos una mejora inmediata en la estabilidad de las señales, aunque todavía existían variaciones importantes. Posteriormente, el filtro de Kalman permitió obtener resultados mucho más consistentes, especialmente cuando el robot avanzaba cerca de obstáculos.

También observamos que la navegación reactiva básica tiene varias limitaciones. En algunos escenarios, el robot quedaba atrapado en esquinas o entraba en ciclos de giro entre izquierda y derecha. Esto nos permitió entender la importancia de agregar memoria temporal o estados internos para estabilizar las decisiones del sistema.

## Conclusión
Este laboratorio permitió implementar un sistema básico de navegación autónoma utilizando sensores, encoders y técnicas de filtrado.

A través de las pruebas realizadas, fue posible comprobar cómo los filtros ayudan a mejorar la calidad de las mediciones y cómo pequeñas decisiones en la lógica de navegación pueden afectar considerablemente el comportamiento del robot.

Finalmente, el uso del filtro de Kalman permitió obtener estimaciones más estables y confiables, demostrando su utilidad en sistemas robóticos móviles.

