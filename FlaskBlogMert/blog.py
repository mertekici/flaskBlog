from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField
from functools  import wraps

# Giriş Yapmadan bazı sayfaları görüntülemek istemiyorsak bu fonksiyonu yazıyoruz
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntüleyebilmek için giriş yapmak zorundasınız","danger")
            return redirect(url_for("login"))
    return decorated_function   

class makaleOlustur(Form):
    baslik=StringField("Makale Başlığı",validators=[validators.Length(min=4,max=80,message="en az 4 en çok 80 karakter giriniz")])
    makale=TextAreaField("Makalenizi Giriniz")

#Kullanıcı Kayıt Formu Klası oluşturma
class RegisterForm(Form):
    name=StringField("İsim Soyisim",validators=[validators.Length(min=4,max=30),validators.DataRequired()])
    username=StringField("Kullanıcı Adınız",validators=[validators.Length(min=4,max=35),validators.DataRequired()])
    eposta=EmailField("E posta Adresiniz",validators=[validators.Email(message="eposta girin")])
    password=PasswordField("Paralonızı giriniz",validators=[
        validators.Length(min=4,max=30),
        validators.input_required(message="Lütfen Bir Parola giriniz.."),
        validators.EqualTo(fieldname="confirm",message="Paralanız uyuşmuyor lütfen kontrol ediniz")
        ])
    
    confirm=PasswordField("Parola Tekrar",validators=[
        validators.Length(min=4,max=30),
        validators.input_required(message="Lütfen parolayı tekrar giriniz")        
        ])

class LoginForm(Form):
    username=StringField("Kullanıcı Adınız",validators=[validators.Length(min=4,max=35),validators.DataRequired()])
    password=PasswordField("Paralonızı giriniz",validators=[
        validators.Length(min=4,max=30),
        validators.input_required(message="Lütfen Bir Parola giriniz.."),
        ])
    
    
app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zQczn\xec]/'


app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="mertekicidb"
app.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql=MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method=="GET":
        return redirect(url_for("index"))
    else:
        keyword=request.form.get("keyword")
        sorgu="select * from articles where title like '%" + keyword +"%' "
        cursor=mysql.connection.cursor()
        result=cursor.execute(sorgu)
        if result==0:
            flash("böyle bir makale bulunamadı","warning")
            return redirect(url_for("articles"))
        else:
            articles=cursor.fetchall()    
            return render_template("articles.html",articles=articles)

@app.route("/edit/<string:id>", methods=["GET","POST"])
@login_required
def updateArticle(id):
    if request.method=="GET":
        cursor=mysql.connection.cursor()
        sorgu="select * from articles where id=%s and author=%s"
        result=cursor.execute(sorgu,(id,session["username"]))
        if result==0:
            flash("Böyle bir makale yok yada yetkili değilsiniz")
            return redirect(url_for("index"))
        else:
            article=cursor.fetchone()
            form=makaleOlustur()
            form.baslik.data=article["title"]
            form.makale.data=article["content"]
            return render_template("update.html",form=form)

    else: #post request yapacak iken olacakları yazıyoruz
        form=makaleOlustur(request.form)
        cursor=mysql.connection.cursor()
        sorgu="UPDATE articles SET title = %s , content=%s WHERE id = %s"
        baslik=form.baslik.data
        makale=form.makale.data
        cursor.execute(sorgu,(baslik,makale,id))
        mysql.connection.commit()
        flash("Makaleniz Başarı ile Güncellenmiştir","success")
        return redirect(url_for("dashboard",form=form))



@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor=mysql.connection.cursor()
    sorgu="select * from articles where author=%s and id=%s "
    result=cursor.execute(sorgu,(session["username"],id))
    if result>0:
        sorgu2="delete from articles where id=%s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        return redirect(url_for("dashboard"))
    else:
        flash("Bu makale yok veya bu makaleyi silmeye yetkili değilsiniz","danger")
        return redirect(url_for("index"))

@app.route("/article/<string:id>")
def article(id):
    #form=makaleOlustur(request.form)
    cursor=mysql.connection.cursor()
    sorgu=("select * from articles where id=%s")
    result=cursor.execute(sorgu,(id,))
    if result>0:
        article=cursor.fetchone()
        return render_template("article.html",article=article)
    else:
        return render_template("article.html")

@app.route("/articles")
def articles():
    cursor=mysql.connection.cursor()
    sorgu="select * from articles"
    result=cursor.execute(sorgu)
    if result>0:
        articles=cursor.fetchall()
        return render_template("articles.html",articles=articles)
    else:
        return render_template("articles.html")



@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm(request.form)
    if request.method=="POST" and form.validate():
        username=form.username.data
        password_entered=(form.password.data)
        cursor=mysql.connection.cursor()
        sorgu="select * from users where username=%s"
        result=cursor.execute(sorgu,(username,))
        if result>0:
            data=cursor.fetchone()
            real_password=data["password"]
            if sha256_crypt.verify(password_entered ,real_password):
                flash("TEbrikler "+username+" başarıyla giriş yaptınız","success")
                session["logged_in"]=True
                session["username"]=username
                return redirect(url_for("index",kadi=username)) 
            else:       
                flash("üzgünüm "+username+" girdiğiniz parola yanlıştır.","danger")
                return redirect(url_for("login"))
        else:
            flash("Sistemimizde böyle bir kullanıcıya rastlamadık","danger")
            return redirect(url_for("login"))

    else:
        return render_template("login.html", form=form)




@app.route("/register",methods=["GET","POST"]) #bu sayfanın get ve post olabileceğini söyledik
def register():
    form=RegisterForm(request.form) #oluşturduğumuz formdan bir örnek aldık
    if request.method=="POST" and form.validate():
        name=form.name.data
        username=form.username.data
        eposta=form.eposta.data
        password=sha256_crypt.encrypt(form.password.data)
        cursor=mysql.connection.cursor()
        sorgu="insert into users (name,username,email,password) values(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,username,eposta,password))
        mysql.connection.commit()
        cursor.close()
        flash("Tebrikler "+username+" Başarıyla kayıt oldunuz","success")
        return redirect(url_for("login")) 
    else:
        return render_template("register.html", form=form)

@app.route("/logout")
def logout(): 
    session.clear()
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard(): 
    cursor=mysql.connection.cursor()
    sorgu="select * from articles where author=%s"
    result=cursor.execute(sorgu,(session["username"],))
    
    if result>0:
        articles=cursor.fetchall()
        return render_template("dashboard.html",articles=articles)  
    else:
        return render_template("dashboard.html")  



@app.route("/addarticle", methods=["GET","POST"])
def addarticle():
    form=makaleOlustur(request.form)
    if request.method=="POST" and form.validate(): 
        
        baslik=form.baslik.data
        makaleİcerik=form.makale.data
        cursor=mysql.connection.cursor()
        yazar=session["username"]
        sorgu="insert into articles (title,author,content) values (%s,%s,%s)"
        cursor.execute(sorgu,(baslik,yazar,makaleİcerik))
        mysql.connection.commit()
        cursor.close()
        flash("Makaleniz Başarıyla eklenmiştir ","success")
        return redirect(url_for("dashboard"))
    
    else:
        return render_template("addarticle.html", form=form)  




if __name__=="__main__":
    app.run(debug=True)
