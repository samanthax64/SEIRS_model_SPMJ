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


# DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'utils')
# OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')

# Diretório atual: Retorna ao diretório atual
# print('>>> Local atual:', pathlib.Path().absolute())
# Onde começa o script
# print('Local do arquivo: ',pathlib.Path(__file__).parent.absolute())

# #############################################################
# # Em intro.py [Municipios] Retorna lista de dict dos mun. BR.
# #############################################################
# # Retorna dicionário c/ dados dos múnicípio do Brasil: "codigo_ibge",
# # "nome", "latitude", "longitude", "eh capital?", "codigo_uf"
# def load_municipalities():
#     # Carrega a lista de municípios do Brasil
#     with cd(pathlib.Path(__file__).parent.absolute()):
#         with open('municipios.json', 'r', encoding='utf-8-sig') as m:
#             mun_list_dic = json.load(m)
#         return mun_list_dic


# #############################################################
# # Em intro.py [Municipios] Gera lista de casos dos municipios
# #############################################################
# # Diretório atual: Retorna ao diretório atual
# # print('>>> Local atual:', pathlib.Path().absolute())
# def mun_pop_cases_deaths(mun_name):
#     # Carrega a lista de casos nos municípios do Brasil
#     read_mun_cases()
#     # os.chdir(DATA_DIR)
#     # with cd(DATA_DIR):
#     with cd(pathlib.Path(__file__).parent.absolute()):
#         with open('mun_casos.json', 'r', encoding='utf-8-sig') as m:
#             dic_mun_cases = json.load(m)
#
#     dic_mun_pop_cases_deaths = {}
#     for dic_mun in dic_mun_cases:
#         if dic_mun["nome"] == mun_name:
#             dic_mun_pop_cases_deaths[mun_name] = \
#             [dic_mun["pop"], dic_mun["casos"], dic_mun["mortes"]]
#     # print("dic_mun_pop_cases_deaths: ", dic_mun_pop_cases_deaths)
#     return dic_mun_pop_cases_deaths.get(mun_name, '** Município inválido **')



# #############################################################
# # Em intro.py [Municípios] Lê url e armazena casos por município
# #############################################################
# def read_mun_cases(url='https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv'):
#     """
#     Armazena os casos covid por municpipio no Brasil
#     Dados baixados de https://labs.wesleycota.com/sarscov2/br/
#     """
#     with request.urlopen(url) as entrada:
#         print('Baixando os dados covid-19 dos municípios em csv...')
#         # dados = entrada.read().decode('latin1')
#         dados = entrada.read().decode('utf-8')
#         print('Download completo!')
#
#         # for cidade in csv.reader(dados.splitlines()):
#         #     # country,state,city,ibgeID,deaths,totalCases
#         #     print('{0:30s}: {1:30s}'.format(cidade[2], cidade[5]))
#
#         ##############################################################
#         # Cabeçalhos
#         # country,state,city,ibgeID,deaths,totalCases
#         ##############################################################
#         # with open(DATA_DIR + '/mun_casos.csv', 'w') as saida:
#         with cd(pathlib.Path(__file__).parent.absolute()):
#             with open('mun_casos.csv', 'w') as saida:
#                 for cidade in csv.reader(dados.splitlines()):
#                     # pessoa = registro.strip().split(',')
#                     print('{0:s},{1:s},{2:s},{3:s}'.format(cidade[3],
#                                                    cidade[2],
#                                                    cidade[5],
#                                                    cidade[4]), file = saida)
#
#         # if saida.closed:
#         #     print('Arquivo de saída: fechado.')
#
#
#         ##############################################################
#         # Le a população dos municipios
#         # Cabeçalhos: "cod_mun";"pop_tcu";"pop_ans";"pop_sus"
#         ##############################################################
#         dic_mun_pop = {}
#         # with open(DATA_DIR + '/pop_sus_mun.csv', newline='') as file:
#         with cd(pathlib.Path(__file__).parent.absolute()):
#             with open('pop_sus_mun.csv', newline='') as file:
#                 csv_reader = csv.reader(file, delimiter=';')
#                 next(csv_reader)
#                 for cidade in csv_reader:
#                     dic_mun_pop[cidade[0]] = int(cidade[1])
#
#         # print('dic_mun_pop: ', dic_mun_pop)
#
#         ##############################################################
#         # Dicionários dos municipios (json)
#         ##############################################################
#         # os.chdir(DATA_DIR)
#         # os.chdir('..')
#         # with cd(DATA_DIR):
#         dic_mun_list = load_municipalities()
#
#
#         # ##############################################################
#         # # Cria novo Dicionário dos municipios (json) com população
#         # ##############################################################
#         # dic_mun_list_pop = []
#         # for dic_munic in dic_mun_list:
#         #     # print("Codigo: ", int(str(dic_munic["codigo_ibge"])[:-1]))
#         #     # população
#         #     # print('Populacao: ', dic_mun_pop[int(str(dic_munic["codigo_ibge"])[:-1])])
#         #     dic_munic["populacao"] = dic_mun_pop[int(str(dic_munic["codigo_ibge"])[:-1])]
#         #
#         #     dic_mun_list_pop.append(dic_munic)
#         #
#         # # print('dic_mun_list_pop: ', dic_mun_list_pop)
#         #
#         # with open(DATA_DIR + '/municipios.json', 'w', encoding='utf8') as outfile:
#         #     json.dump(dic_mun_list_pop, outfile, ensure_ascii=False)
#
#
#         ##############################################################
#         # Le a população dos municipios
#         # Cabeçalhos: city, totalCases, deaths
#         ##############################################################
#         # dic_mun = {}
#         # with open(DATA_DIR + '/mun_casos.csv', newline='') as file:
#         #     csv_reader = csv.reader(file, delimiter=',')
#         #     next(csv_reader)
#         #     for cidade in csv_reader:
#         #         for dic_munic in dic_mun_list:
#         #             if int(cidade[0]) == dic_munic["codigo_ibge"]:
#         #             # if int(dic_mun[cidade[0]]) == int(str(dic_munic["codigo_ibge"])[:-1]):
#         #                 dic_mun[dic_munic["nome"]] = [
#         #                     # dic_mun_pop[int(str(dic_munic["codigo_ibge"])[:-1])],
#         #                     dic_mun_pop[str(dic_munic["codigo_ibge"])[:-1]],
#         #                     int(cidade[2]),int(cidade[3]),
#         #                     dic_munic["longitude"], dic_munic["latitude"]]
#         #
#         # with open(DATA_DIR + '/mun_casos.json', 'w', encoding='utf8') as outfile:
#         #     json.dump(dic_mun, outfile, ensure_ascii=False)
#
#         lis_mun = []
#         # with open(DATA_DIR + '/mun_casos.csv', newline='') as file:
#         with cd(pathlib.Path(__file__).parent.absolute()):
#             with open('mun_casos.csv', newline='') as file:
#                 csv_reader = csv.reader(file, delimiter=',')
#                 next(csv_reader)
#                 for cidade in csv_reader:
#                     for dic_munic in dic_mun_list:
#                         dic_mun = {}
#                         if int(cidade[0]) == dic_munic["codigo_ibge"]:
#                         # if int(dic_mun[cidade[0]]) == int(str(dic_munic["codigo_ibge"])[:-1]):
#                             dic_mun["nome"] = dic_munic["nome"]
#                             dic_mun["cod_ibge"] = dic_munic["codigo_ibge"]
#                             dic_mun["pop"] = dic_mun_pop[str(dic_munic["codigo_ibge"])[:-1]]
#                             dic_mun["casos"] = int(cidade[2])
#                             dic_mun["mortes"] = int(cidade[3])
#                             dic_mun["lon"] = dic_munic["longitude"]
#                             dic_mun["lat"] = dic_munic["latitude"]
#                             lis_mun.append(dic_mun)
#
#
#         # with open(DATA_DIR + '/mun_casos.json', 'w', encoding='utf8') as outfile:
#         with cd(pathlib.Path(__file__).parent.absolute()):
#             with open('mun_casos.json', 'w', encoding='utf8') as outfile:
#                 json.dump(lis_mun, outfile, ensure_ascii=False)


# if __name__ == '__main__':
#     read_mun_cases()
