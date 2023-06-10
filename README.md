# YouTube Video Downloader v3 - Программное обеспечение для загрузки видео с ютуб на стационарный компьютер
Можно скачать приложение для Windows и Mac OS
##
<div align="center">
 <img src= "https://media.tenor.com/OVjLk6kZF_QAAAAd/a-certain-scientific-railgun-t-toaru-kagaku-no-railgun-t.gif" />
</div>

По сравнению с **YouTube Video Downloader v2**, v3 была написана за меньший промежуток времени с меньшим количеством нервотрепки. По большей части это связано с обновлением библиотеки [**pytube**](https://github.com/pytube/pytube).

В основном программных изменений как таковых нет, однако:
1. Отошел от загрузки видео по частям - теперь сразу скачивается видео и аудио в одном файле, что увеличило быстроту работы программы и уменьшило количество возникаемых ошибок.
2. Не использовал обработчик ошибок **<i>try: ... except: ... </i>**- теперь все на **<i>if-ах</i>** работает (вроде критических ошибок не наблюдается)
3. Приложение также многопоточно, но теперь вместо 3-х потоков только 2 используются (основной и дополнительный для загрузки видео)
4. Наконец-то разобрался как визуализировать процесс загрузки видео в реальном времени, ввиду чего убрал функцию заглушку визуализации.

Как и в прошлой версии, по всем возникшим вопросам писать в [Вконтакте](https://vk.com/kupriyashinnick).
