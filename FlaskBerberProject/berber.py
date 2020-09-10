from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,BooleanField,SelectField
from passlib.hash import sha256_crypt,pbkdf2_sha256
from wtforms.validators import InputRequired, Email, DataRequired,Length,EqualTo,input_required
from wtforms.fields.html5 import EmailField
from functools  import wraps
from flask_wtf.recaptcha import RecaptchaField

app=Flask(__name__)
app.secret_key = '_5#y2L"F4Q8zQczn\xec]/'

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="berberdb"
app.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql=MySQL(app)

class girisForm(Form):
    username=StringField("Kullanıcı Adı : ", validators=[DataRequired()])
    password=PasswordField("Şifre",validators=[DataRequired()])

class kullaniciKayit(Form):
    name=StringField("Ad",validators=[DataRequired(),Length(min=4,max=50,message="en az 4, en çok 50 karakter giriniz")])
    surname=StringField("Soyad",validators=[DataRequired(),Length(min=4,max=50,message="en az 4, en çok 50 karakter giriniz")])
    username=StringField("Kullanıcı adı",validators=[DataRequired(),Length(min=4,max=50,message="en az 4, en çok 50 karakter giriniz")])
    email=EmailField("E-posta Adresi",validators=[DataRequired(),Email("Lütfen Geçerli bir eposta adresi giriniz")])
    tel1=SelectField("Tel",choices=["505","535","542","532"])
    tel2=StringField("Telefon numaranızı başında Sıfır olmadan")
    password = PasswordField('Şifre Belirleyin', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Şifreler eşleşmiyor')
    ])
    confirm = PasswordField('Şifrenizi Tekrar Girin')
    accept_tos = BooleanField('Gabul ittim', [validators.DataRequired()])
    




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/berber_ekle")
def berber_ekle():
    return render_template("berber_ekle.html")

@app.route("/berber_bul")
def berber_bul():
    return render_template("berber_bul.html")

@app.route("/berber_gecmisi")
def berber_gecmisi():
    return render_template("berber_gecmisi.html")

@app.route("/register",methods=["GET","POST"])
def register():
    form=kullaniciKayit(request.form)
    if request.method=="GET":
        return render_template("register.html",form=form)
    else:
        cursor=mysql.connection.cursor()

        name=str(form.name.data)
        surname=form.surname.data
        username=form.username.data
        email=form.email.data
        tel1=form.tel1.data
        tel2=form.tel2.data
        tel=str(tel1)+str(tel2)
        password=pbkdf2_sha256.hash(str(form.password.data))
      
        sorgu="insert into users (name,surname,username,email,tel,password) values(%s,%s,%s,%s,%s,%s)"

        cursor.execute(sorgu,(name,surname,username,email,tel,password))
        mysql.connection.commit()
        flash("Kullanıcı kaydınız oluşturulmuştur..","success")
        return render_template("login.html")

    

@app.route("/login", methods=["POST","GET"])
def login():
    form=girisForm(request.form)
    if request.method=="POST":
        usernameForm=form.username.data
        passwordForm=form.password.data
        cursor=mysql.connection.cursor()
        
        if result==0:
            flask("Böyle Bir kullanıcı sistemimizde kayıtlı değil","danger")
            return render_template("login.html")
        else:
            sorgu="select * from users where username=%s and password=%s" 
            result=cursor.execute(sorgu,(usernameForm,passwordForm))
            if result==0:
                flask("Hatalı Şifre girdiniz tekrar deneyiniz","warning")
                return render_template("login.html")
            else:
                session["username"]=usernameForm

                flask("Hoş Geldiniz"+session["username"],"success")
                return redirect(url_for("index"))
            
    else:

        return render_template("login.html",form=form)

if __name__=="__main__":
    app.run(debug=True)




