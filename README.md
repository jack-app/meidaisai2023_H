# meidaisai2023_F

## 要件

### TRANSITION DIAGRAM

```mermaid
flowchart TB

QUERY1("GET")
TEXT0{"自動分岐"}
TEXT1(["動的コンテンツ"])
TEXT2("潜在的動的コンテンツ")
TEXT3["画面遷移未確定*"]

subgraph RootServer
    SCENE1("サーバー選択")
    IF1{"COOKIE"}
end

subgraph StellarServer
    IF2{"COOKIE"}

    SCENE2(["トピック一覧（ゲスト）"])
    SCENE3(["トピック（ゲスト）*"])
    SCENE4["ログイン"]
    SCENE5["登録"]
    SCENE6(["トピック一覧"])
    SCENE7["ユーザー設定*"]
    SCENE9(["トピック*"])
end

QUERY1-->IF1
IF1--"サーバーに参加済み"-->IF2
IF1--"サーバーに未参加"-->SCENE1
SCENE1-->IF2
IF2 --> SCENE2
IF2 --> SCENE6
SCENE2-->SCENE1
SCENE6-->SCENE1
SCENE9-->SCENE1
SCENE3-->SCENE1
SCENE2---SCENE4
SCENE2---SCENE5
SCENE4-->SCENE6
SCENE5-->SCENE6
SCENE2---SCENE3
SCENE6---SCENE7
SCENE9---SCENE6
SCENE7---SCENE9
SCENE6-->SCENE2
```

### SYSTEM FLOW

#### RootServer

##### initialize

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant RootServer
participant RootDatabase

Client->>RootServer:GET
alt cookie is passed
    RootServer->>RootDatabase:query:cookie
    alt Client have joined server
        RootServer ->> RootDatabase:fetch server status
        RootServer->>Frontend:redirect to server
        Frontend-->Server:establish websocket  connection
    else Client have not joined server
        RootServer-->>Client: サーバー選択
    end
else cookie is not passed
    RootServer->>Client:set cookie
    RootServer-->>Client:サーバー選択
end    
```

##### サーバー選択

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant RootServer
participant RootDatabase
participant Server

Frontend -->> Client: サーバー選択
Client ->> Frontend: Join
Note right of Client:ServerName
Frontend ->> RootServer:redirect to server
RootServer ->> RootDatabase:fetch server status
RootServer -->> Frontend:redirect to server
Frontend --> Server:establish websocket connection
```

#### Server

##### Initialize

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Server
participant Database

Client --> Server:establish websocket connection
alt cookie is passed
    Server ->> Database:fetch cookie status
    Server ->> Frontend:restore last session
else cookie is not passed
    Server ->> Database:set cookie
    Server ->> Frontend:set cookie
    Server -) Frontend:User information
    Server ->> Frontend:show トピック一覧(ゲスト)
end
```

##### ログイン

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Server
participant Database

Client ->> Frontend: Log in
Frontend -->> Client: ログイン
Client ->> Frontend: Log in
Note right of Client: Username,Password
Frontend ->> Server: Log in
Server ->> Server: salt,hash
Server ->> Database: fetch password's hash
Server ->> Database: set cookie
Server ->> Frontend: set cookie
Server -) Frontend: user information
Server ->> Frontend: restore last session
```

##### 登録

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Server
participant Database

Client ->> Frontend: Sign up
Frontend -->> Client: 登録
Client ->> Frontend: Sign up
Note right of Client: Username,Password,PasswordConfirmation
Frontend ->> Server: Sign up
Server ->> Server: salt,hash
Server ->> Database: set password's hash
Server ->> Database: set cookie
Server ->> Frontend: set cookie
Server -) Frontend: user information
Server ->> Frontend: restore last session
```

##### トピック一覧

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Server
participant Database

Server ->> Frontend: show トピック一覧
Frontend ->> Database: fetch topic-list
Frontend -->> Client:トピック一覧
```

##### トピック

- unspecified

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Server
participant Database

Server ->> Frontend: show トピック
Frontend ->> Database: fetch topic
Frontend -->> Client:トピック
```

##### トピック一覧->トピック

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Database

Client ->> Frontend: topic
Frontend ->> Frontend: update cookie
Frontend ->> Database: fetch topic
Frontend -->> Client: トピック
```

##### トピック->トピック一覧

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Server
participant Database

Client ->> Frontend: topic list
Frontend ->> Frontend: update cookie
Frontend ->> Database: fetch topic
Frontend -->> Client: トピック一覧
```

##### ユーザー設定

- unspecified

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Server
participant Database

Client ->> Frontend: user settings
Frontend ->> Server: fetch user settings
Server ->> Database: fetch user settings
Server -->> Frontend: user settings
Frontend -->> Client: ユーザー設定
Client ->> Frontend: modify user settings
Frontend ->> Server: modify user settings
Server ->> Database: modify user settings
Server -->> Frontend: user settings are modified

```

##### post

```mermaid
sequenceDiagram
actor AnotherClient
actor Client
participant Frontend
participant Server
participant Database

Client ->> Frontend:Post
Note right of Client: Content,Context
Frontend ->> Server:Post
Server ->> Database:Set
Server -->> Frontend:Posted
alt AnotherClient should notice the post
  Server ->> AnotherClient:sync signal
  AnotherClient ->> Database:fetch
end
```

##### Log out

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Server
participant Database

Client ->> Frontend:Logout
Frontend ->> Server:update cookie status
Server ->> Database:update cookie status
Frontend -->> Client:トピック一覧(ゲスト)

```

##### Leaving Server

```mermaid
sequenceDiagram
actor Client
participant Frontend
participant Server
participant Database

Client ->> Frontend:Leave server
Frontend ->> Server:delete cookie
Server ->> Database:delete cookie
Frontend ->> Frontend:clear all cookies
Frontend ->> Frontend:redirect to RootServer

```

### DATA STRUCTURE

#### RootServer

```mermaid
erDiagram

client||--o| cookies: has
cookies{
    String IpAddress
}

SERVER-LIST{
    String ServerName
    String IpAddress
    String Description
}
```

#### Server

```mermaid
erDiagram
cookies{
    String Topic
    String SessionID
    Datatime SessionIDLastUpdate
}
client ||--o| cookies: has

POST{
    String UserID
    String UserName
    File Icon
    String TopicID
    Datatime PostedAt
    String Content
    File Atached
}

client ||--o{ POST: posted

USER-STATUS{
    String UserID
    String UserName
    String PasswordHash
    File Icon
    String[] SessionID
    Datatime SessionIDLastUpdate
}

client ||--o| USER-STATUS: has

TOPIC{
    String TopicID
    String TopicName
    Int TheNumberOfPosts
}

TOPIC ||--o{ POST: has
```
