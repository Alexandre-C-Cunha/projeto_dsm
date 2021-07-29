from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import pandas as pd
import os
from pymongo import MongoClient
from guppy import hpy
from memory_profiler import profile
from flask import jsonify, json, current_app as app
import wtforms as wt
from wtforms import TextField, Form
from ModuloBusca import ListadeBusca, Listando_item_escolha

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db=client["cfem"]
db.list_collection_names()
cfem_municpio=db['cfem_municipio']
empresas_cfem=db['empresas']
operacao=db['operacao']
codigo_municipio=db['codigo_municipio']
nome_substancia=db['nome_substancia']
nome_subgrupo=db['nome_subgrupo']
cnpj_basico=db['cnpj_basico']
cnpj_completo=db['cnpj_completo']
cfem_estados=db['cfem_estados']
sigla_estado=db['sigla_estado']
natureza_juridica=db['natureza_juridica']
codigo_cnae=db['codigo_cnae']
todos_cnpj=db['todos_cnpjs']
cfem_ano=db['cfem_ano']

def acentuacao(x):
    from unicodedata import normalize
    source = x
    target = normalize('NFKD', source).encode('ASCII','ignore').decode('ASCII')
    return(target)

df_lista_busca=pd.read_pickle('C:/Users/vanes/Documents/projeto MIM/BeautifulSoup/Projeto IMP/Base de Dados/Notebook/df_lista_de_busca_final_rev1.pickle')
df_lista=pd.read_json('static\\data\\api.jason')
df_lista['NOME']=df_lista['NOME'].apply(lambda x: acentuacao(x).upper())
df_lista=df_lista.drop_duplicates()

@app.route('/rota_jason')
def rota_jason():
	termo = request.args.get('term')
	a=acentuacao(termo).upper()
	df_term=df_lista[df_lista['NOME'].str.contains(a)]
	df_term2=df_lista_busca[df_lista_busca['Nome_lista'].str.contains(a)]
	lista_amarradinho=[]
	for index, row in df_term2.iterrows():
		lista_amarradinho.append({'id':index,'text':row['NOME']+" ("+row['TIPO']+")"})
	final={'results':lista_amarradinho}
	with open('static\\data\\lista_amarradinho.json', 'w') as outfile:
		json.dump(final, outfile)
	teste_arq= open('static\\data\\lista_amarradinho.json')
	data = json.load(teste_arq)
	return (data)

@app.route('/rota_escolha/<todas>')
def rota_escolha(todas):
	global Sfiltro2
	Sfiltro2 = str(todas)
	info_item=Listando_item_escolha()
	item2=Sfiltro2.split(',')[0]
	item3=info_item.item_categoria(item2, df_lista_busca)[0]
	resposta=info_item.razao_social(item3,cnpj_basico,cnpj_completo,todos_cnpj,empresas_cfem,codigo_municipio,operacao,codigo_cnae,natureza_juridica)
	cnpj=resposta[7][0]
	print(cnpj)
	return jsonify({'Sfiltro2':Sfiltro2, 'item2':cnpj})

@app.route('/home/')
def home():
	try:
		Sfiltro2 =Sfiltro2
	except:
		Sfiltro2=0
	return render_template("select2_rev1.html", Sfiltro2=Sfiltro2)


if __name__=='__main__':
    app.run(debug=True, port=5000, threaded=True)