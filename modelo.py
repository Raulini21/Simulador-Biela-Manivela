import numpy as np


class ModeloBielaManivela:
    """
    Modelo cinematico de un mecanismo biela-manivela.

    Unidades:
    - Longitudes: mm
    - Angulos: radianes
    - Velocidad angular: rad/s
    - Velocidad lineal: mm/s
    - Aceleracion lineal: mm/s2
    """

    def __init__(
        self,
        radio_manivela: float,
        longitud_biela: float,
        rpm: float,
    ) -> None:
        self.radio = float(radio_manivela)
        self.longitud = float(longitud_biela)
        self.rpm = float(rpm)

        self._validar_parametros()

        self.omega = (
            2.0
            * np.pi
            * self.rpm
            / 60.0
        )

    def _validar_parametros(self) -> None:
        if self.radio <= 0:
            raise ValueError(
                "El radio de la manivela debe ser mayor que cero."
            )

        if self.longitud <= 0:
            raise ValueError(
                "La longitud de la biela debe ser mayor que cero."
            )

        if self.rpm <= 0:
            raise ValueError(
                "Las RPM deben ser mayores que cero."
            )

        if self.longitud <= self.radio:
            raise ValueError(
                "La longitud de la biela debe ser mayor "
                "que el radio de la manivela."
            )

    def posicion(self, theta):
        theta = np.asarray(
            theta,
            dtype=float,
        )

        seno = np.sin(theta)
        coseno = np.cos(theta)

        raiz = np.sqrt(
            self.longitud**2
            - self.radio**2
            * seno**2
        )

        posicion_piston = (
            self.radio
            * coseno
            + raiz
        )

        return posicion_piston

    def velocidad(self, theta):
        theta = np.asarray(
            theta,
            dtype=float,
        )

        seno = np.sin(theta)
        coseno = np.cos(theta)

        raiz = np.sqrt(
            self.longitud**2
            - self.radio**2
            * seno**2
        )

        derivada_posicion = (
            -self.radio
            * seno
            - (
                self.radio**2
                * seno
                * coseno
            )
            / raiz
        )

        velocidad_piston = (
            derivada_posicion
            * self.omega
        )

        return velocidad_piston

    def aceleracion(self, theta):
        theta = np.asarray(
            theta,
            dtype=float,
        )

        seno = np.sin(theta)
        coseno = np.cos(theta)

        raiz = np.sqrt(
            self.longitud**2
            - self.radio**2
            * seno**2
        )

        termino_1 = (
            -self.radio
            * coseno
        )

        termino_2 = (
            -self.radio**2
            * np.cos(
                2.0 * theta
            )
            / raiz
        )

        termino_3 = (
            -self.radio**4
            * seno**2
            * coseno**2
            / raiz**3
        )

        segunda_derivada = (
            termino_1
            + termino_2
            + termino_3
        )

        aceleracion_piston = (
            segunda_derivada
            * self.omega**2
        )

        return aceleracion_piston

    def angulo_biela(self, theta):
        theta = np.asarray(
            theta,
            dtype=float,
        )

        relacion = (
            self.radio
            / self.longitud
        )

        angulo = np.arcsin(
            relacion
            * np.sin(theta)
        )

        return angulo

    def velocidad_angular_biela(
        self,
        theta,
    ):
        theta = np.asarray(
            theta,
            dtype=float,
        )

        relacion = (
            self.radio
            / self.longitud
        )

        seno = np.sin(theta)
        coseno = np.cos(theta)

        denominador = np.sqrt(
            1.0
            - (
                relacion
                * seno
            )**2
        )

        omega_biela = (
            relacion
            * coseno
            / denominador
        ) * self.omega

        return omega_biela

    def coordenadas(self, theta):
        theta = np.asarray(
            theta,
            dtype=float,
        )

        x_manivela = (
            self.radio
            * np.cos(theta)
        )

        y_manivela = (
            self.radio
            * np.sin(theta)
        )

        x_piston = self.posicion(
            theta
        )

        y_piston = np.zeros_like(
            x_piston
        )

        return (
            x_manivela,
            y_manivela,
            x_piston,
            y_piston,
        )