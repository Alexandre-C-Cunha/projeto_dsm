from flask import Flask, render_template
import pandas as pd
from guppy import hpy
from memory_profiler import profile


app = Flask(__name__)

#df_cfem=pd.read_pickle('C:/Users/vanes/Documents/projeto MIM/BeautifulSoup/Projeto IMP/Base de Dados/Notebook/dados_cfem_geral.pickle')


@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/grid')
@profile
def dashboard():
	#soma=df_cfem[(df_cfem['Ano']==2008)&(df_cfem['Substância']=='AREIA COMUM')&(df_cfem['Município']=='SENGÉS')]['ValorRecolhido2'].sum()
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
    app.run(debug=True, port=5000, threaded=True)