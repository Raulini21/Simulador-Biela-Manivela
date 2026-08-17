import numpy as np

from PySide6.QtCore import (
    Qt,
    QTimer,
    QPointF,
    QRectF,
)

from PySide6.QtGui import (
    QPainter,
    QPen,
    QBrush,
    QFont,
    QColor,
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QToolButton,
    QDoubleSpinBox,
    QAbstractSpinBox,
    QFrame,
)

from modelo import ModeloBielaManivela


class VistaMotorV8(QWidget):
    """
    Representacion visual simplificada de dos bancadas de un motor V8.

    La bancada izquierda se anima.
    La bancada derecha permanece estatica y semitransparente.
    """

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(470)

        self.radio = 44.20
        self.longitud = 144.78

        self.angulo_activo = 0.0
        self.angulo_estatico = np.radians(35.0)

    def configurar_geometria(
        self,
        radio,
        longitud,
    ):
        self.radio = float(radio)
        self.longitud = float(longitud)

        self.update()

    def actualizar_angulo(
        self,
        theta,
    ):
        self.angulo_activo = float(theta)

        self.update()

    def transformar_punto(
        self,
        x_local,
        y_local,
        angulo_bancada,
        centro_x,
        centro_y,
        escala,
    ):
        """
        Rota un punto local y lo convierte a coordenadas de pantalla.
        """

        coseno = np.cos(
            angulo_bancada
        )

        seno = np.sin(
            angulo_bancada
        )

        x_rotado = (
            x_local * coseno
            - y_local * seno
        )

        y_rotado = (
            x_local * seno
            + y_local * coseno
        )

        x_pantalla = (
            centro_x
            + x_rotado * escala
        )

        y_pantalla = (
            centro_y
            - y_rotado * escala
        )

        return QPointF(
            x_pantalla,
            y_pantalla,
        )

    def calcular_coordenadas(
        self,
        theta,
    ):
        """
        Calcula las coordenadas locales del mecanismo.
        """

        seno = np.sin(theta)
        coseno = np.cos(theta)

        x_manivela = (
            self.radio
            * coseno
        )

        y_manivela = (
            self.radio
            * seno
        )

        raiz = np.sqrt(
            self.longitud**2
            - self.radio**2
            * seno**2
        )

        x_piston = (
            self.radio
            * coseno
            + raiz
        )

        y_piston = 0.0

        return (
            x_manivela,
            y_manivela,
            x_piston,
            y_piston,
        )

    def paintEvent(
        self,
        event,
    ):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.fillRect(
            self.rect(),
            QColor(
                255,
                255,
                255,
            ),
        )

        ancho = self.width()
        alto = self.height()

        centro_x = ancho * 0.50
        centro_y = alto * 0.66

        longitud_total = (
            self.radio
            + self.longitud
        )

        espacio_horizontal = (
            ancho * 0.30
        )

        espacio_vertical = (
            alto * 0.43
        )

        escala_horizontal = (
            espacio_horizontal
            / longitud_total
        )

        escala_vertical = (
            espacio_vertical
            / longitud_total
        )

        escala = min(
            escala_horizontal,
            escala_vertical,
        )

        escala = max(
            escala,
            0.65,
        )

        self.dibujar_titulo(
            painter,
            ancho,
        )

        self.dibujar_lineas_bancadas(
            painter,
            centro_x,
            centro_y,
            escala,
        )

        self.dibujar_circulo_manivela(
            painter,
            centro_x,
            centro_y,
            escala,
        )

        self.dibujar_mecanismo(
            painter=painter,
            theta=self.angulo_estatico,
            angulo_bancada=np.radians(45.0),
            centro_x=centro_x,
            centro_y=centro_y,
            escala=escala,
            activo=False,
        )

        self.dibujar_mecanismo(
            painter=painter,
            theta=self.angulo_activo,
            angulo_bancada=np.radians(135.0),
            centro_x=centro_x,
            centro_y=centro_y,
            escala=escala,
            activo=True,
        )

        self.dibujar_centro_ciguenal(
            painter,
            centro_x,
            centro_y,
        )

        self.dibujar_angulo_bancadas(
            painter,
            centro_x,
            centro_y,
            escala,
        )

        self.dibujar_leyenda(
            painter,
            ancho,
            alto,
        )

    def dibujar_titulo(
        self,
        painter,
        ancho,
    ):
        fuente = QFont(
            "Arial",
            13,
        )

        fuente.setBold(
            True
        )

        painter.setFont(
            fuente
        )

        painter.setPen(
            QPen(
                QColor(
                    32,
                    36,
                    42,
                ),
                1,
            )
        )

        painter.drawText(
            QRectF(
                0.0,
                10.0,
                float(ancho),
                35.0,
            ),
            Qt.AlignCenter,
            "Representacion de las bancadas del Chevy 350 V8",
        )

    def dibujar_lineas_bancadas(
        self,
        painter,
        centro_x,
        centro_y,
        escala,
    ):
        longitud_guia = (
            self.radio
            + self.longitud
            + 30.0
        )

        punto_centro = QPointF(
            centro_x,
            centro_y,
        )

        punto_izquierdo = self.transformar_punto(
            longitud_guia,
            0.0,
            np.radians(135.0),
            centro_x,
            centro_y,
            escala,
        )

        punto_derecho = self.transformar_punto(
            longitud_guia,
            0.0,
            np.radians(45.0),
            centro_x,
            centro_y,
            escala,
        )

        painter.setPen(
            QPen(
                QColor(
                    165,
                    171,
                    180,
                ),
                2,
                Qt.DashLine,
            )
        )

        painter.drawLine(
            punto_centro,
            punto_izquierdo,
        )

        painter.drawLine(
            punto_centro,
            punto_derecho,
        )

    def dibujar_circulo_manivela(
        self,
        painter,
        centro_x,
        centro_y,
        escala,
    ):
        radio_pantalla = (
            self.radio
            * escala
        )

        painter.setPen(
            QPen(
                QColor(
                    180,
                    184,
                    190,
                ),
                2,
            )
        )

        painter.setBrush(
            Qt.NoBrush
        )

        painter.drawEllipse(
            QPointF(
                centro_x,
                centro_y,
            ),
            radio_pantalla,
            radio_pantalla,
        )

    def dibujar_mecanismo(
        self,
        painter,
        theta,
        angulo_bancada,
        centro_x,
        centro_y,
        escala,
        activo,
    ):
        (
            x_manivela,
            y_manivela,
            x_piston,
            y_piston,
        ) = self.calcular_coordenadas(
            theta
        )

        punto_centro = QPointF(
            centro_x,
            centro_y,
        )

        punto_manivela = self.transformar_punto(
            x_manivela,
            y_manivela,
            angulo_bancada,
            centro_x,
            centro_y,
            escala,
        )

        punto_piston = self.transformar_punto(
            x_piston,
            y_piston,
            angulo_bancada,
            centro_x,
            centro_y,
            escala,
        )

        if activo:
            color_manivela = QColor(
                38,
                105,
                190,
                255,
            )

            color_biela = QColor(
                224,
                82,
                45,
                255,
            )

            color_piston = QColor(
                168,
                176,
                187,
                255,
            )

            color_borde = QColor(
                35,
                40,
                46,
                255,
            )

            opacidad = 1.0

        else:
            color_manivela = QColor(
                100,
                110,
                122,
                90,
            )

            color_biela = QColor(
                100,
                110,
                122,
                90,
            )

            color_piston = QColor(
                175,
                181,
                190,
                75,
            )

            color_borde = QColor(
                100,
                110,
                122,
                105,
            )

            opacidad = 0.52

        painter.save()

        painter.setOpacity(
            opacidad
        )

        painter.setPen(
            QPen(
                color_manivela,
                7,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin,
            )
        )

        painter.drawLine(
            punto_centro,
            punto_manivela,
        )

        painter.setPen(
            QPen(
                color_biela,
                8,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin,
            )
        )

        painter.drawLine(
            punto_manivela,
            punto_piston,
        )

        painter.setBrush(
            QBrush(
                color_manivela
            )
        )

        painter.setPen(
            QPen(
                color_borde,
                2,
            )
        )

        painter.drawEllipse(
            punto_manivela,
            7.0,
            7.0,
        )

        self.dibujar_piston(
            painter=painter,
            centro=punto_piston,
            angulo_bancada=angulo_bancada,
            relleno=color_piston,
            borde=color_borde,
            activo=activo,
        )

        painter.restore()

    def dibujar_piston(
        self,
        painter,
        centro,
        angulo_bancada,
        relleno,
        borde,
        activo,
    ):
        """
        Dibuja el piston orientado segun el eje de la bancada.
        """

        if activo:
            ancho = 40.0
            alto = 30.0
        else:
            ancho = 38.0
            alto = 28.0

        painter.save()

        painter.translate(
            centro
        )

        angulo_pantalla = -np.degrees(
            angulo_bancada
        )

        painter.rotate(
            angulo_pantalla
        )

        rectangulo = QRectF(
            -ancho / 2.0,
            -alto / 2.0,
            ancho,
            alto,
        )

        painter.setPen(
            QPen(
                borde,
                2,
            )
        )

        painter.setBrush(
            QBrush(
                relleno
            )
        )

        painter.drawRoundedRect(
            rectangulo,
            4.0,
            4.0,
        )

        painter.restore()

    def dibujar_centro_ciguenal(
        self,
        painter,
        centro_x,
        centro_y,
    ):
        centro = QPointF(
            centro_x,
            centro_y,
        )

        painter.setPen(
            QPen(
                QColor(
                    20,
                    22,
                    25,
                ),
                2,
            )
        )

        painter.setBrush(
            QBrush(
                QColor(
                    25,
                    27,
                    31,
                )
            )
        )

        painter.drawEllipse(
            centro,
            10.0,
            10.0,
        )

        painter.setFont(
            QFont(
                "Arial",
                10,
            )
        )

        painter.drawText(
            QRectF(
                centro_x - 85.0,
                centro_y + 14.0,
                170.0,
                22.0,
            ),
            Qt.AlignCenter,
            "Eje del ciguenal",
        )

    def dibujar_angulo_bancadas(
        self,
        painter,
        centro_x,
        centro_y,
        escala,
    ):
        radio_arco = (
            self.radio
            * escala
            * 1.30
        )

        rectangulo = QRectF(
            centro_x - radio_arco,
            centro_y - radio_arco,
            radio_arco * 2.0,
            radio_arco * 2.0,
        )

        painter.setPen(
            QPen(
                QColor(
                    63,
                    112,
                    170,
                ),
                2,
            )
        )

        painter.setBrush(
            Qt.NoBrush
        )

        painter.drawArc(
            rectangulo,
            45 * 16,
            90 * 16,
        )

        painter.setFont(
            QFont(
                "Arial",
                10,
            )
        )

        painter.drawText(
            QRectF(
                centro_x - 50.0,
                centro_y
                - radio_arco
                - 28.0,
                100.0,
                24.0,
            ),
            Qt.AlignCenter,
            "90 grados",
        )

    def dibujar_leyenda(
        self,
        painter,
        ancho,
        alto,
    ):
        painter.setFont(
            QFont(
                "Arial",
                10,
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    38,
                    105,
                    190,
                ),
                1,
            )
        )

        painter.drawText(
            QRectF(
                30.0,
                alto - 45.0,
                ancho / 2.0 - 45.0,
                25.0,
            ),
            Qt.AlignCenter,
            "Bancada activa: mecanismo animado",
        )

        painter.setPen(
            QPen(
                QColor(
                    125,
                    132,
                    142,
                ),
                1,
            )
        )

        painter.drawText(
            QRectF(
                ancho / 2.0 + 15.0,
                alto - 45.0,
                ancho / 2.0 - 45.0,
                25.0,
            ),
            Qt.AlignCenter,
            "Bancada opuesta: referencia estatica",
        )


class PanelMotorChevy(QWidget):
    """
    Pestana dedicada al Chevrolet Small Block 350 V8.
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

        self.angulo_actual = 0.0
        self.velocidad_visual = 0.12
        self.animacion_activa = False

        self.temporizador = QTimer(
            self
        )

        self.temporizador.setInterval(
            16
        )

        self.crear_interfaz()
        self.conectar_eventos()
        self.actualizar_resultados()
        self.actualizar_vista()

    def crear_interfaz(self):
        layout_principal = QVBoxLayout(
            self
        )

        panel_superior = QWidget()

        layout_superior = QHBoxLayout(
            panel_superior
        )

        grupo_datos = self.crear_panel_datos()
        grupo_visual = self.crear_panel_visual()

        layout_superior.addWidget(
            grupo_datos,
            0,
        )

        layout_superior.addWidget(
            grupo_visual,
            1,
        )

        grupo_inferior = self.crear_panel_calculos()

        layout_principal.addWidget(
            panel_superior,
            4,
        )

        layout_principal.addWidget(
            grupo_inferior,
            2,
        )

    def crear_panel_datos(self):
        grupo = QGroupBox(
            "Datos generales del motor"
        )

        grupo.setFixedWidth(
            390
        )

        layout = QGridLayout(
            grupo
        )

        datos = [
            (
                "Motor:",
                "Chevrolet Small Block 350",
            ),
            (
                "Configuracion:",
                "V8",
            ),
            (
                "Cilindrada:",
                "350 pulgadas cubicas",
            ),
            (
                "Cilindrada aproximada:",
                "5.7 litros",
            ),
            (
                "Numero de cilindros:",
                "8",
            ),
            (
                "Angulo entre bancadas:",
                "90 grados",
            ),
            (
                "Carrera del piston:",
                "88.40 mm",
            ),
            (
                "Radio de manivela:",
                "44.20 mm",
            ),
            (
                "Longitud de biela:",
                "144.78 mm",
            ),
            (
                "Relacion L/r:",
                "3.28",
            ),
        ]

        for fila, (
            nombre,
            valor,
        ) in enumerate(datos):
            etiqueta_nombre = QLabel(
                nombre
            )

            etiqueta_nombre.setStyleSheet(
                "font-weight: bold;"
            )

            etiqueta_valor = QLabel(
                valor
            )

            etiqueta_valor.setAlignment(
                Qt.AlignRight
                | Qt.AlignVCenter
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

        layout.setRowStretch(
            len(datos),
            1,
        )

        return grupo

    def crear_panel_visual(self):
        grupo = QGroupBox(
            "Configuracion visual del motor"
        )

        layout = QVBoxLayout(
            grupo
        )

        self.vista_motor = VistaMotorV8()

        self.vista_motor.configurar_geometria(
            self.radio,
            self.longitud,
        )

        layout.addWidget(
            self.vista_motor
        )

        return grupo

    def crear_control_numerico(
        self,
        spinbox,
    ):
        """
        Crea un SpinBox con botones externos.
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
            4
        )

        spinbox.setButtonSymbols(
            QAbstractSpinBox.NoButtons
        )

        spinbox.setMinimumHeight(
            42
        )

        panel_botones = QWidget()

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
            32,
            20,
        )

        boton_bajar.setFixedSize(
            32,
            20,
        )

        boton_subir.setAutoRepeat(
            True
        )

        boton_bajar.setAutoRepeat(
            True
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
            panel_botones
        )

        return contenedor

    def crear_panel_calculos(self):
        grupo = QGroupBox(
            "Calculos y control del motor"
        )

        layout_principal = QHBoxLayout(
            grupo
        )

        panel_controles = QWidget()

        layout_controles = QGridLayout(
            panel_controles
        )

        self.entrada_rpm = QDoubleSpinBox()

        self.entrada_rpm.setRange(
            1.0,
            10000.0,
        )

        self.entrada_rpm.setValue(
            1000.0
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

        self.entrada_velocidad_visual = QDoubleSpinBox()

        self.entrada_velocidad_visual.setRange(
            0.02,
            1.0,
        )

        self.entrada_velocidad_visual.setValue(
            0.12
        )

        self.entrada_velocidad_visual.setDecimals(
            2
        )

        self.entrada_velocidad_visual.setSingleStep(
            0.02
        )

        self.entrada_velocidad_visual.setSuffix(
            " x"
        )

        control_rpm = self.crear_control_numerico(
            self.entrada_rpm
        )

        control_velocidad = self.crear_control_numerico(
            self.entrada_velocidad_visual
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

        layout_controles.addWidget(
            QLabel("Velocidad del motor:"),
            0,
            0,
        )

        layout_controles.addWidget(
            control_rpm,
            0,
            1,
        )

        layout_controles.addWidget(
            QLabel("Velocidad visual:"),
            1,
            0,
        )

        layout_controles.addWidget(
            control_velocidad,
            1,
            1,
        )

        layout_controles.addWidget(
            self.boton_aplicar,
            2,
            0,
            1,
            2,
        )

        layout_controles.addWidget(
            self.boton_iniciar,
            3,
            0,
        )

        layout_controles.addWidget(
            self.boton_pausar,
            3,
            1,
        )

        layout_controles.addWidget(
            self.boton_reiniciar,
            4,
            0,
            1,
            2,
        )

        panel_resultados = QWidget()

        layout_resultados = QGridLayout(
            panel_resultados
        )

        self.etiqueta_omega = QLabel(
            "0.00 rad/s"
        )

        self.etiqueta_frecuencia = QLabel(
            "0.00 rev/s"
        )

        self.etiqueta_tiempo_revolucion = QLabel(
            "0.0000 s"
        )

        self.etiqueta_tiempo_ciclo = QLabel(
            "0.0000 s"
        )

        self.etiqueta_velocidad_media = QLabel(
            "0.00 m/s"
        )

        self.etiqueta_angulo = QLabel(
            "0.0 grados"
        )

        resultados = [
            (
                "Velocidad angular:",
                self.etiqueta_omega,
            ),
            (
                "Frecuencia de giro:",
                self.etiqueta_frecuencia,
            ),
            (
                "Tiempo por revolucion:",
                self.etiqueta_tiempo_revolucion,
            ),
            (
                "Tiempo por ciclo de 4 tiempos:",
                self.etiqueta_tiempo_ciclo,
            ),
            (
                "Velocidad media del piston:",
                self.etiqueta_velocidad_media,
            ),
            (
                "Angulo actual del ciguenal:",
                self.etiqueta_angulo,
            ),
        ]

        for fila, (
            nombre,
            etiqueta,
        ) in enumerate(resultados):
            etiqueta.setAlignment(
                Qt.AlignRight
                | Qt.AlignVCenter
            )

            etiqueta.setStyleSheet(
                "font-weight: bold;"
            )

            layout_resultados.addWidget(
                QLabel(nombre),
                fila,
                0,
            )

            layout_resultados.addWidget(
                etiqueta,
                fila,
                1,
            )

        linea = QFrame()

        linea.setFrameShape(
            QFrame.VLine
        )

        linea.setFrameShadow(
            QFrame.Sunken
        )

        layout_principal.addWidget(
            panel_controles,
            1,
        )

        layout_principal.addWidget(
            linea
        )

        layout_principal.addWidget(
            panel_resultados,
            1,
        )

        return grupo

    def conectar_eventos(self):
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

    def aplicar_parametros(self):
        self.rpm = float(
            self.entrada_rpm.value()
        )

        self.velocidad_visual = float(
            self.entrada_velocidad_visual.value()
        )

        self.modelo = ModeloBielaManivela(
            radio_manivela=self.radio,
            longitud_biela=self.longitud,
            rpm=self.rpm,
        )

        self.actualizar_resultados()

    def iniciar_animacion(self):
        self.animacion_activa = True

        self.temporizador.start()

    def pausar_animacion(self):
        self.animacion_activa = False

        self.temporizador.stop()

    def reiniciar_animacion(self):
        self.temporizador.stop()

        self.animacion_activa = False
        self.angulo_actual = 0.0

        self.actualizar_vista()

    def avanzar_animacion(self):
        if not self.animacion_activa:
            return

        intervalo_segundos = (
            self.temporizador.interval()
            / 1000.0
        )

        incremento = (
            self.modelo.omega
            * self.velocidad_visual
            * intervalo_segundos
        )

        self.angulo_actual += incremento

        self.angulo_actual = (
            self.angulo_actual
            % (2.0 * np.pi)
        )

        self.actualizar_vista()

    def actualizar_vista(self):
        self.vista_motor.actualizar_angulo(
            self.angulo_actual
        )

        angulo_grados = np.degrees(
            self.angulo_actual
        )

        self.etiqueta_angulo.setText(
            f"{angulo_grados:.1f} grados"
        )

    def actualizar_resultados(self):
        rpm = float(
            self.rpm
        )

        omega = (
            2.0
            * np.pi
            * rpm
            / 60.0
        )

        frecuencia = (
            rpm
            / 60.0
        )

        tiempo_revolucion = (
            60.0
            / rpm
        )

        tiempo_ciclo = (
            120.0
            / rpm
        )

        carrera_metros = (
            88.40
            / 1000.0
        )

        velocidad_media_piston = (
            2.0
            * carrera_metros
            * rpm
            / 60.0
        )

        self.etiqueta_omega.setText(
            f"{omega:.2f} rad/s"
        )

        self.etiqueta_frecuencia.setText(
            f"{frecuencia:.2f} rev/s"
        )

        self.etiqueta_tiempo_revolucion.setText(
            f"{tiempo_revolucion:.4f} s"
        )

        self.etiqueta_tiempo_ciclo.setText(
            f"{tiempo_ciclo:.4f} s"
        )

        self.etiqueta_velocidad_media.setText(
            f"{velocidad_media_piston:.2f} m/s"
        )

        self.actualizar_vista()