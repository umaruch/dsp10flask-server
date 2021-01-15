const WebSocket = require("ws");
const MPC = require("mpc-js").MPC;
const http = require("http");

// MPC connection
var mpc = new MPC();
mpc.connectTCP('localhost', 6600);
var current_song_id = null;
// WebSocket init server
var wss = new WebSocket.Server({noServer:true});
// Http Server
var server = http.createServer();

function broadcast(data){
    // Send data to all connections
    data = JSON.stringify(data);
    wss.clients.forEach(function(conn, index){
        if(conn.readyState === WebSocket.OPEN){
           conn.send(data);
        }
    });
}

function start_mpd_status(ws){
    mpc.status.status().then(
        status=>{
            mpc.status.currentSong().then(
                song=>{
                    status.songinfo = song;
                    ws.send(JSON.stringify(status));
            });
    });
}

function send_mpd_status(){
    // Отправка статуса плеера
    mpc.status.status().then(
        status=>{
            if(current_song_id!=status.songId){
                current_song_id=status.songId;
                mpc.status.currentSong().then(
                    song=>{
                        status.songinfo = song;
                        broadcast(status);
                });
            }
            else{
                broadcast(status);
            }
        }
    );
}
setInterval(send_mpd_status, 5000);

wss.on("connection", function(ws){
    start_mpd_status(ws);
});

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

