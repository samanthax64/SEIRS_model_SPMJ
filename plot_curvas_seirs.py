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

######################################################################
# fmt: on
# Turn off black formatting for this function to present the user with more
# compact code.
# fmt: off
import streamlit as st
import time
import numpy as np
import pandas as pd
import re
import csv
import os # Local (path) do sistema
import sys # Importa modulos do sistema
from math import *
import pathlib  # Local do diretório (pasta)
# sys.path.insert(1, './seir/')
# from seir.seir import get_Ndias



########################################################################
# Modelo SEIR (basico)
########################################################################

def plotting_seir_g1():

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # ('..', 'images')    > Um níveil acima
    # ('../..', 'images') > Dois níveis acima
    IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '', 'images')
    # print('IMAG_DIR: ', IMAG_DIR)

    data = pd.read_csv(
                       IMAG_DIR + '/chart_seir.csv', # Dado no seu endereço
                       sep=',',             # Dados separados por virgula
                       quotechar="'",       # Caracteres sob aspas ''
                       dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
                       # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data: ', data)
    # st.line_chart(data)

    # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
    # chart_data = pd.DataFrame(data, columns=['S'])
    chart_data = pd.DataFrame(data)
    # st.line_chart(chart_data)
    # chart = st.line_chart(chart_data)
    chart = st.line_chart(chart_data[:1])

    # print('chart_data[300]: ', chart_data[-1:])
    # print('chart_data[1]: ', chart_data[:1])

    # Numero de dias (Ndias) em 100 etapas de impressao
    # do gráfico
    ch_days = int(len(data)/100)
    print('ch_days: ', ch_days)

    for i in range(1, 101):
        # new_rows = chart_data[3*i-3:3*i]
        new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
        # print('new_rows: ', new_rows)
        status_text.text("%i%% Completo" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Rodar modelo Geral")


def plotting_seir_g2():

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # ('..', 'images')    > Um níveil acima
    # ('../..', 'images') > Dois níveis acima
    IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '', 'images')
    # print('IMAG_DIR: ', IMAG_DIR)

    data = pd.read_csv(
                       IMAG_DIR + '/chart_seir2.csv', # Dado no seu endereço
                       sep=',',             # Dados separados por virgula
                       quotechar="'",       # Caracteres sob aspas ''
                       dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
                       # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data: ', data)
    # st.line_chart(data)

    # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
    # chart_data = pd.DataFrame(data, columns=['S'])
    chart_data = pd.DataFrame(data)
    # st.line_chart(chart_data)
    # chart = st.line_chart(chart_data)
    # chart = st.line_chart(chart_data[:1])
    chart = st.area_chart(chart_data[:1])

    # print('chart_data[300]: ', chart_data[-1:])
    # print('chart_data[1]: ', chart_data[:1])

    # Numero de dias (Ndias) em 100 etapas de impressao
    # do gráfico
    ch_days = int(len(data)/100)
    print('ch_days: ', ch_days)

    for i in range(1, 101):
        # new_rows = chart_data[3*i-3:3*i]
        new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
        # print('new_rows: ', new_rows)
        status_text.text("%i%% Completo" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Rodar modelo Infectados")

########################################################################
# Modelo SEIRS (com re-susceptibilidade) - Ondas
########################################################################

def plotting_seirs_g1():

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # ('..', 'images')    > Um níveil acima
    # ('../..', 'images') > Dois níveis acima
    IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '', 'images')
    # print('IMAG_DIR: ', IMAG_DIR)

    data = pd.read_csv(
                       IMAG_DIR + '/chart_seirs.csv', # Dado no seu endereço
                       sep=',',             # Dados separados por virgula
                       quotechar="'",       # Caracteres sob aspas ''
                       dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
                       # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data: ', data)
    # st.line_chart(data)

    # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
    # chart_data = pd.DataFrame(data, columns=['S'])
    chart_data = pd.DataFrame(data)
    # st.line_chart(chart_data)
    # chart = st.line_chart(chart_data)
    chart = st.line_chart(chart_data[:1])

    # print('chart_data[300]: ', chart_data[-1:])
    # print('chart_data[1]: ', chart_data[:1])

    # Numero de dias (Ndias) em 100 etapas de impressao
    # do gráfico
    ch_days = int(len(data)/100)
    print('ch_days: ', ch_days)

    for i in range(1, 101):
        # new_rows = chart_data[3*i-3:3*i]
        new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
        # print('new_rows: ', new_rows)
        status_text.text("%i%% Completo" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Rodar modelo Re-susceptibilidade")


def plotting_seirs_g2():

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # ('..', 'images')    > Um níveil acima
    # ('../..', 'images') > Dois níveis acima
    IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '', 'images')
    # print('IMAG_DIR: ', IMAG_DIR)

    data = pd.read_csv(
                       IMAG_DIR + '/chart_seirs2.csv', # Dado no seu endereço
                       sep=',',             # Dados separados por virgula
                       quotechar="'",       # Caracteres sob aspas ''
                       dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
                       # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data: ', data)
    # st.line_chart(data)

    # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
    # chart_data = pd.DataFrame(data, columns=['S'])
    chart_data = pd.DataFrame(data)
    # st.line_chart(chart_data)
    # chart = st.line_chart(chart_data)
    # chart = st.line_chart(chart_data[:1])
    chart = st.area_chart(chart_data[:1])

    # print('chart_data[300]: ', chart_data[-1:])
    # print('chart_data[1]: ', chart_data[:1])

    # Numero de dias (Ndias) em 100 etapas de impressao
    # do gráfico
    ch_days = int(len(data)/100)
    print('ch_days: ', ch_days)

    for i in range(1, 101):
        # new_rows = chart_data[3*i-3:3*i]
        new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
        # print('new_rows: ', new_rows)
        status_text.text("%i%% Completo" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Rodar modelo Infectados Re-susceptibilidade")


########################################################################
# Modelo SEIRS+
########################################################################

def plotting_seirs_plus_g1():

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # ('..', 'images')    > Um níveil acima
    # ('../..', 'images') > Dois níveis acima
    IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '', 'images')
    # print('IMAG_DIR: ', IMAG_DIR)

    data = pd.read_csv(
                       IMAG_DIR + '/chart_seirs_plus.csv', # Dado no seu endereço
                       sep=',',             # Dados separados por virgula
                       quotechar="'",       # Caracteres sob aspas ''
                       dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
                       # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data: ', data)
    # st.line_chart(data)

    # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
    # chart_data = pd.DataFrame(data, columns=['S'])
    chart_data = pd.DataFrame(data)
    # st.line_chart(chart_data)
    # chart = st.line_chart(chart_data)
    chart = st.line_chart(chart_data[:1])

    # print('chart_data[300]: ', chart_data[-1:])
    # print('chart_data[1]: ', chart_data[:1])

    # Numero de dias (Ndias) em 100 etapas de impressao
    # do gráfico
    ch_days = int(len(data)/100)
    print('ch_days: ', ch_days)

    for i in range(1, 101):
        # new_rows = chart_data[3*i-3:3*i]
        new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
        # print('new_rows: ', new_rows)
        status_text.text("%i%% Completo" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Rodar modelo Quarentena")


def plotting_seirs_plus_g2():

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # ('..', 'images')    > Um níveil acima
    # ('../..', 'images') > Dois níveis acima
    IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '', 'images')
    # print('IMAG_DIR: ', IMAG_DIR)

    data = pd.read_csv(
                       IMAG_DIR + '/chart_seirs_plus2.csv', # Dado no seu endereço
                       sep=',',             # Dados separados por virgula
                       quotechar="'",       # Caracteres sob aspas ''
                       dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
                       # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data: ', data)
    # st.line_chart(data)

    # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
    # chart_data = pd.DataFrame(data, columns=['S'])
    chart_data = pd.DataFrame(data)
    # st.line_chart(chart_data)
    # chart = st.line_chart(chart_data)
    # chart = st.line_chart(chart_data[:1])
    chart = st.area_chart(chart_data[:1])

    # print('chart_data[300]: ', chart_data[-1:])
    # print('chart_data[1]: ', chart_data[:1])

    # Numero de dias (Ndias) em 100 etapas de impressao
    # do gráfico
    ch_days = int(len(data)/100)
    print('ch_days: ', ch_days)

    for i in range(1, 101):
        # new_rows = chart_data[3*i-3:3*i]
        new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
        # print('new_rows: ', new_rows)
        status_text.text("%i%% Completo" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Rodar modelo Infectados Quarentena")


plotting_seir_g1()
plotting_seir_g2()

# plotting_seirs_g1()
# plotting_seirs_g2()

plotting_seirs_plus_g1()
plotting_seirs_plus_g2()

######################################################################
# # fmt: on
# # Turn off black formatting for this function to present the user with more
# # compact code.
# # fmt: off

# def plotting_demo():
#     import streamlit as st
#     import time
#     import numpy as np
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#     last_rows = np.random.randn(1, 1)
#     chart = st.line_chart(last_rows)
#
#     for i in range(1, 101):
#         new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#         status_text.text("%i%% Complete" % i)
#         chart.add_rows(new_rows)
#         progress_bar.progress(i)
#         last_rows = new_rows
#         time.sleep(0.05)
#
#     progress_bar.empty()
#
#     # Streamlit widgets automatically run the script from top to bottom. Since
#     # this button is not connected to any other logic, it just causes a plain
#     # rerun.
#     st.button("Re-run")
#
# plotting_demo()
######################################################################


# ######################################################################
# import matplotlib.pyplot as plt
# import numpy as np
# import streamlit as st
# import time
#
# fig, ax = plt.subplots()
#
# max_x = 5
# max_rand = 10
#
# x = np.arange(0, max_x)
# ax.set_ylim(0, max_rand)
# line, = ax.plot(x, np.random.randint(0, max_rand, max_x))
# the_plot = st.pyplot(plt)
#
# def init():  # give a clean slate to start
#     line.set_ydata([np.nan] * len(x))
#
# def animate(i):  # update the y values (every 1000ms)
#     line.set_ydata(np.random.randint(0, max_rand, max_x))
#     the_plot.pyplot(plt)
#
# init()
# for i in range(100):
#     animate(i)
#     time.sleep(0.1)
# ######################################################################

# ######################################################################
# import streamlit as st
# import numpy as np
# import time
#
# def get_frame():
#     return np.random.randint(0, 255, size=(10,10))
#
# my_image = st.image(get_frame(), caption='Random image', width=600)
#
# while True:
#     time.sleep(0.1)
#     my_image.image(get_frame(), caption='Random image', width=600)
# ######################################################################


#####################################################################
# Tentativas fracassadas ... :(
#####################################################################

    # with open('chart_seirs_net.csv', newline ='') as csv_file:
    #     data = csv_file.read()
    #     matrix = []
    #     for row in csv.reader(data.splitlines()):
    #         # for item in row:
    #     # data = csv_file.readlines().split(',')
    #     # for i in
    #         matrix.append(row)
    #     # matrix = re.sub('\n', '', ''.join(matrix))
    #     # data = []
    #     # data_temp =  csv.reader(csv_file, delimiter=',')
    #     # for row in data_temp:
    #     #     # print(', '.join(row))
    #     #     data.append(row)
    # # data = data.split(',')
    # # data = pd.read_csv('chart_seirs_net.csv', sep=',')
    # mat = np.array(matrix)
    # mtx = mat.transpose()
    # # print('data: ', data)
    # print('matrix: ', mat)
    # # df = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_i', 'F'])
    # df = pd.DataFrame(mat,
    #                   columns=['S', 'E', 'I', 'R', 'D_E', 'D_i', 'F'],
    #                   # columns=['S']
    #                   # index=['S', 'E', 'I', 'R', 'D_E', 'D_i', 'F']
    #                   )
    # chart_data = df
#####################################################################

#####################################################################

# # with open('chart_seirs_net.csv', newline ='') as csv_file:
# #     data = csv_file.read()
# #     matrix = []
# #     for row in csv.reader(data.splitlines()):
# #         # for item in row:
# #     # data = csv_file.readlines().split(',')
# #     # for i in
# #         matrix.append(row)
# #     # matrix = re.sub('\n', '', ''.join(matrix))
# #     # data = []
# #     # data_temp =  csv.reader(csv_file, delimiter=',')
# #     # for row in data_temp:
# #     #     # print(', '.join(row))
# #     #     data.append(row)
# # # data = data.split(',')
# # # data = pd.read_csv('chart_seirs_net.csv', sep=',')
# # mat = np.array(matrix)
# # mtx = mat.transpose()
# # # print('data: ', data)
# # print('matrix: ', mat)
# # # df = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_i', 'F'])
# # df = pd.DataFrame(mat,
# #                   columns=['S', 'E', 'I', 'R', 'D_E', 'D_i', 'F'],
# #                   # columns=['S']
# #                   # index=['S', 'E', 'I', 'R', 'D_E', 'D_i', 'F']
# #                   )
# # chart_data = df
#
# dic_list = []
# dic_list_S = []
# dic_list_E = []
# dic_list_I = []
# dic_list_R = []
# dic_list_DE = []
# dic_list_DI = []
# dic_list_F = []
#
# # ('..', 'images')    > Um níveil acima
# # ('../..', 'images') > Dois níveis acima
# IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                         '', 'images')
# # print('IMAG_DIR: ', IMAG_DIR)
#
#
# # with open(IMAG_DIR + '/chart_seirs_net.csv', newline ='') as csv_file:
# #     data = csv_file.read()
# #     for row in csv.reader(data.splitlines()):
# #         dic_seir = {}
# #         # print('row: ', row)
# #         dic_seir['S'] = row[0]
# #         dic_seir['E'] = row[1]
# #         dic_seir['I'] = row[2]
# #         dic_seir['R'] = row[3]
# #         dic_seir['D_E'] = row[4]
# #         dic_seir['D_I'] = row[5]
# #         dic_seir['F'] = row[6]
# #         dic_list_S.append(dic_seir['S'])
# #         dic_list_E.append(dic_seir['E'])
# #         dic_list_I.append(dic_seir['I'])
# #         dic_list_R.append(dic_seir['R'])
# #         dic_list_DE.append(dic_seir['D_E'])
# #         dic_list_DI.append(dic_seir['D_I'])
# #         dic_list_F.append(dic_seir['F'])
# #         dic_list.append(dic_seir)
# #     dic_seir['S'] = dic_list_S
# #     dic_seir['E'] = dic_list_E
# #     dic_seir['I'] = dic_list_I
# #     dic_seir['R'] = dic_list_R
# #     dic_seir['D_E'] = dic_list_DE
# #     dic_seir['D_I'] = dic_list_DI
# #     dic_seir['F'] = dic_list_F
# #
# # print('dic_seir: ', dic_seir)
#
# # print('dic_list_S: ', dic_list_S)
# # print('dic_list_E: ', dic_list_E)
# # print('dic_list_I: ', dic_list_I)
# # print('dic_list_R: ', dic_list_R)
# # print('dic_list_DE: ',dic_list_DE)
# # print('dic_list_DI: ', dic_list_DI)
# # print('dic_list_F: ', dic_list_F)
#     # data = csv_file.readlines().split(',')
#     # for i in
# #         matrix.append(row)
# #
# # mat = np.array(matrix)
# # mtx = mat.transpose()
# #     print('matrix: ', mat)
# # df = pd.DataFrame(mat,
# #                   columns=['S', 'E', 'I', 'R', 'D_E', 'D_i', 'F'],
# #
# #                   )
# # chart_data = df
#
# # print('chart_data: ', chart_data)
# # st.line_chart(chart_data)
# # last_rows1 = np.random.randn(1, 1)
# # last_rows = np.random.randn(2, 1)
# # chart = st.line_chart(df)
#
# # st.line_chart(dic_seir)
# # st.line_chart(dic_list_S)
# # st.line_chart(dic_list_E)
# # st.line_chart(dic_list_I)
# # st.line_chart(dic_list_R)
# # st.line_chart(dic_list_DE)
# # st.line_chart(dic_list_DI)
# # st.line_chart(dic_list_F)
