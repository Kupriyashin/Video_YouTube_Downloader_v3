import sys
from datetime import datetime
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog
from loguru import logger

from Forms import Ui_Form

"""
Преобразование uic -> py: pyuic5 Forms/Form_downloader.ui -o Forms/Form_downloader.py
Создание requirements файла: pip3 freeze > requirements.txt
"""

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")


class MainWindow(QtWidgets.QWidget, Ui_Form):
    """
    Основное окно программы где располагаются все элементы и начальные условия работы
    """

    def __init__(self):
        super().__init__()

        self.__path_saved = None

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.url_video.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)

        self.setFixedSize(525, 643)
        self.setWindowIcon(QIcon(str(Path('Resources', 'folderreddownload_93315.ico'))))
        self.ui.title_image.setPixmap(QPixmap(str(Path('Title Image', 'error_image.jpg'))))

        self.ui.listWidget.setWordWrap(True)

        self.ui.pushButton.clicked.connect(lambda: self.path_saved_add())

    @logger.catch()
    def logging_of_information(self, text: str, true_false: bool):
        """
        визуализация действий программы в listWidget'е для логирования
        :param text:
        :param true_false:
        :return:
        """
        try:
            if true_false:
                self.ui.listWidget.addItem(f"✅{datetime.now().strftime('%H:%M:%S')} - {text}")
                self.ui.listWidget.scrollToBottom()

            else:
                self.ui.listWidget.addItem(f"❌{datetime.now().strftime('%H:%M:%S')} - {text}")
                self.ui.listWidget.scrollToBottom()
        except Exception:

            self.ui.listWidget.addItem(
                f"❌{datetime.now().strftime('%H:%M:%S')} - Произошла внутренняя ошибка обмена данными")
            self.ui.listWidget.addItem(
                f"❌{datetime.now().strftime('%H:%M:%S')} - ❌ПЕРЕЗАГРУЗИТЕ ПРИЛОЖЕНИЕ!❌")
            self.ui.listWidget.scrollToBottom()

    @logger.catch()
    def path_saved_add(self):
        """
        Срабатывает при нажатии на кнопку "Указать папку сохранения"
        Вызывает QDialog-окно по выбору директории сохранения видео
        :return:
        """
        self.__path_saved = QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения видео')

        if self.__path_saved:

            self.__path_saved = Path(self.__path_saved)

            self.ui.save_path.setEnabled(False)
            self.ui.pushButton.setEnabled(False)

            self.ui.pushButton_2.setEnabled(True)
            self.ui.url_video.setEnabled(True)

            self.logging_of_information(text="Папка сохранения видео выбрана!", true_false=True)
            self.logging_of_information(text=f"Папка сохранения: {self.__path_saved}", true_false=True)

        else:
            self.logging_of_information(text="Выберите папку сохранения", true_false=False)

        logger.info(f"Путь сохранения видео: {Path(self.__path_saved)}")


if __name__ == '__main__':
    _app = QApplication(sys.argv)
    _app.setStyle("Fusion")
    _window = MainWindow()
    _window.show()
    sys.exit(_app.exec_())
