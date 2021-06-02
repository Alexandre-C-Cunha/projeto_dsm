from flask import Flask, render_template
import pandas as pd
from guppy import hpy
from memory_profiler import profile

app = Flask(__name__)

df_lista_de_Busca_final=pd.read_pickle('dados_tabela/df_lista_busca.pickle')

@app.route('/')
def home():
	df=df_lista_de_Busca_final.sample(2000)
	return render_template('select2.html',df=df)



if __name__=='__main__':
    app.run(debug=True, port=5000, threaded=True)