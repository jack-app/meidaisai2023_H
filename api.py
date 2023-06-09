# モジュールをインポート
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import MeCab
from aiofiles import open

from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
import sqlite3 as sql
import os

# FastAPIを起動
app = FastAPI()

# 静的ファイルを設定
app.mount(
    '/src',
    StaticFiles(directory="src"),
    name='static'
)

# ミドルウェア(ここはあんまり考えなくてもいい)
app.add_middleware(
    CORSMiddleware, # アクセスにCORSを使用
    allow_origins=["*"], # クロスオリジンの許可するリスト
    allow_credentials=True, # クッキーの共有を許可するか
    allow_methods=["*"], # 許可するHTTPメソッド
    allow_headers=["*"], # 許可するヘッダー
)

tagger = MeCab.Tagger() # MeCabのインスタンス

# Jinja2テンプレートで反映させる
templates = Jinja2Templates(directory='./templates')

# カレントディレクトリを変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# テーブルを新規作成
def initial_sql(dbpath):

    solars_data = [(1, '名大祭記念', 'StarImage.png'),
        (2, 'ユニバース', 'StarImage2.png'),
        (3, '住んでる町', 'StarImage3.png'),
        ]
    planets_data = [
        [],
        [(1, 'えんぴつ'), (2, 'けしごむ'), (3, '数学'), (4, '工学'), (5, 'マリオカート'), (6, '橋本環奈')],
        [(1, '本山'), (2, '八事'), (3, '今池'), (4, '栄'), (5, '金山'), (6, '一宮'), (7, '東岡崎')],
    ]

    # ファイルを作成
    conn = sql.connect(dbpath)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS solars(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            path TEXT NOT NULL)
        """)
    sqls = 'INSERT INTO solars (id, name, path) values (?, ?, ?)'
    cur.executemany(sqls, solars_data)

    # 太陽系のDBを作成
    for idx in range(len(solars_data)):
        table_name = "planets" + str(idx + 1)
        cur.execute("CREATE TABLE IF NOT EXISTS " + table_name +
            """(id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL)
            """)
        sqls = 'INSERT INTO ' + table_name +'(id, name) values(?, ?)'
        if len(planets_data[idx]) > 0: cur.executemany(sqls, planets_data[idx])
    conn.commit()

# データベースに接続
dbpath = "./src/db/planets.sqlite"
if os.path.isfile(dbpath) == False:
    initial_sql(dbpath)
conn = sql.connect(dbpath)

# 太陽系を表示する
@app.get("/")
async def title(request: Request):
    cur = conn.cursor()
    cur.execute("SELECT * FROM solars")
    solars = cur.fetchall()
    planets = []
    for idx in range(len(solars)):
        solars_name = "planets" + str(idx + 1)
        cur.execute("SELECT * FROM " + solars_name)
        planets.append(cur.fetchall())
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "solars": solars,
            "planets": planets,
        }
    )

@app.get("/{id}/planets/") # 惑星を選択
# ボタン投下後の処理を並行処理で受け取る
async def root(text = None):
    result = tagger.parseToNode(text) # 形態素分析の結果を返す
    node = result
    response = [] # レスポンスをリストで格納

    while node: # 分析結果が残っているか

        # node.surfaceは形態素分析された単語
        # node.featureは形態素分析の結果
        print(node.surface)
        print(node.feature.split(",")) 

        if node.surface: # node.surfaceが存在する場合
            response.append(node.surface) # 形態素分析された単語をレスポンスに追加
        node = node.next # 次の形態素分析結果に移る

    return {"list":response} # レスポンスを返す

#渡されたtextをwords.datに追記
@app.get("/write")
async def write(string):
    async with open("./src/words.dat","a",encoding="utf-8") as f:
        await f.write("\n"+string)
    return {}

#words.datに保存された内容を読み出し
@app.get("/read")
async def read():
    async with open("./src/words.dat","r",encoding="utf-8") as f:
        content = await f.read()
    return {"list":content.split("\n")}