

addEventListener('click', function(event){
    tgtElm = event.target;
    if( tgtElm.getAttribute("css") != "btn" ){
        remove_elms_by_class("actMenuFrame");
    }
});

function data_menu_call(event, typ){
    
    remove_elms_by_class("actMenuFrame");
    
    event.preventDefault();
    var tgtElm = event.target;
    var lnk = tgtElm.getAttribute("lnk");

    var snapTgt = document.getElementById("snapTarget");
    var xPos = event.clientX + "px";
    var yPos = event.clientY + "px";

    var menuOpt = {}
    menuOpt['dir'] = {
        "open": lnk,
        "download zip": "/api/zip/download"+lnk, 
        "delete": "/data/delete"+lnk
    }
    if(lnk.endsWith("../")){
        menuOpt['dir'] = {
            "up": lnk
        }
    }
    menuOpt['file'] = {
        "download": "/api/file/download"+lnk, 
        "download zip": "/api/zip/download"+lnk, 
        "delete": "/data/delete"+lnk
    }

    var actMenuFrame = document.createElement("DIV");
    actMenuFrame.className = "actMenuFrame";
    snapTgt.appendChild(actMenuFrame);
    actMenuFrame.style.top = yPos;
    actMenuFrame.style.left = xPos;
    
    var actMenuArrow = document.createElement("DIV");
    actMenuFrame.appendChild(actMenuArrow);
    actMenuArrow.setAttribute("css", "arrow");
    
    for(var prop in menuOpt[typ]){
        var actMenuBtn = document.createElement("DIV");
        actMenuFrame.appendChild(actMenuBtn);
        actMenuBtn.setAttribute("css", "btn");
        actMenuBtn.setAttribute("lnk", menuOpt[typ][prop]);
        actMenuBtn.innerHTML = prop;
        actMenuBtn.onclick = function(){
            var lnk = this.getAttribute("lnk");
            location.href = lnk;
            var browserBox = document.getElementById("browserBox");
            //loader_call(browserBox);
            //console.log(lnk);
            remove_elms_by_class("actMenuFrame");
        }
    }
}



//-Helpers---------------------------------------------------------

function remove_elms_by_class(clName){
    var elmAry = document.getElementsByClassName(clName);
    for (var i = 0; i < elmAry.length; i++) {
        elmAry[i].parentNode.removeChild(elmAry[i]);
    }
}

//--------------------------------

function post_data(url){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhttp.responseText);
        }
    };
xhttp.open("POST", url, true);
xhttp.send();
}

//--------------------------------

function add_files_to_list(iptElm, elmId ){
    var tgtDiv = document.getElementById(elmId);
    tgtDiv.innerHTML = "";

    for (var i = 0; i < iptElm.files.length; i++) {
        var flDiv = document.createElement("DIV");
        tgtDiv.appendChild(flDiv);
        flDiv.innerHTML = iptElm.files[i]['name'];
    }
}

//--------------------------------

function loader_call(target=document.body){
		
    var blocker = document.createElement("div");
    blocker.classList.add("blocker");

    var loader_frame = document.createElement("div");
    loader_frame.classList.add("spinner");

    for (var i = 1; i < 4; i++) {
        var loader_bounce = document.createElement("div");
        loader_bounce.classList.add("bounce"+i);
        loader_frame.appendChild(loader_bounce);
    }

    blocker.appendChild(loader_frame);
    setTimeout( function(){
        target.appendChild(blocker);
    },200);
}


function loader_remove(target, sleep=0, follow_func=function(){}){
    
    setTimeout( function(){
        var blocker = target.getElementsByClassName("blocker")[0];
        target.removeChild(blocker);
        follow_func();
    }, sleep );
}

//---------------------------------------------------------------