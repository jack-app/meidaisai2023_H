var user = document.getElementById('user');
var userPos = user.getBoundingClientRect();

// JSを一時停止する
const sleep = waitTime => new Promise( resolve => setTimeout(resolve, waitTime) );

// キャラクターの初期位置
var usery = userPos.top;
var userx = userPos.left;
var timer = Date.now();

// キーが押されたときに呼び出される関数
addEventListener("keydown", keydownfunc);
function keydownfunc( event ) {
    var key_code = event.keyCode;
    if ( Date.now() - timer < 100) return;
    if ( key_code === 37) userx -= 30;
    if ( key_code === 38) usery -= 30;
    if ( key_code === 39) userx += 30;
    if ( key_code === 40) usery += 30;
    user.style.top = Math.floor(usery) + "px";
    user.style.left = Math.floor(userx) + "px";
    user.style.zIndex = Math.floor(usery + 100).toString();
    timer = Date.now();
}

// 近づいたらCPUのコメントを表示
addEventListener("keydown", cpufunc);
function cpufunc() {
    const ele = document.getElementsByClassName("cpu-img");
    for (let i=0; i<ele.length; i++) {
        var cpuPos = ele[i].getBoundingClientRect();
        var cpuDis = Math.sqrt(Math.pow( userx - cpuPos.left, 2 ) + Math.pow( usery - cpuPos.top, 2 ));
        if (cpuDis <= 150) {
            ele[i].nextElementSibling.style.opacity = "1";
        }
        else {
            ele[i].nextElementSibling.style.opacity = "0";
        }
    }
}


// ロード時の設定
window.onload = function() {
    // CPUをメッセージ分だけセットする
    const ele = document.getElementsByClassName("cpu");
    for (let i=0; i<ele.length; i++) {
        var img = ele[i].getElementsByClassName("cpu-img")[0];
        console.log(img.src);
        img.src = "/src/img/spaceman/spaceman"+ (Math.floor(Math.random() * 12)).toString() +".png";
        ele[i].style.top = (Math.floor(Math.random() * 50) + 20).toString() + "%";
        ele[i].style.left = (Math.floor(Math.random() * 70) + 10).toString() + "%";
        ele[i].style.zIndex = Math.floor(ele[i].getBoundingClientRect().top + 100).toString();
    }
    // その他設定
    user.style.zIndex = Math.floor(usery + 100).toString();
    cpufunc();
}


/*
//CPU
document.getElementById("speech-wrapper1").style.visibility = "hidden";
var cpu1 = document.getElementById( 'cpu1' ) ;
var cpu1pos = cpu1.getBoundingClientRect() ;
var cpu1y = cpu1pos.top;
var cpu1x = cpu1pos.left;
addEventListener( "keydown",  cpufunc1);
function cpufunc1(){
    var cpu1dis = Math.sqrt( Math.pow( userx-cpu1x, 2 ) + Math.pow( usery-cpu1y, 2 ) ) 
    if(cpu1dis <= 150) document.getElementById("speech-wrapper1").style.visibility = "visible";
    else document.getElementById("speech-wrapper1").style.visibility = "hidden";
}

document.getElementById("speech-wrapper2").style.visibility = "hidden";
var cpu2 = document.getElementById( 'cpu2' ) ;
var cpu2pos = cpu2.getBoundingClientRect() ;
var cpu2y = cpu2pos.top;
var cpu2x = cpu2pos.left;
addEventListener( "keydown",  cpufunc2);
function cpufunc2(){
    var cpu2dis = Math.sqrt( Math.pow( userx-cpu2x, 2 ) + Math.pow( usery-cpu2y, 2 ) ) 
    if(cpu2dis <= 150) document.getElementById("speech-wrapper2").style.visibility = "visible";
    else document.getElementById("speech-wrapper2").style.visibility = "hidden";
}
*/