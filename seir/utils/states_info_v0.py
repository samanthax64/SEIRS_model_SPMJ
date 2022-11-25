#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys # Importa modulos do sistema
import os # Local (path) do sistema
import pathlib  # Local do diretório (pasta)
import csv
from urllib import request
import json
from seir.utils.folders import cd


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

def load_states():
    # Carrega a lista de municípios do Brasil
    with cd(pathlib.Path(__file__).parent.absolute()):
        with open('estados.json', 'r', encoding='utf-8-sig') as est:
            list_dic_est = json.load(est)
        return list_dic_est

# Diretório atual: Retorna ao diretório atual
# print('>>> Local atual:', pathlib.Path().absolute())
# Retorna a população, o numero de casos e mortes (em 2020) pelo covid-19.
def states_pop_cases_deaths(state_name):
    # Estado: [população, casos, mortes]
    read_est_cases()
    # Carrega a lista de casos nos estados do Brasil
    # os.chdir(DATA_DIR)
    # with cd(DATA_DIR):
    with cd(pathlib.Path(__file__).parent.absolute()):
        with open('est_casos.json', 'r', encoding='utf-8-sig') as m:
            dic_state_cases = json.load(m)

    dic_est_pop_cases_deaths = {}
    for dic_est in dic_state_cases:
        if dic_est["nome"] == state_name:
            dic_est_pop_cases_deaths[state_name] = \
            [dic_est["pop"], dic_est["casos"], dic_est["mortes"]]
    # print("dic_est_pop_cases_deaths: ", dic_est_pop_cases_deaths)
    return dic_est_pop_cases_deaths.get(state_name, '** Município inválido **')


def read_est_cases(url='https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv'):
    """
    Armazena os casos covid por estado no Brasil
    Dados baixados de https://labs.wesleycota.com/sarscov2/br/
    """
    with request.urlopen(url) as entrada:
        print('Baixando os dados covid-19 dos estados em csv...')
        # dados = entrada.read().decode('latin1')
        dados = entrada.read().decode('utf-8')
        print('Download completo!')

        # for estado in csv.reader(dados.splitlines()):
        #     # country,state,totalCases,totalCasesMS,notConfirmedByMS,deaths,URL
        #     print('{0:s}: {1:s} {2:s}'.format(estado[1], estado[2], estado[5]))

        ##############################################################
        # Cabeçalhos
        # # country,state,totalCases,totalCasesMS,notConfirmedByMS,deaths,URL
        # Cabeçalhos: state, população, totalCases, deaths
        ##############################################################
        # with open(DATA_DIR + '/est_casos.csv', 'w') as saida:
        with cd(pathlib.Path(__file__).parent.absolute()):
            with open('est_casos.csv', 'w') as saida:
                for estado in csv.reader(dados.splitlines()):
                    # pessoa = registro.strip().split(',')
                    print('{0:s},{1:s},{2:s}'.format(estado[1],
                                                   estado[2],
                                                   estado[5]), file = saida)

        # if saida.closed:
        #     print('Arquivo de saída: fechado.')

        ##############################################################
        # Dicionários dos estados (json)
        ##############################################################
        # os.chdir(DATA_DIR)
        # os.chdir('..')
        # with cd(DATA_DIR):
        list_dic_est = load_states()

        ##############################################################
        # Le a população dos estados
        # Cabeçalhos: estado, população, casos, mortes
        ##############################################################
        lis_est = []
        # with open(DATA_DIR + '/est_casos.csv', newline='') as file:
        with cd(pathlib.Path(__file__).parent.absolute()):
            with open('est_casos.csv', newline='') as file:
                csv_reader = csv.reader(file, delimiter=',')
                next(csv_reader)
                next(csv_reader) # Dados 'TOTAL' > 'Brasil Escala Nacional'
                for estado in csv_reader:
                    for dic_estado in list_dic_est:
                        dic_est = {}
                        if  estado[0] == dic_estado["sigla"]:
                            dic_est["nome"] = dic_estado["nome"]
                            dic_est["pop"]  = dic_estado["populacao"]
                            dic_est["casos"] = int(estado[1])
                            dic_est["mortes"] = int(estado[2])
                            dic_est["lon"] = dic_estado["longitude"]
                            dic_est["lat"] = dic_estado["latitude"]
                            lis_est.append(dic_est)
                    # if  estado[0] == 'TOTAL':
                    #     dic_est["nome"] = 'Brasil Escala Nacional'
                    #     dic_est["pop"]  = 210147125
                    #     dic_est["casos"] = int(estado[1])
                    #     dic_est["mortes"] = int(estado[2])
                    #     dic_est["lon"] = -47.86
                    #     dic_est["lat"] = -15.83
                    #     lis_est.append(dic_est)


        # with open(DATA_DIR + '/est_casos.json', 'w', encoding='utf8') as outfile:
        with cd(pathlib.Path(__file__).parent.absolute()):
            with open('est_casos.json', 'w', encoding='utf8') as outfile:
                json.dump(lis_est, outfile, ensure_ascii=False)



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


# if __name__ == '__main__':
#     read_est_cases()
