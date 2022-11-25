from sqlite3 import DatabaseError
from seir import seirsbr
import ipdb
import intro 
import pandas as pd


local = 'Minas Gerais'
list_local = []
T_dias = 1 #dias
Ndias = 500
ini_dist = 30   # Data de início do distanciamento
fim_dist = 60  # Data do término do distanciamento
TResus = 0.05  # Taxa de resusceptibilidade
Testes = 0.02  # Taxa de testes de detectados
N_transmissao = 0.72 #
slider_pop = 0.03 #

list_local = intro.states_pop_cases_deaths(local) #[População, casos, mortes]

casos1,mortes1=seirsbr.modelo_SEIRS_plus(local=local, tdias=T_dias, ndias=Ndias,
                      list_local=list_local, T_resus=TResus,
                      id=ini_dist, fd=fim_dist, tst=Testes,
                      ntrans=N_transmissao,
                      sl_pop=slider_pop,
                      imprime=False, pop_real=True)

ini_dist = 1
fim_dist = 2

casos2,mortes2=seirsbr.modelo_SEIRS_plus(local=local, tdias=T_dias, ndias=Ndias,
                      list_local=list_local, T_resus=TResus,
                      id=ini_dist, fd=fim_dist, tst=Testes,
                      ntrans=N_transmissao,
                      sl_pop=slider_pop,
                      imprime=False, pop_real=True)

df=pd.DataFrame()
df['casos 60']=casos1
df['casos 0']=casos2
df['mortes 60'] = mortes1
df['mortes 0'] = mortes2
df.to_excel('casos.xlsx')
#ipdb.set_trace()

