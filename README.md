# api-flask ![Heroku](https://heroku-badge.herokuapp.com/?app=gardrop-api)
Flask ile yazilan Api(Web service). Suan api heroku da calisiyor. Local'e kurmaya gerek yok.Heroku'ya pushlamaya da gerek yok. Otomatik master branch'i herokuya pushlaniyor.

# Gardop Uygulamasinin Repolari

Projenin Ionic reposu: https://github.com/erginipekci7/Gardrop-Ionic

Projenin Api reposi: https://github.com/erginipekci7/api-flask

Projenin Api Test reposu : https://github.com/erginipekci7/api-flask-test

# Proje Yapisi
<h4>Burasi guncellenmeli. Detayli bir sekilde proje anlatilmali.</h4>

# API - Routes

| Method  | Path                   | Description                                   |
| ------- |---------------------   |-----------------------------------------------|
| GET     | /                      | Api ayakta olup olmadigi kontrol edilir.      |
| GET     | /v1/pingpongjson       | Gelen json'i gonderir.                        |
| GET     | /v1/mysql_test         | Mysql'in calisip calismadigi kontrol edilir.  |
| GET     | /v1/mysql_init         | Mysql hazir tablolar ve kullanicilar eklenir. |
| POST    | /v1/create_user        | Yeni kullanici olusturulur.                   |
| GET     | /v1/user/:username     | Kullanicinin bilgisi doner.                   |
| PUT     | /v1/user/:username     | Kullanicinin bilgisi guncellenir.             |
| DELETE  | /v1/user/:username     | Kullanici silinir.                            |
| GET     | /v1/temperature/: city | Girilen sehrin hava durumu bilgileri doner.   |

# Localde Kurulum - Api
<p>Linux kullaniyorsan terminalle ulasip bu komutlari calistirmalisin, MacOs ayni sekil. Windows icin bash <a href="https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/">yukle</a></p>


```bash
 $ sudo apt-get install libmysqlclient-dev  # for mysql connection for ubuntu
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
 (venv)$ python app.py                        # Run App.
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
