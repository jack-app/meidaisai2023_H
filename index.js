//要素の取得
const post_form = document.getElementById('post_form');
const post_button = document.getElementById('post_button');
const dynamic_part = document.getElementById('dynamic_part');
const dynamic_css = document.getElementById('dynamic_css');

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
    /* MeCabを呼ぶ */
};

function update_dynamic_part(res){
    /* 動的部分のアップデート */
};
