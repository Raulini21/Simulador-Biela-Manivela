from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
)

from simulacion import PanelSimulacion
from analisis import PanelAnalisis
from motor_chevy import PanelMotorChevy


class VentanaPrincipal(QMainWindow):
    """
    Ventana principal de la aplicacion.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Sistema de Analisis Cinematico - Biela Manivela"
        )

        self.resize(
            1400,
            850,
        )

        self.setMinimumSize(
            1100,
            700,
        )

        self.crear_interfaz()
        self.conectar_paneles()
        self.aplicar_estilo()

    def crear_interfaz(self):
        self.pestanas = QTabWidget()

        self.panel_simulacion = (
            PanelSimulacion()
        )

        self.panel_analisis = (
            PanelAnalisis()
        )

        self.panel_motor_chevy = (
            PanelMotorChevy()
        )

        self.pestanas.addTab(
            self.panel_simulacion,
            "Simulacion",
        )

        self.pestanas.addTab(
            self.panel_analisis,
            "Analisis",
        )

        self.pestanas.addTab(
            self.panel_motor_chevy,
            "Motor Chevy 350",
        )

        self.setCentralWidget(
            self.pestanas
        )

    def conectar_paneles(self):
        """
        Conecta Simulacion con Analisis.
        """

        self.panel_simulacion.parametros_actualizados.connect(
            self.panel_analisis.actualizar_parametros
        )

        self.panel_analisis.actualizar_parametros(
            self.panel_simulacion.radio,
            self.panel_simulacion.longitud,
            self.panel_simulacion.rpm,
        )

    def aplicar_estilo(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #eef1f5;
            }

            QWidget {
                color: #20242a;
                font-family: Arial;
                font-size: 13px;
            }

            QTabWidget {
                background-color: #eef1f5;
            }

            QTabWidget::pane {
                background-color: #ffffff;
                border: 1px solid #bcc3cc;
                border-radius: 4px;
                top: -1px;
            }

            QTabBar::tab {
                background-color: #dfe4ea;
                color: #20242a;
                border: 1px solid #bcc3cc;
                border-bottom: none;
                min-width: 130px;
                min-height: 38px;
                padding: 4px 16px;
                font-size: 14px;
                font-weight: bold;
            }

            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #1558a6;
            }

            QTabBar::tab:hover {
                background-color: #edf3fa;
            }

            QGroupBox {
                background-color: #ffffff;
                color: #20242a;
                border: 1px solid #bcc3cc;
                border-radius: 7px;
                margin-top: 14px;
                padding-top: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 6px;
                color: #20242a;
                background-color: #ffffff;
            }

            QLabel {
                color: #20242a;
                background-color: transparent;
                font-size: 13px;
            }

            QPushButton {
                color: #20242a;
                background-color: #e7ebf0;
                border: 1px solid #aeb6c0;
                border-radius: 5px;
                min-height: 34px;
                padding: 3px 10px;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #d8e7f8;
                border-color: #4b84c6;
            }

            QPushButton:pressed {
                background-color: #c7dbf2;
            }

            QDoubleSpinBox {
                color: #20242a;
                background-color: #ffffff;
                border: 1px solid #aeb6c0;
                border-radius: 5px;
                padding-left: 8px;
                padding-right: 8px;
                font-size: 13px;
            }

            QDoubleSpinBox:hover {
                border-color: #3478c5;
            }

            QDoubleSpinBox:focus {
                border: 2px solid #3478c5;
            }

            QToolButton {
                color: #20242a;
                background-color: #eef1f5;
                border: 1px solid #aeb6c0;
                border-radius: 3px;
                padding: 0px;
            }

            QToolButton:hover {
                background-color: #d8e7f8;
                border-color: #3478c5;
            }

            QToolButton:pressed {
                background-color: #bfd6ef;
            }

            QComboBox {
                color: #20242a;
                background-color: #ffffff;
                border: 1px solid #aeb6c0;
                border-radius: 4px;
                padding: 2px 7px;
            }

            QComboBox:hover {
                border-color: #3478c5;
            }

            QComboBox QAbstractItemView {
                color: #20242a;
                background-color: #ffffff;
                selection-background-color: #d8e7f8;
                selection-color: #20242a;
            }

            QCheckBox {
                color: #20242a;
                spacing: 9px;
            }

            QCheckBox::indicator {
                width: 17px;
                height: 17px;
                background-color: #ffffff;
                border: 2px solid #7d8793;
                border-radius: 3px;
            }

            QCheckBox::indicator:checked {
                background-color: #3478c5;
                border-color: #245f9f;
            }

            QSlider::groove:horizontal {
                background-color: #c7cdd5;
                height: 6px;
                border-radius: 3px;
            }

            QSlider::sub-page:horizontal {
                background-color: #3478c5;
                height: 6px;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                background-color: #ffffff;
                border: 2px solid #3478c5;
                width: 17px;
                height: 17px;
                margin: -6px 0;
                border-radius: 9px;
            }
            """
        )