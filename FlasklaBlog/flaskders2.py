from flask import Flask, render_template

app=Flask(__name__)    # Bir flask uygulaması tanımladık 
#Eğer Bu dosya terminalden çalıştırılırsa name in değeri __main__ oluyor
#başka bir yerden çalıştırılırsa __name__ değeri main olmuyor
@app.route("/") # bu dekoratör çağırıldığında hemen aldındaki fonksiyonu çağırıyor..
def index():         # Bu fonksiyonda alttaki yazıyı döndürüyor.
    sayi1=10
    sayi2=255 
    return render_template("index.html",number1=sayi1, number2=sayi2 ) #Burada index html dosyasına bir number anahtarı yolluyoruz bunu index html sayfasında kullanabiliriz
@app.route("/about")# bu dekoratör çağırıldığında hemen aldındaki fonksiyonu çağırıyor..
def about():
    return render_template("about.html") #render template komutu sayesinde html sayfaları çevirebiliyoruz.
if __name__=="__main__":
    app.run(debug=True)
