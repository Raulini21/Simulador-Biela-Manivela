import numpy as np

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QSlider,
    QPushButton,
    QComboBox,
)

from modelo import ModeloBielaManivela

from graficos import (
    MecanismoGrafico,
    GraficaCinematica,
)


class PanelAnalisis(QWidget):
    """
    Pestana destinada al analisis manual del mecanismo.

    Utiliza los mismos parametros fisicos definidos
    en la pestana Simulacion.
    """

    def __init__(self):
        super().__init__()

        self.radio = 44.20
        self.longitud = 144.78
        self.rpm = 1000.0

        self.modelo = ModeloBielaManivela(
            radio_manivela=self.radio,
            longitud_biela=self.longitud,
            rpm=self.rpm,
        )

        self.angulos_grafica_grados = np.linspace(
            0.0,
            360.0,
            721,
        )

        self.angulos_grafica_radianes = np.radians(
            self.angulos_grafica_grados
        )

        self.crear_interfaz()
        self.conectar_eventos()

        self.actualizar_resultados_globales()
        self.actualizar_grafica()
        self.actualizar_analisis()

    def crear_interfaz(self):
        """
        Construye la interfaz completa de analisis.
        """

        layout_principal = QVBoxLayout(self)

        layout_principal.setContentsMargins(10, 10, 10, 10)
        layout_principal.setSpacing(7)

        grupo_parametros = self.crear_panel_parametros()
        grupo_angulo = self.crear_control_angulo()
        panel_central = self.crear_panel_central()

        layout_principal.addWidget(grupo_parametros, 0)
        layout_principal.addWidget(grupo_angulo, 0)
        layout_principal.addWidget(panel_central, 1)

    def crear_panel_parametros(self):
        """
        Muestra los parametros recibidos desde Simulacion.
        """

        grupo = QGroupBox(
            "Parametros recibidos desde Simulacion"
        )

        grupo.setMaximumHeight(
            85
        )

        layout = QHBoxLayout(
            grupo
        )

        layout.setContentsMargins(
            12,
            10,
            12,
            8,
        )

        self.etiqueta_radio = QLabel(
            "Radio: 44.20 mm"
        )

        self.etiqueta_biela = QLabel(
            "Biela: 144.78 mm"
        )

        self.etiqueta_rpm = QLabel(
            "Velocidad: 1000 RPM"
        )

        self.etiqueta_relacion = QLabel(
            "Relacion L/r: 3.28"
        )

        etiquetas = [
            self.etiqueta_radio,
            self.etiqueta_biela,
            self.etiqueta_rpm,
            self.etiqueta_relacion,
        ]

        for etiqueta in etiquetas:
            etiqueta.setAlignment(
                Qt.AlignCenter
            )

            etiqueta.setStyleSheet(
                "font-weight: bold;"
            )

            layout.addWidget(
                etiqueta
            )

        return grupo

    def crear_control_angulo(self):
        """
        Crea el slider de seleccion angular.
        """

        grupo = QGroupBox(
            "Posicion angular"
        )

        grupo.setMaximumHeight(
            90
        )

        layout = QHBoxLayout(
            grupo
        )

        layout.setContentsMargins(
            12,
            10,
            12,
            8,
        )

        self.slider_angulo = QSlider(
            Qt.Horizontal
        )

        self.slider_angulo.setRange(
            0,
            3600,
        )

        self.slider_angulo.setValue(
            0
        )

        self.slider_angulo.setSingleStep(
            1
        )

        self.slider_angulo.setPageStep(
            100
        )

        self.etiqueta_angulo = QLabel(
            "0.0 grados"
        )

        self.etiqueta_angulo.setMinimumWidth(
            115
        )

        self.etiqueta_angulo.setAlignment(
            Qt.AlignCenter
        )

        self.etiqueta_angulo.setStyleSheet(
            "font-weight: bold;"
        )

        layout.addWidget(
            QLabel("Angulo de la manivela:")
        )

        layout.addWidget(
            self.slider_angulo,
            1,
        )

        layout.addWidget(
            self.etiqueta_angulo
        )

        return grupo

    def crear_panel_central(self):
        """
        Crea una distribucion de dos columnas.

        Columna izquierda:
        - Mecanismo
        - Grafica cinematica

        Columna derecha:
        - Resultados instantaneos
        - Resultados globales
        """

        contenedor = QWidget()

        layout_principal = QHBoxLayout(
            contenedor
        )

        layout_principal.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout_principal.setSpacing(
            8
        )

        panel_izquierdo = QWidget()

        layout_izquierdo = QVBoxLayout(
            panel_izquierdo
        )

        layout_izquierdo.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout_izquierdo.setSpacing(
            8
        )

        grupo_mecanismo = QGroupBox(
            "Mecanismo"
        )

        layout_mecanismo = QVBoxLayout(
            grupo_mecanismo
        )

        layout_mecanismo.setContentsMargins(
            8,
            12,
            8,
            8,
        )

        self.vista_mecanismo = (
            MecanismoGrafico()
        )

        self.vista_mecanismo.configurar_geometria(
            self.modelo.radio,
            self.modelo.longitud,
        )

        layout_mecanismo.addWidget(
            self.vista_mecanismo
        )

        grupo_grafica = (
            self.crear_panel_grafica()
        )

        layout_izquierdo.addWidget(
            grupo_mecanismo,
            1,
        )

        layout_izquierdo.addWidget(
            grupo_grafica,
            1,
        )

        panel_resultados = (
            self.crear_panel_resultados()
        )

        layout_principal.addWidget(
            panel_izquierdo,
            1,
        )

        layout_principal.addWidget(
            panel_resultados,
            0,
        )

        return contenedor

    def crear_panel_resultados(self):
        """
        Crea la columna derecha de resultados.
        """

        contenedor = QWidget()

        contenedor.setFixedWidth(
            390
        )

        layout = QVBoxLayout(
            contenedor
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            8
        )

        grupo_instantaneos = (
            self.crear_resultados_instantaneos()
        )

        grupo_globales = (
            self.crear_resultados_globales()
        )

        layout.addWidget(
            grupo_instantaneos,
            1,
        )

        layout.addWidget(
            grupo_globales,
            2,
        )

        return contenedor

    def crear_resultados_instantaneos(self):
        """
        Crea el cuadro de resultados dependientes del angulo.
        """

        grupo = QGroupBox(
            "Resultados instantaneos"
        )

        layout = QGridLayout(
            grupo
        )

        layout.setContentsMargins(
            12,
            14,
            12,
            10,
        )

        layout.setHorizontalSpacing(
            12
        )

        layout.setVerticalSpacing(
            4
        )

        self.resultados = {}

        nombres = [
            (
                "Posicion del piston",
                "mm",
            ),
            (
                "Velocidad del piston",
                "mm/s",
            ),
            (
                "Aceleracion del piston",
                "mm/s2",
            ),
            (
                "Angulo de la biela",
                "grados",
            ),
            (
                "Velocidad angular biela",
                "rad/s",
            ),
            (
                "Velocidad tangencial",
                "mm/s",
            ),
        ]

        for fila, (
            nombre,
            unidad,
        ) in enumerate(nombres):
            etiqueta_nombre = QLabel(
                nombre + ":"
            )

            etiqueta_valor = QLabel(
                "0.00 " + unidad
            )

            etiqueta_valor.setAlignment(
                Qt.AlignRight
                | Qt.AlignVCenter
            )

            etiqueta_valor.setStyleSheet(
                "font-weight: bold;"
            )

            layout.addWidget(
                etiqueta_nombre,
                fila,
                0,
            )

            layout.addWidget(
                etiqueta_valor,
                fila,
                1,
            )

            self.resultados[
                nombre
            ] = etiqueta_valor

        fila_botones = len(
            nombres
        )

        self.boton_pms = QPushButton(
            "Ir a PMS"
        )

        self.boton_pmi = QPushButton(
            "Ir a PMI"
        )

        self.boton_velocidad_maxima = QPushButton(
            "Ir a velocidad maxima"
        )

        self.boton_pms.setFixedHeight(
            28
        )

        self.boton_pmi.setFixedHeight(
            28
        )

        self.boton_velocidad_maxima.setFixedHeight(
            28
        )

        layout.addWidget(
            self.boton_pms,
            fila_botones,
            0,
        )

        layout.addWidget(
            self.boton_pmi,
            fila_botones,
            1,
        )

        layout.addWidget(
            self.boton_velocidad_maxima,
            fila_botones + 1,
            0,
            1,
            2,
        )

        return grupo

    def crear_resultados_globales(self):
        """
        Crea el cuadro de resultados de todo el ciclo.
        """

        grupo = QGroupBox(
            "Resultados globales"
        )

        layout = QGridLayout(
            grupo
        )

        layout.setContentsMargins(
            12,
            14,
            12,
            10,
        )

        layout.setHorizontalSpacing(
            12
        )

        layout.setVerticalSpacing(
            3
        )

        self.resultados_globales = {}

        nombres = [
            (
                "PMS",
                "mm",
            ),
            (
                "PMI",
                "mm",
            ),
            (
                "Carrera total",
                "mm",
            ),
            (
                "Relacion L/r",
                "",
            ),
            (
                "Velocidad maxima",
                "mm/s",
            ),
            (
                "Angulo de V max",
                "grados",
            ),
            (
                "Aceleracion maxima",
                "mm/s2",
            ),
            (
                "Angulo de A max",
                "grados",
            ),
            (
                "Angulo maximo biela",
                "grados",
            ),
        ]

        for fila, (
            nombre,
            unidad,
        ) in enumerate(nombres):
            etiqueta_nombre = QLabel(
                nombre + ":"
            )

            texto_inicial = "0.00"

            if unidad:
                texto_inicial += (
                    " " + unidad
                )

            etiqueta_valor = QLabel(
                texto_inicial
            )

            etiqueta_valor.setAlignment(
                Qt.AlignRight
                | Qt.AlignVCenter
            )

            etiqueta_valor.setStyleSheet(
                "font-weight: bold;"
            )

            layout.addWidget(
                etiqueta_nombre,
                fila,
                0,
            )

            layout.addWidget(
                etiqueta_valor,
                fila,
                1,
            )

            self.resultados_globales[
                nombre
            ] = etiqueta_valor

        return grupo

    def crear_panel_grafica(self):
        """
        Crea la grafica cinematica sincronizada.
        """

        grupo = QGroupBox(
            "Grafica cinematica"
        )

        layout = QVBoxLayout(
            grupo
        )

        layout.setContentsMargins(
            10,
            12,
            10,
            8,
        )

        layout.setSpacing(
            5
        )

        panel_selector = QWidget()

        panel_selector.setFixedHeight(
            38
        )

        layout_selector = QHBoxLayout(
            panel_selector
        )

        layout_selector.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout_selector.setSpacing(
            8
        )

        self.selector_grafica = QComboBox()

        self.selector_grafica.addItems(
            [
                "Posicion del piston",
                "Velocidad del piston",
                "Aceleracion del piston",
                "Angulo de la biela",
                "Velocidad angular de la biela",
                "Velocidad tangencial",
            ]
        )

        self.selector_grafica.setMinimumWidth(
            260
        )

        self.selector_grafica.setFixedHeight(
            32
        )

        self.etiqueta_valor_grafica = QLabel(
            "Valor actual: 0.00 mm"
        )

        self.etiqueta_valor_grafica.setAlignment(
            Qt.AlignRight
            | Qt.AlignVCenter
        )

        self.etiqueta_valor_grafica.setStyleSheet(
            "font-weight: bold;"
        )

        layout_selector.addWidget(
            QLabel("Magnitud mostrada:")
        )

        layout_selector.addWidget(
            self.selector_grafica
        )

        layout_selector.addStretch()

        layout_selector.addWidget(
            self.etiqueta_valor_grafica
        )

        self.vista_grafica = (
            GraficaCinematica()
        )

        layout.addWidget(
            panel_selector,
            0,
        )

        layout.addWidget(
            self.vista_grafica,
            1,
        )

        return grupo

    def conectar_eventos(self):
        """
        Conecta sliders, botones y selector.
        """

        self.slider_angulo.valueChanged.connect(
            self.actualizar_analisis
        )

        self.selector_grafica.currentTextChanged.connect(
            self.actualizar_grafica
        )

        self.boton_pms.clicked.connect(
            self.ir_a_pms
        )

        self.boton_pmi.clicked.connect(
            self.ir_a_pmi
        )

        self.boton_velocidad_maxima.clicked.connect(
            self.ir_a_velocidad_maxima
        )

    def actualizar_parametros(
        self,
        radio,
        longitud,
        rpm,
    ):
        """
        Recibe parametros desde Simulacion.
        """

        self.radio = float(
            radio
        )

        self.longitud = float(
            longitud
        )

        self.rpm = float(
            rpm
        )

        self.modelo = ModeloBielaManivela(
            radio_manivela=self.radio,
            longitud_biela=self.longitud,
            rpm=self.rpm,
        )

        self.vista_mecanismo.configurar_geometria(
            self.modelo.radio,
            self.modelo.longitud,
        )

        relacion = (
            self.longitud
            / self.radio
        )

        self.etiqueta_radio.setText(
            f"Radio: {self.radio:.2f} mm"
        )

        self.etiqueta_biela.setText(
            f"Biela: {self.longitud:.2f} mm"
        )

        self.etiqueta_rpm.setText(
            f"Velocidad: {self.rpm:.0f} RPM"
        )

        self.etiqueta_relacion.setText(
            f"Relacion L/r: {relacion:.2f}"
        )

        self.actualizar_resultados_globales()
        self.actualizar_grafica()
        self.actualizar_analisis()

    def actualizar_analisis(
        self,
        valor=None,
    ):
        """
        Actualiza mecanismo, resultados y marcador.
        """

        angulo_grados = (
            self.slider_angulo.value()
            / 10.0
        )

        theta = np.radians(
            angulo_grados
        )

        self.etiqueta_angulo.setText(
            f"{angulo_grados:.1f} grados"
        )

        (
            x_manivela,
            y_manivela,
            x_piston,
            y_piston,
        ) = self.modelo.coordenadas(
            theta
        )

        self.vista_mecanismo.actualizar(
            x_manivela=x_manivela,
            y_manivela=y_manivela,
            x_piston=x_piston,
            y_piston=y_piston,
            angulo_grados=angulo_grados,
        )

        self.vista_grafica.actualizar_marcador(
            angulo_grados
        )

        posicion = float(
            self.modelo.posicion(
                theta
            )
        )

        velocidad = float(
            self.modelo.velocidad(
                theta
            )
        )

        aceleracion = float(
            self.modelo.aceleracion(
                theta
            )
        )

        angulo_biela = float(
            np.degrees(
                self.modelo.angulo_biela(
                    theta
                )
            )
        )

        velocidad_angular_biela = float(
            self.modelo.velocidad_angular_biela(
                theta
            )
        )

        velocidad_tangencial = float(
            self.modelo.radio
            * self.modelo.omega
        )

        self.resultados[
            "Posicion del piston"
        ].setText(
            f"{posicion:.2f} mm"
        )

        self.resultados[
            "Velocidad del piston"
        ].setText(
            f"{velocidad:.2f} mm/s"
        )

        self.resultados[
            "Aceleracion del piston"
        ].setText(
            f"{aceleracion:.2f} mm/s2"
        )

        self.resultados[
            "Angulo de la biela"
        ].setText(
            f"{angulo_biela:.2f} grados"
        )

        self.resultados[
            "Velocidad angular biela"
        ].setText(
            f"{velocidad_angular_biela:.2f} rad/s"
        )

        self.resultados[
            "Velocidad tangencial"
        ].setText(
            f"{velocidad_tangencial:.2f} mm/s"
        )

        self.actualizar_valor_grafica(
            theta
        )

    def actualizar_resultados_globales(self):
        """
        Calcula resultados representativos de todo el ciclo.
        """

        angulos_grados = np.linspace(
            0.0,
            360.0,
            3601,
        )

        angulos_radianes = np.radians(
            angulos_grados
        )

        posiciones = self.modelo.posicion(
            angulos_radianes
        )

        velocidades = self.modelo.velocidad(
            angulos_radianes
        )

        aceleraciones = self.modelo.aceleracion(
            angulos_radianes
        )

        angulos_biela = np.degrees(
            self.modelo.angulo_biela(
                angulos_radianes
            )
        )

        pms = float(
            np.max(
                posiciones
            )
        )

        pmi = float(
            np.min(
                posiciones
            )
        )

        carrera = float(
            pms - pmi
        )

        relacion = float(
            self.modelo.longitud
            / self.modelo.radio
        )

        indice_velocidad_maxima = int(
            np.argmax(
                np.abs(
                    velocidades
                )
            )
        )

        velocidad_maxima = float(
            np.abs(
                velocidades[
                    indice_velocidad_maxima
                ]
            )
        )

        angulo_velocidad_maxima = float(
            angulos_grados[
                indice_velocidad_maxima
            ]
        )

        indice_aceleracion_maxima = int(
            np.argmax(
                np.abs(
                    aceleraciones
                )
            )
        )

        aceleracion_maxima = float(
            np.abs(
                aceleraciones[
                    indice_aceleracion_maxima
                ]
            )
        )

        angulo_aceleracion_maxima = float(
            angulos_grados[
                indice_aceleracion_maxima
            ]
        )

        angulo_maximo_biela = float(
            np.max(
                np.abs(
                    angulos_biela
                )
            )
        )

        self.resultados_globales[
            "PMS"
        ].setText(
            f"{pms:.2f} mm"
        )

        self.resultados_globales[
            "PMI"
        ].setText(
            f"{pmi:.2f} mm"
        )

        self.resultados_globales[
            "Carrera total"
        ].setText(
            f"{carrera:.2f} mm"
        )

        self.resultados_globales[
            "Relacion L/r"
        ].setText(
            f"{relacion:.3f}"
        )

        self.resultados_globales[
            "Velocidad maxima"
        ].setText(
            f"{velocidad_maxima:.2f} mm/s"
        )

        self.resultados_globales[
            "Angulo de V max"
        ].setText(
            f"{angulo_velocidad_maxima:.1f} grados"
        )

        self.resultados_globales[
            "Aceleracion maxima"
        ].setText(
            f"{aceleracion_maxima:.2f} mm/s2"
        )

        self.resultados_globales[
            "Angulo de A max"
        ].setText(
            f"{angulo_aceleracion_maxima:.1f} grados"
        )

        self.resultados_globales[
            "Angulo maximo biela"
        ].setText(
            f"{angulo_maximo_biela:.2f} grados"
        )

    def actualizar_grafica(
        self,
        texto=None,
    ):
        """
        Calcula la curva seleccionada.
        """

        seleccion = (
            self.selector_grafica.currentText()
        )

        theta = (
            self.angulos_grafica_radianes
        )

        if seleccion == "Posicion del piston":
            valores = self.modelo.posicion(
                theta
            )

            nombre = "Posicion del piston"
            unidad = "mm"

        elif seleccion == "Velocidad del piston":
            valores = self.modelo.velocidad(
                theta
            )

            nombre = "Velocidad del piston"
            unidad = "mm/s"

        elif seleccion == "Aceleracion del piston":
            valores = self.modelo.aceleracion(
                theta
            )

            nombre = "Aceleracion del piston"
            unidad = "mm/s2"

        elif seleccion == "Angulo de la biela":
            valores = np.degrees(
                self.modelo.angulo_biela(
                    theta
                )
            )

            nombre = "Angulo de la biela"
            unidad = "grados"

        elif seleccion == (
            "Velocidad angular de la biela"
        ):
            valores = (
                self.modelo.velocidad_angular_biela(
                    theta
                )
            )

            nombre = (
                "Velocidad angular de la biela"
            )

            unidad = "rad/s"

        elif seleccion == "Velocidad tangencial":
            valor_constante = (
                self.modelo.radio
                * self.modelo.omega
            )

            valores = np.full_like(
                theta,
                valor_constante,
                dtype=float,
            )

            nombre = (
                "Velocidad tangencial de la manivela"
            )

            unidad = "mm/s"

        else:
            valores = self.modelo.posicion(
                theta
            )

            nombre = "Posicion del piston"
            unidad = "mm"

        self.vista_grafica.establecer_datos(
            angulos_grados=(
                self.angulos_grafica_grados
            ),
            valores=valores,
            nombre_magnitud=nombre,
            unidad=unidad,
        )

        angulo_grados = (
            self.slider_angulo.value()
            / 10.0
        )

        self.vista_grafica.actualizar_marcador(
            angulo_grados
        )

        theta_actual = np.radians(
            angulo_grados
        )

        self.actualizar_valor_grafica(
            theta_actual
        )

    def actualizar_valor_grafica(
        self,
        theta,
    ):
        """
        Actualiza el valor numerico junto al selector.
        """

        seleccion = (
            self.selector_grafica.currentText()
        )

        if seleccion == "Posicion del piston":
            valor = float(
                self.modelo.posicion(
                    theta
                )
            )

            unidad = "mm"

        elif seleccion == "Velocidad del piston":
            valor = float(
                self.modelo.velocidad(
                    theta
                )
            )

            unidad = "mm/s"

        elif seleccion == "Aceleracion del piston":
            valor = float(
                self.modelo.aceleracion(
                    theta
                )
            )

            unidad = "mm/s2"

        elif seleccion == "Angulo de la biela":
            valor = float(
                np.degrees(
                    self.modelo.angulo_biela(
                        theta
                    )
                )
            )

            unidad = "grados"

        elif seleccion == (
            "Velocidad angular de la biela"
        ):
            valor = float(
                self.modelo.velocidad_angular_biela(
                    theta
                )
            )

            unidad = "rad/s"

        elif seleccion == "Velocidad tangencial":
            valor = float(
                self.modelo.radio
                * self.modelo.omega
            )

            unidad = "mm/s"

        else:
            valor = float(
                self.modelo.posicion(
                    theta
                )
            )

            unidad = "mm"

        self.etiqueta_valor_grafica.setText(
            f"Valor actual: {valor:.2f} {unidad}"
        )

    def ir_a_pms(self):
        """
        Mueve el mecanismo al PMS.
        """

        self.slider_angulo.setValue(
            0
        )

    def ir_a_pmi(self):
        """
        Mueve el mecanismo al PMI.
        """

        self.slider_angulo.setValue(
            1800
        )

    def ir_a_velocidad_maxima(self):
        """
        Busca y selecciona la velocidad maxima absoluta.
        """

        angulos_grados = np.linspace(
            0.0,
            360.0,
            3601,
        )

        angulos_radianes = np.radians(
            angulos_grados
        )

        velocidades = self.modelo.velocidad(
            angulos_radianes
        )

        indice_maximo = int(
            np.argmax(
                np.abs(
                    velocidades
                )
            )
        )

        angulo_maximo = float(
            angulos_grados[
                indice_maximo
            ]
        )

        valor_slider = int(
            round(
                angulo_maximo
                * 10.0
            )
        )

        self.slider_angulo.setValue(
            valor_slider
        )