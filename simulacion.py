import numpy as np

from PySide6.QtCore import (
    Qt,
    QTimer,
    Signal,
)

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QToolButton,
    QDoubleSpinBox,
    QComboBox,
    QCheckBox,
    QAbstractSpinBox,
    QMessageBox,
)

from modelo import ModeloBielaManivela

from graficos import (
    MecanismoGrafico,
    GraficaCinematica,
)


class PanelSimulacion(QWidget):
    """
    Pestana destinada a la simulacion animada
    del mecanismo biela-manivela.
    """

    parametros_actualizados = Signal(
        float,
        float,
        float,
    )

    def __init__(self):
        super().__init__()

        self.radio = 44.20
        self.longitud = 144.78
        self.rpm = 1000.0
        self.velocidad_visual = 0.25

        self.angulo_actual = 0.0
        self.animacion_activa = False

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

        self.temporizador = QTimer(
            self
        )

        self.temporizador.setInterval(
            16
        )

        self.crear_interfaz()
        self.conectar_eventos()

        self.actualizar_grafica()
        self.actualizar_mecanismo()

    def crear_interfaz(self):
        """
        Crea la interfaz principal de la simulacion.
        """

        layout_principal = QHBoxLayout(
            self
        )

        layout_principal.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        layout_principal.setSpacing(
            10
        )

        panel_controles = (
            self.crear_panel_controles()
        )

        panel_visual = (
            self.crear_panel_visual()
        )

        layout_principal.addWidget(
            panel_controles,
            0,
        )

        layout_principal.addWidget(
            panel_visual,
            1,
        )

    def crear_control_numerico(
        self,
        spinbox,
    ):
        """
        Crea un control numerico con botones externos.
        """

        contenedor = QWidget()

        contenedor.setFixedHeight(
            38
        )

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
            3
        )

        spinbox.setButtonSymbols(
            QAbstractSpinBox.NoButtons
        )

        spinbox.setFixedHeight(
            36
        )

        panel_botones = QWidget()

        panel_botones.setFixedSize(
            30,
            36,
        )

        layout_botones = QVBoxLayout(
            panel_botones
        )

        layout_botones.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout_botones.setSpacing(
            2
        )

        boton_subir = QToolButton()
        boton_bajar = QToolButton()

        boton_subir.setArrowType(
            Qt.UpArrow
        )

        boton_bajar.setArrowType(
            Qt.DownArrow
        )

        boton_subir.setFixedSize(
            30,
            17,
        )

        boton_bajar.setFixedSize(
            30,
            17,
        )

        boton_subir.setAutoRepeat(
            True
        )

        boton_bajar.setAutoRepeat(
            True
        )

        boton_subir.setAutoRepeatDelay(
            400
        )

        boton_bajar.setAutoRepeatDelay(
            400
        )

        boton_subir.setAutoRepeatInterval(
            80
        )

        boton_bajar.setAutoRepeatInterval(
            80
        )

        boton_subir.clicked.connect(
            spinbox.stepUp
        )

        boton_bajar.clicked.connect(
            spinbox.stepDown
        )

        layout_botones.addWidget(
            boton_subir
        )

        layout_botones.addWidget(
            boton_bajar
        )

        layout_principal.addWidget(
            spinbox,
            1,
        )

        layout_principal.addWidget(
            panel_botones,
            0,
        )

        return contenedor

    def crear_panel_controles(self):
        """
        Crea el panel izquierdo.
        """

        grupo = QGroupBox(
            "Parametros de simulacion"
        )

        grupo.setFixedWidth(
            370
        )

        layout = QVBoxLayout(
            grupo
        )

        layout.setContentsMargins(
            10,
            14,
            10,
            10,
        )

        layout.setSpacing(
            6
        )

        formulario = QGridLayout()

        formulario.setHorizontalSpacing(
            10
        )

        formulario.setVerticalSpacing(
            6
        )

        self.entrada_radio = QDoubleSpinBox()

        self.entrada_radio.setRange(
            1.0,
            500.0,
        )

        self.entrada_radio.setValue(
            self.radio
        )

        self.entrada_radio.setDecimals(
            2
        )

        self.entrada_radio.setSingleStep(
            1.0
        )

        self.entrada_radio.setSuffix(
            " mm"
        )

        self.entrada_biela = QDoubleSpinBox()

        self.entrada_biela.setRange(
            1.0,
            1000.0,
        )

        self.entrada_biela.setValue(
            self.longitud
        )

        self.entrada_biela.setDecimals(
            2
        )

        self.entrada_biela.setSingleStep(
            1.0
        )

        self.entrada_biela.setSuffix(
            " mm"
        )

        self.entrada_rpm = QDoubleSpinBox()

        self.entrada_rpm.setRange(
            1.0,
            10000.0,
        )

        self.entrada_rpm.setValue(
            self.rpm
        )

        self.entrada_rpm.setDecimals(
            0
        )

        self.entrada_rpm.setSingleStep(
            100.0
        )

        self.entrada_rpm.setSuffix(
            " RPM"
        )

        self.entrada_velocidad_visual = (
            QDoubleSpinBox()
        )

        self.entrada_velocidad_visual.setRange(
            0.01,
            5.0,
        )

        self.entrada_velocidad_visual.setValue(
            self.velocidad_visual
        )

        self.entrada_velocidad_visual.setDecimals(
            2
        )

        self.entrada_velocidad_visual.setSingleStep(
            0.05
        )

        self.entrada_velocidad_visual.setSuffix(
            " x"
        )

        control_radio = (
            self.crear_control_numerico(
                self.entrada_radio
            )
        )

        control_biela = (
            self.crear_control_numerico(
                self.entrada_biela
            )
        )

        control_rpm = (
            self.crear_control_numerico(
                self.entrada_rpm
            )
        )

        control_velocidad = (
            self.crear_control_numerico(
                self.entrada_velocidad_visual
            )
        )

        formulario.addWidget(
            QLabel("Radio manivela:"),
            0,
            0,
        )

        formulario.addWidget(
            control_radio,
            0,
            1,
        )

        formulario.addWidget(
            QLabel("Longitud biela:"),
            1,
            0,
        )

        formulario.addWidget(
            control_biela,
            1,
            1,
        )

        formulario.addWidget(
            QLabel("Velocidad fisica:"),
            2,
            0,
        )

        formulario.addWidget(
            control_rpm,
            2,
            1,
        )

        formulario.addWidget(
            QLabel("Velocidad visual:"),
            3,
            0,
        )

        formulario.addWidget(
            control_velocidad,
            3,
            1,
        )

        formulario.setColumnStretch(
            1,
            1,
        )

        layout.addLayout(
            formulario
        )

        layout.addSpacing(
            4
        )

        self.boton_aplicar = QPushButton(
            "Aplicar parametros"
        )

        self.boton_iniciar = QPushButton(
            "Iniciar"
        )

        self.boton_pausar = QPushButton(
            "Pausar"
        )

        self.boton_reiniciar = QPushButton(
            "Reiniciar"
        )

        botones = [
            self.boton_aplicar,
            self.boton_iniciar,
            self.boton_pausar,
            self.boton_reiniciar,
        ]

        for boton in botones:
            boton.setFixedHeight(
                34
            )

            layout.addWidget(
                boton
            )

        layout.addSpacing(
            5
        )

        self.etiqueta_estado = QLabel(
            "Estado: detenido"
        )

        self.etiqueta_angulo = QLabel(
            "Angulo: 0.0 grados"
        )

        self.etiqueta_revoluciones = QLabel(
            "Revoluciones: 0"
        )

        self.etiqueta_valor_actual = QLabel(
            "Valor actual: 0.00 mm"
        )

        etiquetas = [
            self.etiqueta_estado,
            self.etiqueta_angulo,
            self.etiqueta_revoluciones,
            self.etiqueta_valor_actual,
        ]

        for etiqueta in etiquetas:
            etiqueta.setAlignment(
                Qt.AlignCenter
            )

            etiqueta.setFixedHeight(
                20
            )

            layout.addWidget(
                etiqueta
            )

        self.etiqueta_estado.setStyleSheet(
            "font-weight: bold;"
        )

        self.etiqueta_valor_actual.setStyleSheet(
            "font-weight: bold;"
        )

        layout.addSpacing(
            5
        )

        etiqueta_selector = QLabel(
            "Grafica mostrada:"
        )

        etiqueta_selector.setFixedHeight(
            20
        )

        layout.addWidget(
            etiqueta_selector
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

        self.selector_grafica.setFixedHeight(
            34
        )

        layout.addWidget(
            self.selector_grafica
        )

        layout.addSpacing(
            4
        )

        self.opcion_vectores = QCheckBox(
            "Mostrar vectores de velocidad"
        )

        self.opcion_cir = QCheckBox(
            "Mostrar CIR"
        )

        self.opcion_segunda_bancada = QCheckBox(
            "Mostrar segunda bancada"
        )

        self.opcion_etiquetas = QCheckBox(
            "Mostrar etiquetas numericas"
        )

        opciones = [
            self.opcion_vectores,
            self.opcion_cir,
            self.opcion_segunda_bancada,
            self.opcion_etiquetas,
        ]

        for opcion in opciones:
            opcion.setFixedHeight(
                25
            )

            opcion.setEnabled(
                True
            )

            layout.addWidget(
                opcion
            )

        layout.addStretch()

        return grupo

    def crear_panel_visual(self):
        """
        Crea la vista del mecanismo y la grafica.
        """

        contenedor = QWidget()

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

        grupo_mecanismo = QGroupBox(
            "Mecanismo animado"
        )

        layout_mecanismo = QVBoxLayout(
            grupo_mecanismo
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

        grupo_grafica = QGroupBox(
            "Grafica sincronizada"
        )

        layout_grafica = QVBoxLayout(
            grupo_grafica
        )

        self.vista_grafica = (
            GraficaCinematica()
        )

        self.vista_grafica.setMinimumHeight(
            220
        )

        layout_grafica.addWidget(
            self.vista_grafica
        )

        layout.addWidget(
            grupo_mecanismo,
            3,
        )

        layout.addWidget(
            grupo_grafica,
            2,
        )

        return contenedor

    def conectar_eventos(self):
        """
        Conecta botones, selector y opciones visuales.
        """

        self.temporizador.timeout.connect(
            self.avanzar_animacion
        )

        self.boton_aplicar.clicked.connect(
            self.aplicar_parametros
        )

        self.boton_iniciar.clicked.connect(
            self.iniciar_animacion
        )

        self.boton_pausar.clicked.connect(
            self.pausar_animacion
        )

        self.boton_reiniciar.clicked.connect(
            self.reiniciar_animacion
        )

        self.selector_grafica.currentTextChanged.connect(
            self.actualizar_grafica
        )

        self.opcion_etiquetas.toggled.connect(
            self.cambiar_etiquetas_numericas
        )

        self.opcion_vectores.toggled.connect(
            self.cambiar_vectores_velocidad
        )

        self.opcion_cir.toggled.connect(
            self.cambiar_cir
        )

        self.opcion_segunda_bancada.toggled.connect(
            self.cambiar_segunda_bancada
        )

    def cambiar_etiquetas_numericas(
        self,
        activadas,
    ):
        """
        Muestra u oculta las etiquetas.
        """

        self.vista_mecanismo.establecer_etiquetas_visibles(
            activadas
        )

        self.actualizar_mecanismo()

    def cambiar_vectores_velocidad(
        self,
        activados,
    ):
        """
        Muestra u oculta los vectores.
        """

        self.vista_mecanismo.establecer_vectores_visibles(
            activados
        )

        self.actualizar_mecanismo()

    def cambiar_cir(
        self,
        activado,
    ):
        """
        Muestra u oculta el CIR.
        """

        self.vista_mecanismo.establecer_cir_visible(
            activado
        )

        self.actualizar_mecanismo()

    def cambiar_segunda_bancada(
        self,
        activada,
    ):
        """
        Muestra u oculta la segunda bancada.
        """

        self.vista_mecanismo.establecer_segunda_bancada_visible(
            activada
        )

        self.actualizar_mecanismo()

    def aplicar_parametros(self):
        """
        Aplica radio, longitud, RPM y velocidad visual.
        """

        radio_nuevo = float(
            self.entrada_radio.value()
        )

        longitud_nueva = float(
            self.entrada_biela.value()
        )

        rpm_nuevas = float(
            self.entrada_rpm.value()
        )

        velocidad_visual_nueva = float(
            self.entrada_velocidad_visual.value()
        )

        try:
            modelo_nuevo = ModeloBielaManivela(
                radio_manivela=radio_nuevo,
                longitud_biela=longitud_nueva,
                rpm=rpm_nuevas,
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Parametros invalidos",
                str(error),
            )

            return

        estaba_animando = (
            self.animacion_activa
        )

        self.temporizador.stop()

        self.radio = radio_nuevo
        self.longitud = longitud_nueva
        self.rpm = rpm_nuevas

        self.velocidad_visual = (
            velocidad_visual_nueva
        )

        self.modelo = modelo_nuevo

        self.vista_mecanismo.configurar_geometria(
            self.modelo.radio,
            self.modelo.longitud,
        )

        self.actualizar_grafica()
        self.actualizar_mecanismo()

        self.parametros_actualizados.emit(
            self.radio,
            self.longitud,
            self.rpm,
        )

        if estaba_animando:
            self.temporizador.start()

    def iniciar_animacion(self):
        """
        Inicia o reanuda la simulacion.
        """

        if self.animacion_activa:
            return

        self.animacion_activa = True

        self.etiqueta_estado.setText(
            "Estado: ejecutando"
        )

        self.temporizador.start()

    def pausar_animacion(self):
        """
        Pausa la simulacion.
        """

        self.animacion_activa = False

        self.temporizador.stop()

        self.etiqueta_estado.setText(
            "Estado: pausado"
        )

    def reiniciar_animacion(self):
        """
        Reinicia el angulo a cero.
        """

        self.temporizador.stop()

        self.animacion_activa = False
        self.angulo_actual = 0.0

        self.etiqueta_estado.setText(
            "Estado: detenido"
        )

        self.actualizar_mecanismo()

    def avanzar_animacion(self):
        """
        Avanza el angulo del mecanismo.
        """

        if not self.animacion_activa:
            return

        intervalo_segundos = (
            self.temporizador.interval()
            / 1000.0
        )

        incremento_angular = (
            self.modelo.omega
            * self.velocidad_visual
            * intervalo_segundos
        )

        self.angulo_actual += (
            incremento_angular
        )

        self.actualizar_mecanismo()

    def actualizar_mecanismo(self):
        """
        Actualiza ambos mecanismos y los elementos visuales.
        """

        theta_visible = (
            self.angulo_actual
            % (2.0 * np.pi)
        )

        angulo_grados = float(
            np.degrees(
                theta_visible
            )
        )

        (
            x_manivela,
            y_manivela,
            x_piston,
            y_piston,
        ) = self.modelo.coordenadas(
            theta_visible
        )

        posicion_piston = float(
            self.modelo.posicion(
                theta_visible
            )
        )

        velocidad_piston = float(
            self.modelo.velocidad(
                theta_visible
            )
        )

        aceleracion_piston = float(
            self.modelo.aceleracion(
                theta_visible
            )
        )

        angulo_biela = float(
            np.degrees(
                self.modelo.angulo_biela(
                    theta_visible
                )
            )
        )

        velocidad_a_x = float(
            -self.modelo.radio
            * self.modelo.omega
            * np.sin(
                theta_visible
            )
        )

        velocidad_a_y = float(
            self.modelo.radio
            * self.modelo.omega
            * np.cos(
                theta_visible
            )
        )

        velocidad_b_x = (
            velocidad_piston
        )

        velocidad_b_y = 0.0

        theta_segunda = (
            theta_visible
            + np.pi
        ) % (
            2.0 * np.pi
        )

        (
            x_manivela_segunda,
            y_manivela_segunda,
            x_piston_segunda,
            y_piston_segunda,
        ) = self.modelo.coordenadas(
            theta_segunda
        )

        self.vista_mecanismo.actualizar(
            x_manivela=x_manivela,
            y_manivela=y_manivela,
            x_piston=x_piston,
            y_piston=y_piston,
            angulo_grados=angulo_grados,
            posicion_piston=posicion_piston,
            velocidad_piston=velocidad_piston,
            aceleracion_piston=aceleracion_piston,
            angulo_biela=angulo_biela,
            rpm=self.modelo.rpm,
            velocidad_a_x=velocidad_a_x,
            velocidad_a_y=velocidad_a_y,
            velocidad_b_x=velocidad_b_x,
            velocidad_b_y=velocidad_b_y,
            x_manivela_segunda=x_manivela_segunda,
            y_manivela_segunda=y_manivela_segunda,
            x_piston_segunda=x_piston_segunda,
            y_piston_segunda=y_piston_segunda,
        )

        self.vista_grafica.actualizar_marcador(
            angulo_grados
        )

        revoluciones = int(
            self.angulo_actual
            // (2.0 * np.pi)
        )

        self.etiqueta_angulo.setText(
            f"Angulo: {angulo_grados:.1f} grados"
        )

        self.etiqueta_revoluciones.setText(
            f"Revoluciones: {revoluciones}"
        )

        self.actualizar_valor_actual(
            theta_visible
        )

    def actualizar_grafica(
        self,
        texto=None,
    ):
        """
        Actualiza la curva seleccionada.
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

        theta_visible = (
            self.angulo_actual
            % (2.0 * np.pi)
        )

        angulo_grados = np.degrees(
            theta_visible
        )

        self.vista_grafica.actualizar_marcador(
            angulo_grados
        )

        self.actualizar_valor_actual(
            theta_visible
        )

    def actualizar_valor_actual(
        self,
        theta,
    ):
        """
        Actualiza el valor numerico seleccionado.
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

        self.etiqueta_valor_actual.setText(
            f"Valor actual: {valor:.2f} {unidad}"
        )