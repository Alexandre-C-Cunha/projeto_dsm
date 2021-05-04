from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
def dashboard():
    return render_template('dashboard.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa_interativo.html')

@app.route('/info')
def artigo():
    return render_template('artigos_interativos.html')

@app.route('/export')
def info():
    return render_template('infografico_interativo.html')


if __name__=='__main__':
    app.run(debug=True)