##############################################################################
# Webcovid - Pandemia COVID-19 (para o Brasil - estados e municipios)
# Nescon e DEP (UFMG)
# Equipe: João Flávio de Freitas Almeida <joao.flavio@dep.ufmg.br>
#         Francisco Cardoso (Chico) <cardoso@nescon.medicina.ufmg.br>
#         Luiz Ricardo Pinto <luiz@dep.ufmg.br>
#         Samuel Vieira Conceição <svieira@dep.ufmg.br>
#         Virginia Magalhães <vmagalhaes@nescon.medicina.ufmg.br>
# Fonte:
# Dados:  Wesley Cota (https://covid19br.wcota.me/)
# SEIR:   Ryan McGee(https://github.com/ryansmcgee/seirsplus)
# Leitos: Array Advisors (https://www.healthleadersmedia.com/
# welcome-ad?toURL=/covid-19/see-when-states-will-face-hospital
# -bed-capacity-shortages-during-covid-19-outbreak)
##############################################################################

# Modelo SEIRS+
from seir import models
from seir.models import *
import networkx
from math import *
import ipdb

import sys # Importa modulos do sistema
import os # Local (path) do sistema
import pathlib  # Local do diretório (pasta)
# sys.path.insert(1, './utils/')
# import utils
# from app import load_municipalities
# from app import read_mun_cases
# from app import mun_pop_cases_deaths
# from seir.utils.mun_info import load_municipalities
# from seir.utils.mun_info import read_mun_cases
# from seir.utils.mun_info import mun_pop_cases_deaths
# from intro import load_municipalities
# from intro import read_mun_cases
# from intro import mun_pop_cases_deaths


# from app import load_states
# from app import read_est_cases
# from app import states_pop_cases_deaths
# from seir.utils.states_info import load_states
# from seir.utils.states_info import read_est_cases
# from seir.utils.states_info import states_pop_cases_deaths
# from intro import load_states
# from intro import read_est_cases
# from intro import states_pop_cases_deaths



# from app import cd
from seir.utils.folders import cd

# ('..', 'images')    > Um níveil acima
# ('../..', 'images') > Dois níveis acima
IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', 'images')

########################################################################
# Modelo SEIRS - Parâmetros
########################################################################
# O modelo SEIRS+ implementa um modelo SEIR genérico incluindo complementos
# de estrutura de população, distanciamento social, nível de testes,
# rastreamento de contatos e casos em quarentena detectados.

# O pacote possui a implementação do modelo estocástico em redes dinâmicas

# A dinâmica do SEIRS:
# SEIR é um modelo de infecção. A população é dividida em indivíduos:
#   (S) Susceptível: Essa pessoa fica ...
#   (E) Exposta    : ...ao contato com infectados, ficando...
#   (I) Infectada  : ... e depois, retorna (ou não) para o estado de ...
#   (R) Recuperada. No modelo SEIRS, essa pessoa talvez retorne ao estado ...
#   (S) Susceptível. (Isso pode ser excluído do modelo, se necessário)

# initN:    população
# initI:    número de inicial de casos de indivíduos infectados (casos diários)
# beta:     taxa de transmissão por contato (S>I) por período
# sigma:    taxa de progressão (inverso do período de incubação)
# gamma:    taxa de recuperação (inverso do período de infecção)
# mu_0:     taxa de mortalidade base (mortes por período)
# mu_I:     taxa de mortalidade pela infecção (mortes por período)
# xi:       taxa de re-susceptibilidade (0 se permanentemente imune)

# A dinâmica do SEIRS com Testes
# O efeitos de testes de infecção é modelada pelos estados:
#   (D_E)   Exposto detectado e
#   (D_I)   Infectado detectado

# initE:    número de inicial de indivíduos expostos
# initD_E:  número de inicial de indivíduos expostos detectados
# initD_I:  número de inicial de indivíduos infectados
# initR:    número de inicial de indivíduos recuperados
# initF:    número de inicial de mortes

# theta_E:  taxa de testes de indivíduos expostos
# theta_I:  taxa de testes de indivíduos infectados
# psi_E:    prob de resultados positivos p/ indivíduos expostos
# psi_I:    prob de resultados positivos p/ indivíduos infectados
# beta_D:   taxa de transmissão de casos detectados
# sigma_D:  taxa de progressão de casos detectados
# gamma_D:  taxa de recuperação de casos detectados
# mu_D:     taxa de mortalidade  de casos detectados

########################################################################
# Simulação por Estado ou Município
########################################################################
# Inicializações default (As incializações são feitas no arquivo seir.py)
local = ''
list_local = []
T_dias = 1
Ndias = 1
ini_dist = 1   # Data de início do distanciamento
fim_dist = 2  # Data do término do distanciamento
TResus = 0.0  # Taxa de resusceptibilidade
Testes = 0.0  # Taxa de testes de detectados
N_transmissao = 1
slider_pop = 0.01

# Estatísticas COVID por Estado
########################################################################
def state_fatality_rate_covid(nome):
    states_sigla = {# Estado : sigla
			'Acre':	0.0012685139,
            'Alagoas':	0.0014594894,
            'Amazonas':	0.0019804,
            'Amapá':	0.000712753,
            'Bahia':	0.000409428,
            'Ceará':	0.000606175,
            'Espírito Santo':	0.00095768,
            'Goiás':	0.000496748,
            'Maranhão':	0.000355282,
            'Minas Gerais':	0.00040927,
            'Mato Grosso do Sul':	0.00067552,
            'Mato Grosso':	0.00094192,
            'Pará':	0.000509811,
            'Paraíba':	0.000635481,
            'Pernambuco':	0.000704207,
            'Piauí':	0.000609361,
            'Paraná':	0.000560098,
            'Rio de Janeiro':	0.001188855,
            'Rio Grande do Norte':	0.000553843,
            'Rondônia':	0.001010582,
            'Roraima':	0.000902662,
            'Rio Grande do Sul':	0.00053979,
            'Santa Catarina':	0.000559656,
            'Sergipe':	0.000705237,
            'São Paulo':	0.000735623,
            'Tocantins':	0.000535538,
            'Distrito Federal':	0.000992911,
            # 'Acre':	0.0012685139,
            # 'Alagoas':	0.0014594894,
            # 'Amazonas':	0.0013804,
            # 'Amapá':	0.000712753,
            # 'Bahia':	0.001059428,
            # 'Ceará':	0.001706175,
            # 'Espírito Santo':	0.00153768,
            # 'Goiás':	0.001536748,
            # 'Maranhão':	0.001095282,
            # 'Minas Gerais':	0.00153927,
            # 'Mato Grosso do Sul':	0.00097552,
            # 'Mato Grosso':	0.00225192,
            # 'Pará':	0.001539811,
            # 'Paraíba':	0.001075481,
            # 'Pernambuco':	0.002644207,
            # 'Piauí':	0.001479361,
            # 'Paraná':	0.001690098,
            # 'Rio de Janeiro':	0.004588855,
            # 'Rio Grande do Norte':	0.002583843,
            # 'Rondônia':	0.001220582,
            # 'Roraima':	0.000702662,
            # 'Rio Grande do Sul':	0.00199979,
            # 'Santa Catarina':	0.001089656,
            # 'Sergipe':	0.001205237,
            # 'São Paulo':	0.003085623,
            # 'Tocantins':	0.001035538,
            # 'Distrito Federal':	0.000792911,
                }
    # return states_sigla.get(nome, '** Estado inválido **')
    return states_sigla.get(nome, 0.00081)


# https://www.medrxiv.org/content/10.1101/2020.05.09.20096701v1.full.pdf
def taxa_de_transmissao_beta(sigla):
    st_tx_transm_beta = {# Estado : Pop    : Cód
            'Acre':	    0.1985,
            'Alagoas':	0.1985,
            'Amazonas':	0.1985,
            'Amapá':	0.1985,
            'Bahia':	0.1985,
            'Ceará':	0.1985,
            'Espírito Santo':	0.1985,
            'Goiás':	0.1985,
            'Maranhão':	0.1985,
            'Minas Gerais':	0.1985,
            'Mato Grosso do Sul':	0.1985,
            'Mato Grosso':	0.1985,
            'Pará':	    0.1985,
            'Paraíba':	0.1985,
            'Pernambuco':	0.1985,
            'Piauí':	0.1985,
            'Paraná':	0.1985,
            'Rio de Janeiro':	0.1985,
            'Rio Grande do Norte':	0.1985,
            'Rondônia':	0.1985,
            'Roraima':	0.1985,
            'Rio Grande do Sul': 0.1985,
            'Santa Catarina': 0.1985,
            'Sergipe':	0.1985,
            'São Paulo': 0.1985,
            'Tocantins': 0.1985,
            'Distrito Federal':	0.1985,
            # 'Acre':	    0.1514,
            # 'Alagoas':	0.1390,
            # 'Amazonas':	0.1985,
            # 'Amapá':	0.2280,
            # 'Bahia':	0.1515,
            # 'Ceará':	0.2016,
            # 'Espírito Santo':	0.1717,
            # 'Goiás':	0.1290,
            # 'Maranhão':	0.1943,
            # 'Minas Gerais':	0.1155,
            # 'Mato Grosso do Sul':	0.1210,
            # 'Mato Grosso':	0.134,
            # 'Pará':	    0.2104,
            # 'Paraíba':	0.1848,
            # 'Pernambuco':	0.1704,
            # 'Piauí':	0.1355,
            # 'Paraná':	0.1265,
            # 'Rio de Janeiro':	0.1321,
            # 'Rio Grande do Norte':	0.1258,
            # 'Rondônia':	0.1640,
            # 'Roraima':	0.198,
            # 'Rio Grande do Sul':0.1167,
            # 'Santa Catarina':	0.1282,
            # 'Sergipe':	0.1614,
            # 'São Paulo':0.1271,
            # 'Tocantins':0.1384,
            # 'Distrito Federal':	0.1602,
                }
    # return st_tx_transm_beta.get(sigla, '** Estado inválido **')
    return st_tx_transm_beta.get(sigla, 0.195)

def est_InitI(sigla):
    st_tx_transm_beta = {# Estado : Pop    : Cód
            'Acre':	    5,
            'Alagoas':	25,
            'Amazonas':	15,
            'Amapá':	30,
            'Bahia':	50,
            'Ceará':	150,
            'Espírito Santo':	30,
            'Goiás':	50,
            'Maranhão':	40,
            'Minas Gerais':	150,
            'Mato Grosso do Sul':	30,
            'Mato Grosso':	20,
            'Pará':	    50,
            'Paraíba':	30,
            'Pernambuco':	60,
            'Piauí':	20,
            'Paraná':	100,
            'Rio de Janeiro':	150,
            'Rio Grande do Norte':	30,
            'Rondônia':	10,
            'Roraima':	30,
            'Rio Grande do Sul':70,
            'Santa Catarina':	40,
            'Sergipe':	30,
            'São Paulo':250,
            'Tocantins':10,
            'Distrito Federal':	40,
                }
    # return st_tx_transm_beta.get(sigla, '** Estado inválido **')
    return st_tx_transm_beta.get(sigla, 10)

########################################################################
# Model SEIR (basico)
########################################################################

def modelo_SEIR(local=local, ndias=Ndias,
                list_local=list_local,
                imprime=False, pop_real=False):

    # print('list_local: ', list_local)
    NDIAS  = ndias
    pop    = list_local[0]
    pop_10M = 10000

    if pop_real:
        casos  = list_local[1]
        mortes = list_local[2]
        print(f'Casos [{local}]: ', casos)
        print(f'Mortes [{local}]: ', mortes)
    else:
        casos = max(ceil((list_local[1] * pop_10M) / pop),10)
        mortes = max(ceil((list_local[2] * pop_10M) / pop),5)
        print(f'Casos [{local}] (para {pop_10M} hab): ', casos)
        print(f'Mortes [{local} (para {pop_10M} hab)]: ', mortes)

    if pop_real:
        model  = SEIRSModel(initN=pop,         # população real
                            beta=0.155,        # taxa de transmissão/período
                            sigma=1/5.2,       # taxa de progressão
                            gamma=1/12.39,     # taxa de recuperação
                            initI=casos,       # número de casos
                            initF=mortes)      # número de mortes
    else:
        model  = SEIRSModel(initN=pop_10M,     # população 10 mil
                            beta=0.155,        # taxa de transmissão/período
                            sigma=1/5.2,       # taxa de progressão
                            gamma=1/12.39,     # taxa de recuperação
                            initI=casos,       # número de casos
                            initF=mortes)      # número de mortes

    model.run(T=NDIAS)

    titulo_grafico = 'Modelo SEIR de infecção pelo COVID-19 para ' + str(local)
    compr_graf = 14
    altur_graf = 8
    dimen_graf = (compr_graf, altur_graf)

    if imprime:
        if pop_real:
            model.figure_basic(title=titulo_grafico,
                               figsize=dimen_graf,
                               plot_percentages=False)
            model.figure_infections(title=titulo_grafico,
                                    figsize=dimen_graf,
                                    plot_percentages=False)
        else:
            model.figure_basic(title=titulo_grafico,
                               figsize=dimen_graf)
            model.figure_infections(title=titulo_grafico,
                                    figsize=dimen_graf)

    #####################################################################
    # Acessando os dados da Simulação: Geração de arquivo .csv
    #####################################################################

    S = model.numS      # time series of S counts
    E = model.numE      # time series of E counts
    I = model.numI      # time series of I counts
    D_E = model.numD_E    # time series of D_E counts
    D_I = model.numD_I    # time series of D_I counts
    R = model.numR      # time series of R counts
    F = model.numF      # time series of F counts

    t = model.tseries   # time values corresponding to the above time series

    with open(IMAG_DIR + '/chart_seir.csv', 'w') as saida:
        # print('S, E, I, R, D_E, D_I, F', file = saida)
        print(  '(S) Suscetiveis,',
                '(E) Expostos,',
                '(I) Infectados,',
                '(R) Recuperados,',
                '(D_E) Expostos detectados,',
                '(D_I) Infectados detectados,',
                '(M) Mortes', file = saida)
        tt = 1
        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d},{2:d},{3:d},{4:d},{5:d},{6:d}'
                    .format(int(S[i]),int(E[i]),int(I[i]),
                            int(R[i]),int(D_E[i]),int(D_I[i]),int(F[i])),
                    file = saida)
            tt+=1

    with open(IMAG_DIR + '/chart_seir2.csv', 'w') as saida:
        # print('I, D_all, E', file = saida)
        print(  '(I) Infectados,',
                '(D_all) Detectados,',
                '(E) Expostos', file = saida)
        tt = 1
        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d},{2:d}'
                      .format(int(I[i]),int(D_E[i]+D_I[i]) ,int(E[i])),
                              file = saida)
            tt+=1

    ref_model = model
    return ref_model

########################################################################
# Model SEIRS (com re-susceptibilidade) - Ondas
########################################################################
def modelo_SEIRS(local=local, ndias=Ndias, list_local=list_local,
                imprime=False, pop_real=False):

    # print('list_local: ', list_local)

    NDIAS  = ndias
    pop    = list_local[0]
    pop_10M = 10000

    if pop_real:
        casos  = list_local[1]
        mortes = list_local[2]
        print(f'Casos [{local}]: ', casos)
        print(f'Mortes [{local}]: ', mortes)
    else:
        casos = max(ceil((list_local[1] * pop_10M) / pop),10)
        mortes = max(ceil((list_local[2] * pop_10M) / pop),5)
        print(f'Casos [{local}] (para {pop_10M} hab): ', casos)
        print(f'Mortes [{local} (para {pop_10M} hab)]: ', mortes)

    if pop_real:
        model = SEIRSModel(initN=pop,         # população real
                           beta=0.155,        # taxa de transmissão/período
                           sigma=1/5.2,       # taxa de progressão
                           gamma=1/12.39,     # taxa de recuperação
                           xi=0.001,          # taxa de re-susceptibilidade
                           initI=casos,       # número de casos
                           initF=mortes)      # número de mortes
    else:
        model = SEIRSModel(initN=pop_10M,     # população 10 mil
                           beta=0.155,        # taxa de transmissão/período
                           sigma=1/5.2,       # taxa de progressão
                           gamma=1/12.39,     # taxa de recuperação
                           xi=0.001,          # taxa de re-susceptibilidade
                           initI=casos,       # número de casos
                           initF=mortes)      # número de mortes

    model.run(T=NDIAS)

    titulo_grafico = 'Modelo SEIRS de infecção pelo COVID-19 para ' + str(local)
    compr_graf = 14
    altur_graf = 8
    dimen_graf = (compr_graf, altur_graf)

    if imprime:
        if pop_real:
            model.figure_basic(title=titulo_grafico,
                               figsize=dimen_graf,
                               plot_percentages=False)
            model.figure_infections(title=titulo_grafico,
                                    figsize=dimen_graf,
                                    plot_percentages=False)
        else:
            model.figure_basic(title=titulo_grafico,
                               figsize=dimen_graf)
            model.figure_infections(title=titulo_grafico,
                                    figsize=dimen_graf)

    #####################################################################
    # Acessando os dados da Simulação: Geração de arquivo .csv
    #####################################################################

    S = model.numS      # time series of S counts
    E = model.numE      # time series of E counts
    I = model.numI      # time series of I counts
    D_E = model.numD_E    # time series of D_E counts
    D_I = model.numD_I    # time series of D_I counts
    R = model.numR      # time series of R counts
    F = model.numF      # time series of F counts

    t = model.tseries   # time values corresponding to the above time series

    with open(IMAG_DIR + '/chart_seirs.csv', 'w') as saida:
        # print('S, E, I, R, D_E, D_I, F', file = saida)
        print(  '(S) Suscetiveis,',
                '(E) Expostos,',
                '(I) Infectados,',
                '(R) Recuperados,',
                '(D_E) Expostos detectados,',
                '(D_I) Infectados detectados,',
                '(M) Mortes', file = saida)
        tt = 1
        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d},{2:d},{3:d},{4:d},{5:d},{6:d}'
                    .format(int(S[i]),int(E[i]),int(I[i]),
                            int(R[i]),int(D_E[i]),int(D_I[i]),int(F[i])),
                    file = saida)
            tt+=1

    with open(IMAG_DIR + '/chart_seirs2.csv', 'w') as saida:
        # print('I, D_all, E', file = saida)
        print(  '(I) Infectados,',
                '(D_all) Detectados,',
                '(E) Expostos', file = saida)
        tt = 1
        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d},{2:d}'
                      .format(int(I[i]),int(D_E[i]+D_I[i]) ,int(E[i])),
                              file = saida)
            tt+=1

########################################################################
# Model SEIRS + (plus) (População uniforme)
########################################################################
# def modelo_SEIRS_plus(ref_model, local=local, ndias=Ndias,
#                       list_local=list_local, T_resus=TResus,
#                       id=ini_dist, fd=fim_dist, tst=Testes,
#                       imprime=False, pop_real=False):

def modelo_SEIRS_plus(local=local, tdias=T_dias, ndias=Ndias,
                      list_local=list_local, T_resus=TResus,
                      id=ini_dist, fd=fim_dist, tst=Testes,
                      ntrans=N_transmissao,
                      sl_pop=slider_pop,
                      imprime=False, pop_real=False):

    #
    # print('list_local: ', list_local)

    NDIAS  = ndias
    pop    = list_local[0]
    pop_10M = 10000

    if pop_real:
        casos  = list_local[1]
        mortes = list_local[2]
        print(f'Casos [{local}]: ', casos)
        print(f'Mortes [{local}]: ', mortes)
    else:
        casos = max(ceil((list_local[1] * pop_10M) / pop),10)
        mortes = max(ceil((list_local[2] * pop_10M) / pop),5)
        print(f'Casos [{local}] (para {pop_10M} hab): ', casos)
        print(f'Mortes [{local} (para {pop_10M} hab)]: ', mortes)

    if pop_real:
        model = SEIRSModel(initN=pop*sl_pop,           # população real
                           initI=est_InitI(local), # número de casos. Era: casos, max(100,int((casos/1000)))
                           initF=max(1,int(mortes/100)),  # número de mortes. Era: mortes
                           beta    =taxa_de_transmissao_beta(local),      # taxa de transmissão/período. Ro = e^(K.t) = e^(0.155*5.2) = 2.24
                           # beta    =0.147,    # taxa de transmissão/período. Era: 0.155 e 0.2047
                           sigma   =1/5.2,      # taxa de progressão (1/periodo de incubação)
                           gamma   =1/24.0,     # taxa de recuperação (14 dias ABIM e Folha). (1/período de infecção). Era: 1/12.39 (inverse of infectious period)
                           mu_I    = state_fatality_rate_covid(local),  # Era: 0.0004, 0.0004161
                           mu_0    =0,
                           nu      =0,
                           xi      =T_resus,
                           beta_D  =taxa_de_transmissao_beta(local),      # taxa de transmissão/período. Ro = e^(K.t) = e^(0.155*5.2) = 2.24
                           # beta_D  =0.147,     # taxa de transmissão de casos detectados
                           sigma_D =1/5.2,     # taxa de progressão de casos detectados
                           gamma_D =1/24.0,    # taxa de recuperação de casos detectados (14 dias ABIM e Folha). Era: 1/12.39
                           mu_D    =0.0004161, # Era: 0.0004,
                           theta_E =0,          # taxa de testes de indivíduos expostos
                           theta_I =0,          # taxa de testes de indivíduos infectados
                           psi_E   =1.0,        # prob de resultados positivos p/ indivíduos expostos
                           psi_I   =1.0,        # prob de resultados positivos p/ indivíduos infectados
                           initE   =0,
                           initD_E =0,
                           initR   =0
                           )
    else:
        model = SEIRSModel(initN=pop_10M,       # população 10 mil
                           initI=casos,         # número de casos
                           initF=mortes,        # número de mortes
                           beta    =0.155,      # taxa de transmissão/período
                           sigma   =1/5.2,      # taxa de progressão
                           # gamma   =1/12.39,    # taxa de recuperação
                           gamma   =1/12.39,    # taxa de recuperação
                           mu_I    =0.0004,
                           mu_0    =0,
                           nu      =0,
                           xi      =0,
                           beta_D  =0.155,      # taxa de transmissão de casos detectados
                           sigma_D =1/5.2,      # taxa de progressão de casos detectados
                           gamma_D =1/12.39,    # taxa de recuperação de casos detectados
                           mu_D    =0.0004,
                           theta_E =0,          # taxa de testes de indivíduos expostos
                           theta_I =0,          # taxa de testes de indivíduos infectados
                           psi_E   =1.0,        # prob de resultados positivos p/ indivíduos expostos
                           psi_I   =1.0,        # prob de resultados positivos p/ indivíduos infectados
                           initE   =0,
                           initD_E =0,
                           initR   =0
                           )

    # Mudança de parâmetros ao longo da simulação
    ini_dist = id
    fim_dist = fd
    Testes = tst
    beta_antes = taxa_de_transmissao_beta(local)*ntrans
    beta_depois = taxa_de_transmissao_beta(local)
    # beta_antes = taxa_de_transmissao_beta(local)

    # print('ntrans: ', ntrans)
    # print('sl_pop: ', sl_pop)

    # períodos de tempo de distanciamento
    checkpoints = {'t': [ini_dist, fim_dist],
               # Taxa de infecção do covid reduz e retoma
               # O distanciamento produz uma redução de transmissão até 74%
               'beta':    [beta_antes, beta_depois],
               # Taxa de testes e detecção do covid
               # no período de quarentena
               'theta_E': [Testes, Testes],
               'theta_I': [Testes, Testes]
               # 'theta_E': [0.02, 0.02],
               # 'theta_I': [0.02, 0.02]
              }
    
    
    # model.run(T=NDIAS)
    model.run(T=NDIAS, checkpoints=checkpoints)

    titulo_grafico = 'Modelo SEIRS+ de infecção pelo COVID-19 para ' + str(local)
    compr_graf = 14
    altur_graf = 8
    dimen_graf = (compr_graf, altur_graf)


    if imprime:
        if pop_real:
            model.figure_basic(title=titulo_grafico,
                               figsize=dimen_graf,
                               plot_percentages=False,
                               vlines=checkpoints['t'],
                               vline_labels=['Início quarentena', 'Fim da quarentena'],
                               # shaded_reference_results=ref_model,
                               shaded_reference_label='Sem intervenção'
                               )
            model.figure_infections(title=titulo_grafico,
                                    figsize=dimen_graf,
                                    plot_percentages=False,
                                    vlines=checkpoints['t'],
                                    vline_labels=['Início quarentena', 'Fim da quarentena'],
                                    # shaded_reference_results=ref_model,
                                    shaded_reference_label='Sem intervenção'
                                    )
        else:
            model.figure_basic(title=titulo_grafico,
                               figsize=dimen_graf,
                               # plot_percentages=False,
                               vlines=checkpoints['t'],
                               vline_labels=['Início quarentena', 'Fim da quarentena'],
                               # shaded_reference_results=ref_model,
                               shaded_reference_label='Sem intervenção'
                               )
            model.figure_infections(title=titulo_grafico,
                                    figsize=dimen_graf,
                                    # plot_percentages=False,
                                    vlines=checkpoints['t'],
                                    vline_labels=['Início quarentena', 'Fim da quarentena'],
                                    # shaded_reference_results=ref_model,
                                    shaded_reference_label='Sem intervenção'
                                    )

    #####################################################################
    # Acessando os dados da Simulação: Geração de arquivo .csv
    #####################################################################

    S = model.numS      # time series of S counts
    E = model.numE      # time series of E counts
    I = model.numI      # time series of I counts
    # print("I: ", I)
    D_E = model.numD_E    # time series of D_E counts
    D_I = model.numD_I    # time series of D_I counts
    R = model.numR      # time series of R counts
    F = model.numF      # time series of F counts

    N = S + E + I + D_E + D_I + R

    t = model.tseries   # time values corresponding to the above time series

    with open(IMAG_DIR + '/chart_seirs_plus.csv', 'w') as saida:
        # print('S, E, I, R, D_E, D_I, F', file = saida)
        print(  '(S) Suscetiveis,',
                '(M) Mortes,',
                '(D_E) Expostos detectados,',
                '(D_I) Infectados detectados,',
                '(R) Recuperados,',
                '(I) Infectados,',
                '(E) Expostos',
                file = saida)
        tt = 1
        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d},{2:d},{3:d},{4:d},{5:d},{6:d}'
                    .format(
                            int(S[i]),
                            int(F[i]),
                            int(D_E[i]),int(D_I[i]),
                            int(R[i]),
                            int(I[i]),
                            int(E[i])
                            ),
                    file = saida)
            tt+=1


    with open(IMAG_DIR + '/chart_seirs_plus2.csv', 'w') as saida:
        # print('I, D_all, E', file = saida)
        print(  '(M) Mortes (acumulado),',
                '(I) Infectados',
                # '(D_all) Detectados',
                # '(E) Expostos'
                file = saida)
        tt = 1
        I_acum = 0
        F_acum = 0
        Tot_casos = []
        Nov_casos = []
        Morte_casos = []

        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d}'
                      .format(int(F[i]),
                              int(I[i]),
                              # int(D_E[i]+D_I[i])
                              # int(E[i]),
                              ),
                              file = saida)


                Tot_casos.append(int(I[i]) + int(R[i]))
                Nov_casos.append(int(I[i]))
                Morte_casos.append(int(F[i]))

                if tt == int(tdias*10):
                    print(f"Pop_total[{tt/10}]: ", N[tt])
                    print(f"Infect_acum[{tt/10}]: ", I[tt] + R[tt])
                    print(f"Mortes_acum[{tt/10}]: ", F[tt])
                # if tt == 1640:
                    print(f"Infectados[{tt/10}]: ", I[tt])
            tt+=1
    # print(f'Nov_casos [{tdias}:]: ', Nov_casos[tdias:])

    # return Tot_casos[tdias:], Nov_casos[tdias:]
    return Nov_casos[tdias:],Morte_casos[tdias:]



########################################################################
# Model SEIR básico em um rede (Network) - Interação em rede
# A função geradora gera grafos sem escala (redes complexas cuja
# distribuição segue a lei de potência) P(k) ~ k^(-gamma)
# gamma: expoente de livre escala
# k: grau da rede (conexões, interações)
# Os grafos possuem grau de distribuição exponencial com 2 caudas.
########################################################################
def modelo_SEIR_Network_base(local=local, ndias=Ndias, list_local=list_local,
                imprime=False):

    # print('list_local: ', list_local)

    NDIAS  = ndias
    pop    = list_local[0]
    pop_10M = 10000

    if imprime:
        casos  = list_local[1]
        mortes = list_local[2]
        print(f'Casos [{local}]: ', casos)
        print(f'Mortes [{local}]: ', mortes)

    casos = max(ceil((list_local[1] * pop_10M) / pop),10)
    mortes = max(ceil((list_local[2] * pop_10M) / pop),5)
    print(f'Casos [{local}] (para {pop_10M} hab): ', casos)
    print(f'Mortes [{local} (para {pop_10M} hab)]: ', mortes)

    # n       : nós da rede de interação
    # m       : média de: arestas, contatos, conexões, interações
    baseGraph = networkx.barabasi_albert_graph(n=pop_10M, m=9)

    # Interações normais - Base:
    G_normal     = custom_exponential_graph(baseGraph, scale=100)
    if imprime:
        plot_degree_distn(G_normal, '1 Interações normais (Base)', max_degree=40)

    # Interações com distanciamento social:
    G_distancing = custom_exponential_graph(baseGraph, scale=10)
    if imprime:
        plot_degree_distn(G_distancing, '2 Interações com distanciamento social', max_degree=40)

    # Interações com Quarentena:
    G_quarantine = custom_exponential_graph(baseGraph, scale=5)
    if imprime:
        plot_degree_distn(G_quarantine, '3 Interações com Quarentena', max_degree=40)

    # Modelo SEIR network com parametros similares à pandemia COVID-19
    model = SEIRSNetworkModel(G=G_normal,     # população
                              initI=casos,    # número de casos
                              # initI=pop_10M/100, # número inicial de casos de infecção
                              initF=mortes,   # número de mortes
                              # initF   =0,     # número inicial de casos de morte
                              beta=0.155,     # taxa de transmissão/período
                              sigma=1/5.2,    # taxa de progressão
                              gamma=1/12.39,  # taxa de recuperação
                              xi=0.0,         # > SEIRS: Há taxa de re-susceptibilidade
                              p=0.5,          # > SEIR com de interações globais (prob.)
                              Q       =G_quarantine, # Interações com Quarentena:
                              mu_I    =0.0004,# taxa de mortalidade de infecção
                              mu_0    =0,     # taxa de mortalidade base da população
                              nu      =0,     # taxa de nataliadde da população
                              beta_D  =0.155, # taxa de transmissão de casos detectados
                              sigma_D=1/5.2,  # taxa de progressão de casos detectados
                              gamma_D=1/12.39,# taxa de recuperação de casos detectados
                              mu_D=0.0004,    # taxa de mortalidade  de casos detectados
                              theta_E=0.0,    # taxa de testes de indivíduos expostos
                              theta_I=0.0,    # taxa de testes de indivíduos infectados
                              phi_E=0.0,      # taxa de rastreamento de expostos
                              phi_I=0.0,      # taxa de rastreamento de infectados
                              psi_E=1.0,      # prob de resultados positivos p/ indivíduos expostos
                              psi_I=1.0,      # prob de resultados positivos p/ indivíduos infectados
                              q=0.5,          # probabilidade de interações na quarentena
                              initE   =0,     # número inicial de casos de expostos
                              initD_E =0,     # número inicial de casos de expostos detectados
                              initD_I =0,     # número inicial de casos de infectados detectados
                              initR   =0)     # número inicial de casos de recuperação


    model.run(T=NDIAS)

    titulo_grafico = 'Modelo SEIR Network de infecção pelo COVID-19 para ' + str(local)
    compr_graf = 14
    altur_graf = 8
    dimen_graf = (compr_graf, altur_graf)

    if imprime:
        model.figure_basic(title=titulo_grafico,
                           figsize=dimen_graf)

        model.figure_infections(title=titulo_grafico,
                                figsize=dimen_graf,
                                ylim=0.2)


    #####################################################################
    # Acessando os dados da Simulação: Geração de arquivo .csv
    #####################################################################

    S = model.numS      # time series of S counts
    E = model.numE      # time series of E counts
    I = model.numI      # time series of I counts
    D_E = model.numD_E    # time series of D_E counts
    D_I = model.numD_I    # time series of D_I counts
    R = model.numR      # time series of R counts
    F = model.numF      # time series of F counts

    t = model.tseries   # time values corresponding to the above time series

    with open(IMAG_DIR + '/chart_seirs_net.csv', 'w') as saida:
        # print('S, E, I, R, D_E, D_I, F', file = saida)
        print(  '(S) Suscetiveis,',
                '(E) Expostos,',
                '(I) Infectados,',
                '(R) Recuperados,',
                '(D_E) Expostos detectados,',
                '(D_I) Infectados detectados,'
                '(M) Mortes', file = saida)
        tt = 1
        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d},{2:d},{3:d},{4:d},{5:d},{6:d}'
                    .format(int(S[i]),int(E[i]),int(I[i]),
                            int(R[i]),int(D_E[i]),int(D_I[i]),int(F[i])),
                    file = saida)
            tt+=1

    with open(IMAG_DIR + '/chart_seirs_net2.csv', 'w') as saida:
        # print('I, D_all, E', file = saida)
        print(  '(I) Infectados,',
                '(D_all) Detectados,',
                '(E) Expostos', file = saida)
        tt = 1
        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d},{2:d}'
                      .format(int(I[i]),int(D_E[i]+D_I[i]) ,int(E[i])),
                              file = saida)
            tt+=1


    ref_model = model
    return ref_model

########################################################################
# Model SEIRS Network completo
########################################################################

def modelo_SEIRS_network(ref_model, ref_model_determ, local=local,
                         ndias=Ndias, list_local=list_local,imprime=False,
                         id=ini_dist, fd=fim_dist):
    # print('list_local: ', list_local)

    NDIAS  = ndias
    pop    = list_local[0]
    # casos  = list_local[1]
    # mortes = list_local[2]
    # Gerando Redes de Interação: A dinâmica de epidemia ocorre em redes de
    # interação (diferentemente dos modelos determinísticos)
    # (Fixo: Outros parâmetros variam de maneira proporcional)
    pop_10M = 10000 # nós da rede de interação


    if imprime:
        casos  = list_local[1]
        mortes = list_local[2]
        print(f'Casos [{local}]: ', casos)
        print(f'Mortes [{local}]: ', mortes)

        casos = max(ceil((list_local[1] * pop_10M) / pop),10)
        mortes = max(ceil((list_local[2] * pop_10M) / pop),5)
        print(f'Casos [{local}] (para {pop_10M} hab): ', casos)
        print(f'Mortes [{local} (para {pop_10M} hab)]: ', mortes)

    # n       : nós da rede de interação
    # m       : média de: arestas, contatos, conexões, interações
    baseGraph = networkx.barabasi_albert_graph(n=pop_10M, m=9)

    # Interações normais - Base:
    G_normal     = custom_exponential_graph(baseGraph, scale=100)
    # if imprime:
    #     plot_degree_distn(G_normal, 'Interações normais (Base)', max_degree=40)

    # Interações com distanciamento social:
    G_distancing = custom_exponential_graph(baseGraph, scale=10)
    # if imprime:
    #     plot_degree_distn(G_distancing, 'Interações com distanciamento social', max_degree=40)

    # Interações com Quarentena:
    G_quarantine = custom_exponential_graph(baseGraph, scale=5)
    # if imprime:
    #     plot_degree_distn(G_quarantine, 'Interações com Quarentena', max_degree=40)

    if imprime:
        # Todos os gráficos em conjunto:
        import matplotlib.pyplot as pyplot
        import seaborn
        seaborn.set_style('ticks')
        seaborn.despine()

        # Get a list of the node degrees:
        graph = baseGraph
        if type(graph)==numpy.ndarray:
            BasenodeDegrees = graph.sum(axis=0).reshape((graph.shape[0],1))   # sums of adj matrix cols
        elif type(graph)==networkx.classes.graph.Graph:
            BasenodeDegrees = [d[1] for d in graph.degree()]
        else:
            raise BaseException("Insira uma matriz de adjacencia ou um objeto networkx apenas.")

        # Get a list of the node degrees:
        graph = G_normal
        if type(graph)==numpy.ndarray:
            G_normalnodeDegrees = graph.sum(axis=0).reshape((graph.shape[0],1))   # sums of adj matrix cols
        elif type(graph)==networkx.classes.graph.Graph:
            G_normalnodeDegrees = [d[1] for d in graph.degree()]
        else:
            raise BaseException("Insira uma matriz de adjacencia ou um objeto networkx apenas.")

        # Get a list of the node degrees:
        graph = G_distancing
        if type(graph)==numpy.ndarray:
            G_distancingnodeDegrees = graph.sum(axis=0).reshape((graph.shape[0],1))   # sums of adj matrix cols
        elif type(graph)==networkx.classes.graph.Graph:
            G_distancingnodeDegrees = [d[1] for d in graph.degree()]
        else:
            raise BaseException("Insira uma matriz de adjacencia ou um objeto networkx apenas.")

        # Get a list of the node degrees:
        graph = G_quarantine
        if type(graph)==numpy.ndarray:
            G_quarantinenodeDegrees = graph.sum(axis=0).reshape((graph.shape[0],1))   # sums of adj matrix cols
        elif type(graph)==networkx.classes.graph.Graph:
            G_quarantinenodeDegrees = [d[1] for d in graph.degree()]
        else:
            raise BaseException("Insira uma matriz de adjacencia ou um objeto networkx apenas.")

        # Calculate the mean degree:
        meanDegreeBA = numpy.mean(BasenodeDegrees)
        meanDegreeNM = numpy.mean(G_normalnodeDegrees)
        meanDegreeDT = numpy.mean(G_distancingnodeDegrees)
        meanDegreeQT = numpy.mean(G_quarantinenodeDegrees)

        # Generate a histogram of the node degrees:
        max_degree=40
         # {'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'}
        pyplot.hist(BasenodeDegrees, bins=range(max(BasenodeDegrees)), alpha=0.5, color='tab:gray', label=('Grafo Base: Grau médio = %.1f' % meanDegreeBA))
        pyplot.hist(G_normalnodeDegrees, bins=range(max(G_normalnodeDegrees)), alpha=0.5, color='tab:blue', label=('Interação Normal: Grau médio = %.1f' % meanDegreeNM))
        pyplot.hist(G_distancingnodeDegrees, bins=range(max(G_distancingnodeDegrees)), alpha=0.5, color='tab:orange', label=('Distanciamento: Grau médio = %.1f' % meanDegreeDT))
        pyplot.hist(G_quarantinenodeDegrees, bins=range(max(G_quarantinenodeDegrees)), alpha=0.5, color='tab:red', label=('Quarentena: Grau médio = %.1f' % meanDegreeQT))
        pyplot.xlim(0, max(BasenodeDegrees) if not max_degree else max_degree)
        pyplot.xlabel('Nível') # degree > nível
        pyplot.ylabel('Número de nós')
        pyplot.legend(loc='upper right')
        pyplot.title('Modelo SEIRS Network [Interações]: Normal > Distanciamento > Quarentena')
        with cd(IMAG_DIR):
            pyplot.savefig('fig_seirs_network_interacoes.png')
        pyplot.show()


    model = SEIRSNetworkModel(G=G_normal,
                              initI=casos,      # número de casos
                              initF=mortes,     # número de mortes
                              beta=0.155,       # taxa de transmissão/período
                              sigma=1/5.2,      # taxa de progressão
                              gamma=1/12.39,    # taxa de recuperação
                              mu_I=0.0004,      # taxa de mortalidade de infecção
                              xi=0.001,         # > SEIRS: Há taxa de re-susceptibilidade
                              p=0.5,            # > SEIR com de interações globais (prob.)
                              Q=G_quarantine,   # Interações com Quarentena. Se desativada > G_distancing
                              beta_D=0.155,     # taxa de transmissão de casos detectados
                              sigma_D=1/5.2,    # taxa de progressão de casos detectados
                              gamma_D=1/12.39,  # taxa de recuperação de casos detectados
                              mu_D=0.0004,      # taxa de mortalidade  de casos detectados
                              theta_E=0.00,     # taxa de testes de indivíduos expostos
                              theta_I=0.00,     # taxa de testes de indivíduos infectados
                              phi_E=0.0,        # taxa de rastreamento de expostos
                              phi_I=0.0,        # taxa de rastreamento de infectados
                              psi_E=1.0,        # prob de resultados positivos p/ indivíduos expostos
                              psi_I=1.0,        # prob de resultados positivos p/ indivíduos infectados
                              q=0.5,            # probabilidade de interações na quarentena
                              initE   =0,       # número inicial de casos de expostos
                              initD_E =0,       # número inicial de casos de expostos detectados
                              initD_I =0,       # número inicial de casos de infectados detectados
                              initR   =0)       # número inicial de casos de recuperação


    # Mudança de parâmetros ao longo da simulação
    ini_dist = id
    fim_dist = fd

    # períodos de tempo
    checkpoints = {'t': [ini_dist, fim_dist],
                   'G': [G_distancing, G_normal],
                   'p': [0.1, 0.5],             # prob de interações globais
                   'theta_E': [0.02, 0.02],     # taxa de testes de indivíduos expostos
                   'theta_I': [0.02, 0.02],     # taxa de testes de indivíduos infectados
                   'phi_E':   [0.2, 0.2],       # taxa de rastreamento de expostos
                   'phi_I':   [0.2, 0.2]        # taxa de rastreamento de infectados
                   }

    # Rodadas consecutivas
    # As rodadas do model.run() subsequente inicia-se no estado final da rodada
    # model.run() anterior, exemplo:

    ####################################################
    #              Executando a Simulação              #
    ####################################################
    # T: Período final da simulação. t = 1..T
    model.run(T=NDIAS, checkpoints=checkpoints)
    # model.run(T=20, checkpoints=checkpoints)

    titulo_grafico = 'Modelo SEIRS Network de infecção pelo COVID-19 para ' + str(local)
    compr_graf = 14
    altur_graf = 8
    dimen_graf = (compr_graf, altur_graf)

    if imprime:
        model.figure_basic(title=titulo_grafico,
                           figsize=dimen_graf,
                           vlines=checkpoints['t'],
                           vline_labels=['Início quarentena', 'Fim da quarentena'],
                           # ylim=0.2,
                           shaded_reference_results=ref_model,
                           shaded_reference_label='Rede: sem intervenção',
                           dashed_reference_results=ref_model_determ,
                           dashed_reference_label='Deter: sem intervenção'
                           )
        model.figure_infections(title=titulo_grafico,
                                figsize=dimen_graf,
                                vlines=checkpoints['t'],
                                vline_labels=['Início quarentena', 'Fim da quarentena'],
                                # ylim=0.2,
                                shaded_reference_results=ref_model,
                                shaded_reference_label='Rede: sem intervenção',
                                dashed_reference_results=ref_model_determ,
                                dashed_reference_label='Deter: sem intervenção'
                                )


    #####################################################################
    # Acessando os dados da Simulação: Geração de arquivo .csv
    #####################################################################

    S = model.numS      # time series of S counts
    E = model.numE      # time series of E counts
    I = model.numI      # time series of I counts
    D_E = model.numD_E    # time series of D_E counts
    D_I = model.numD_I    # time series of D_I counts
    R = model.numR      # time series of R counts
    F = model.numF      # time series of F counts

    t = model.tseries   # time values corresponding to the above time series

    with open(IMAG_DIR + '/chart_seirs_net.csv', 'w') as saida:
        # print('S, E, I, R, D_E, D_I, F', file = saida)
        print(  '(S) Suscetiveis,',
                '(E) Expostos,',
                '(I) Infectados,',
                '(R) Recuperados,',
                '(S) Re-Suscetiveis,',
                '(D_E) Expostos detectados,',
                '(D_I) Infectados detectados,'
                '(M) Mortes', file = saida)
        tt = 1
        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d},{2:d},{3:d},{4:d},{5:d},{6:d}'
                    .format(int(S[i]),int(E[i]),int(I[i]),
                            int(R[i]),int(D_E[i]),int(D_I[i]),int(F[i])),
                    file = saida)
            tt+=1

    with open(IMAG_DIR + '/chart_seirs_net2.csv', 'w') as saida:
        # print('I, D_all, E', file = saida)
        print(  '(I) Infectados,',
                '(D_all) Detectados,',
                '(E) Expostos', file = saida)
        tt = 1
        for i in range(len(t)):
            if tt%10 == 0: # Para não imprimir muitos dados contínuos
                print('{0:d},{1:d},{2:d}'
                      .format(int(I[i]),int(D_E[i]+D_I[i]) ,int(E[i])),
                              file = saida)
            tt+=1



########################################################################
# Código antigo, de backup
########################################################################
# Deterministic Model

# # Basic SEIR
# model = SEIRSModel(beta=0.155,        # taxa de transmissão/período
#                    sigma=1/5.2,       # taxa de progressão
#                    gamma=1/12.39,     # taxa de recuperação
#                    initN=10000,      # população
#                    initI=100)         # número de casos
#
# model.run(T=100)
# model.figure_infections()

# # Basic SEIRS
# model = SEIRSModel(beta=0.155,        # taxa de transmissão/período
#                    sigma=1/5.2,       # taxa de progressão
#                    gamma=1/12.39,     # taxa de recuperação
#                    xi=0.001,          # taxa de re-susceptibilidade
#                    initN=10000,      # população
#                    initI=100)         # número de casos
#
# model.run(T=100)
# model.figure_infections()

# A dinâmica do SEIRS com testes:

# # SEIR with testing and different progression rates for
# # detected cases (```theta``` and ```psi``` testing params > 0,
# # rate parameters provided for detected states)

# model = SEIRSModel(beta=0.155,        # taxa de transmissão/período
#                    sigma=1/5.2,       # taxa de progressão
#                    gamma=1/12.39,     # taxa de recuperação
#                    initN=10000,      # população
#                    initI=100,         # número de casos
#                    beta_D=0.100,      # taxa de transmissão de casos detectados
#                    sigma_D=1/4.0,     # taxa de progressão de casos detectados
#                    gamma_D=1/9.0,     # taxa de recuperação de casos detectados
#                    theta_E=0.02,      # taxa de testes de indivíduos expostos
#                    theta_I=0.02,      # taxa de testes de indivíduos infectados
#                    psi_E=1.0,         # prob de resultados positivos p/ indivíduos expostos
#                    psi_I=1.0)         # prob de resultados positivos p/ indivíduos infectados
#
# model.run(T=100)
# model.figure_infections()


# Network Model

# Neste modelo, há um nível de interação da rede G (movimentação).

# nu     : taxa base de nascimento
# p      : probabilidade de interações globais (localidade da rede)
# Q      : grafo de interação na quarentena
# q      : probabilidade de interações na quarentena
# phi_I  : taxa de rastreamento de contato de indivíduos infectados
# phi_E  : taxa de rastreamento de contato de indivíduos expostos

# # # Basic SEIR on a network
# numNodes = 10000                            # população
# # n       : nós
# # m       : arestas (contatos)
# baseGraph = networkx.barabasi_albert_graph(n=numNodes, m=9)
# myGraph = baseGraph

# model = SEIRSNetworkModel(G=myGraph,      # população
#                           beta=0.155,     # taxa de transmissão/período
#                           sigma=1/5.2,    # taxa de progressão
#                           gamma=1/12.39,  # taxa de recuperação
#                           initI=100)      # número de casos
#
# model.run(T=100)
# model.figure_infections()

# # Basic SEIRS on a network
# model = SEIRSNetworkModel(G=myGraph,      # população
#                           beta=0.155,     # taxa de transmissão/período
#                           sigma=1/5.2,    # taxa de progressão
#                           gamma=1/12.39,  # taxa de recuperação
#                           xi=0.001,       # taxa de re-susceptibilidade
#                           initI=100)      # número de casos
#
# model.run(T=100)
# model.figure_infections()

# # SEIR on a network with global interactions (p>0)
# model = SEIRSNetworkModel(G=myGraph,      # população
#                           beta=0.155,     # taxa de transmissão/período
#                           sigma=1/5.2,    # taxa de progressão
#                           gamma=1/12.39,  # taxa de recuperação
#                           p=0.5,          # prob de interações globais
#                           initI=100)      # número de casos
#
# model.run(T=100)
# model.figure_infections()

# SEIR on a network with testing and quarantining
# (```theta``` and ```psi``` testing params > 0,
# quarantine network ```Q``` provided)

# Grafo custom_exponential_graph: custom_exponential_graph()
# base_graph=None, scale=100, min_num_edges=0, m=9, n=None
# base_graph      : grafo inicial (None = barabasi_albert_graph(n,m,networkx))
# scale           : média da dist. exp. do base_graph
#   (valores grandes aproximando o base_graph original)
#   (valores menores resultam em grafos mais esparsos)
# min_num_edges   : número mínimo de arestas que os nós precisam ter no grafo
# n               : parâmetro do algoritmo barabasi_albert_graph (n = nós, se base_graph não é dado)
# m               : parâmetro do algoritmo barabasi_albert_graph (m = arestas, se base_graph não é dado)


# G_quarantine = custom_exponential_graph(baseGraph, scale=5)
# quarantineNetwork = G_quarantine
# G_normal = custom_exponential_graph(baseGraph, scale=100)
# myNetwork = G_normal

# model = SEIRSNetworkModel(G=myNetwork,    # população
#                           beta=0.155,     # taxa de transmissão/período
#                           sigma=1/5.2,    # taxa de progressão
#                           gamma=1/12.39,  # taxa de recuperação
#                           p=0.5,          # prob de interações globais
#                           Q=quarantineNetwork,
#                           q=0.5,          # probabilidade de interações na quarentena
#                           theta_E=0.02,   # taxa de testes de indivíduos expostos
#                           theta_I=0.02,   # taxa de testes de indivíduos infectados
#                           psi_E=1.0,      # prob de resultados positivos p/ indivíduos expostos
#                           psi_I=1.0,      # prob de resultados positivos p/ indivíduos infectados
#                           initI=100)      # número de casos
#
# model.run(T=100)
# model.figure_infections()

# SEIR on a network with testing, quarantining,
# and contact tracing (```theta``` and ```psi``` testing params > 0,
# quarantine network ```Q``` provided, ```phi``` contact tracing params > 0)

# model = SEIRSNetworkModel(G=myNetwork,
#                           beta=0.155,     # taxa de transmissão/período
#                           sigma=1/5.2,    # taxa de progressão
#                           gamma=1/12.39,  # taxa de recuperação
#                           p=0.5,          # prob de interações globais
#                           Q=quarantineNetwork,
#                           q=0.5,          # probabilidade de interações na quarentena
#                           theta_E=0.02,   # taxa de testes de indivíduos expostos
#                           theta_I=0.02,   # taxa de testes de indivíduos infectados
#                           phi_E=0.2,      # taxa de rastreamento de expostos
#                           phi_I=0.2,      # taxa de rastreamento de infectados
#                           psi_E=1.0,      # prob de resultados positivos p/ indivíduos expostos
#                           psi_I=1.0,      # prob de resultados positivos p/ indivíduos infectados
#                           initI=100)      # número de casos
#
# model.run(T=100)
# model.figure_infections()



# # Modelo SEIRSNetworkModel completo
# numNodes = 10000                            # população
# # n       : nós
# # m       : arestas (contatos)
# baseGraph    = networkx.barabasi_albert_graph(n=numNodes, m=9)
# G_normal     = custom_exponential_graph(baseGraph, scale=100)
# # Social distancing interactions:
# G_distancing = custom_exponential_graph(baseGraph, scale=10)
# # Quarantine interactions:
# G_quarantine = custom_exponential_graph(baseGraph, scale=5)
#
# model = SEIRSNetworkModel(G=G_normal,
#                           beta=0.155,       # taxa de transmissão/período
#                           sigma=1/5.2,      # taxa de progressão
#                           gamma=1/12.39,    # taxa de recuperação
#                           mu_I=0.0004,      # taxa de mortalidade  de casos iniciais
#                           p=0.5,            # prob de interações globais
#                           Q=G_quarantine,
#                           beta_D=0.155,     # taxa de transmissão de casos detectados
#                           sigma_D=1/5.2,    # taxa de progressão de casos detectados
#                           gamma_D=1/12.39,  # taxa de recuperação de casos detectados
#                           mu_D=0.0004,      # taxa de mortalidade  de casos detectados
#                           theta_E=0.02,     # taxa de testes de indivíduos expostos
#                           theta_I=0.02,     # taxa de testes de indivíduos infectados
#                           phi_E=0.2,        # taxa de rastreamento de expostos
#                           phi_I=0.2,        # # taxa de rastreamento de infectados
#                           psi_E=1.0,        # prob de resultados positivos p/ indivíduos expostos
#                           psi_I=1.0,        # prob de resultados positivos p/ indivíduos infectados
#                           q=0.5,            # probabilidade de interações na quarentena
#                           initI=10)         # número de casos

# # Alterando parâmetros ao longo da simulação (checkpoints)
# # checkpoints['t']: dicionário com lista de novos valores a cada período t
#     # Exemplo: No tempo 't=20' inicia-se o distanciamento social, com grafo 'G'
#     # e a probabilidade de interações é reduzido para 0.1. Os parâmetros
#     # de testes (theta_E e theta_I) e rastreamento (phi_E e phi_I) deixam de ser
#     # nulos e o fim do distanciamento social ocorre em 't=100', onde 'G' e 'p'
#     # retornam ao seu valor original e os parâmetros de testes retornam a zero.
#
# checkpoints = {'t': [20, 100],              # períodos de tempo
#                'G': [G_distancing, G_normal],
#                'p': [0.1, 0.5],             # prob de interações globais
#                'theta_E': [0.02, 0.02],     # taxa de testes de indivíduos expostos
#                'theta_I': [0.02, 0.02],     # taxa de testes de indivíduos infectados
#                'phi_E':   [0.2, 0.2],       # taxa de rastreamento de expostos
#                'phi_I':   [0.2, 0.2]        # taxa de rastreamento de infectados
#                }
#
# # T   : Período final da simulação. t = 1..T

# Rodadas consecutivas
# As rodadas do model.run() subsequente inicia-se no estado final da rodada
# model.run() anterior, exemplo:

####################################################
#              Executando a Simulação              #
####################################################
# model.run(T=90, checkpoints=checkpoints)
# model.run(T=20, checkpoints=checkpoints)

# Visualizando os resultados
# Os modelos possuem uma função plot() por conveniencia.
#   A figure_basic() chama a função plot() com parâmetros default e gera uma
#   linha de frequencia de cada estado da população.
#   A figure_infections() chama a função plot() com parâmetros default para
#   gerar uma área de frequencia apenas dos estados de infecção de
#   (E)xpostos, (I)nfectados, (D_E) Expostos detec. e (D_I) Infectado detectado.

# Parâmetros:
# plot_S = 'line', 'shaded', 'stacked' ou False
# plot_E = 'line', 'shaded', 'stacked' ou False
# plot_I = 'line', 'shaded', 'stacked' ou False
# plot_R = 'line', 'shaded', 'stacked' ou False
# plot_F = 'line', 'shaded', 'stacked' ou False
# plot_D_E = 'line', 'shaded', 'stacked' ou False
# plot_D_I = 'line', 'shaded', 'stacked' ou False
# combine_D = True ou False

# Cores matplotlib: https://matplotlib.org/2.0.2/api/colors_api.html
    # color_S = (cor matplotlib da linha ou área)
    # color_E = (cor matplotlib da linha ou área)
    # color_I = (cor matplotlib da linha ou área)
    # color_R = (cor matplotlib da linha ou área)
    # color_F = (cor matplotlib da linha ou área)
    # color_D_E = (cor matplotlib da linha ou área)
    # color_D_I = (cor matplotlib da linha ou área)

# color_reference = (cor de referência do matplotlib da linha ou área)

# Para modelos seirsplus:
    # dashed_reference_results = modelo seirsplus de referência
    # dashed_reference_label
    # shaded_reference_results = modelo seirsplus de referência
    # shaded_reference_label
    # vlines: lista de posições 'x' para plotar linhas verticais
    # vline_colors: cores de vlines (cor matplotlib)
    # vline_styles: estilos de linhas de vlines (matplotlib)
    # vline_labels: lista de string labels
    # ylim: limite máximo do eixo y
    # xlim: limite máximo do eixo x
    # legend= True ou False
    # title= 'String de titulo'
    # side_title=posição no eixo x
    # plot_percentages = True ou False
    # figsize=(x,y) tupla com dimensao da figura
    # use_seaborn=True ou False

# Exemplo
# model.figure_basic() # Valores default
# model.figure_basic(
#                    plot_S='line',   # Susceptível
#                    plot_E='line',   # Exposto
#                    plot_I='line',   # Infectado
#                    plot_R='line',   # Recuperado
#                    plot_F='line',   # Mortes
#                    plot_D_E='line', # Exposto Detectado
#                    plot_D_I='line', # Infectado Detectado
#                    combine_D=True,
#                    # color_S='m',
#                    # dashed_reference_results=model,
#                    # dashed_reference_label=model,
#                    # vlines=[3,8],
#                    vline_labels=['Início', 'Fim'],
#                    legend=True,
#                    title='Modelo COVID-19',
#                    plot_percentages=True,
#                    figsize=(17,5),
#                    use_seaborn=False
#                    )

# model.figure_infections()
# model.figure_infections(
#                    plot_S=False,   # Susceptível
#                    plot_E='stacked',   # Exposto
#                    plot_I='stacked',   # Infectado
#                    plot_R='stacked',   # Recuperado
#                    plot_F='stacked',   # Mortes
#                    plot_D_E='stacked', # Exposto Detectado
#                    plot_D_I='stacked', # Infectado Detectado
#                    combine_D=True,
#                    # color_S='m',
#                    # dashed_reference_results=model,
#                    # dashed_reference_label=model,
#                    # vlines=[3,8],
#                    # vline_labels=['Início', 'Fim'],
#                    legend=True,
#                    title='Modelo COVID-19',
#                    plot_percentages=True,
#                    # plot_percentages=False,
#                    figsize=(17,5),
#                    use_seaborn=True
# )
########################################################################
