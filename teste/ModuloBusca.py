import pandas as pd
from pymongo import MongoClient
import time
import numpy as np
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
import math
import locale
import re
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
df_lista_busca=pd.read_pickle('C:/Users/vanes/Documents/projeto MIM/BeautifulSoup/Projeto IMP/Base de Dados/Notebook/df_lista_de_busca_final_rev1.pickle')

class ListadeBusca:
    #cria um df de qualquer coleção
    def lista_qualquer(self,colecao,categoria,lista_item):
        #cria um dataframe de uma coleção em uma busca especifica
        df = pd.DataFrame(list(colecao.find({categoria:{'$in':lista_item}})))
        return(df)
    #Identifica a categoria
    def categoria(self,item,df):
        categoria=list(df[df['Nome_lista']==item]['TIPO'])[0].lower()
        return(categoria)
    #criando uma lista de anos e valores 
    def anos_cfem_lista_valores(self, item,df):
        #identifica quantos tipos de unidade
        num_unidade=df['unidade'].unique()
        return(num_unidade)
    def testa_razao_ou_nome_fantasia(self, item,cnpj_basico,cnpj_completo):
        a=cnpj_basico.find({'razao_social':item}).count()
        b=cnpj_completo.find({'nome_fantasia':item}).count()
        if a>=1:
            resp='razao_social'
        else:
            resp='nome_fantasia'
        return(resp)
    def valor_float(self,x):
        try:
            y=locale.atof(x)
        except:
            y=x
        return(y)
    def quantida_unidade_valor_float(self,df,coluna):
        try:
            df[coluna]=df[coluna].apply(lambda x: locale.atof(x))
        except:
            df[coluna]=df[coluna]
        return(df)
    def lista_itens_colunas_df(self,lista_item, colunaA,colunaB,df):
        nomes_itens=list(df[df[colunaA].isin(lista_item)][colunaB].unique())
        num_itens=len(nomes_itens)
        return(nomes_itens,num_itens)
    def item_categoria(self,item,df):
        teste=ListadeBusca()
        df_lista_busca=df
        item2=list(df_lista_busca[df_lista_busca['Nome_lista']==item]['NOME'])[0]
        categorias=teste.categoria(item,df_lista_busca)
        return(item2,categorias)

class Listando_item_escolha(ListadeBusca):
    def razao_social(self,item2,cnpj_basico,cnpj_completo,todos_cnpj,empresas_cfem,codigo_municipio,operacao,codigo_cnae,natureza_juridica):
        #achar o cnpj basico
        #Verifica se é razão social ou fantasia
        testa_razao=super().testa_razao_ou_nome_fantasia(item2,cnpj_basico,cnpj_completo)
        #cria os dois df (completo e basico)
        if testa_razao=='razao_social':
            #cria o df basico
            df_basico=super().lista_qualquer(cnpj_basico, 'razao_social', [item2])
            #Lista os cnpj_basicos
            cnpjs=list(df_basico['cnpj_basico'].unique())
            cnpjs2=list(map(int, cnpjs))
            #cria o df_cnpj_completo
            df_cnpj_completo=super().lista_qualquer(cnpj_completo, 'cnpj_basico', cnpjs2)
        else:
            #cria o df completo
            df_cnpj_completo=super().lista_qualquer(cnpj_completo, 'nome_fantasia', [item2])
            #Lista os cnpj_basicos
            cnpjs=list(df_cnpj_completo['cnpj_basico'].unique())
            cnpjs2=list(map(int, cnpjs))
            #cria df_basico
            df_basico=super().lista_qualquer(cnpj_basico, 'cnpj_basico', cnpjs2)
        #encontrando CNPJs completos
        #cria o df dos cnpjs
        df_t_cnpj=super().lista_qualquer(todos_cnpj,'cnpj_basico',cnpjs2)
        #Lista os cnpj_completo
        cnpjs_completos=list(df_t_cnpj['cnpj_completo'].unique())
        #Cria df cfem 
        df_cfem=super().lista_qualquer(empresas_cfem, 'cnpj', cnpjs_completos)
        #Lista substancias
        substancias=super().lista_itens_colunas_df(cnpjs_completos,'cnpj','substancia',df_cfem)
        #Lista Estados
        estados=super().lista_itens_colunas_df(cnpjs_completos,'cnpj','uf',df_cfem)
        #Lista Municipios
        municipios=super().lista_itens_colunas_df(cnpjs_completos,'cnpj','municipio',df_cfem)
        #Nome Fantasia
        nome_fantasia=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','nome_fantasia',df_cnpj_completo)
        #Telefone Empresa
        telefone=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','telefone',df_cnpj_completo)
        #Anos CFEM
        anos_cfem=super().lista_itens_colunas_df(cnpjs_completos,'cnpj','ano',df_cfem)
        #transforma em float os valores 
        #valor cfem
        df_cfem2=super().quantida_unidade_valor_float(df_cfem, 'valor_cfem')
        #quantidade
        df_cfem2=super().quantida_unidade_valor_float(df_cfem, 'quantidade')
        #agrupa valores e quantdade por ano
        df_agrupado=df_cfem2.groupby(['ano','unidade'])['quantidade','valor_cfem'].sum()
        #Email
        email=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','email',df_cnpj_completo)
        #Municipio da Empresa
        muni_empresa=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','municipio',df_cnpj_completo)
        #convert em int numero dos municipios
        muni_empresa2=list(map(int, muni_empresa[0]))
        #Nomes Municipio Empresas
        nome_municipio_empresa=list(super().lista_qualquer(codigo_municipio, 'codigo_municipio',muni_empresa2)['municipio'].unique())
        #Df da operação
        df_operacao=super().lista_qualquer(operacao,'cnpj',cnpjs_completos)
        if len(df_operacao)==0:
            anos_operacao='não encontrado'
            valores_operacao_ano='não encontrado'
            valor_operacao2='não encontrado'
        else:
            #tras o valor da operacação geral da empresa 
            valor_operacao=super().quantida_unidade_valor_float(df_operacao,'operacao')['operacao'].sum()
            #Converte o valor da operacação da empresa em moeda
            valor_operacao2=locale.currency(valor_operacao, grouping=True)
            #Anos de operacao
            anos_operacao=super().lista_itens_colunas_df(cnpjs_completos,'cnpj','ano',df_operacao)
            #Valor da operacao por ano
            valores_operacao_ano=df_operacao.groupby(['ano','substancia'])['operacao'].sum()
        #Tipos de unidade de medida
        uni_medida=super().lista_itens_colunas_df(cnpjs_completos,'cnpj','unidade',df_cfem)
        #Porte da empresa
        porte_empresa=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','porte_empresa',df_basico)
        #Matriz e filial
        matriz_filial=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','matriz_filial',df_cnpj_completo)

        #Lista CNAEs

        #Lista CNAE principal
        cnae_principal=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','cnae_principal',df_cnpj_completo)
        #convert em int cnae principal
        cnae_principal2=list(map(int, cnae_principal[0]))
        #Nome CNAE Principal
        nome_cnae_principal=list(super().lista_qualquer(codigo_cnae, 'codigo_cnae',cnae_principal2)['cnae'].unique())

        #Lista CNAE secundário
        cnae_secundario=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','cnae_secundario',df_cnpj_completo)
        lista_transition=[]
        for x in cnae_secundario[0]:
            if type(x)==str:
                lista_x=x.split(',')
                lista_transition.extend(lista_x)
            else:
                lista_transition.extend(str(x))
        lista_cnaes_secundario=list(map(int, lista_transition))
        lista_cnaes_secundario2=super().lista_qualquer(codigo_cnae,'codigo_cnae',lista_cnaes_secundario)
        try:
            #Lista nomes CNAE secundário
            lista_cnaes_secundario3=list(lista_cnaes_secundario2['cnae'].unique())
        except:
            #Lista nomes CNAE secundário
            lista_cnaes_secundario3=[]
        #Capital Social
        capital_social=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','capital_social',df_basico)
        #Natureza Juridica
        cod_natureza_juridica=super().lista_itens_colunas_df(cnpjs2,'cnpj_basico','nat_juridica',df_basico)
        #convert em int cnae principal
        cod_natureza_juridica2=list(map(int, cod_natureza_juridica[0]))
        #Nome Natureza Juridica
        nome_natureza_juridica=list(super().lista_qualquer(natureza_juridica, 'codigo_natureza',cod_natureza_juridica2)['natureza_juridica'].unique())
        return(item2,cnpjs_completos,substancias,estados,municipios,nome_fantasia,telefone,anos_cfem,df_agrupado,email,nome_municipio_empresa,anos_operacao,valor_operacao2,valores_operacao_ano,uni_medida,porte_empresa,matriz_filial,nome_cnae_principal,cnae_principal,lista_cnaes_secundario,lista_cnaes_secundario3,capital_social,nome_natureza_juridica)