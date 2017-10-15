#import re

#from flask_mysqldb import MySQL
#from werkzeug import generate_password_hash,check_password_hash
#from flask_scrypt import generate_password_hash, generate_random_salt, check_password_hash
#from passlib.hash import sha256_crypt
#from flask_hashing import Hashing
#from passlib.hash import sha256_crypt


#mysql=MySQL()
#app.config['MYSQL_HOST']='localhost'
#app.config['MYSQL_USER']='root'
#app.config['MYSQL_PASSWORD']='123qweasd'
#app.config['MYSQL_DB']='gardrop'
#mysql.init_app(app)
#passlib= Passlib(app)


#@app.route("/api/sign2", methods=["POST"])
#def sign2():
 #   username= str(request.form["user"])
  #  password=str(request.form["password"])
   # email=str(request.form["email"])
    #resultmail=is_email_address_valid(email)
    #print("regex sonuc ----- ")
    #print(resultmail)
    #hashpassword=generate_password_hash(password)
    #print("hash uzunluk")
    #print(len(hashpassword))
    #if resultmail==True:
    #    cur = mysql.connection.cursor()
    #    cur.execute("INSERT INTO login (username,password,email) VALUES(%s,%s,%s)",(username,hashpassword,email))
    #    mysql.connection.commit()
    #else:
    #    return render_template("index.html",title="parola hatali")

    #cur = mysql.connection.cursor()
    #cur.execute("INSERT INTO login (username,password,email) VALUES(%s,%s,%s)",(username,hashpassword,email))
    #mysql.connection.commit()
    #return "kayit basarili"



#def is_email_address_valid(email):
#    """Validate the email address using a regex."""
#    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
#        return False
#    return True
