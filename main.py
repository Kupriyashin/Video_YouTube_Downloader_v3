from loguru import logger


"""
Преобразование uic -> py: pyuic5 Forms/Form_downloader.ui -o Forms/Form_downloader.py
"""

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")



