import os
import sys
from datetime import datetime
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread, Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFontMetrics, QPainter
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
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

            logger.info(
                f"Настраиваю стартовые сигналы")
            self.download_video_thread.started.connect(
                lambda: self.updated_progress_bar_ADDITIONALMETHOD(value_of_progress=0))
            self.download_video_thread.started.connect(
                lambda: self.logging_of_information_COMPLEMENTARYMETHOD(information=f"Начал загрузку видео",
                                                                        true_false=True))

            logger.info(f"Настраиваю рабочие сигналы")
            self.download_video_class._signal_error.connect(
                lambda err: self.logging_of_information_COMPLEMENTARYMETHOD(information=err, true_false=False))
            self.download_video_class._signal_progress.connect(
                lambda progress: self.updated_progress_bar_ADDITIONALMETHOD(value_of_progress=progress))
            self.download_video_class._signal_information.connect(
                lambda inform: self.logging_of_information_COMPLEMENTARYMETHOD(information=inform, true_false=True))


            logger.info(f"Настраиваю сигнал получения автора")
            self.download_video_class._signal_author.connect(
                lambda author: self.add_author_ADDITIONALMETHOD(author=author))
            self.download_video_class._signal_author.connect(
                lambda author: self.logging_of_information_COMPLEMENTARYMETHOD(information=f"Автор видео: {author}",
                                                                               true_false=True))

            logger.info(f"Настраиваю сигнал получения названия видео")
            self.download_video_class._signal_title.connect(
                lambda title: self.add_title_ADDITIONALMETHOD(title=title))
            self.download_video_class._signal_title.connect(
                lambda title: self.logging_of_information_COMPLEMENTARYMETHOD(information=f"Название видео: {title}",
                                                                              true_false=True))

            logger.info(f"Настраиваю сигнал получения ключевых слов")
            self.download_video_class._signal_key_words.connect(
                lambda keywords: self.add_key_words_ADDITIONALMETHOD(key_word=keywords))
            self.download_video_class._signal_key_words.connect(
                lambda keywords: self.logging_of_information_COMPLEMENTARYMETHOD(
                    information=f"Ключевые слова видео: {keywords}",
                    true_false=True))

            logger.info(f"Настраиваю сигнал получения количества просмотров")
            self.download_video_class._signal_number_of_views.connect(
                lambda views: self.logging_of_information_COMPLEMENTARYMETHOD(
                    information=f"Количество просмотров видео: {views}",
                    true_false=True))
            self.download_video_class._signal_number_of_views.connect(
                lambda views: self.add_views_ADDITIONALMETHOD(views=views))

            logger.info(f"Настраиваю сигнал получения длины видео")
            self.download_video_class._signal_length.connect(
                lambda length: self.logging_of_information_COMPLEMENTARYMETHOD(
                    information=f"Длина видео: {length}",
                    true_false=True))
            self.download_video_class._signal_length.connect(
                lambda length: self.add_length_ADDITIONALMETHOD(length=length))

            logger.info(f"Настраиваю сигнал получения описания видео")
            self.download_video_class._signal_description.connect(
                lambda description: self.logging_of_information_COMPLEMENTARYMETHOD(
                    information=f"Описание видео: {description}",
                    true_false=True))
            self.download_video_class._signal_description.connect(
                lambda description: self.ui.textEdit.setText(description))

            logger.info(f"Настраиваю сигнал получения титульного изображения видео")
            self.download_video_class._signal_image_title.connect(
                lambda path_image: self.logging_of_information_COMPLEMENTARYMETHOD(
                    information=f"Путь к титульному изображению: {path_image}",
                    true_false=True))
            self.download_video_class._signal_image_title.connect(
                lambda path_image: self.add_title_image_ADDITIONALMETHOD(path_image=path_image))

            logger.info(f"Настраиваю сигнал КРИТИЧЕСКОЙ ОШИБКИ")
            self.download_video_class._SIGNAL_CRITICAL_ERROR.connect(
                lambda: self.logging_of_information_COMPLEMENTARYMETHOD(
                    information="КРИТИЧЕСКАЯ ОШИБКА! ИЗУЧИТЕ ЛОГИ ПРИЛОЖЕНИЯ", true_false=False))
            self.download_video_class._SIGNAL_CRITICAL_ERROR.connect(
                lambda: self.end_of_download_ADDITIONALMETHOD())
            self.download_video_class._SIGNAL_CRITICAL_ERROR.connect(
                lambda: self.updated_progress_bar_ADDITIONALMETHOD(value_of_progress=0))

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
                lambda: logger.info("Поток закрыт"))
            self.download_video_thread.finished.connect(
                lambda: self.finish_window_ADDITIONALMETHOD())

            self.download_video_thread.start()
            logger.info("download_video_thread.start()")

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

    @logger.catch()
    @pyqtSlot()
    def add_author_ADDITIONALMETHOD(self, author: str):
        if author:
            self.ui.author.setText(self.elided_text(text=author, pyqt_object=self.ui.author))
            self.ui.author.setStyleSheet("color: green;")

            logger.info("Установил автора в поле")

    @logger.catch()
    @pyqtSlot()
    def add_title_ADDITIONALMETHOD(self, title: str):
        if title:
            self.ui.title_video.setText(self.elided_text(text=title, pyqt_object=self.ui.title_video))
            self.ui.title_video.setStyleSheet("color: green;")

            logger.info("Установил название видео в поле")

    @logger.catch()
    @pyqtSlot()
    def add_key_words_ADDITIONALMETHOD(self, key_word: str):
        if key_word:
            self.ui.key_words.setText(self.elided_text(text=key_word, pyqt_object=self.ui.key_words))
            self.ui.key_words.setStyleSheet("color: green;")

            logger.info("Установил ключевые слова в поле")

    @logger.catch()
    @pyqtSlot()
    def add_views_ADDITIONALMETHOD(self, views: str):
        if views:
            self.ui.number_of_views.setText(self.elided_text(text=views, pyqt_object=self.ui.number_of_views))
            self.ui.number_of_views.setStyleSheet("color: green;")
            logger.info("Установил количество просмотров в поле")

    @logger.catch()
    @pyqtSlot()
    def add_length_ADDITIONALMETHOD(self, length: str):
        if length:
            self.ui.video_length.setText(self.elided_text(text=length, pyqt_object=self.ui.video_length))
            self.ui.video_length.setStyleSheet("color: green;")
            logger.info("Установил длину видео в поле")

    @logger.catch()
    @pyqtSlot()
    def add_title_image_ADDITIONALMETHOD(self, path_image: Path):
        if path_image:

            logger.info(f"Путь к титульному изображению: {str(path_image)}")

            self.ui.title_image.setPixmap(QPixmap(str(path_image)))
            logger.info("Титульное изображение установлено")

            os.remove(path_image)
            logger.info("Титульное изображение удалено из папки сохранения")

        else:
            self.logging_of_information_COMPLEMENTARYMETHOD(information=f"Ошибка доступа к титульному изображению!",
                                                            true_false=False)

    @logger.catch()
    def elided_text(self, text, pyqt_object):

        metric = QFontMetrics(pyqt_object.font())
        logger.info(f"Объект metric создан: {metric}")
        elided = metric.elidedText(text, Qt.ElideRight, pyqt_object.width())
        logger.info(f"Объект elided создан: {elided}")

        return str(elided)

    @logger.catch()
    @pyqtSlot()
    def finish_window_ADDITIONALMETHOD(self):
        logger.info("Запускаю диалоговое окно завершения загрузки")

        msg = QMessageBox(self)
        msg.setFixedSize(300, 150)
        logger.info(f"Создал объект QMessageBox: {msg}")

        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Информационное окно")
        msg.setText("Загрузка завершена")
        logger.info("Установил в QMessageBox основные данные")

        x = msg.exec_()
        logger.info("Окно QMessageBox закрыто")


if __name__ == '__main__':
    _app = QApplication(sys.argv)
    _app.setStyle("Fusion")
    _window = MainWindow()
    _window.show()
    sys.exit(_app.exec_())
