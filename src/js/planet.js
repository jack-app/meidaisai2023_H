//要素の取得
const post_form = document.getElementById('post_form');
const post_textbox = document.getElementById('post_textbox');
const post_button = document.getElementById('post_button');
const dynamic_part = document.getElementById('dynamic_part');

//イベントハンドラの除去
post_form.onsubmit = ()=>{return false;};
post_button.onsubmit = ()=>{return false;};
post_textbox.onsubmit = ()=>{return false;};

//イベントリスナの追加
async function post(event){
    try {
        var content = sanitize(post_textbox.value);
        var res = await split_sentence(content);
        console.log(res);
        update_dynamic_part(res);
        /* フォームをクリア */
        post_textbox.value = "";
        /* ローカルに保存します */
        register_strings(res.list);
    } catch (error) {
        console.log(error);
    }
    return false;
};

post_button.addEventListener('click',post);
document.addEventListener('keypress',(event) => {
    if (event.code === "Enter" && event.shiftKey === true) {post();};
});

//以下各種関数定義
function sanitize(input){
    /* フォームの入力内容を無害化 */
    return input
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
};

async function split_sentence(content){
    /* ローカルホストにMecabを動かしてもらいます */
    return (
        await fetch(location.pathname + '/addmsg?text=' + content)
        ).json();
};

function update_dynamic_part(res){
    /* 分割された単語それぞれに処理を施します */
    res.list.forEach((word) => {
        /* 画面に反映します */
        var obj = document.createElement("div");
        obj.innerHTML = "<div class='obj-text'>" + word + "</div>";
        obj.classList.add("obj");
        obj.setAttribute("obj-id",dynamic_part.childElementCount + 1);
        obj.setAttribute("tremor",Math.random());

        dynamic_part.append(obj);
        update_style(obj);
    })
};

function update_style(obj){
    console.log(obj);
    const duration = Math.floor(obj.getAttribute("tremor")*60) + 10;
    /* objにのみ適用されるスタイル */
    /*回転中心が画面中央になるように調整しています*/
    obj.style.animation = duration.toString() + "s linear -" + (Math.floor(Math.random() * duration)).toString() + "s infinite spine";
    obj.firstElementChild.style.top = (Math.floor(obj.getAttribute("tremor") * 35)).toString() + "%";
};

async function register_strings(strings){
    /*渡されたstringの配列をデータベースに保存します*/
    string = strings.join("%0D%0A");
    //await fetch('planet_write?string=${string}');
};

async function load_objects(){
    /* データベースに保存された内容を読み出します。 */
    return (await fetch(location.pathname + '/read')).json();
};

// 以前の内容を呼び出させる
async function restore_previous_state(){
    var res = await load_objects();
    console.log(res);
    update_dynamic_part(res);
};
restore_previous_state();