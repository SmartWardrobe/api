# api-flask ![Heroku](https://heroku-badge.herokuapp.com/?app=gardrop-api)
Flask ile yazilan Api(Web service). Suan api heroku da calisiyor. Local'e kurmaya gerek yok.Heroku'ya pushlamaya da gerek yok. Otomatik master branch'i herokuya pushlaniyor.

# Gardop Uygulamasinin Repolari

Projenin Ionic reposu: https://github.com/erginipekci7/Gardrop-Ionic

Projenin Api reposi: https://github.com/erginipekci7/api-flask

Projenin Api Test reposu : https://github.com/erginipekci7/api-flask-test

# Proje Dokumani
<h4>Burasi guncellenmeli. Detayli bir sekilde proje anlatilmali.</h4>

<h4>REST API mantigi, CRUD islemlerini methodlarla ayirmak.</h4>
<li> GET       - READ  islemleri</li>
<li> POST      - CREATE islemleri</li>
<li> PUT       - UPDATE islemleri</li>
<li> DELETE    - DELETE islemleri</li>

# API - Routers

| Method  | Path                      | Description                                                                 |
| ------- |------------------------   |-----------------------------------------------------------------------------|
| GET     | /                         | Api ayakta olup olmadigi kontrol edilir.                                    |
| GET     | /v1/pingpongjson          | Gelen json'i gonderir.                                                      |
| GET     | /v1/mysql_test            | Mysql'in calisip calismadigi kontrol edilir.                                |
| GET     | /v1/project_init          | Mysql'e hazir tablolar ve kullanicilar eklenir. Aws'e resim yukler.         |
| GET     | /v1/upload                | upload.html dosyasini render eder.                                          |
| POST    | /v1/uploader              | Fotograf'i uploads dizinine kaydeder.                                       |
| GET     | /v2/upload_form           | upload_form.html dosyasini render eder.                                     |
| POST    | /v2/upload/pic            | Aws'e fotograf'i, mysql'e de fotograf bilgilerini kaydeder.                 |
| GET     | /v1/pic/:photoname        | Fotograf'i indirir.                                                         |
| PUT     | /v1/pic                   | Fotograf guncelleniyor.                                                     |
| POST    | /v1/login                 | Email ve parolaya gore kullaniciyi kontrol eder. Ve kullanici bilgisi doner.|   
| POST    | /v1/users                 | Yeni kullanici olusturulur.                                                 |
| GET     | /v1/users                 | Tum kullanicilarin listesini doner.                                         |       
| GET     | /v1/user/:username        | Kullanicinin bilgisi doner.                                                 |
| PUT     | /v1/user/:username        | Kullanicinin bilgisi guncellenir.                                           |
| DELETE  | /v1/user/:username        | Kullanici silinir.                                                          |
| GET     | /v1/user/:username/pics   | Kullanicinin pics listesini doner.                                          |
| GET     | /v1/show/pics             | uploads dizinindeki fotograflari gosterir.                                  |
| GET     | /v1/show/photonames       | Mysql deki fotograf listesini gosterir.                                     |
| GET     | /v1/show/bucketsNfiles    | Aws de bulunan buckets ve files listesi gosterilir.                         |
| GET     | /v1/temperature/:city     | Girilen sehrin hava durumu bilgileri doner.                                 |


# Localde Güncelleme Yapmak
<p>Son değişiklikleri (commit) yerel deponuza almak için terminalde git pull komutunu çalıştırın. Bu değişiklikleri al (fetch) ve birleştir (merge) yapacaktır. Konu hakkında faydalı bilgiler -> http://rogerdudler.github.io/git-guide/index.tr.html  </p>

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

# Aws - S3
Aws cli ile login olmak ve s3 dosya atmayi bu videodan bulabilirsiniz.[Getting Started with AWS S3 CLI](https://www.youtube.com/watch?v=WrVqrvIQRAI)

# Flask - Proje Yapisi
[How to structure large flask apps](https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications)

[Appfactories](http://flask.pocoo.org/docs/0.10/patterns/appfactories/)
