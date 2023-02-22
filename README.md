# Расчёт некоторых видов геоагрегаций по датасету жилых домов Москвы

Для развёртывания docker контейнера нужно выполнить команду docker compose up (контейнер запустится не в фоновом режиме) или docker compose up -d (контейнер запустится в фоновом режиме) из директории проекта.

geoaggr.py - файл с классом, в котором хранится данный датасет и имеются два метода, которые нужно реализовать.
schemas.py - файл, содержащий JSON схемы для валидации поля geometry.
main.py - главный файл, в котором реализован web на fastapi и запуск uvicorn сервера.

Внутри контейнера сервер работает на host = 0.0.0.0 и port = 8000. Запросы к серверу отправляются с того же устройства, где запущен контейнер, на адреса http://localhost:8000/aggr_hexes или http://localhost:8000/aggr_polygon для первого и второго метода соответственно.

Подразумевается, что входные данные предоставляются в том виде, который указан в примерах, то есть в виде словаря, иначе выводится сообщение об ошибке входных данных. Я тестировал сервис через библиотеку requests для python путём отправки POST запроса, причём, если передавать вышеописанные данные через data = ... , то нужно оборачивать данные в кавычки, а, если через json = ... - то не нужно. По идее, отправка запросов к сервису через браузер, curl и т.п. тоже должна работать, но я не успел проверить.

Не разобрался с тем, как сделать ограничение на количество передаваемых параметров в данных в запросе, то есть, если в запросе с валидными данными (например, как в примере) добавить ещё какие-нибудь параметры, то в моей реализации всё отработает верно.

В целом, я постарался обработать большинство некорректных обращений к сервису, но вероятно имеются не совсем очевидные случаи, которые не были предусмотрены в моей реализации.