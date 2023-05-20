//要素の取得
const post_form = document.getElementById('post_form');
const post_button = document.getElementById('post_button');
const dynamic_part = document.getElementById('dynamic_part');

//イベントリスナの追加
post_button.addEventListener('click', async (event) => {
    var content = sanitize(post_form.value);
    var res = await exploit_sentence(content);
    update_dynamic_part(res);
    /* フォームをクリア */
    post_form.value = "";
});

//以下各種関数定義
function sanitize(input){
    /* フォームの入力内容を無害化 */
    return input.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
};

async function exploit_sentence(content){
    /* ローカルホストにMecabを動かしてもらいます */
    return (await fetch(`http://127.0.0.1:8000/?text=${content}`)).json();
};

function update_dynamic_part(res){
    /* 分割された単語それぞれに処理を施します */
    res.list.forEach((elem) => {
        var obj = document.createElement("div");
        obj.innerText = elem;
        obj.classList.add("obj");
        obj.setAttribute("obj-id",dynamic_part.childElementCount + 1);
        obj.setAttribute("tremor",Math.random());
        dynamic_part.append(obj);
        update_style(obj);
    })
};

function update_style(obj){
    obj.setAttribute("style",
        /* objにのみ適用されるスタイル transform: scaleX(${obj.getAttribute("tremor")}%);\
        */    
        `animation-duration:${Math.abs(1-obj.getAttribute("tremor"))*60}s;\
        top:${obj.getAttribute("tremor")*40}%;\
        height:${100-obj.getAttribute("tremor")*80}%;`
    );
}