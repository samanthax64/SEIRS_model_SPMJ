import Samantha_estimator as estimator
import Samantha_aux as aux
import ipdb
import pandas as pd

#============================================================
parametrosCode = {'taxaMorteInfectNVac':0.0257, 
                  'taxaMorteInfectVac':0.0093,
                  'arquivoParametros':'Parametros_5.xlsx'
                  }

runEstadoTeste = False
estadoTeste = 'Ceará'

popInitialInfect = {'Bahia': 30,
                    'Minas Gerais': 0,
                    'Espírito Santo': 30,
                    'Piauí': 55,
                    'Santa Catarina': 40,
                    'Rio Grande do Sul': 20,
                    'Paraná': 0,
                    'Acre': 80,
                    'Rio de Janeiro': 0,
                    'São Paulo': 0,
                    'Tocantins': 60,
                    'Rondônia': 60,
                    'Pará': 40,
                    'Maranhão': 45,
                    'Goiás': 35,
                    'Ceará': 0,
                    'Alagoas': 55,
                    'Paraíba': 45,
                    'Amapá': 53,
                    'Amazonas': 55,
                    'Mato Grosso': 55,
                    'Mato Grosso do Sul': 45,
                    'Pernambuco': 35,
                    'Sergipe': 48,
                    'Rio Grande do Norte': 48,
                    'Roraima': 45,
                    'Distrito Federal': 45,
                    }

dfHistALL = pd.read_excel('cases-brazil-states.xlsx', sheet_name = None)
dfParamALL = pd.read_excel(parametrosCode['arquivoParametros'], sheet_name = None)
parametrosCode['AntVac'] = dfParamALL['Parametros'].set_index('Parametro').loc['Antecipação Vacina','Valor']


#============================================================
#Resultado para um estado
if runEstadoTeste:
    casosEstimados = estimator.run(estadoTeste, popInitialInfect, parametrosCode,
                                   dfHistALL[estadoTeste], dfParamALL[estadoTeste],
                                    printGraph=True, saveXLS=True,
                                    printProgress=True)

#Resultado para o país
if not runEstadoTeste:
    casosEstimados = pd.DataFrame()
    for estado in popInitialInfect.keys():
        print(f'''Estimando {estado}''')
        
        casosEstimadosUF = estimator.run(estado, popInitialInfect, parametrosCode,
                                         dfHistALL[estado], dfParamALL[estado], 
                                         printGraph=False, saveXLS=False, 
                                         printProgress=False)
        
        casosEstimados = pd.concat([casosEstimados , casosEstimadosUF])
    
    casosBR = casosEstimados.groupby('dia').sum()
    
    aux.export_BR(casosEstimados, casosBR)
    aux.plot_BR(casosBR)
    
        
    
    
