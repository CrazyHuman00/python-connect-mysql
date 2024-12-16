# python-connect-mysql
### 概要
Python(FastAPI)とsqlite3を使ったデータベース操作ができるwebサイトです。http://localhost:8000 のローカルホスト上で動くだけなので、パプリックには公開してません。簡単に扱えるので、ぜひ遊んでみてください。

### 環境構築
#### Pythonの環境構築
pythonの環境構築が必要です。著者は以下のとおりです。
```bash
$ pyenv -v
pyenv 2.4.1

$ python -V
Python 3.12.7
```
上記のようにするにはpyenvでPythonのversion3.11.6をインストールしてください。
```bash
$ pyenv install 3.12.7
```

#### その他の環境構築
以下のコマンドを叩いてもらって、必要なパッケージをインストールします。
```bash
$ pip install -r requirements.txt
```

### 使い方
Makefileを用意しているので下記のコマンドを入力してもらえば、データベースが作成され、webサイトが開き動作します。

```bash
$ make test
```

作成したデータベースをチャラにしたい場合は下記のコマンドを入力してください。

```bash
$ make clean
```

### 参考
- [FastAPIとsqlite3による簡単なウェブサイトを実装する](https://qiita.com/phyblas/items/c3ff92b6dd353f887f1d)