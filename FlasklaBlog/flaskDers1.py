from flask import Flask

app=Flask(__name__)    # Bir flask uygulaması tanımladık 
#Eğer Bu dosya terminalden çalıştırılırsa name in değeri __main__ oluyor
#başka bir yerden çalıştırılırsa __name__ değeri main olmuyor
@app.route("/") # bu dekoratör çağırıldığında hemen aldındaki fonksiyonu çağırıyor..
def index():         # Bu fonksiyonda alttaki yazıyı döndürüyor.
    return "Ana Sayfa Hazırlanıyor..."
@app.route("/about")# bu dekoratör çağırıldığında hemen aldındaki fonksiyonu çağırıyor..
def about():
    return "Hakkımızda sayfası hazırlanıyor..."
if __name__=="__main__":
    app.run(debug=True)
