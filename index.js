const WebSocket = require("ws");
const MPC = require("mpc-js").MPC;
const http = require("http");

// MPC connection
var mpc = new MPC();
mpc.connectTCP('localhost', 6600);
var current_song_id = null;
// WebSocket init server
var wss = new WebSocket.Server({noServer:true});
// // Http Server
var server = http.createServer();

// Отправка необходимых данных всем пользователям
function broadcast(data){
    data = JSON.stringify(data);
    wss.clients.forEach(function(conn, index){
        if(conn.readyState === WebSocket.OPEN){
           conn.send(data);
        }
    });
}

// Отправка текущего статуса новому соединению
function start_mpd_status(ws){
    mpc.status.status().then(
        status=>{
            mpc.currentPlaylist.playlistInfo().then(
                songs=>{
                    status.queue = songs;
                    ws.send(JSON.stringify(status));
            });
    });
}

// Отправка статуса плеера при смене состояния воспроизведения
function send_mpd_status_witch_song_check(){
    // Получаем статус плеера
    mpc.status.status().then(
        status=>{
            // Проверка на то что музыка сменилась
            if(current_song_id!=status.songId){
                current_song_id=status.songId;
                mpc.currentPlaylist.playlistInfo().then(
                    songs=>{
                        status.queue = songs;
                        broadcast(status);
                });
            }
            else{
                broadcast(status);
            }
        }
    );
}

// Отправка статуса плеера при смене состояния воспроизведения
function send_mpd_status_with_current_playlist(){
    // Получаем статус плеера
    mpc.status.status().then(
        status=>{
                mpc.currentPlaylist.playlistInfo().then(
                    songs=>{
                        status.queue = songs;
                        broadcast(status);
                });
        }
    );
}

// Отправка статуса плеера
function send_mpd_status(){
    // Получаем статус плеера
    mpc.status.status().then(
        status=>{
            broadcast(status);
        }
    );
}

// Прослушивание событий, связанных с воспроизведением
mpc.on("changed-player", function(){
    console.log("Трек изменен");
    send_mpd_status_witch_song_check();
});

// Прослушивание событий, связанных с настройками воспроизведения
mpc.on("changed-options", function(){
    send_mpd_status();
});

// Прослушивание событий, связанных с настройками громкости
mpc.on("changed-mixer", function(){
    send_mpd_status();
});

// При изменениях в текущем плейлисте
mpc.on("changed-playlist", function(){
    send_mpd_status_with_current_playlist()
});

// Обработка подключения нового клиента
wss.on("connection", function(ws){
    console.log("Новое подключение");
    start_mpd_status(ws);
});

// Обработка запроса клиента апгрейднуть соединение до вебсокета
server.on('upgrade', function(request, socket, head){
    if(request.url=="/api/ws"){
        wss.handleUpgrade(request, socket, head, function(ws){
            wss.emit("connection", ws, request);
        });
    }
    else{
        socket.destroy();
    }
});

server.listen(8088);
