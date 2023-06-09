var positionX;					/* スクロール位置のX座標 */
var STORAGE_KEY = "scrollX";	/* ローカルストレージキー */

/*
 * checkOffset関数: 現在のスクロール量をチェックしてストレージに保存
 */
function checkOffset(){
	positionX = window.pageXOffset;
	localStorage.setItem(STORAGE_KEY, positionX);
}

// 惑星の移動速度・色をランダムに設定
window.onload = function() {
    const ele = document.getElementsByClassName("orbit");
    for (let i=0; i<ele.length; i++) {
        
        // 回転速度
        var velocity = Math.floor( Math.random() * 91 ) + 30;
        var initial = Math.floor( Math.random() * velocity);
        ele[i].style.transformOrigin = "0 0 0";
        if (Math.random() > 0.5) {
            var direct = "rotation";
            var undirect = "rotation2";
        }
        else {
            var direct = "rotation2";
            var undirect = "rotation";
        }
        ele[i].style.animation = velocity.toString() + "s linear -" + initial.toString() + "s infinite " + direct;

        // 回転半径・色
        var planet = ele[i].getElementsByClassName('planet')[0];
        planet.style.left = (Math.floor(Math.random() * 201) + 150).toString() + "%";
        planet.style.animation = velocity.toString() + "s linear -" + initial.toString() + "s infinite " + undirect;

        var color = {r:0, g:0, b:0};
        for (let i in color) {
            color[i] = Math.floor(Math.random() * 100) + 100;
        }
        planet.style.background = "rgb(" + color.r + ", " + color.g + ", " + color.b + ")";
    }
    rewrite_solarname();

    // ストレージチェック
	positionX = localStorage.getItem(STORAGE_KEY);
	// 前回の保存データがあればスクロールする
	if(positionX !== null){
		scrollTo(positionX, 0);
	}
}

// 惑星名を表示
function rewrite_solarname() {
    const solars = document.getElementsByClassName('polar');
    let value = 99999;
    let solarName = "";
    for (let i=0; i<solars.length; i++) {
        let distance = Math.abs(solars[i].getBoundingClientRect().left - window.innerWidth / 2);
        if (distance < value) {
            value = distance;
            solarName = solars[i].id;
        }
    }
    
    // 惑星名を書き換え
    const nameUI = document.getElementsByClassName('solar-name-UI')[0];
    nameUI.textContent = "惑星系: " + solarName;
    console.log(nameUI.textContent);
};

window.addEventListener('scroll', function() {
    rewrite_solarname();
});

// 惑星名を追加
async function add_planets() {
    let solarName = document.getElementsByClassName('solar-name-UI')[0]
    solarName = solarName.textContent.slice(5);
    const planetsName = document.getElementById('planets-name').value;
    console.log(solarName);
    console.log(planetsName);

    /* pythonのデータベースに登録 */
    const params = {
        solar: solarName,
        planet: planetsName
    }
    const urlParams = new URLSearchParams(params).toString();
    checkOffset();
    console.log(positionX);
    try {
        await fetch('/addplanets/?' + urlParams)
    } catch {
        return;
    }

    // 変更を反映
    document.location.reload();
}