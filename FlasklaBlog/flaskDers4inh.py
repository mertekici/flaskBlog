from flask import Flask, render_template

app=Flask(__name__)    

@app.route("/") # bu dekoratör çağırıldığında hemen aldındaki fonksiyonu çağırıyor..
def index():         # Bu fonksiyonda alttaki yazıyı döndürüyor.
    return render_template("indexDers4.html") #Burada index html dosyasına bir sözlük yolluyoruz
@app.route("/about")# bu dekoratör çağırıldığında hemen aldındaki fonksiyonu çağırıyor..
def about():
    return render_template("about.html") #render template komutu sayesinde html sayfaları çevirebiliyoruz.
if __name__=="__main__":
    app.run(debug=True)
