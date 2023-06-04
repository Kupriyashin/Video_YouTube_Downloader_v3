import sys
from datetime import datetime
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog
from loguru import logger
from Forms import Ui_Form
import re
from DownloadVideo import UploadingAVideoInAnotherStream

"""
Преобразование uic -> py: pyuic5 Forms/Form_downloader.ui -o Forms/Form_downloader.py
Создание requirements файла: pip3 freeze > requirements.txt

Приписка ADDITIONALMETHOD - означает неосновной метод
Приписка MAINMETOD - означает основной метод
Приписка COMPLEMENTARYMETHOD - означает метод для визуализации информации
"""

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")


class MainWindow(QtWidgets.QWidget, Ui_Form):
    """
    Основное окно программы где располагаются все элементы и начальные условия работы
    """

    def __init__(self):
        super().__init__()

        self.download_video_class = None
        self.download_video_thread = None

        self.__path_saved = None
        self.__url_video = None

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.url_video.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)

        self.setFixedSize(525, 643)
        self.setWindowIcon(QIcon(str(Path('Resources', 'folderreddownload_93315.ico'))))
        self.ui.title_image.setPixmap(QPixmap(str(Path('Title Image', 'error_image.jpg'))))

        self.ui.listWidget.setWordWrap(True)

        self.ui.pushButton.clicked.connect(lambda: self.path_saved_add_MAINMETOD())
        self.ui.pushButton_2.clicked.connect(lambda: self.download_video_MAINMETOD())

    @logger.catch()
    @pyqtSlot()
    def logging_of_information_COMPLEMENTARYMETHOD(self, information: str, true_false: bool) -> None:
        """
        Визуализация действий программы в listWidget'е для логирования
        :param information: 
        :param true_false:
        :return:
        """
        try:
            if true_false:
                self.ui.listWidget.addItem(f"✅{datetime.now().strftime('%H:%M:%S')} - {information}")
                self.ui.listWidget.scrollToBottom()

            else:
                self.ui.listWidget.addItem(f"❌{datetime.now().strftime('%H:%M:%S')} - {information}")
                self.ui.listWidget.scrollToBottom()
        except Exception:

            self.ui.listWidget.addItem(
                f"❌{datetime.now().strftime('%H:%M:%S')} - Произошла внутренняя ошибка обмена данными")
            self.ui.listWidget.addItem(
                f"❌{datetime.now().strftime('%H:%M:%S')} - ❌ПЕРЕЗАГРУЗИТЕ ПРИЛОЖЕНИЕ!❌")
            self.ui.listWidget.scrollToBottom()

    @logger.catch()
    @pyqtSlot()
    def path_saved_add_MAINMETOD(self):
        """
        Срабатывает при нажатии на кнопку "Указать папку сохранения"
        Вызывает QDialog-окно по выбору директории сохранения видео
        :return:
        """
        self.__path_saved = QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения видео')

        if self.__path_saved:

            self.__path_saved = Path(self.__path_saved)
            self.ui.save_path.setText(str(self.__path_saved))
            logger.info(f"Сохранил путь для скачивания: {self.__path_saved} и установил его в поле пути")

            self.ui.save_path.setEnabled(False)
            self.ui.pushButton.setEnabled(False)
            logger.info("Заблокировал взаимодействие с элементами получения пути сохранения")

            self.ui.pushButton_2.setEnabled(True)
            self.ui.url_video.setEnabled(True)
            logger.info("Включил кнопки указания ссылки на видео и его скачивания")

            self.logging_of_information_COMPLEMENTARYMETHOD(information="Папка сохранения видео выбрана!",
                                                            true_false=True)
            self.logging_of_information_COMPLEMENTARYMETHOD(information=f"Папка сохранения: {self.__path_saved}",
                                                            true_false=True)

        else:
            self.logging_of_information_COMPLEMENTARYMETHOD(information="Выберите папку сохранения", true_false=False)

            logger.info(f"Путь сохранения видео не получен: {Path(self.__path_saved)}")

    @logger.catch()
    @pyqtSlot()
    def download_video_MAINMETOD(self):
        """
        Срабатывает при нажатии кнопки "Скачать видео"
        Проверяет корректность ссылки
        Открывает новый поток, в котором будет получаться информация о видео и скачиваться само видео
        :return:
        """

        if re.fullmatch(r"^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+", self.ui.url_video.text()):

            self.logging_of_information_COMPLEMENTARYMETHOD(
                information=f"Введена корректная ссылка: {self.ui.url_video.text()}",
                true_false=True)

            self.__url_video = self.ui.url_video.text()
            logger.info(f"Сохранил ссылку на видео: {self.__url_video}")

            self.ui.url_video.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            logger.info("Заблокировал кнопки до окончания загрузки")

            self.download_video_class = UploadingAVideoInAnotherStream(
                path_saved=str(self.__path_saved),
                url_video=str(self.__url_video),
            )
            logger.info(f"Создан экземпляр класса UploadingAVideoInAnotherStream: {self.download_video_class}")

            self.download_video_thread = QThread()
            logger.info(f"Создан экземпляр класса потока: {self.download_video_thread}")

            self.download_video_class.moveToThread(self.download_video_thread)
            logger.info(f"Помещен класс загрузки видео в новый поток")

            logger.info(
                f"Настраиваю функцию получения и загрузки видео в другом потоке и выполняю действия при запуске")
            self.download_video_thread.started.connect(self.download_video_class.download_video_and_getting_information)
            self.download_video_thread.started.connect(
                lambda: self.updated_progress_bar_ADDITIONALMETHOD(value_of_progress=0))
            self.download_video_thread.started.connect(
                lambda: self.logging_of_information_COMPLEMENTARYMETHOD(information=f"Начал загрузку видео",
                                                                        true_false=True))

            logger.info(f"Настраиваю рабочие сигналы")
            self.download_video_class._signal_run_thread.connect(
                lambda: self.logging_of_information_COMPLEMENTARYMETHOD(information=f"Поток запущен", true_false=True))
            self.download_video_class._signal_error.connect(
                lambda err: self.logging_of_information_COMPLEMENTARYMETHOD(information=err, true_false=False))

            logger.info("Настраиваю сигналы конца")
            self.download_video_class._signal_finished_all.connect(self.download_video_thread.quit)
            self.download_video_class._signal_finished_all.connect(
                lambda: self.logging_of_information_COMPLEMENTARYMETHOD(information="Загрузка завершена",
                                                                        true_false=True))

            logger.info("Настраиваю действия после закрытия потока")
            self.download_video_thread.finished.connect(
                lambda: self.updated_progress_bar_ADDITIONALMETHOD(value_of_progress=100))
            self.download_video_thread.finished.connect(lambda: self.end_of_download_ADDITIONALMETHOD())
            self.download_video_thread.finished.connect(
                lambda: self.logging_of_information_COMPLEMENTARYMETHOD(information="Поток успешно закрыт", true_false=True))

            self.download_video_thread.start()
            logger.info("Поток запущен")

        else:
            logger.info(f"Некорректная ссылка: {self.ui.url_video.text()}")
            self.logging_of_information_COMPLEMENTARYMETHOD(
                information=f"Некорректная ссылка: {self.ui.url_video.text()}",
                true_false=False)

    @logger.catch()
    @pyqtSlot()
    def updated_progress_bar_ADDITIONALMETHOD(self, value_of_progress: int):
        self.ui.progressBar.setValue(value_of_progress)
        logger.info(f"Установил в progressBar значение: {value_of_progress}")

    @logger.catch()
    @pyqtSlot()
    def end_of_download_ADDITIONALMETHOD(self):
        self.ui.url_video.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)
        self.ui.url_video.clear()
        logger.info("Загрузка завершена! Установил поля ввода ссылки в активное состояние.")


if __name__ == '__main__':
    _app = QApplication(sys.argv)
    _app.setStyle("Fusion")
    _window = MainWindow()
    _window.show()
    sys.exit(_app.exec_())
