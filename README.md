# Simulador de Mecanismo Biela-Manivela

Aplicación desarrollada en **Python** para simular y analizar cinemáticamente un mecanismo **biela-manivela**.

El programa permite visualizar en tiempo real el movimiento del mecanismo y calcular la **posición, velocidad y aceleración del pistón** a partir de sus parámetros geométricos y de la velocidad de giro de la manivela.

---

## Modelo matemático

El análisis parte de la ecuación de posición del pistón:

```math
s(\theta)=r\cos(\theta)+\sqrt{L^2-r^2\sin^2(\theta)}
```

Donde:

- `r`: radio de la manivela
- `L`: longitud de la biela
- `θ`: ángulo instantáneo de la manivela
- `s`: posición del pistón sobre el eje del cilindro

La velocidad del pistón se obtiene derivando la posición respecto al tiempo:

```math
v=\frac{ds}{dt}
```

Y la aceleración se obtiene mediante la segunda derivada:

```math
a=\frac{d^2s}{dt^2}
```

Como el ángulo de la manivela cambia con el tiempo:

```math
\theta(t)=\omega t
```

La velocidad angular de la manivela se obtiene a partir de las RPM:

```math
\omega=\frac{2\pi N}{60}
```

De esta forma, el programa puede evaluar el estado cinemático del mecanismo para cada instante de tiempo.

---

## Validación del modelo

Una comprobación sencilla del modelo consiste en evaluar la posición del pistón en los dos puntos extremos del movimiento.

Para:

```math
\theta=0^\circ
```

se obtiene:

```math
s_{max}=L+r
```

Mientras que para:

```math
\theta=180^\circ
```

se obtiene:

```math
s_{min}=L-r
```

Por lo tanto:

```math
s_{max}-s_{min}=2r
```

Esto coincide con la carrera geométrica esperada del mecanismo.

Para un radio de manivela de:

```text
r = 44.20 mm
```

la carrera es:

```text
Carrera = 2r = 88.40 mm
```

---

## Bancadas inclinadas

El modelo cinemático se resuelve utilizando un **sistema de referencia local alineado con el eje del cilindro**.

Por esta razón, las ecuaciones calculan directamente la magnitud de:

- Posición
- Velocidad
- Aceleración

a lo largo del eje de movimiento del pistón.

La inclinación de la bancada se utiliza posteriormente para representar gráficamente el mecanismo en su orientación correspondiente.

En el caso de una bancada inclinada **45 grados respecto a la vertical**, esta inclinación no modifica las magnitudes cinemáticas calculadas, sino únicamente su orientación respecto al sistema global.

---

## Características

- Simulación animada del mecanismo biela-manivela
- Modificación de la longitud de la biela
- Modificación del radio de la manivela
- Modificación de las RPM
- Cálculo instantáneo de posición
- Cálculo instantáneo de velocidad
- Cálculo instantáneo de aceleración
- Gráficas en tiempo real
- Cálculo del ángulo de la biela
- Cálculo de la velocidad angular de la biela
- Representación de vectores cinemáticos
- Pausar y reanudar la simulación
- Detener y reiniciar el movimiento
- Visualización de valores instantáneos
- Análisis de valores máximos y mínimos
- Representación de una segunda bancada
- Pestaña de aplicación al motor Chevrolet V8

---

## Tecnologías utilizadas

### Python

Lenguaje principal utilizado para desarrollar el simulador.

### NumPy

Utilizado para:

- Cálculos numéricos
- Operaciones trigonométricas
- Manejo de arreglos
- Evaluación del modelo matemático
- Generación de datos para las gráficas

### PySide6

Utilizado para construir la interfaz gráfica:

- Ventana principal
- Pestañas
- Botones
- Campos de entrada
- Controles de simulación

### PyQtGraph

Utilizado para:

- Gráficas en tiempo real
- Representación del mecanismo
- Animación
- Vectores
- Actualización rápida de los elementos gráficos

### PyInstaller

Utilizado para generar un ejecutable de Windows a partir del proyecto en Python.

---

## Estructura del proyecto

```text
Simulador-Biela-Manivela/
│
├── main.py
├── ventana.py
├── modelo.py
├── simulacion.py
├── graficos.py
├── analisis.py
├── motor_chevy.py
├── requirements.txt
└── .gitignore
```

### `modelo.py`

Contiene el núcleo matemático del proyecto.

Se encarga de calcular:

- Posición del pistón
- Velocidad
- Aceleración
- Ángulo de la biela
- Velocidad angular de la biela

### `simulacion.py`

Gestiona la actualización temporal y el comportamiento de la simulación.

### `graficos.py`

Gestiona la representación visual del mecanismo, las gráficas y los vectores.

### `analisis.py`

Organiza y presenta los resultados cinemáticos obtenidos.

### `motor_chevy.py`

Aplica el modelo del mecanismo a una representación de un motor Chevrolet V8.

### `ventana.py`

Integra las diferentes pestañas y elementos de la interfaz gráfica.

### `main.py`

Inicia la aplicación.

---

## Flujo general del programa

```text
Radio de manivela
        +
Longitud de biela
        +
RPM
        |
        v
     modelo.py
        |
        v
Posicion - Velocidad - Aceleracion
        |
        v
Simulacion y graficas
        |
        v
Analisis de resultados
```

---

## Parámetros de referencia

Durante el desarrollo se utilizaron como valores de referencia:

```text
Radio de manivela: 44.20 mm
Longitud de biela: 144.78 mm
Velocidad de giro: 1000 RPM
Carrera del piston: 88.40 mm
```

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Raulin21/Simulador-Biela-Manivela.git
```

Entrar en la carpeta:

```bash
cd Simulador-Biela-Manivela
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el programa:

```bash
python main.py
```

---

## Actualización del modelo durante la simulación

Para cada instante de tiempo, el programa determina el nuevo ángulo de la manivela:

```math
\theta(t)=\omega t
```

Posteriormente evalúa ese ángulo dentro del modelo matemático para obtener los nuevos valores de:

```text
θ(t)
 |
 v
Posicion
 |
 v
Velocidad
 |
 v
Aceleracion
 |
 v
Actualizacion de la animacion y las graficas
```

Esto permite representar continuamente el movimiento del pistón durante una revolución completa.

---

## Objetivo del proyecto

El objetivo principal es implementar un modelo matemático del mecanismo biela-manivela y utilizarlo para desarrollar una herramienta interactiva que permita estudiar su comportamiento cinemático.

El proyecto busca conectar:

**Geometría + Cinemática + Programación + Visualización**

permitiendo observar cómo las ecuaciones matemáticas se transforman en una simulación dinámica del mecanismo.

---

## Autor

**Raúl Miranda**

Estudiante de Ingeniería Mecatrónica
