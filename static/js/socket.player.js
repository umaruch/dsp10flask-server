let ws;

window.onload = function(){
    // Корректное отключение ws подключения при переходе на новую страницу
    ws = new WebSocket("ws://"+window.location.host+"/api/ws");

    ws.onmessage = function(event){
        let data = JSON.parse(event.data);
        sync_player_status(data);
    };

    ws.onclose = function(event){
        alert("Connection closed");
    };
}
