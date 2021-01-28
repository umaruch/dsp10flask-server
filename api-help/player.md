- Подключение к плееру(пример)

Если необходимы своевременные уведомления пользователя об изменениях

```javascript
var ws = new Websocket("ws://{host}/api/player/ws");
```

При корректном подключении выдает в ответе текущее состоение и текущий трек, если он есть.
Далее при изменениях плеера снова отправляет данные( songinfo отправляется только при подключении и при изменении трека )

Ответ:
```json
{
	"state":"pause",
	"song":2,
	"songId":36,
	"nextSong":0,
	"nextSongId":34,
	"elapsed":31.634,
	"duration":151.882,
	"bitRate":125,
	"audio":"44100:f:2",
	"sampleRate":44100,
	"bitDepth":null,
	"channels":2,
	"volume":50,
	"mixrampdb":0,
	"playlistVersion":29,
	"playlistLength":3,
	"repeat":true,
	"random":false,
	"single":false,
	"consume":false,
	"songinfo":
		{
			"id":36,
			"position":2,
			"title":"Time to Make History REAL Lyrics",
			"artist":"Persona 4 Golden",
			"album":"xPervertedkida",
			"date":"2013-06-24",
			"genre":"Music",
			"duration":151.882,
			"path":"Persona/Persona 4 Golden - Time to Make History REAL Lyr YK9Y1EqjDpY.m4a","lastModified":"2020-12-24T06:55:20.000Z"
		}
}
```

------------

- Команды плееру
Используется для отправки команд для управления плеером
```
/player/?cmd=(команда)&value=(аргумент, не всем командам нужно)
```
При успешном выполнении возвращает код 204, при неправильном запросе 400, при ошибке на стороне сервера возвращает код 500 с JSON обьектом:
```json
{
	error: "Текст ошибки"
}
```
Примеры команд и аргументы для них
|Команда  |Аргумент  |Назначение  |
|--|--|--|
|status  |-  |Отправка статуса плеера  |
|play  |-  |Проигрывать трек  |
|pause  |-  |Поставить на паузу  |
|stop  |-  |Остановить воспроизведение  |
|next  |-  |Следующий трек  |
|prev  |-  |Предыдущий трек  |
|time  |timeposition in sec |Переключить время трека|
|volume  |0-100  |Изменение громкости  |
|repeat  |0-выкл, 1-плейлист, 2-трек|Переключение плейлиста  |
|random  |0/1  |Переключение рандомного воспроизведения  |
