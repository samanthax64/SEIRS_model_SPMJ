#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import sys # Importa modulos do sistema
import os # Local (path) do sistema
import pathlib  # Local do diretório (pasta)
import csv
from urllib import request
import json
from seir.utils.folders import cd
import urllib.error
import pandas as pd


# DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'utils')
# OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')

# DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '', 'utils')
# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

# Retorna o código dos estados brasileiros selecionado por sigla.
def states_codes(state):
    states_cod = {# Estado : Cód
                "AC" : 12,
                "AL" : 27,
                "AM" : 13,
                "AP" : 16,
                "BA" : 29,
                "CE" : 23,
                "ES" : 32,
                "GO" : 52,
                "MA" : 21,
                "MG" : 31,
                "MS" : 50,
                "MT" : 51,
                "PA" : 15,
                "PB" : 25,
                "PE" : 26,
                "PI" : 22,
                "PR" : 41,
                "RJ" : 33,
                "RN" : 24,
                "RO" : 11,
                "RR" : 14,
                "RS" : 43,
                "SC" : 42,
                "SE" : 28,
                "SP" : 35,
                "TO" : 17,
                "DF" : 53,
                }
    return states_cod.get(state, '** Estado inválido **')

# Retorna o número de municípios por estado selecionado por sigla.
def states_mun(state_mun = "BR"):
    states_mun = {
                "AC" : 22,
                "AL" : 102,
                "AM" : 62,
                "AP" : 16,
                "BA" : 417,
                "CE" : 184,
                "ES" : 78,
                "GO" : 247,
                "MA" : 217,
                "MG" : 853,
                "MS" : 79,
                "MT" : 141,
                "PA" : 144,
                "PB" : 223,
                "PE" : 184,
                "PI" : 224,
                "PR" : 399,
                "RJ" : 92,
                "RN" : 167,
                "RO" : 52,
                "RR" : 15,
                "RS" : 497,
                "SC" : 295,
                "SE" : 75,
                "SP" : 645,
                "TO" : 139,
                "DF" : 1,
                "BR" : 5569,
                }
    return states_mun.get(state_mun, '** Estado inválido **')

# Retorna a população (em 2018) de cada estado selecionado por sigla.
def states_pop(state_pop):
    states_pop = {# Estado : Pop    : Cód
                "AC" : 869265,      # 12
                "AL" : 3322820,     # 27
                "AM" : 4080610,     # 13
                "AP" : 829494,      # 16
                "BA" : 14812600,    # 29
                "CE" : 9075650,     # 23
                "ES" : 3972390,     # 32
                "GO" : 9895860,     # 52
                "MA" : 7035060,     # 21
                "MG" : 21040700,    # 31
                "MS" : 2748020,     # 50
                "MT" : 3442000,     # 51
                "PA" : 8513500,     # 15
                "PB" : 3996500,     # 25
                "PE" : 9493270,     # 26
                "PI" : 3264530,     # 22
                "PR" : 11348900,    # 41
                "RJ" : 17160000,    # 33
                "RN" : 3479010,     # 24
                "RO" : 1757590,     # 11
                "RR" : 576568,      # 14
                "RS" : 11329600,    # 43
                "SC" : 7075490,     # 42
                "SE" : 2278310,     # 28
                "SP" : 45538900,    # 35
                "TO" : 1555230,     # 17
                "DF" : 3015268,     # 53
                "TOTAL" : 210147125,     #
                }
    return states_pop.get(state_pop, '** Estado inválido **')


# def states_leitos_UTI(estado):
#     st_leitos_UTI = {# Estado : Pop    : Cód
#                 "AC" : 58 ,
#                 "AL" : 426 ,
#                 "AM" : 450 ,
#                 "AP" : 78 ,
#                 "BA" : 1573 ,
#                 "CE" : 1002 ,
#                 "ES" : 804 ,
#                 "GO" : 1200 ,
#                 "MA" : 682 ,
#                 "MG" : 3151 ,
#                 "MS" : 432 ,
#                 "MT" : 591 ,
#                 "PA" : 661 ,
#                 "PB" : 536 ,
#                 "PE" : 1647 ,
#                 "PI" : 293 ,
#                 "PR" : 2444 ,
#                 "RJ" : 4008 ,
#                 "RN" : 526 ,
#                 "RO" : 285 ,
#                 "RR" : 25 ,
#                 "RS" : 1660 ,
#                 "SC" : 1064 ,
#                 "SE" : 295 ,
#                 "SP" : 9269 ,
#                 "TO" : 161 ,
#                 "DF" : 997 ,
#                 "TOTAL" : 30774 ,
#                 }
#     return st_leitos_UTI.get(estado, '** Estado inválido **')

# Leitos UTI dedicados ao COVID19
def states_leitos_UTI(estado):
    st_leitos_UTI = {# Estado : Pop    : Cód
                "AC" : 74 ,
                "AL" : 269 ,
                "AM" : 242 ,
                "AP" : 93 ,
                "BA" : 1268 ,
                "CE" : 831 ,
                "ES" : 608 ,
                "GO" : 547 ,
                "MA" : 393 ,
                "MG" : 2168 ,
                "MS" : 252 ,
                "MT" : 383 ,
                "PA" : 486 ,
                "PB" : 249 ,
                "PE" : 992 ,
                "PI" : 335 ,
                "PR" : 886 ,
                "RJ" : 1946 ,
                "RN" : 443 ,
                "RO" : 158 ,
                "RR" : 25 ,
                "RS" : 917 ,
                "SC" : 822 ,
                "SE" : 169 ,
                "SP" : 5185 ,
                "TO" : 91 ,
                "DF" : 426 ,
                "TOTAL" : 20258 ,
                }
    return st_leitos_UTI.get(estado, '** Estado inválido **')


def states_novos_leitos_UTI_covid(estado):
    st_novos_leitos_UTI_covid = {# Estado : Pop    : Cód
                "AC" : 0 ,
                "AL" : 0 ,
                "AM" : 0 ,
                "AP" : 0 ,
                "BA" : 0 ,
                "CE" : 0 ,
                "ES" : 0 ,
                "GO" : 0 ,
                "MA" : 0 ,
                "MG" : 0 ,
                "MS" : 0 ,
                "MT" : 0 ,
                "PA" : 0 ,
                "PB" : 0 ,
                "PE" : 0 ,
                "PI" : 0 ,
                "PR" : 0 ,
                "RJ" : 0 ,
                "RN" : 0 ,
                "RO" : 0 ,
                "RR" : 0 ,
                "RS" : 0 ,
                "SC" : 0 ,
                "SE" : 0 ,
                "SP" : 0 ,
                "TO" : 0 ,
                "DF" : 0 ,
                "TOTAL" : 0 ,
                }
    return st_novos_leitos_UTI_covid.get(estado, '** Estado inválido **')


# def states_leitos_Gerais(estado):
#     st_leitos_Gerais = {# Estado : Pop    : Cód
#                 "AC" : 924 ,
#                 "AL" : 3756 ,
#                 "AM" : 3604 ,
#                 "AP" : 692 ,
#                 "BA" : 18528 ,
#                 "CE" : 11728 ,
#                 "ES" : 5430 ,
#                 "GO" : 10914 ,
#                 "MA" : 8480 ,
#                 "MG" : 29160 ,
#                 "MS" : 3592 ,
#                 "MT" : 4726 ,
#                 "PA" : 9260 ,
#                 "PB" : 5130 ,
#                 "PE" : 15425 ,
#                 "PI" : 4677 ,
#                 "PR" : 17851 ,
#                 "RJ" : 22212 ,
#                 "RN" : 4785 ,
#                 "RO" : 2930 ,
#                 "RR" : 1048 ,
#                 "RS" : 20500 ,
#                 "SC" : 10555 ,
#                 "SE" : 2362 ,
#                 "SP" : 58438 ,
#                 "TO" : 2139 ,
#                 "DF" : 4419 ,
#                 "TOTAL" : 268134 ,
#                 }
#     return st_leitos_Gerais.get(estado, '** Estado inválido **')

# Leitos clínicos por estado
def states_leitos_Gerais(estado):
    st_leitos_Gerais = {# Estado : Pop    : Cód
                "AC" : 738 ,
                "AL" : 2639 ,
                "AM" : 2518 ,
                "AP" : 657 ,
                "BA" : 11573 ,
                "CE" : 7682 ,
                "ES" : 3382 ,
                "GO" : 6528 ,
                "MA" : 6509 ,
                "MG" : 20496 ,
                "MS" : 2265 ,
                "MT" : 3132 ,
                "PA" : 6366 ,
                "PB" : 3566 ,
                "PE" : 10622 ,
                "PI" : 3219 ,
                "PR" : 11229 ,
                "RJ" : 15143 ,
                "RN" : 3111 ,
                "RO" : 2280 ,
                "RR" : 996 ,
                "RS" : 13910 ,
                "SC" : 6775 ,
                "SE" : 1466 ,
                "SP" : 36741 ,
                "TO" : 1022 ,
                "DF" : 2906 ,
                "TOTAL" : 187471 ,
                }
    return st_leitos_Gerais.get(estado, '** Estado inválido **')


def states_novos_leitos_Gerais_covid(estado):
    st_novos_leitos_Gerais_covid = {# Estado : Pop    : Cód
                "AC" : 0 ,
                "AL" : 0 ,
                "AM" : 0 ,
                "AP" : 0 ,
                "BA" : 0 ,
                "CE" : 0 ,
                "ES" : 0 ,
                "GO" : 0 ,
                "MA" : 0 ,
                "MG" : 0 ,
                "MS" : 0 ,
                "MT" : 0 ,
                "PA" : 0 ,
                "PB" : 0 ,
                "PE" : 0 ,
                "PI" : 0 ,
                "PR" : 0 ,
                "RJ" : 0 ,
                "RN" : 0 ,
                "RO" : 0 ,
                "RR" : 0 ,
                "RS" : 0 ,
                "SC" : 0 ,
                "SE" : 0 ,
                "SP" : 0 ,
                "TO" : 0 ,
                "DF" : 0 ,
                "TOTAL" : 0 ,
                }
    return st_novos_leitos_Gerais_covid.get(estado, '** Estado inválido **')


# https://www.medrxiv.org/content/10.1101/2020.04.25.20077396v1.full.pdf
def taxa_internacao_hospitalar(sigla):
    st_tx_intern_hosp = {# Estado : Pop    : Cód
                "AC"   :   0.0559,
                "AL"   :   0.0802,
                "AM"   :   0.0729,
                "AP"   :   0.0606,
                "BA"   :   0.0681,
                "CE"   :   0.0920,
                "DF"   :   0.0633,
                "ES"   :   0.0705,
                "GO"   :   0.0695,
                "MA"   :   0.0804,
                "MG"   :   0.0774,
                "MS"   :   0.0581,
                "MT"   :   0.0556,
                "PA"   :   0.0842,
                "PB"   :   0.0715,
                "PE"   :   0.1117,
                "PI"   :   0.0704,
                "PR"   :   0.0761,
                "RJ"   :   0.0970,
                "RN"   :   0.0715,
                "RO"   :   0.0604,
                "RR"   :   0.0503,
                "RS"   :   0.0740,
                "SC"   :   0.0653,
                "SE"   :   0.0554,
                "SP"   :   0.0882,
                "TO"   :   0.0545,
                }
    return st_tx_intern_hosp.get(sigla, '** Estado inválido **')


def states_name(sigla):
    states_name = {# Estado : nome
                'RO' : 'Rondônia',
                'AC' : 'Acre',
                'AM' : 'Amazonas',
                'RR' : 'Roraima',
                'PA' : 'Pará',
                'AP' : 'Amapá',
                'TO' : 'Tocantins',
                'MA' : 'Maranhão',
                'PI' : 'Piauí',
                'CE' : 'Ceará',
                'RN' : 'Rio Grande do Norte',
                'PB' : 'Paraíba',
                'PE' : 'Pernambuco',
                'AL' : 'Alagoas',
                'SE' : 'Sergipe',
                'BA' : 'Bahia',
                'MG' : 'Minas Gerais',
                'ES' : 'Espírito Santo',
                'RJ' : 'Rio de Janeiro',
                'SP' : 'São Paulo',
                'PR' : 'Paraná',
                'SC' : 'Santa Catarina',
                'RS' : 'Rio Grande do Sul',
                'MS' : 'Mato Grosso do Sul',
                'MT' : 'Mato Grosso',
                'GO' : 'Goiás',
                'DF' : 'Distrito Federal',
                # "TOTAL" : 'Brasil Escala Nacional',
                }
    return states_name.get(sigla, '** Estado inválido **')


def states_sigla(nome):
    states_sigla = {# Estado : sigla
			 'Rondônia': 'RO' ,
			 'Acre': 'AC' ,
			 'Amazonas': 'AM' ,
			 'Roraima': 'RR' ,
			 'Pará': 'PA' ,
			 'Amapá': 'AP' ,
			 'Tocantins': 'TO' ,
			 'Maranhão': 'MA' ,
			 'Piauí': 'PI' ,
			 'Ceará': 'CE' ,
			 'Rio Grande do Norte': 'RN' ,
			 'Paraíba': 'PB' ,
			 'Pernambuco': 'PE' ,
			 'Alagoas': 'AL' ,
			 'Sergipe': 'SE' ,
			 'Bahia': 'BA' ,
			 'Minas Gerais': 'MG' ,
			 'Espírito Santo': 'ES' ,
			 'Rio de Janeiro': 'RJ' ,
			 'São Paulo': 'SP' ,
			 'Paraná': 'PR' ,
			 'Santa Catarina': 'SC' ,
			 'Rio Grande do Sul': 'RS' ,
			 'Mato Grosso do Sul': 'MS' ,
			 'Mato Grosso': 'MT' ,
			 'Goiás': 'GO' ,
			 'Distrito Federal': 'DF' ,
                }
    return states_sigla.get(nome, '** Estado inválido **')

# Retorna dicionário c/ dados dos múnicípio do Brasil: "codigo_ibge",
# "nome", "latitude", "longitude", "eh capital?", "codigo_uf"
# Diretório atual: Retorna ao diretório atual
# print('>>> Local atual:', pathlib.Path().absolute())
# Onde começa o script
# print('Local do arquivo: ',pathlib.Path(__file__).parent.absolute())

# #############################################################
# # Em intro.py [Estados] Gera lista de casos dos estados
# #############################################################
# def load_states():
#     # Carrega a lista de municípios do Brasil
#     with cd(pathlib.Path(__file__).parent.absolute()):
#         with open('estados.json', 'r', encoding='utf-8-sig') as est:
#             list_dic_est = json.load(est)
#         return list_dic_est

# #############################################################
# # Em intro.py [Estados] Gera lista de casos dos estados
# #############################################################
# # Diretório atual: Retorna ao diretório atual
# # print('>>> Local atual:', pathlib.Path().absolute())
# # Retorna a população, o numero de casos e mortes (em 2020) pelo covid-19.
# def states_pop_cases_deaths(state_name):
#     # Estado: [população, casos, mortes]
#     read_est_cases()
#     # Carrega a lista de casos nos estados do Brasil
#     # os.chdir(DATA_DIR)
#     # with cd(DATA_DIR):
#     with cd(pathlib.Path(__file__).parent.absolute()):
#         with open('est_casos.json', 'r', encoding='utf-8-sig') as m:
#             dic_state_cases = json.load(m)
#
#     dic_est_pop_cases_deaths = {}
#     for dic_est in dic_state_cases:
#         if dic_est["nome"] == state_name:
#             dic_est_pop_cases_deaths[state_name] = \
#             [dic_est["pop"], dic_est["casos"], dic_est["mortes"]]
#     # print("dic_est_pop_cases_deaths: ", dic_est_pop_cases_deaths)
#     return dic_est_pop_cases_deaths.get(state_name, '** Estado inválido **')


#############################################################
# Em intro.py [Estados] Lê url e armazena casos por estado
#############################################################
# def read_est_cases(url='https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv'):
#     """
#     Armazena os casos covid por estado no Brasil
#     Dados baixados de https://covid19br.wcota.me/
#     """
#     with request.urlopen(url) as entrada:
#         print('Baixando os dados covid-19 dos estados em csv...')
#         # dados = entrada.read().decode('latin1')
#         dados = entrada.read().decode('utf-8')
#         print('Download completo!')
#
#         # for estado in csv.reader(dados.splitlines()):
#         #     # country,state,totalCases,totalCasesMS,notConfirmedByMS,deaths,URL
#         #     print('{0:s}: {1:s} {2:s}'.format(estado[1], estado[2], estado[5]))
#
#         ##############################################################
#         # Cabeçalhos
#         # # country,state,totalCases,totalCasesMS,notConfirmedByMS,deaths,URL
#         # Cabeçalhos: state, população, totalCases, deaths
#         ##############################################################
#         # with open(DATA_DIR + '/est_casos.csv', 'w') as saida:
#         with cd(pathlib.Path(__file__).parent.absolute()):
#             with open('est_casos.csv', 'w') as saida:
#                 for estado in csv.reader(dados.splitlines()):
#                     # pessoa = registro.strip().split(',')
#                     print('{0:s},{1:s},{2:s}'.format(estado[1],
#                                                    estado[2],
#                                                    estado[5]), file = saida)
#
#         # if saida.closed:
#         #     print('Arquivo de saída: fechado.')
#
#         ##############################################################
#         # Dicionários dos estados (json)
#         ##############################################################
#         # os.chdir(DATA_DIR)
#         # os.chdir('..')
#         # with cd(DATA_DIR):
#         list_dic_est = load_states()
#
#         ##############################################################
#         # Le a população dos estados
#         # Cabeçalhos: estado, população, casos, mortes
#         ##############################################################
#         lis_est = []
#         # with open(DATA_DIR + '/est_casos.csv', newline='') as file:
#         with cd(pathlib.Path(__file__).parent.absolute()):
#             with open('est_casos.csv', newline='') as file:
#                 csv_reader = csv.reader(file, delimiter=',')
#                 next(csv_reader)
#                 next(csv_reader) # Dados 'TOTAL' > 'Brasil Escala Nacional'
#                 for estado in csv_reader:
#                     for dic_estado in list_dic_est:
#                         dic_est = {}
#                         if  estado[0] == dic_estado["sigla"]:
#                             dic_est["nome"] = dic_estado["nome"]
#                             dic_est["pop"]  = dic_estado["populacao"]
#                             dic_est["casos"] = int(estado[1])
#                             dic_est["mortes"] = int(estado[2])
#                             dic_est["lon"] = dic_estado["longitude"]
#                             dic_est["lat"] = dic_estado["latitude"]
#                             lis_est.append(dic_est)
#                     # if  estado[0] == 'TOTAL':
#                     #     dic_est["nome"] = 'Brasil Escala Nacional'
#                     #     dic_est["pop"]  = 210147125
#                     #     dic_est["casos"] = int(estado[1])
#                     #     dic_est["mortes"] = int(estado[2])
#                     #     dic_est["lon"] = -47.86
#                     #     dic_est["lat"] = -15.83
#                     #     lis_est.append(dic_est)
#
#
#         # with open(DATA_DIR + '/est_casos.json', 'w', encoding='utf8') as outfile:
#         with cd(pathlib.Path(__file__).parent.absolute()):
#             with open('est_casos.json', 'w', encoding='utf8') as outfile:
#                 json.dump(lis_est, outfile, ensure_ascii=False)


#############################################################
# Em intro.py [Estados] Lê url e retorna casos por estado por dia
#############################################################
# def get_EST_data_by_day():
#
#     #######################################################################
#     URL = "https://raw.githubusercontent.com/wcota/covid19br/master/"
#     df = pd.read_csv(URL + "cases-brazil-cities-time.csv", encoding='utf-8')
#     df_est = df.copy()
#     #######################################################################
#
#     #####################################################################
#     # Casos dos estados no tempo
#     #####################################################################
#
#     df_est.drop(columns=['country', 'city', 'ibgeID','newDeaths',
#                      'deaths', 'newCases'], axis=1, inplace=True)
#
#     index_names = df_est[(df_est['state'] == 'TOTAL')].index
#     df_est.drop(index_names, inplace=True)
#
#     # index_names = df_est[(df_est['city'].str.contains('INDEFINIDA'))].index
#     # df_est.drop(index_names, inplace=True)
#     df_est.reset_index(drop=True, inplace=True)
#     df_est.rename(columns={"state": "Estados"}, inplace=True)
#
#     # https://pandas.pydata.org/docs/user_guide/reshaping.html
#     Estados = df_est.pivot_table(index='Estados', columns='date',
#                           values='totalCases', aggfunc='sum').fillna(0)
#
#     Estados = Estados.T.reset_index(drop=True).T
#     # print('df_est2: ', df_est2)
#
#     # print('Estados: ', Estados)
#     # Filtro por linha e coluna (última = -1)
#     # print('Estados: ', Estados[(Estados.index == 'MG')].iloc[:,-7])
#     Estados.to_csv('./data/est_casos_t.csv', sep=',', encoding='utf-8')
#     df = pd.read_csv("./data/est_casos_t.csv")
#
#     return df.set_index("Estados")


# if __name__ == '__main__':
    # read_est_cases()
    # get_EST_data_by_day()
    # print('get_EST_data_by_day(): ', get_EST_data_by_day())



# ##############################################################
# Backup códigos antigos
# ##############################################################

# dic_est = {}
# lis_est = []
# with open(DATA_DIR + '/est_casos.csv', newline='') as file:
#     csv_reader = csv.reader(file, delimiter=',')
#     next(csv_reader)
#     for estado in csv_reader:
#         dic_est["nome"] = states_name(estado[0])
#         dic_est["pop"]  = states_pop(str(estado[0])
#         dic_est["casos"] = int(estado[1])
#         dic_est["mortes"] = int(estado[2])
#         dic_est["lon"] = dic_munic["longitude"]
#         dic_est["lat"] = dic_munic["latitude"]
#
#
# with open(DATA_DIR + '/est_casos.json', 'w', encoding='utf8') as outfile:
#     json.dump(lis_est, outfile, ensure_ascii=False)
# ################################################################

# # ##############################################################
# # Código para criar arquivo estados.json
# # ##############################################################
# states_name = {# Estado : nome
#             "RO" : 'Rondônia',
#             "AC" : 'Acre',
#             "AM" : 'Amazonas',
#             "RR" : 'Roraima',
#             "PA" : 'Pará',
#             "AP" : 'Amapá',
#             "TO" : 'Tocantins',
#             "MA" : 'Maranhão',
#             "PI" : 'Piauí',
#             "CE" : 'Ceará',
#             "RN" : 'Rio Grande do Norte',
#             "PB" : 'Paraíba',
#             "PE" : 'Pernambuco',
#             "AL" : 'Alagoas',
#             "SE" : 'Sergipe',
#             "BA" : 'Bahia',
#             "MG" : 'Minas Gerais',
#             "ES" : 'Espírito Santo',
#             "RJ" : 'Rio de Janeiro',
#             "SP" : 'São Paulo',
#             "PR" : 'Paraná',
#             "SC" : 'Santa Catarina',
#             "RS" : 'Rio Grande do Sul',
#             "MS" : 'Mato Grosso do Sul',
#             "MT" : 'Mato Grosso',
#             "GO" : 'Goiás',
#             "DF" : 'Distrito Federal',
#             # "TOTAL" : 'Brasil Escala Nacional',
#             }
#
# states_lat_lon = {
#         "AC" : [ -8.77, -70.55],
#         "AL" : [ -9.71, -35.73],
#         "AM" : [ -3.07, -61.66],
#         "AP" : [  1.41, -51.77],
#         "BA" : [-12.96, -38.51],
#         "CE" : [ -3.71, -38.54],
#         "DF" : [-15.83, -47.86],
#         "ES" : [-19.19, -40.34],
#         "GO" : [-16.64, -49.31],
#         "MA" : [ -2.55, -44.30],
#         "MT" : [-12.64, -55.42],
#         "MS" : [-20.51, -54.54],
#         "MG" : [-18.10, -44.38],
#         "PA" : [ -5.53, -52.29],
#         "PB" : [ -7.06, -35.55],
#         "PR" : [-24.89, -51.55],
#         "PE" : [ -8.28, -35.07],
#         "PI" : [ -8.28, -43.68],
#         "RJ" : [-22.84, -43.15],
#         "RN" : [ -5.22, -36.52],
#         "RO" : [-11.22, -62.80],
#         "RS" : [-30.01, -51.22],
#         "RR" : [  1.89, -61.22],
#         "SC" : [-27.33, -49.44],
#         "SE" : [-10.90, -37.07],
#         "SP" : [-23.55, -46.64],
#         "TO" : [-10.25, -48.25],
#     }
#
#
#
# lis_est = []
# # iteratin over dic:
# # for key in d:
# for key in states_name:
#     dic_est = {}
#     dic_est["codigo_uf"] = int(states_codes(key))
#     dic_est["sigla"] = str(key)
#     dic_est["nome"] = states_name[key]
#     dic_est["latitude"] = states_lat_lon[key][0]
#     dic_est["longitude"] = states_lat_lon[key][1]
#     dic_est["populacao"]  = int(states_pop(key))
#     # print('dic_est: ', dic_est)
#     lis_est.append(dic_est)
#
# with open(DATA_DIR + '/estados.json', 'w', encoding='utf8') as outfile:
#     json.dump(lis_est, outfile, ensure_ascii=False)
