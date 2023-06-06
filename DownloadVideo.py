import pytube
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from loguru import logger


class UploadingAVideoInAnotherStream(QObject):
    """
    Класс дополнительного потока для получения информации о видео и его загрузки
    """
    _signal_progress = pyqtSignal(int)
    _signal_error = pyqtSignal(str)
    _signal_finished_all = pyqtSignal()
    logger.info(f"Создал основные сигналы")

    _SIGNAL_CRITICAL_ERROR = pyqtSignal()
    logger.info(f"Создал важные сигналы")

    _signal_author = pyqtSignal(str)
    _signal_title = pyqtSignal(str)
    _signal_key_words = pyqtSignal(str)
    logger.info("Создал дополнительные сигналы")

    def __init__(self, path_saved: str, url_video: str):
        super(UploadingAVideoInAnotherStream, self).__init__()

        self._key_words = None
        self._title = None
        self._author = None

        self.__stream = None
        self.__YouTube_object = None

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
        logger.info("Поток начал работу")

        # ______________________________________________________________________________________
        self.__YouTube_object = pytube.YouTube(url=self.__url_video)
        logger.info("Попытка создания объекта видео")

        if self.__YouTube_object:
            logger.info(f"Объект видео создан: {self.__YouTube_object}")
        else:
            logger.info(f"Неудачная попытка создания объекта видео: {self.__YouTube_object}")
            self._signal_error.emit("Ошибка в создании объекта видео")
            self._SIGNAL_CRITICAL_ERROR.emit()

        # ______________________________________________________________________________________
        self.__stream = self.__YouTube_object.streams.get_highest_resolution()
        logger.info("Попытка получения наилучшего стрима объекта видео")

        if self.__stream:
            logger.info(f"Объект стрима видео создан: {self.__stream}")
        else:
            logger.info(f"Неудачная попытка создания объекта стрима видео: {self.__stream}")
            self._signal_error.emit("Ошибка в получении стрима видео")
            self._SIGNAL_CRITICAL_ERROR.emit()

        # ______________________________________________________________________________________
        self._author = self.__YouTube_object.author
        logger.info("Попытка получения автора видео")

        if self._author:
            logger.info(f"Автор получен: {self._author}")
            self._signal_author.emit(str(self._author))
        else:
            logger.info(f"Неудачная попытка получения автора видео: {self._author}")
            self._signal_error.emit("Ошибка при получении автора видео")

        # ______________________________________________________________________________________
        self._title = self.__YouTube_object.title
        logger.info("Попытка получения названия видео")

        if self._title:
            logger.info(f"Название видео получено: {self._title}")
            self._signal_title.emit(str(self._title))
        else:
            logger.info(f"Неудачная попытка получения названия видео: {self._title}")
            self._signal_error.emit("Ошибка при получении названия видео")

        # ______________________________________________________________________________________
        self._key_words = self.__YouTube_object.keywords
        logger.info("Попытка получения ключевых слов видео")

        if self._key_words:
            self._key_words = ', '.join(self._key_words)
            logger.info(f"Ключевые слова видео получены: {self._key_words}")
            self._signal_key_words.emit(str(self._key_words))
        else:
            logger.info(f"Неудачная попытка получения ключевых слов видео: {self._key_words}")
            self._signal_error.emit("Ошибка при получении ключевых слов видео")

        # ______________________________________________________________________________________
        self._signal_finished_all.emit()
        logger.info("Испущен сигнал окончания работы потока")
