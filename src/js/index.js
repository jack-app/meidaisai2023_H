// 惑星の移動速度・色をランダムに設定
window.onload = function() {
    const ele = document.getElementsByClassName("orbit");
    for (let i=0; i<ele.length; i++) {
        
        // 回転速度
        var velocity = Math.floor( Math.random() * 91 ) + 30;
        ele[i].style.transformOrigin = "0 0 0";
        if (Math.random() > 0.5) {
            var direct = "rotation";
            var undirect = "rotation2";
        }
        else {
            var direct = "rotation2";
            var undirect = "rotation";
        }
        ele[i].style.animation = velocity.toString() + "s linear infinite " + direct;

        // 回転半径・色
        var planet = ele[i].getElementsByClassName('planet')[0];
        planet.style.left = (Math.floor(Math.random() * 201) + 150).toString() + "%";
        planet.style.animation = velocity.toString() + "s linear infinite " + undirect;

        var color = {r:0, g:0, b:0};
        for (let i in color) {
            color[i] = Math.floor(Math.random() * 100) + 100;
        }
        planet.style.background = "rgb(" + color.r + ", " + color.g + ", " + color.b + ")";
    }
}