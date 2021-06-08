from flask import Flask, render_template, request
import pandas as pd
import os
from guppy import hpy
from memory_profiler import profile
from flask import jsonify, json, current_app as app
import wtforms as wt
from wtforms import TextField, Form


app = Flask(__name__)

def acentuacao(x):
    from unicodedata import normalize
    source = x
    target = normalize('NFKD', source).encode('ASCII','ignore').decode('ASCII')
    return(target)


df_lista=pd.read_json('static\\data\\api.jason')
df_lista['NOME']=df_lista['NOME'].apply(lambda x: acentuacao(x).upper())
df_lista=df_lista.drop_duplicates()

@app.route('/rota_jason')
def rota_jason():
	termo = request.args.get('term')
	a=acentuacao(termo).upper()
	df_term=df_lista[df_lista['NOME'].str.contains(a)]
	lista_amarradinho=[]
	for index, row in df_term.iterrows():
		lista_amarradinho.append({'id':index,'text':row['NOME']+" ("+row['TIPO']+")"})
	final={'results':lista_amarradinho}
	with open('static\\data\\lista_amarradinho.json', 'w') as outfile:
		json.dump(final, outfile)
	teste_arq= open('static\\data\\lista_amarradinho.json')
	data = json.load(teste_arq)
	return (data)

@app.route('/rota_escolha/<todas>')
def rota_escolha(todas):
	Sfiltro2 = str(todas)
	print(Sfiltro2)
	return jsonify({'Sfiltro2':Sfiltro2})

@app.route('/home/')
def home():
	
	return render_template("select2.html")


if __name__=='__main__':
    app.run(debug=True, port=5000, threaded=True)