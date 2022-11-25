'''
Código para estimar número de casos e de mortes usando os parametros da planilha Parametros
'''
from sqlite3 import DatabaseError
from seir import seirsbr
import matplotlib.pyplot as plt
import ipdb
import intro 
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import warnings
warnings.simplefilter("ignore")

def run(local, popInitialInfect, parametrosCode, dfHist, dfParam, printGraph=True, saveXLS=True,  printProgress=True):
    
    #%% LEITURA DE DADOS 
    infect_inicial_add = popInitialInfect[local]
    dfMediaMovel = dfHist[['date','MEDIA_MOVEL 30']]
    

    #%% MODELO SEIRS

    #Parametros não usados
    N_transmissao = 0.72 # 0.72 Eficiencia do distanciamento, substituimos pelo beta_list
    ini_dist = 1   # Data de início do distanciamento, substuimos por meses_mud_beta
    fim_dist = 2  # Data do término do distanciamento, substuimos por meses_mud_beta

    #Parametros modelo original

    list_local = []
    T_dias = 1 #dias
    Ndias = 826
    cortarAposNdias = 5500
    TResus = dfParam['taxa_resusceptibilidade'].to_list()[0]  # 0.04 Taxa de resusceptibilidade, depois do pico
    Testes = 0.04  # Taxa de testes de detectados, influencia na subida da curva
    slider_pop = 0.00045 # 0.03, amplitude, -porcentagem da população exposta
    list_local = intro.states_pop_cases_deaths(local) #[População, casos, mortes]

    # Taxas de Transmissão e Distanciamento
    meses_mud_beta = dfParam['mês'].to_list() #Mes de mudança de um parametro
    beta_list = dfParam['beta'].to_list() # Taxa de Transmissão
    efic_dist = dfParam['efic_dist'].to_list() #Eficiencia do distanciamento(0,1): 1 significa 100% da população em isolamento.
    pop_vac = dfParam['pop_vac'].to_list() # Porcentagem da população vacinada
    efic_vac = dfParam['efic_vac'].to_list() # Eficiencia das vacinas 
    '''
    meses_mud_beta = [1, 2, 145, 195, 230, 255, 270, 290, 313, 345]
    beta_list = [0.1985, 0.1985*0.6, 0.1985*0.3, 0.1985*1.1, 0.1985*1.2, 0.1985*0.9, 0.1985*0.9, 0.1985*2, 0.1985*7.5, 0.1985*10]
    efic_dist = [1-0.00045, 1-0.00045, 1-0.00045, 1-0.00045, 1-0.4, 1-1, 1-0.5, 1-0.7, 1-0.9,1-1] #Taxa de eficiencia do distanciamneto(%da população em isolamento)
    pop_vac = [0,0,0,0,0,0,0,0,0,0]# Porcentagem da população vacinada {0,1}
    efic_vac = [0,0,0,0,0,0,0,0,0,0] #Eficiencia da vacina
    '''
    pop_list = [] 

    for count in range(0, len(meses_mud_beta)):
        pop_rua = 1-efic_dist[count]
        pop_suceptivel = pop_rua * (1-pop_vac[count]*efic_vac[count]*1.5)
        pop_suceptivel = max(0,pop_suceptivel)
        pop_list.append(pop_suceptivel/200)
    slider_pop = pop_list[0]
    theta_E_list = [Testes,Testes,Testes,Testes,Testes,Testes,Testes,Testes,Testes,Testes]
    theta_I_list = theta_E_list
    dfParam.pop = list_local[0]
    dfParam.infect_add = infect_inicial_add
    dfParam.parametrosCode = parametrosCode

    #ipdb.set_trace()
    casos1,mortes1=seirsbr.modelo_SEIRS_plus(local=local, tdias=T_dias, ndias=Ndias,
                        list_local=list_local, T_resus=TResus,
                        id=ini_dist, fd=fim_dist, tst=Testes,
                        ntrans=N_transmissao,
                        sl_pop=slider_pop, pop_list = pop_list,
                        dfParam = dfParam,
                        imprime=False, pop_real=True,
                        printProgress_seirbr= printProgress,  
                        meses_mud_beta = meses_mud_beta, beta_list = beta_list, theta_E_list = [], theta_I_list = [])

    #%% IMPRIMIR RESULTADOS
    df=pd.DataFrame()
   
    #df['data'] = dfMediaMovel.loc[0:Ndias-2,'date'].tolist()
    df['Media_Movel'] = dfMediaMovel.loc[dfMediaMovel['MEDIA_MOVEL 30']>100,'MEDIA_MOVEL 30'].iloc[0:Ndias+1].tolist()
    #ipdb.set_trace()
    if len(df['Media_Movel'])>len(casos1):
        df=pd.DataFrame()
        df['Media_Movel'] = dfMediaMovel.loc[dfMediaMovel['MEDIA_MOVEL 30']>100,'MEDIA_MOVEL 30'].iloc[0:len(casos1)].tolist()
        
    df['casos previstos']=casos1[0:len(df['Media_Movel'])]
    df['mortes_modelSEIRS'] = mortes1[0:len(df['Media_Movel'])]
    df['Media_Movel_Mortes'] = dfHist.rolling(30).mean()['newDeaths']
    df['perc_popvac'] = 0
    
    for d in df.index:
        try:
            df.loc[d,'perc_popvac'] = dfParam.loc[dfParam['mês']<=d,'pop_vac'].tail(1).values[0]
        except:
            df.loc[d,'perc_popvac'] = 0
    df['Mortes_Previstas_CALC'] = parametrosCode['taxaMorteInfectNVac']*df['casos previstos']*(1-df['perc_popvac']) + parametrosCode['taxaMorteInfectVac']*df['casos previstos']*df['perc_popvac']
    df['Mortes_Previstas_CALC'] = df['Mortes_Previstas_CALC'].shift(periods=parametrosCode['AntVac'], fill_value=0)
    df['estado'] = local
    df['dia'] = df.index
    
    df['erro'] = abs(( df['casos previstos'] - df['Media_Movel']) / df['Media_Movel']) 
    df = df[['estado','dia','Media_Movel','casos previstos','mortes_modelSEIRS','Media_Movel_Mortes','perc_popvac','Mortes_Previstas_CALC', 'erro']]
    
    df=df.drop(df.index[df.index>cortarAposNdias], axis=0)
    
    if saveXLS:
        df.to_excel('casos_'+str(local)+'.xlsx')
    #Para criar vários momentos de distanciamento, alterar o seirsbr.py (checkpoints linha 588)
    

    #%%Gráfico
   
    if printGraph:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Media_Movel'],
                            mode='lines',
                            name='Casos Históricos'))
        fig.add_trace(go.Scatter(x=df.index, y=df['casos previstos'],
                            mode='lines',
                            name='Casos Previstos'))
        fig.update_layout(legend_font_size=19)
        fig.update_layout(font_size=19)
        fig.show()
        
    return df