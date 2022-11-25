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

# Read csv File

import pandas as pd
import sys # Importa modulos do sistema
import os # Local (path) do sistema
import pathlib  # Local do diretório (pasta)
import json
import csv
from seir.utils.folders import cd
from urllib import request
import urllib.error

# DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '', 'data/')
#
# with cd(DATA_DIR):
#     file=pd.read_csv("arquivo_geral.csv")
#     file.to_csv("covidbr.csv", index=False)
#     file2=pd.read_csv("covidbr.csv")
# # print('file: ', file)
# print('file2: ', file2)


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '', 'seir/utils/')

# with cd(DATA_DIR):
#     dados=[]
#     with open ('cases-brazil-total.csv', 'r') as f:
#         with open('est_casos.csv', 'w') as saida:
#             for line in f:
#                 estado = line.strip().split(',')
#                 dados.append(estado)
#                 print('{0:s},{1:s},{2:s}'.format(estado[2],
#                                                estado[3],
#                                                estado[6]), file = saida)

# #######################################################################
# URL = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv"
# #######################################################################
#
# with request.urlopen(URL) as entrada:
#     print('Baixando os dados covid-19 dos municípios em csv...')
#
#     file=pd.read_csv(URL, encoding='utf-8')
#     # print('file: ', file)
#     with cd(DATA_DIR):
#         file.to_csv("cases-brazil-cities.csv")
#     print('Download completo!')

# with cd(DATA_DIR):
#     # dados=[]
#     with open ('cases-brazil-cities.csv', 'r', encoding="utf8") as f:
#         with open('mun_casos.csv', 'w') as saida:
#             for line in f:
#                 cidade = line.strip().split(',')
#                 # dados.append(cidade)
#                 print('{0:s},{1:s},{2:s},{3:s}'.format(cidade[4],
#                                                cidade[3],
#                                                cidade[6],
#                                                cidade[5]), file = saida)



# i = pd.date_range('2020-02-25', periods=58, freq='1D')
# print(i)
