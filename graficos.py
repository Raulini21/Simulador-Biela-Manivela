import numpy as np
import pyqtgraph as pg

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsRectItem


class MecanismoGrafico(pg.PlotWidget):
    """
    Vista grafica del mecanismo biela-manivela.

    Puede mostrar:
    - Mecanismo principal.
    - Etiquetas numericas.
    - Vectores de velocidad.
    - Centro instantaneo de rotacion.
    - Segunda bancada.
    """

    def __init__(self):
        super().__init__()

        self.radio = 44.20
        self.longitud = 144.78

        self.etiquetas_visibles = False
        self.vectores_visibles = False
        self.cir_visible = False
        self.segunda_bancada_visible = False

        self.configurar_grafica()
        self.crear_elementos()

    def configurar_grafica(self):
        self.setBackground("w")

        self.showGrid(
            x=True,
            y=True,
            alpha=0.25,
        )

        self.setAspectLocked(True)

        self.setLabel(
            "bottom",
            "Posicion horizontal",
            units="mm",
        )

        self.setLabel(
            "left",
            "Posicion vertical",
            units="mm",
        )

        self.setMouseEnabled(
            x=True,
            y=True,
        )

        self.setMenuEnabled(False)

    def crear_elementos(self):
        self.linea_eje = self.plot(
            pen=pg.mkPen(
                color=(120, 120, 120),
                width=2,
                style=Qt.DashLine,
            )
        )

        self.circulo_manivela = pg.PlotDataItem(
            pen=pg.mkPen(
                color=(180, 180, 180),
                width=2,
            )
        )

        self.addItem(
            self.circulo_manivela
        )

        self.manivela = self.plot(
            pen=pg.mkPen(
                color=(30, 90, 200),
                width=6,
            ),
            symbol="o",
            symbolSize=11,
            symbolBrush=(30, 90, 200),
            symbolPen=pg.mkPen(
                color=(20, 60, 150),
                width=2,
            ),
        )

        self.biela = self.plot(
            pen=pg.mkPen(
                color=(220, 80, 40),
                width=6,
            ),
            symbol="o",
            symbolSize=11,
            symbolBrush=(220, 80, 40),
            symbolPen=pg.mkPen(
                color=(160, 50, 20),
                width=2,
            ),
        )

        self.centro = pg.ScatterPlotItem(
            size=15,
            brush=pg.mkBrush(
                20,
                20,
                20,
            ),
            pen=pg.mkPen(
                color=(20, 20, 20),
                width=2,
            ),
        )

        self.addItem(
            self.centro
        )

        self.piston = QGraphicsRectItem(
            -12.0,
            -17.0,
            24.0,
            34.0,
        )

        self.piston.setPen(
            pg.mkPen(
                color=(40, 40, 40),
                width=2,
            )
        )

        self.piston.setBrush(
            pg.mkBrush(
                180,
                180,
                180,
            )
        )

        self.addItem(
            self.piston
        )

        self.crear_etiquetas()
        self.crear_vectores()
        self.crear_cir()
        self.crear_segunda_bancada()

    def crear_etiquetas(self):
        self.etiqueta_angulo = pg.TextItem(
            text="0.0 grados",
            anchor=(0, 1),
        )

        self.etiqueta_angulo.setColor(
            (30, 30, 30)
        )

        self.addItem(
            self.etiqueta_angulo
        )

        self.etiqueta_manivela = pg.TextItem(
            text="",
            anchor=(0.5, 1.0),
            fill=pg.mkBrush(
                255,
                255,
                255,
                220,
            ),
            border=pg.mkPen(
                80,
                80,
                80,
            ),
        )

        self.etiqueta_manivela.setColor(
            (20, 20, 20)
        )

        self.addItem(
            self.etiqueta_manivela
        )

        self.etiqueta_piston = pg.TextItem(
            text="",
            anchor=(0.0, 0.5),
            fill=pg.mkBrush(
                255,
                255,
                255,
                220,
            ),
            border=pg.mkPen(
                80,
                80,
                80,
            ),
        )

        self.etiqueta_piston.setColor(
            (20, 20, 20)
        )

        self.addItem(
            self.etiqueta_piston
        )

        self.etiqueta_modelo = pg.TextItem(
            text="",
            anchor=(0.0, 0.0),
            fill=pg.mkBrush(
                255,
                255,
                255,
                220,
            ),
            border=pg.mkPen(
                80,
                80,
                80,
            ),
        )

        self.etiqueta_modelo.setColor(
            (20, 20, 20)
        )

        self.addItem(
            self.etiqueta_modelo
        )

        self.establecer_etiquetas_visibles(
            False
        )

    def crear_vectores(self):
        self.vector_punto_a = self.plot(
            pen=pg.mkPen(
                color=(30, 160, 80),
                width=4,
            )
        )

        self.vector_piston = self.plot(
            pen=pg.mkPen(
                color=(130, 60, 190),
                width=4,
            )
        )

        self.vector_relativo = self.plot(
            pen=pg.mkPen(
                color=(240, 140, 20),
                width=4,
            )
        )

        self.flecha_punto_a = pg.ArrowItem(
            angle=0,
            tipAngle=30,
            baseAngle=20,
            headLen=14,
            tailLen=None,
            brush=pg.mkBrush(
                30,
                160,
                80,
            ),
            pen=pg.mkPen(
                20,
                110,
                55,
            ),
        )

        self.flecha_piston = pg.ArrowItem(
            angle=0,
            tipAngle=30,
            baseAngle=20,
            headLen=14,
            tailLen=None,
            brush=pg.mkBrush(
                130,
                60,
                190,
            ),
            pen=pg.mkPen(
                90,
                35,
                140,
            ),
        )

        self.flecha_relativa = pg.ArrowItem(
            angle=0,
            tipAngle=30,
            baseAngle=20,
            headLen=14,
            tailLen=None,
            brush=pg.mkBrush(
                240,
                140,
                20,
            ),
            pen=pg.mkPen(
                170,
                90,
                10,
            ),
        )

        self.addItem(
            self.flecha_punto_a
        )

        self.addItem(
            self.flecha_piston
        )

        self.addItem(
            self.flecha_relativa
        )

        self.etiqueta_vector_a = pg.TextItem(
            text="",
            anchor=(0.5, 1.0),
            fill=pg.mkBrush(
                255,
                255,
                255,
                220,
            ),
        )

        self.etiqueta_vector_a.setColor(
            (20, 120, 60)
        )

        self.addItem(
            self.etiqueta_vector_a
        )

        self.etiqueta_vector_b = pg.TextItem(
            text="",
            anchor=(0.5, 1.0),
            fill=pg.mkBrush(
                255,
                255,
                255,
                220,
            ),
        )

        self.etiqueta_vector_b.setColor(
            (105, 45, 160)
        )

        self.addItem(
            self.etiqueta_vector_b
        )

        self.etiqueta_vector_relativo = pg.TextItem(
            text="",
            anchor=(0.5, 1.0),
            fill=pg.mkBrush(
                255,
                255,
                255,
                220,
            ),
        )

        self.etiqueta_vector_relativo.setColor(
            (190, 100, 10)
        )

        self.addItem(
            self.etiqueta_vector_relativo
        )

        self.establecer_vectores_visibles(
            False
        )

    def crear_cir(self):
        self.linea_cir_manivela = self.plot(
            pen=pg.mkPen(
                color=(0, 150, 170),
                width=2,
                style=Qt.DashLine,
            )
        )

        self.linea_cir_piston = self.plot(
            pen=pg.mkPen(
                color=(0, 150, 170),
                width=2,
                style=Qt.DashLine,
            )
        )

        self.punto_cir = pg.ScatterPlotItem(
            size=16,
            symbol="x",
            pen=pg.mkPen(
                color=(0, 100, 125),
                width=4,
            ),
            brush=pg.mkBrush(
                0,
                180,
                200,
            ),
        )

        self.addItem(
            self.punto_cir
        )

        self.etiqueta_cir = pg.TextItem(
            text="",
            anchor=(0.0, 1.0),
            fill=pg.mkBrush(
                255,
                255,
                255,
                225,
            ),
            border=pg.mkPen(
                0,
                130,
                150,
            ),
        )

        self.etiqueta_cir.setColor(
            (0, 90, 110)
        )

        self.addItem(
            self.etiqueta_cir
        )

        self.establecer_cir_visible(
            False
        )

    def crear_segunda_bancada(self):
        """
        Crea una segunda bancada semitransparente.
        """

        self.linea_eje_segunda = self.plot(
            pen=pg.mkPen(
                color=(100, 100, 100, 130),
                width=2,
                style=Qt.DashLine,
            )
        )

        self.circulo_manivela_segunda = self.plot(
            pen=pg.mkPen(
                color=(140, 140, 140, 130),
                width=2,
            )
        )

        self.manivela_segunda = self.plot(
            pen=pg.mkPen(
                color=(70, 120, 210, 150),
                width=5,
            ),
            symbol="o",
            symbolSize=9,
            symbolBrush=(70, 120, 210, 150),
            symbolPen=pg.mkPen(
                color=(40, 80, 160, 150),
                width=2,
            ),
        )

        self.biela_segunda = self.plot(
            pen=pg.mkPen(
                color=(225, 120, 70, 150),
                width=5,
            ),
            symbol="o",
            symbolSize=9,
            symbolBrush=(225, 120, 70, 150),
            symbolPen=pg.mkPen(
                color=(170, 75, 35, 150),
                width=2,
            ),
        )

        self.piston_segunda = QGraphicsRectItem(
            -12.0,
            -17.0,
            24.0,
            34.0,
        )

        self.piston_segunda.setPen(
            pg.mkPen(
                color=(70, 70, 70, 170),
                width=2,
            )
        )

        self.piston_segunda.setBrush(
            pg.mkBrush(
                180,
                180,
                180,
                140,
            )
        )

        self.piston_segunda.setTransformOriginPoint(
            0.0,
            0.0,
        )

        self.addItem(
            self.piston_segunda
        )

        self.etiqueta_segunda_bancada = pg.TextItem(
            text="Bancada 2",
            anchor=(0.5, 1.0),
            fill=pg.mkBrush(
                255,
                255,
                255,
                210,
            ),
        )

        self.etiqueta_segunda_bancada.setColor(
            (80, 80, 80)
        )

        self.addItem(
            self.etiqueta_segunda_bancada
        )

        self.establecer_segunda_bancada_visible(
            False
        )

    def configurar_geometria(
        self,
        radio,
        longitud,
    ):
        self.radio = float(
            radio
        )

        self.longitud = float(
            longitud
        )

        self.actualizar_limites_vista()

        angulos = np.linspace(
            0.0,
            2.0 * np.pi,
            300,
        )

        x_circulo = (
            self.radio
            * np.cos(angulos)
        )

        y_circulo = (
            self.radio
            * np.sin(angulos)
        )

        self.circulo_manivela.setData(
            x_circulo,
            y_circulo,
        )

        self.centro.setData(
            [0.0],
            [0.0],
        )

        self.actualizar_circulo_segunda_bancada()

    def actualizar_limites_vista(self):
        """
        Ajusta la vista segun se muestre una o dos bancadas.
        """

        if self.segunda_bancada_visible:
            limite = (
                self.radio
                + self.longitud
                + self.radio * 1.5
            )

            self.setXRange(
                -limite,
                limite,
                padding=0,
            )

            self.setYRange(
                -limite,
                limite,
                padding=0,
            )

            self.linea_eje.setData(
                [-limite, limite],
                [0.0, 0.0],
            )

            self.etiqueta_angulo.setPos(
                -limite * 0.90,
                -limite * 0.80,
            )

            self.etiqueta_modelo.setPos(
                -limite * 0.90,
                limite * 0.80,
            )

        else:
            margen_horizontal = (
                self.radio * 1.5
            )

            x_min = (
                -self.radio
                - margen_horizontal
            )

            x_max = (
                self.radio
                + self.longitud
                + margen_horizontal
            )

            limite_vertical = max(
                self.radio * 2.0,
                60.0,
            )

            self.setXRange(
                x_min,
                x_max,
                padding=0,
            )

            self.setYRange(
                -limite_vertical,
                limite_vertical,
                padding=0,
            )

            self.linea_eje.setData(
                [x_min, x_max],
                [0.0, 0.0],
            )

            self.etiqueta_angulo.setPos(
                x_min + self.radio * 0.25,
                -limite_vertical * 0.75,
            )

            self.etiqueta_modelo.setPos(
                x_min + self.radio * 0.15,
                limite_vertical * 0.82,
            )

    def actualizar_circulo_segunda_bancada(self):
        angulos = np.linspace(
            0.0,
            2.0 * np.pi,
            300,
        )

        x_local = (
            self.radio
            * np.cos(angulos)
        )

        y_local = (
            self.radio
            * np.sin(angulos)
        )

        x_rotado, y_rotado = self.rotar_coordenadas(
            x_local,
            y_local,
            90.0,
        )

        self.circulo_manivela_segunda.setData(
            x_rotado,
            y_rotado,
        )

        distancia_eje = (
            self.radio
            + self.longitud
            + self.radio
        )

        x_eje_local = np.array(
            [
                -self.radio,
                distancia_eje,
            ]
        )

        y_eje_local = np.array(
            [
                0.0,
                0.0,
            ]
        )

        x_eje, y_eje = self.rotar_coordenadas(
            x_eje_local,
            y_eje_local,
            90.0,
        )

        self.linea_eje_segunda.setData(
            x_eje,
            y_eje,
        )

    def rotar_coordenadas(
        self,
        x,
        y,
        angulo_grados,
    ):
        angulo = np.radians(
            angulo_grados
        )

        coseno = np.cos(
            angulo
        )

        seno = np.sin(
            angulo
        )

        x_rotado = (
            np.asarray(x) * coseno
            - np.asarray(y) * seno
        )

        y_rotado = (
            np.asarray(x) * seno
            + np.asarray(y) * coseno
        )

        return (
            x_rotado,
            y_rotado,
        )

    def establecer_etiquetas_visibles(
        self,
        visibles,
    ):
        self.etiquetas_visibles = bool(
            visibles
        )

        self.etiqueta_manivela.setVisible(
            self.etiquetas_visibles
        )

        self.etiqueta_piston.setVisible(
            self.etiquetas_visibles
        )

        self.etiqueta_modelo.setVisible(
            self.etiquetas_visibles
        )

    def establecer_vectores_visibles(
        self,
        visibles,
    ):
        self.vectores_visibles = bool(
            visibles
        )

        elementos = [
            self.vector_punto_a,
            self.vector_piston,
            self.vector_relativo,
            self.flecha_punto_a,
            self.flecha_piston,
            self.flecha_relativa,
            self.etiqueta_vector_a,
            self.etiqueta_vector_b,
            self.etiqueta_vector_relativo,
        ]

        for elemento in elementos:
            elemento.setVisible(
                self.vectores_visibles
            )

    def establecer_cir_visible(
        self,
        visible,
    ):
        self.cir_visible = bool(
            visible
        )

        elementos = [
            self.linea_cir_manivela,
            self.linea_cir_piston,
            self.punto_cir,
            self.etiqueta_cir,
        ]

        for elemento in elementos:
            elemento.setVisible(
                self.cir_visible
            )

    def establecer_segunda_bancada_visible(
        self,
        visible,
    ):
        """
        Muestra u oculta la segunda bancada.
        """

        self.segunda_bancada_visible = bool(
            visible
        )

        elementos = [
            self.linea_eje_segunda,
            self.circulo_manivela_segunda,
            self.manivela_segunda,
            self.biela_segunda,
            self.piston_segunda,
            self.etiqueta_segunda_bancada,
        ]

        for elemento in elementos:
            elemento.setVisible(
                self.segunda_bancada_visible
            )

        self.actualizar_limites_vista()

    def actualizar_vector(
        self,
        linea,
        flecha,
        x_inicial,
        y_inicial,
        componente_x,
        componente_y,
        escala,
    ):
        componente_x = float(
            componente_x
        )

        componente_y = float(
            componente_y
        )

        magnitud = float(
            np.hypot(
                componente_x,
                componente_y,
            )
        )

        if magnitud <= 1e-9:
            linea.setData(
                [],
                [],
            )

            flecha.setVisible(
                False
            )

            return (
                float(x_inicial),
                float(y_inicial),
                magnitud,
            )

        x_final = (
            float(x_inicial)
            + componente_x * escala
        )

        y_final = (
            float(y_inicial)
            + componente_y * escala
        )

        linea.setData(
            [
                float(x_inicial),
                x_final,
            ],
            [
                float(y_inicial),
                y_final,
            ],
        )

        angulo_vector = float(
            np.degrees(
                np.arctan2(
                    componente_y,
                    componente_x,
                )
            )
        )

        flecha.setPos(
            x_final,
            y_final,
        )

        flecha.setStyle(
            angle=180.0 - angulo_vector
        )

        flecha.setVisible(
            self.vectores_visibles
        )

        return (
            x_final,
            y_final,
            magnitud,
        )

    def actualizar_cir(
        self,
        x_manivela,
        y_manivela,
        x_piston,
        y_piston,
    ):
        x_manivela = float(
            x_manivela
        )

        y_manivela = float(
            y_manivela
        )

        x_piston = float(
            x_piston
        )

        y_piston = float(
            y_piston
        )

        tolerancia = max(
            self.radio * 1e-5,
            1e-6,
        )

        if abs(x_manivela) <= tolerancia:
            self.ocultar_geometria_cir()

            self.etiqueta_cir.setText(
                "CIR en el infinito\n"
                "V_A y V_B son paralelas"
            )

            rango_x = self.viewRange()[0]
            rango_y = self.viewRange()[1]

            self.etiqueta_cir.setPos(
                rango_x[0]
                + 0.04 * (
                    rango_x[1] - rango_x[0]
                ),
                rango_y[1]
                - 0.08 * (
                    rango_y[1] - rango_y[0]
                ),
            )

            return

        factor = (
            x_piston
            / x_manivela
        )

        x_cir = x_piston

        y_cir = (
            factor
            * y_manivela
        )

        distancia_maxima = (
            self.radio
            + self.longitud
        ) * 6.0

        if abs(y_cir) > distancia_maxima:
            self.ocultar_geometria_cir()

            self.etiqueta_cir.setText(
                "CIR muy lejano\n"
                "Aproximacion al infinito"
            )

            rango_x = self.viewRange()[0]
            rango_y = self.viewRange()[1]

            self.etiqueta_cir.setPos(
                rango_x[0]
                + 0.04 * (
                    rango_x[1] - rango_x[0]
                ),
                rango_y[1]
                - 0.08 * (
                    rango_y[1] - rango_y[0]
                ),
            )

            return

        self.linea_cir_manivela.setData(
            [
                0.0,
                x_cir,
            ],
            [
                0.0,
                y_cir,
            ],
        )

        self.linea_cir_piston.setData(
            [
                x_piston,
                x_cir,
            ],
            [
                y_piston,
                y_cir,
            ],
        )

        self.punto_cir.setData(
            [x_cir],
            [y_cir],
        )

        distancia_ia = float(
            np.hypot(
                x_cir - x_manivela,
                y_cir - y_manivela,
            )
        )

        distancia_ib = float(
            np.hypot(
                x_cir - x_piston,
                y_cir - y_piston,
            )
        )

        self.etiqueta_cir.setText(
            f"CIR\n"
            f"I = ({x_cir:.2f}, {y_cir:.2f}) mm\n"
            f"IA = {distancia_ia:.2f} mm\n"
            f"IB = {distancia_ib:.2f} mm"
        )

        separacion = max(
            self.radio * 0.15,
            10.0,
        )

        if y_cir >= 0.0:
            posicion_y = (
                y_cir + separacion
            )
        else:
            posicion_y = (
                y_cir - separacion
            )

        self.etiqueta_cir.setPos(
            x_cir + separacion,
            posicion_y,
        )

    def ocultar_geometria_cir(self):
        self.linea_cir_manivela.setData(
            [],
            [],
        )

        self.linea_cir_piston.setData(
            [],
            [],
        )

        self.punto_cir.setData(
            [],
            [],
        )

    def actualizar_segunda_bancada(
        self,
        x_manivela,
        y_manivela,
        x_piston,
        y_piston,
        angulo_bancada=90.0,
    ):
        """
        Rota las coordenadas del segundo mecanismo.
        """

        (
            x_manivela_rotado,
            y_manivela_rotado,
        ) = self.rotar_coordenadas(
            x_manivela,
            y_manivela,
            angulo_bancada,
        )

        (
            x_piston_rotado,
            y_piston_rotado,
        ) = self.rotar_coordenadas(
            x_piston,
            y_piston,
            angulo_bancada,
        )

        self.manivela_segunda.setData(
            [
                0.0,
                float(x_manivela_rotado),
            ],
            [
                0.0,
                float(y_manivela_rotado),
            ],
        )

        self.biela_segunda.setData(
            [
                float(x_manivela_rotado),
                float(x_piston_rotado),
            ],
            [
                float(y_manivela_rotado),
                float(y_piston_rotado),
            ],
        )

        self.piston_segunda.setRect(
            -12.0,
            -17.0,
            24.0,
            34.0,
        )

        self.piston_segunda.setRotation(
            angulo_bancada
        )

        self.piston_segunda.setPos(
            float(x_piston_rotado),
            float(y_piston_rotado),
        )

        separacion = max(
            self.radio * 0.35,
            18.0,
        )

        self.etiqueta_segunda_bancada.setPos(
            float(x_piston_rotado),
            float(y_piston_rotado) + separacion,
        )

    def actualizar(
        self,
        x_manivela,
        y_manivela,
        x_piston,
        y_piston,
        angulo_grados,
        posicion_piston=None,
        velocidad_piston=None,
        aceleracion_piston=None,
        angulo_biela=None,
        rpm=None,
        velocidad_a_x=None,
        velocidad_a_y=None,
        velocidad_b_x=None,
        velocidad_b_y=None,
        x_manivela_segunda=None,
        y_manivela_segunda=None,
        x_piston_segunda=None,
        y_piston_segunda=None,
    ):
        x_manivela = float(
            x_manivela
        )

        y_manivela = float(
            y_manivela
        )

        x_piston = float(
            x_piston
        )

        y_piston = float(
            y_piston
        )

        self.manivela.setData(
            [0.0, x_manivela],
            [0.0, y_manivela],
        )

        self.biela.setData(
            [x_manivela, x_piston],
            [y_manivela, y_piston],
        )

        self.piston.setRect(
            -12.0,
            -17.0,
            24.0,
            34.0,
        )

        self.piston.setPos(
            x_piston,
            y_piston,
        )

        self.etiqueta_angulo.setText(
            f"Angulo: {angulo_grados:.1f} grados"
        )

        if self.etiquetas_visibles:
            self.actualizar_etiquetas(
                x_manivela=x_manivela,
                y_manivela=y_manivela,
                x_piston=x_piston,
                y_piston=y_piston,
                angulo_grados=angulo_grados,
                posicion_piston=posicion_piston,
                velocidad_piston=velocidad_piston,
                aceleracion_piston=aceleracion_piston,
                angulo_biela=angulo_biela,
                rpm=rpm,
            )

        if self.vectores_visibles:
            self.actualizar_vectores(
                x_manivela=x_manivela,
                y_manivela=y_manivela,
                x_piston=x_piston,
                y_piston=y_piston,
                velocidad_a_x=velocidad_a_x,
                velocidad_a_y=velocidad_a_y,
                velocidad_b_x=velocidad_b_x,
                velocidad_b_y=velocidad_b_y,
            )

        if self.cir_visible:
            self.actualizar_cir(
                x_manivela=x_manivela,
                y_manivela=y_manivela,
                x_piston=x_piston,
                y_piston=y_piston,
            )

        if self.segunda_bancada_visible:
            valores_segunda = [
                x_manivela_segunda,
                y_manivela_segunda,
                x_piston_segunda,
                y_piston_segunda,
            ]

            if not any(
                valor is None
                for valor in valores_segunda
            ):
                self.actualizar_segunda_bancada(
                    x_manivela=x_manivela_segunda,
                    y_manivela=y_manivela_segunda,
                    x_piston=x_piston_segunda,
                    y_piston=y_piston_segunda,
                    angulo_bancada=90.0,
                )

    def actualizar_etiquetas(
        self,
        x_manivela,
        y_manivela,
        x_piston,
        y_piston,
        angulo_grados,
        posicion_piston,
        velocidad_piston,
        aceleracion_piston,
        angulo_biela,
        rpm,
    ):
        separacion_vertical = max(
            self.radio * 0.30,
            16.0,
        )

        self.etiqueta_manivela.setPos(
            x_manivela,
            y_manivela + separacion_vertical,
        )

        self.etiqueta_piston.setPos(
            x_piston + 18.0,
            y_piston,
        )

        texto_manivela = (
            f"Manivela\n"
            f"theta = {angulo_grados:.1f} grados"
        )

        if angulo_biela is not None:
            texto_manivela += (
                f"\nbeta = {float(angulo_biela):.2f} grados"
            )

        self.etiqueta_manivela.setText(
            texto_manivela
        )

        texto_piston = "Piston"

        if posicion_piston is not None:
            texto_piston += (
                f"\nx = {float(posicion_piston):.2f} mm"
            )

        if velocidad_piston is not None:
            texto_piston += (
                f"\nv = {float(velocidad_piston):.2f} mm/s"
            )

        if aceleracion_piston is not None:
            texto_piston += (
                f"\na = {float(aceleracion_piston):.2f} mm/s2"
            )

        self.etiqueta_piston.setText(
            texto_piston
        )

        texto_modelo = (
            f"r = {self.radio:.2f} mm\n"
            f"L = {self.longitud:.2f} mm"
        )

        if rpm is not None:
            texto_modelo += (
                f"\nRPM = {float(rpm):.0f}"
            )

        self.etiqueta_modelo.setText(
            texto_modelo
        )

    def actualizar_vectores(
        self,
        x_manivela,
        y_manivela,
        x_piston,
        y_piston,
        velocidad_a_x,
        velocidad_a_y,
        velocidad_b_x,
        velocidad_b_y,
    ):
        valores = [
            velocidad_a_x,
            velocidad_a_y,
            velocidad_b_x,
            velocidad_b_y,
        ]

        if any(
            valor is None
            for valor in valores
        ):
            return

        velocidad_a_x = float(
            velocidad_a_x
        )

        velocidad_a_y = float(
            velocidad_a_y
        )

        velocidad_b_x = float(
            velocidad_b_x
        )

        velocidad_b_y = float(
            velocidad_b_y
        )

        velocidad_relativa_x = (
            velocidad_b_x
            - velocidad_a_x
        )

        velocidad_relativa_y = (
            velocidad_b_y
            - velocidad_a_y
        )

        magnitud_a = float(
            np.hypot(
                velocidad_a_x,
                velocidad_a_y,
            )
        )

        magnitud_b = float(
            np.hypot(
                velocidad_b_x,
                velocidad_b_y,
            )
        )

        magnitud_relativa = float(
            np.hypot(
                velocidad_relativa_x,
                velocidad_relativa_y,
            )
        )

        magnitud_referencia = max(
            magnitud_a,
            magnitud_b,
            magnitud_relativa,
            1.0,
        )

        longitud_visual_maxima = max(
            self.radio * 0.90,
            35.0,
        )

        escala_vectores = (
            longitud_visual_maxima
            / magnitud_referencia
        )

        final_a_x, final_a_y, magnitud_a = (
            self.actualizar_vector(
                linea=self.vector_punto_a,
                flecha=self.flecha_punto_a,
                x_inicial=x_manivela,
                y_inicial=y_manivela,
                componente_x=velocidad_a_x,
                componente_y=velocidad_a_y,
                escala=escala_vectores,
            )
        )

        final_b_x, final_b_y, magnitud_b = (
            self.actualizar_vector(
                linea=self.vector_piston,
                flecha=self.flecha_piston,
                x_inicial=x_piston,
                y_inicial=y_piston,
                componente_x=velocidad_b_x,
                componente_y=velocidad_b_y,
                escala=escala_vectores,
            )
        )

        (
            final_relativo_x,
            final_relativo_y,
            magnitud_relativa,
        ) = self.actualizar_vector(
            linea=self.vector_relativo,
            flecha=self.flecha_relativa,
            x_inicial=x_manivela,
            y_inicial=y_manivela,
            componente_x=velocidad_relativa_x,
            componente_y=velocidad_relativa_y,
            escala=escala_vectores,
        )

        separacion_texto = max(
            self.radio * 0.12,
            8.0,
        )

        self.etiqueta_vector_a.setText(
            f"V_A = {magnitud_a:.1f} mm/s"
        )

        self.etiqueta_vector_a.setPos(
            final_a_x,
            final_a_y + separacion_texto,
        )

        self.etiqueta_vector_b.setText(
            f"V_B = {magnitud_b:.1f} mm/s"
        )

        self.etiqueta_vector_b.setPos(
            final_b_x,
            final_b_y + separacion_texto,
        )

        self.etiqueta_vector_relativo.setText(
            f"V_B/A = {magnitud_relativa:.1f} mm/s"
        )

        self.etiqueta_vector_relativo.setPos(
            final_relativo_x,
            final_relativo_y - separacion_texto,
        )


class GraficaCinematica(pg.PlotWidget):
    """
    Grafica una magnitud cinematica durante una revolucion.
    """

    def __init__(self):
        super().__init__()

        self.angulos_grados = np.array([])
        self.valores = np.array([])

        self.nombre_magnitud = (
            "Posicion del piston"
        )

        self.unidad = "mm"

        self.configurar_grafica()
        self.crear_elementos()

    def configurar_grafica(self):
        self.setBackground("w")

        self.showGrid(
            x=True,
            y=True,
            alpha=0.25,
        )

        self.setMenuEnabled(False)

        self.setMouseEnabled(
            x=True,
            y=True,
        )

        self.setXRange(
            0.0,
            360.0,
            padding=0.02,
        )

        self.setLabel(
            "bottom",
            "Angulo de la manivela",
            units="grados",
        )

        self.setLabel(
            "left",
            self.nombre_magnitud,
            units=self.unidad,
        )

    def crear_elementos(self):
        self.curva = self.plot(
            pen=pg.mkPen(
                color=(35, 105, 190),
                width=3,
            )
        )

        self.linea_vertical = pg.InfiniteLine(
            angle=90,
            movable=False,
            pen=pg.mkPen(
                color=(90, 90, 90),
                width=1.5,
                style=Qt.DashLine,
            ),
        )

        self.addItem(
            self.linea_vertical
        )

        self.marcador = pg.ScatterPlotItem(
            size=12,
            brush=pg.mkBrush(
                220,
                70,
                40,
            ),
            pen=pg.mkPen(
                color=(130, 35, 20),
                width=2,
            ),
        )

        self.addItem(
            self.marcador
        )

        self.etiqueta_valor = pg.TextItem(
            text="",
            anchor=(0, 1),
        )

        self.etiqueta_valor.setColor(
            (30, 30, 30)
        )

        self.addItem(
            self.etiqueta_valor
        )

    def establecer_datos(
        self,
        angulos_grados,
        valores,
        nombre_magnitud,
        unidad,
    ):
        self.angulos_grados = np.asarray(
            angulos_grados,
            dtype=float,
        )

        self.valores = np.asarray(
            valores,
            dtype=float,
        )

        self.nombre_magnitud = str(
            nombre_magnitud
        )

        self.unidad = str(
            unidad
        )

        self.curva.setData(
            self.angulos_grados,
            self.valores,
        )

        self.setLabel(
            "left",
            self.nombre_magnitud,
            units=self.unidad,
        )

        self.setTitle(
            self.nombre_magnitud
        )

        self.setXRange(
            0.0,
            360.0,
            padding=0.02,
        )

        if self.valores.size > 0:
            minimo = float(
                np.min(
                    self.valores
                )
            )

            maximo = float(
                np.max(
                    self.valores
                )
            )

            diferencia = (
                maximo - minimo
            )

            if diferencia <= 1e-12:
                margen = max(
                    abs(maximo) * 0.1,
                    1.0,
                )
            else:
                margen = (
                    diferencia * 0.12
                )

            self.setYRange(
                minimo - margen,
                maximo + margen,
                padding=0,
            )

        self.actualizar_marcador(
            0.0
        )

    def actualizar_marcador(
        self,
        angulo_grados,
    ):
        if self.angulos_grados.size == 0:
            return

        if self.valores.size == 0:
            return

        angulo_visible = (
            float(angulo_grados)
            % 360.0
        )

        valor_actual = float(
            np.interp(
                angulo_visible,
                self.angulos_grados,
                self.valores,
            )
        )

        self.linea_vertical.setValue(
            angulo_visible
        )

        self.marcador.setData(
            [angulo_visible],
            [valor_actual],
        )

        self.etiqueta_valor.setText(
            f"{angulo_visible:.1f} grados\n"
            f"{valor_actual:.2f} {self.unidad}"
        )

        rango_y = self.viewRange()[1]

        altura_rango = (
            rango_y[1]
            - rango_y[0]
        )

        desplazamiento = (
            altura_rango * 0.05
        )

        self.etiqueta_valor.setPos(
            angulo_visible,
            valor_actual + desplazamiento,
        )