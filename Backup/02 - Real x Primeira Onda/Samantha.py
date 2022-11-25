from sqlite3 import DatabaseError
from seir import seirsbr
import ipdb
import intro 
import pandas as pd

#%% LEITURA DE DADOS HISTORICOS 
dfHist = pd.read_excel('cases-brazil-states.xlsx', sheet_name = 'MINAS GERAIS')
dfMediaMovel = dfHist[['date','MEDIA_MOVEL 30']]

#%% MODELO SEIRS

local = 'Minas Gerais'
list_local = []
T_dias = 1 #dias
Ndias = 500
ini_dist = 1   # Data de início do distanciamento
fim_dist = 2  # Data do término do distanciamento
TResus = 0.04  # Taxa de resusceptibilidade, depois do pico (0, se permanentemente imune)
Testes = 0.04  # Taxa de testes de detectados, influencia na subida da curva
N_transmissao = 0.000001 # 0.72
slider_pop = 0.0012 # 0.03, amplitude

list_local = intro.states_pop_cases_deaths(local) #[População, casos, mortes]

casos1,mortes1=seirsbr.modelo_SEIRS_plus(local=local, tdias=T_dias, ndias=Ndias,
                      list_local=list_local, T_resus=TResus,
                      id=ini_dist, fd=fim_dist, tst=Testes,
                      ntrans=N_transmissao,
                      sl_pop=slider_pop,
                      imprime=False, pop_real=True)

#%% IMPRIMIR RESULTADOS
df=pd.DataFrame()
#df['data'] = dfMediaMovel.loc[0:Ndias-2,'date'].tolist()
df['Media_Movel'] = dfMediaMovel.loc[dfMediaMovel['MEDIA_MOVEL 30']>100,'MEDIA_MOVEL 30'].iloc[0:Ndias-1].tolist()
df['casos previstos']=casos1
df['mortes previstas'] = mortes1
df.to_excel('casos.xlsx')
#ipdb.set_trace()

