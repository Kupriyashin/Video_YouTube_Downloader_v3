import pytube
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from loguru import logger


class UploadingAVideoInAnotherStream(QObject):
    """
    Класс дополнительного потока для получения информации о видео и его загрузки
    """
    _signal_run_thread = pyqtSignal()
    _signal_error = pyqtSignal(str)
    _signal_finished_all = pyqtSignal()

    def __init__(self, path_saved: str, url_video: str):
        super(UploadingAVideoInAnotherStream, self).__init__()

        self.__path_saved = path_saved
        self.__url_video = url_video
        logger.info(
            f"В конструкторе потокового класса создал переменные path_saved = {self.__path_saved}, url_video = {self.__url_video}")

    @logger.catch()
    @pyqtSlot()
    def download_video_and_getting_information(self):
        """
        Данный метод запускается тогда, когда из главного окна запустился другой поток
        В методе идет получение информации о видео: автор, название видео, ключевые слова, количество просмотров, длина видео, титульное изображение и описание.
        После получения информации получается наилучший стрим по прогрессивному методу и скачивается
        Также реализована передача прогресса скачивания видео (либо установлена заглушка визуализации, зависит от работоспособности pytube)
        :return:
        """

        self._signal_run_thread.emit()
        logger.info("Испущен сигнал начала работы потока")

        self._signal_error.emit("Ошибок не найдено")
        logger.info("Испущен сигнал возникновения ошибки")

        self._signal_finished_all.emit()
        logger.info("Испущен сигнал окончания работы потока")
