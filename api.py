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

# MeCabの初期設定
mecab_mode = True
tagger = MeCab.Tagger()

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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    # メッセージのDBを作成
    cur.execute("""CREATE TABLE IF NOT EXISTS message
        (solar_id INTEGER,
        planet_id INTEGER,
        text TEXT NOT NULL)
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS raw_message
        (solar_id INTEGER,
        planet_id INTEGER,
        text TEXT NOT NULL)
    """)
    conn.commit()


# データベースに接続
dbpath = "./src/db/planets.sqlite"
initial_db = False
if initial_db == True or os.path.isfile(dbpath) == False:
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

# 惑星を追加
@app.get("/addplanets")
async def add_planets(solar: str, planet: str):
    solar_id = get_solar_id(solar)
    cur = conn.cursor()
    cur.execute("SELECT id FROM planets" + str(solar_id) + " WHERE name = '" + planet + "'")
    if len(cur.fetchall()): raise Exception()
    cur.execute('INSERT INTO planets' + str(solar_id) +' (name) VALUES ("' + planet + '")')
    conn.commit()
    return {}

def get_solar_id(solar_name):
    conn = sql.connect(dbpath)
    cur = conn.cursor()
    cur.execute("SELECT id FROM solars WHERE name = '" + solar_name + "'")
    solar_id = cur.fetchall()[0][0]
    return solar_id

def get_planet_id(solar_name, planet_name):
    conn = sql.connect(dbpath)
    cur = conn.cursor()
    table_name = "planets" + str(get_solar_id(solar_name))
    cur.execute("SELECT id FROM " + table_name + " WHERE name = '" + planet_name + "'")
    print("SELECT id FROM " + table_name + " WHERE name = '" + planet_name + "'")

    planet_id = cur.fetchall()[0][0]
    return planet_id


# 惑星を選択
@app.get("/planet/{solar}/{planet}")
async def planet(request: Request, solar: str, planet: str):
    return templates.TemplateResponse(
        "planet.html",
        {
            "request": request,
            "solar": solar,
            "planet": planet,
        }
    )

# メッセージを追加
@app.get("/planet/{solar}/{planet}/addmsg")
async def root(solar: str, planet: str, text: str):
    message = ""
    if mecab_mode:
        message = sentence_words(text)
    else:
        message = [text]

    # データベースにまとめて追加
    cur = conn.cursor()
    for msg in message:
        values = "( " + str(get_solar_id(solar)) + ", " + str(get_planet_id(solar, planet)) + ", '" + msg + "')"    
        cur.execute("INSERT INTO message (solar_id, planet_id, text) VALUES " + values)
    values = "( " + str(get_solar_id(solar)) + ", " + str(get_planet_id(solar, planet)) + ", '" + text + "')"    
    cur.execute("INSERT INTO raw_message (solar_id, planet_id, text) VALUES " + values)
    conn.commit()
    
    return {"list": message}

# 形態素分析の結果を返す
def sentence_words(text):
    
    result = tagger.parseToNode(text)
    node = result
    response = [] # レスポンスをリストで格納

    while node: # 分析結果が残っているか
        if node.surface: # node.surfaceが存在する場合
            response.append(node.surface) # 形態素分析された単語をレスポンスに追加
        node = node.next # 次の形態素分析結果に移る

    return response


"""
#渡されたtextをデータベースに追記
@app.get("/planet_write")
async def write(string):
    async with open("./src/words.dat","a",encoding="utf-8") as f:
        await f.write("\n"+string)
    return {}
"""

# データベースに保存された内容を読み出し
@app.get("/planet/{solar}/{planet}/read")
async def read(solar: str, planet: str):
    """
    async with open("./src/words.dat","r",encoding="utf-8") as f:
        content = await f.read()
    return {"list":content.split("\n")}
    """
    cur = conn.cursor()
    cur.execute("SELECT text FROM message WHERE solar_id = " + str(get_solar_id(solar)) + " AND planet_id= " + str(get_planet_id(solar, planet)))
    messages = [row[0] for row in cur.fetchall()]
    return {'list': messages}

# 惑星を探索する
@app.get("/search/{solar}/{planet}")
def search(solar: str, planet: str, request: Request):
    conn = sql.connect(dbpath)
    cur = conn.cursor()  
    cur.execute("SELECT text FROM raw_message WHERE solar_id = " + str(get_solar_id(solar)) + " AND planet_id= " + str(get_planet_id(solar, planet)))
    messages = [row[0] for row in cur.fetchall()]
    return templates.TemplateResponse(
    "star.html",
    {
        "request": request,
        "solar": solar,
        "planet": planet,
        "messages": messages,
    }
)
