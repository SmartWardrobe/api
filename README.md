# api-flask
Flask ile yazilan Api(Web service).

# Proje Yapisi
<p>"api.py" dosyasi api dir. "api-test.py" ise api'yi test eden dosyadir. "empty.py" dosyasi ise suanlik isimize lazim degil.Ama ilerde lazim olucak kodlar.</p>
<p>2 ayri flask uygulamamizi ayaga kaldiriyoruz("api.py" ve "api-test.py" dosyalari). Ve api-test flask uygulamamiza istek atilir.</p>

# API - Routes 

```GET     / ```

```POST    /api/create_user ```

```GET     /api/user/:username ```

```PUT     /api/user/:username ```

```DELETE  /api/user/:username ```

# Kurulum - Api
<p>Linux kullaniyorsan terminalle ulasip bu komutlari calistirmalisin, MacOs ayni sekil. Windows icin bash <a href="https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/">yukle</a></p>


```bash
 $ git clone https://github.com/erginipekci7/api-flask  # First download repo
 $ cd api-flask                               # changed active directory to repo
 $ virtualenv venv                            # create virtual enviroment
 $ source venv/bin/activate                   # actived virtual environment
 (venv)$ pip install -r requirements.txt      # download requirement packages.
 (venv)$ # we create .env file, because we need it for mysql connection
 (venv)$ vim .env   # we're opening .env with vim.
 MYSQL_HOST     = YOUR HOSTNAME
 MYSQL_USER     = YOUR USERNAME
 MYSQL_PASSWORD = YOUR PASSWORD
 MYSQL_DB       = YOUR DATABASE NAME
 (venv)$ cat .env   # we're looking in .env
 (venv)$ # dotenv package reads it, then adds your os's environments.
 (venv)$ python api.py                        # Run App.
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```


# Kurulum - Test Api

```bash
 $ cd api-flask                               # changed active directory to repo
 $ virtualenv venv                            # create virtual enviroment
 $ source venv/bin/active                     # actived virtual environment
 (venv)$ pip install -r requirements.txt      # download requirement packages.
 (venv)$ python api-test.py                   # Run App.
* Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
```

# Test
<p>Burda Test Api'ye istek atiyoruz ki, asil api'ye test istekleri atsin. Tool olarak api-test'i yonlendiriyoruz.</p>


```bash
 $ curl localhost:5001/create_user
 $ curl localhost:5001/user/ergin/get
 $ curl localhost:5001/user/ergin/put
 $ curl localhost:5001/user/ergin/delete
```
