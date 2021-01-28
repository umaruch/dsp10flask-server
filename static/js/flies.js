
// Отображение сведений о файлах или папках пользователю
function render_files(obj, data, root){ 
    data.forEach(element => {
        // Проверка на директориб
        if (typeof(element.directory) != "undefined"){
        
        } else {

        }
    });
}

// Отправка запроса на получение данных о директории
function load_data(obj, path, root){
    var request = XMLHttpRequest();
    if (path != ""){
        equest.open("GET", "http://"+window.location.host+"/api/files?path="+path);      
    } else {
        request.open("GET", "http://"+window.location.host+"/api/files");
    }
    request.send();
    request.onreadystatechange = function(){
        // console.log(rm_request);
        if(request.readyState == 4 && request.status == 200){
            render_files(obj, JSON.parse(request.responseText), root);
        }
    };
}

// Отправка запроса на добавление файла в плейлист

// Запрос на проигрываение директории или файла

load_data(
    document.getElementsByClassName("browser__list")[0],
    "",
    true
);