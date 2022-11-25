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

# Copyright 2018-2020 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
import sys  # Importa modulos do sistema
import os  # Local (path) do sistema
import pathlib  # Local do diretório (pasta)
import gzip
import json
import csv
from urllib import request
import urllib.error
from seir.utils.folders import cd
# from realtimert import run_rt
# from core import run_full_model, load_data, plot_rt
from matplotlib import pyplot as plt


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '', 'seir/utils/')
# IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'', 'images/')
#############################################################
# [Intro] Menagem de boas vindas
#############################################################
def atualizar_dados():
    # Acessos à internet ..................
    try:
        read_est_cases()        # Acesso URL...
        read_mun_cases()        # Acesso URL...
        # read_EST_data_by_day()  # Acesso URL...
        read_MUN_data_by_day()  # Acesso URL...
        # city_df, state_df = load_data()


    except urllib.error.URLError as e:
        st.error(
            """
            **Erro de acesso aos dados >> externos << disponíveis na internet.**
            Erro: %s
            """
            % e.reason
        )
        return

    # #############################################################
    # # [Estados e Municipios] Execução dos códigos abaixo...
    # #############################################################
    try:
        # states_pop_cases_deaths() # chana > make_est_cases()
        # mun_pop_cases_deaths() # chama > # make_mun_cases()    # chama > load_municipalities()
        # load_states()
        # list_dic_est = load_states()
        # mun_list_dic = load_municipalities()
        make_est_cases()
        make_mun_cases()
        get_EST_data()
        get_MUN_data()
        get_EST_data_by_day()
        get_MUN_data_by_day()
        casos_e_mortes_Brasil()
    except Exception as e:
        raise


def intro():
    st.sidebar.success("Selecione uma opção acima.")

    st.markdown(
        """
        **👈 Selecione uma opção à esquerda**: Diagnóstico
        ou Proposta de solução.

        ### NESCON (Medicina-UFMG) e DEP (Engenharia de Produção-UFMG).

        - [LabDec (Laboratório de apoio à Decisão)](https://labdec.nescon.medicina.ufmg.br/)
    """
)

    st.write(
             """
             O sistema permite: \n
             - O monitoramento **em tempo real** dos casos em estados ou municípios
             - Uma modelagem da transmissão e dos impactos de políticas de distanciamento e testes
             - Uma modelagem de previsão da (in)disponibilidade de leitos UTI e Gerais nos estados
             """
             )

    # if st.button('Atualizar'):
    #     with st.spinner('Atualizando os modelos com os dados oficiais mais recentes...'):
    #         atualizar_dados()
    #         run_rt()
    #     st.success('Ok!')


    # try:
    #     df = get_EST_data()
    #     city_df, state_df = load_data()
    #     # para a análise, vamos usar somente novos casos confirmados
    #     city_df = city_df['confirmed_new']
    #     state_df = state_df['confirmed_new']
    #
    # except Exception as e:
    #     st.error(
    #         """
    #         **Erro de acesso >> interno << aos dados dos estados.**
    #         Erro: %s
    #         """
    #         % e.reason
    #     )
    #     return
    #
    # st.markdown("## **Rt em tempo real por estado**")
    #
    # st.write("*\"Qualquer sugestão de reduzir as restrições quando Rt > 1.0 \
    #          é uma decisão explícita de permitir a proliferação do vírus*\". -- Kevin Systrom (2020)")
    #
    # estado = st.selectbox(
    #     # "Escolha o estado", list(df.index), ["MG"]
    #     "Escolha o estado", list(df.index), 0
    # )
    # if not estado:
    #     st.error("Selecione um estado.")
    #     return
    #
    # BRAZIL = {
    #  'Acre':'AC',
    #  'Alagoas':'AL',
    #  'Amapá':'AP',
    #  'Amazonas':'AM',
    #  'Bahia':'BA',
    #  'Ceará':'CE',
    #  'Distrito Federal':'DF',
    #  'Espírito Santo':'ES',
    #  'Goiás':'GO',
    #  'Maranhão':'MA',
    #  'Mato Grosso':'MT',
    #  'Mato Grosso do Sul':'MS',
    #  'Minas Gerais':'MG',
    #  'Pará':'PA',
    #  'Paraíba':'PB',
    #  'Paraná':'PR',
    #  'Pernambuco':'PE',
    #  'Piauí':'PI',
    #  'Rio de Janeiro':'RJ',
    #  'Rio Grande do Norte':'RN',
    #  'Rio Grande do Sul':'RS',
    #  'Rondônia':'RO',
    #  'Roraima':'RR',
    #  'Santa Catarina':'SC',
    #  'São Paulo':'SP',
    #  'Sergipe':'SE',
    #  'Tocantins':'TO',
    #  'Brasil':'Brazil',
    # }
    #
    # # for STATE_NAME in list(BRAZIL_STATES.keys()):
    #
    # STATE_NAME = BRAZIL[estado]
    #
    # series = state_df.loc[lambda x: x.index.get_level_values(0) == STATE_NAME]
    #
    # result = run_full_model(series, sigma=0.01)
    #
    # fig, ax = plt.subplots(figsize=(800/72,450/72), dpi=90)
    #
    # plot_rt(result, ax, STATE_NAME)
    # fig.set_facecolor('w')
    # # ax.set_title(f'Real-time $R_t$ for {STATE_NAME}')
    # ax.set_title(f'$R_t$ em tempo real para {STATE_NAME}')
    # rt_state = 'Rt-' + STATE_NAME
    # fig.savefig('./images/' + rt_state)
    # print(f'Gerando Rt de {STATE_NAME}...')
    # plt.close()
    #
    # # print('result: ', result)
    # st.dataframe(result, width=5000)
    #
    # # ESTADO = [ i for i in list(BRAZIL_STATES.keys())]
    # # print('ESTADO: ', ESTADO)
    # # SIGLA = ESTADO[0]
    # image_por_estado = './images/' + 'Rt-' + BRAZIL[estado] + '.png'
    # if image_por_estado == './images/' + 'Rt-[].png':
    #     image_por_estado = './images/Rt-Brazil.png'
    # else:
    #     image_por_estado = './images/' + 'Rt-' + BRAZIL[estado] + '.png'
    #
    # st.image(image_por_estado, caption='Rt do estado: ' + estado,
    #       use_column_width=True)
    #
    # st.write('---')
    # image_rt_estados = './images/' + 'Rt-dos-estados.png'
    # st.image(image_rt_estados, caption='Rt dos estados',
    #       use_column_width=True)
    #
    # st.write('---')
    # image_rt_comparisson = './images/' + 'Rt-state-comparison.png'
    # st.image(image_rt_comparisson, caption='Rt comparativo dos estados',
    # use_column_width=True)
    #
    # st.markdown("Fonte: [[+](https://github.com/loft-br/realtime_r0_brazil)]\
    #             [[+](http://systrom.com/blog/the-metric-we-need-to-manage-covid-19/)]\
    #             [[+](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0002185)]")



#############################################################
# [Estados] Lê url e armazena casos por estado
#############################################################
# @st.cache
def read_est_cases():
    #######################################################################
    URL = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv"
    #######################################################################

    with request.urlopen(URL) as entrada:
        print('Baixando os dados covid-19 dos estados em csv...')

        file = pd.read_csv(URL, encoding='utf-8', error_bad_lines=False)
        # print('file: ', file)
        with cd(DATA_DIR):
            file.to_csv("cases-brazil-total.csv")
        print('Download completo!')

        # # dados = entrada.read().decode('latin1')
        # dados = entrada.read().decode('utf-8')
        #
        # # for estado in csv.reader(dados.splitlines()):
        # #     # country,state,totalCases,totalCasesMS,notConfirmedByMS,deaths,URL
        # #     print('{0:s}: {1:s} {2:s}'.format(estado[1], estado[2], estado[5]))
        #
        # ##############################################################
        # # Cabeçalhos
        # # # country,state,totalCases,totalCasesMS,notConfirmedByMS,deaths,URL
        # # Cabeçalhos: state, população, totalCases, deaths
        # ##############################################################
        # # with open(DATA_DIR + '/est_casos.csv', 'w') as saida:
        # # with cd(pathlib.Path(__file__).parent.absolute()):
        # with cd(DATA_DIR):
        #     with open('est_casos.csv', 'w') as saida:
        #         for estado in csv.reader(dados.splitlines()):
        #             # pessoa = registro.strip().split(',')
        #             print('{0:s},{1:s},{2:s}'.format(estado[1],
        #                                            estado[2],
        #                                            estado[5]), file = saida)
        #
        # # if saida.closed:
        # #     print('Arquivo de saída: fechado.')
        #
        # ##############################################################
        # # Dicionários dos estados (json)
        # ##############################################################
        # # os.chdir(DATA_DIR)
        # # os.chdir('..')
        # # with cd(DATA_DIR):
        # list_dic_est = load_states()
        #
        # ##############################################################
        # # Le a população dos estados
        # # Cabeçalhos: estado, população, casos, mortes
        # ##############################################################
        # lis_est = []
        # # with open(DATA_DIR + '/est_casos.csv', newline='') as file:
        # # with cd(pathlib.Path(__file__).parent.absolute()):
        # with cd(DATA_DIR):
        #     with open('est_casos.csv', newline='') as file:
        #         csv_reader = csv.reader(file, delimiter=',')
        #         next(csv_reader)
        #         next(csv_reader) # Dados 'TOTAL' > 'Brasil Escala Nacional'
        #         for estado in csv_reader:
        #             for dic_estado in list_dic_est:
        #                 dic_est = {}
        #                 if  estado[0] == dic_estado["sigla"]:
        #                     dic_est["nome"] = dic_estado["nome"]
        #                     dic_est["pop"]  = dic_estado["populacao"]
        #                     dic_est["casos"] = int(estado[1])
        #                     dic_est["mortes"] = int(estado[2])
        #                     dic_est["lon"] = dic_estado["longitude"]
        #                     dic_est["lat"] = dic_estado["latitude"]
        #                     lis_est.append(dic_est)
        #             # if  estado[0] == 'TOTAL':
        #             #     dic_est["nome"] = 'Brasil Escala Nacional'
        #             #     dic_est["pop"]  = 210147125
        #             #     dic_est["casos"] = int(estado[1])
        #             #     dic_est["mortes"] = int(estado[2])
        #             #     dic_est["lon"] = -47.86
        #             #     dic_est["lat"] = -15.83
        #             #     lis_est.append(dic_est)
        #
        #
        # # with open(DATA_DIR + '/est_casos.json', 'w', encoding='utf8') as outfile:
        # # with cd(pathlib.Path(__file__).parent.absolute()):
        # with cd(DATA_DIR):
        #     with open('est_casos.json', 'w', encoding='utf8') as outfile:
        #         json.dump(lis_est, outfile, ensure_ascii=False)


#############################################################
# [Estados] Gera lista de casos dos estados
#############################################################
# @st.cache
def load_states():
    # Carrega a lista de municípios do Brasil
    # with cd(pathlib.Path(__file__).parent.absolute()):
    with cd(DATA_DIR):
        with open('estados.json', 'r', encoding='utf-8-sig') as est:
            list_dic_est = json.load(est)
        return list_dic_est

# list_dic_est = load_states()


# Gera arquivo est_casos.csv e est_casos.json
def make_est_cases(est_ld=load_states()):

    ##############################################################
    # Cabeçalhos
    # # country,state,totalCases,totalCasesMS,notConfirmedByMS,deaths,URL
    # Cabeçalhos: state, população, totalCases, deaths
    ##############################################################
    # with open(DATA_DIR + '/est_casos.csv', 'w') as saida:
    # with cd(pathlib.Path(__file__).parent.absolute()):
    # with cd(DATA_DIR):
    #     # dados = []
    #     with open ('cases-brazil-total.csv', 'r') as f:
    #         dados = csv.reader(f)
    #     with open('est_casos.csv', 'w') as saida:
    #         for estado in csv.reader(dados.splitlines()):
    #             # pessoa = registro.strip().split(',')
    #             print('{0:s},{1:s},{2:s}'.format(estado[1],
    #                                            estado[2],
    #                                            estado[5]), file = saida)
    with cd(DATA_DIR):
        # dados=[]
        with open('cases-brazil-total.csv', 'r', encoding="utf8") as f:
            with open('est_casos.csv', 'w') as saida:
                for line in f:
                    estado = line.strip().split(',')
                    # dados.append(estado)
                    print('{0:s},{1:s},{2:s}'.format(estado[2],
                                                   estado[3],
                                                   estado[6]),
                          file = saida)

    # if saida.closed:
    #     print('Arquivo de saída: fechado.')

    ##############################################################
    # Dicionários dos estados (json)
    ##############################################################
    # os.chdir(DATA_DIR)
    # os.chdir('..')
    # with cd(DATA_DIR):
    # list_dic_est = load_states()
    list_dic_est=est_ld

    ##############################################################
    # Le a população dos estados
    # Cabeçalhos: estado, população, casos, mortes
    ##############################################################
    lis_est = []
    # with open(DATA_DIR + '/est_casos.csv', newline='') as file:
    # with cd(pathlib.Path(__file__).parent.absolute()):
    with cd(DATA_DIR):
        with open('est_casos.csv', newline='') as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            next(csv_reader)
            # tot_casos_mortes = next(csv_reader) # Dados 'TOTAL' > 'Brasil Escala Nacional'
            # dic_tt = {}
            # dic_tt["casos_t"] = tot_casos_mortes[1]
            # dic_tt["mortes_t"] = tot_casos_mortes[2]
            for estado in csv_reader:
                for dic_estado in list_dic_est:
                    dic_est = {}
                    if estado[0] == dic_estado["sigla"]:
                        dic_est["nome"] = dic_estado["nome"]
                        dic_est["pop"] = dic_estado["populacao"]
                        dic_est["casos"] = int(estado[1])
                        dic_est["mortes"] = int(estado[2])
                        # dic_est["casospp"] = int(float(int(estado[1])/int(dic_tt["casos_t"]))*10000)
                        # dic_est["mortespp"] = int(float(int(estado[2])/int(dic_tt["mortes_t"]))*10000)
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
    # with cd(pathlib.Path(__file__).parent.absolute()):
    with cd(DATA_DIR):
        with open('est_casos.json', 'w', encoding='utf8') as outfile:
            json.dump(lis_est, outfile, ensure_ascii=False)

#############################################################
# [Municípios] Lê url e armazena casos por município
#############################################################
# @st.cache
def read_mun_cases():

    #######################################################################
    URL = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv"
    #######################################################################

    with request.urlopen(URL) as entrada:
        print('Baixando os dados covid-19 dos municípios em csv...')

        file = pd.read_csv(URL, encoding='utf-8')
        # print('file: ', file)
        with cd(DATA_DIR):
            file.to_csv("cases-brazil-cities.csv")
        print('Download completo!')

        # # dados = entrada.read().decode('latin1')
        # dados = entrada.read().decode('utf-8')
        # # print('Download completo!')
        #
        # # for cidade in csv.reader(dados.splitlines()):
        # #     # country,state,city,ibgeID,deaths,totalCases
        # #     print('{0:30s}: {1:30s}'.format(cidade[2], cidade[5]))
        #
        # ##############################################################
        # # Cabeçalhos
        # # country,state,city,ibgeID,deaths,totalCases
        # ##############################################################
        # # with open(DATA_DIR + '/mun_casos.csv', 'w') as saida:
        # # with cd(pathlib.Path(__file__).parent.absolute()):
        # with cd(DATA_DIR):
        #     with open('mun_casos.csv', 'w') as saida:
        #         for cidade in csv.reader(dados.splitlines()):
        #             # pessoa = registro.strip().split(',')
        #             print('{0:s},{1:s},{2:s},{3:s}'.format(cidade[3],
        #                                            cidade[2],
        #                                            cidade[5],
        #                                            cidade[4]), file = saida)
        #
        # # if saida.closed:
        # #     print('Arquivo de saída: fechado.')
        #
        # ##############################################################
        # # Le a população dos municipios
        # # Cabeçalhos: "cod_mun";"pop_tcu";"pop_ans";"pop_sus"
        # ##############################################################
        # dic_mun_pop = {}
        # # with open(DATA_DIR + '/pop_sus_mun.csv', newline='') as file:
        # # with cd(pathlib.Path(__file__).parent.absolute()):
        # with cd(DATA_DIR):
        #     with open('pop_sus_mun.csv', newline='') as file:
        #         csv_reader = csv.reader(file, delimiter=';')
        #         next(csv_reader)
        #         for cidade in csv_reader:
        #             dic_mun_pop[cidade[0]] = int(cidade[1])
        #
        # # print('dic_mun_pop: ', dic_mun_pop)
        #
        # ##############################################################
        # # Dicionários dos municipios (json)
        # ##############################################################
        # # os.chdir(DATA_DIR)
        # # os.chdir('..')
        # # with cd(DATA_DIR):
        # dic_mun_list = load_municipalities()
        #
        #
        # lis_mun = []
        # # with open(DATA_DIR + '/mun_casos.csv', newline='') as file:
        # # with cd(pathlib.Path(__file__).parent.absolute()):
        # with cd(DATA_DIR):
        #     with open('mun_casos.csv', newline='') as file:
        #         csv_reader = csv.reader(file, delimiter=',')
        #         next(csv_reader)
        #         for cidade in csv_reader:
        #             for dic_munic in dic_mun_list:
        #                 dic_mun = {}
        #                 if int(cidade[0]) == dic_munic["codigo_ibge"]:
        #                 # if int(dic_mun[cidade[0]]) == int(str(dic_munic["codigo_ibge"])[:-1]):
        #                     dic_mun["nome"] = dic_munic["nome"]
        #                     dic_mun["cod_ibge"] = dic_munic["codigo_ibge"]
        #                     dic_mun["pop"] = dic_mun_pop[str(dic_munic["codigo_ibge"])[:-1]]
        #                     dic_mun["casos"] = int(cidade[2])
        #                     dic_mun["mortes"] = int(cidade[3])
        #                     dic_mun["lon"] = dic_munic["longitude"]
        #                     dic_mun["lat"] = dic_munic["latitude"]
        #                     lis_mun.append(dic_mun)
        #
        #
        # # with open(DATA_DIR + '/mun_casos.json', 'w', encoding='utf8') as outfile:
        # # with cd(pathlib.Path(__file__).parent.absolute()):
        # with cd(DATA_DIR):
        #     with open('mun_casos.json', 'w', encoding='utf8') as outfile:
        #         json.dump(lis_mun, outfile, ensure_ascii=False)

#############################################################
# [Municipios] Retorna lista de dict dos mun. BR.
#############################################################
# @st.cache
def load_municipalities():
    # Carrega a lista de municípios do Brasil
    # with cd(pathlib.Path(__file__).parent.absolute()):
    with cd(DATA_DIR):
        with open('municipios.json', 'r', encoding='utf-8-sig') as m:
            mun_list_dic = json.load(m)
        return mun_list_dic

# mun_list_dic = load_municipalities()

# Gera arquivo mun_casos.csv e mun_casos.json
def make_mun_cases(mun_ld=load_municipalities()):

    ##############################################################
    # Cabeçalhos
    # country,state,city,ibgeID,deaths,totalCases
    ##############################################################
    # with open(DATA_DIR + '/mun_casos.csv', 'w') as saida:
    # with cd(pathlib.Path(__file__).parent.absolute()):
    # with cd(DATA_DIR):
    #     with open('mun_casos.csv', 'w') as saida:
    #         for cidade in csv.reader(dados.splitlines()):
    #             # pessoa = registro.strip().split(',')
    #             print('{0:s},{1:s},{2:s},{3:s}'.format(cidade[3],
    #                                            cidade[2],
    #                                            cidade[5],
    #                                            cidade[4]), file = saida)
    with cd(DATA_DIR):
        # dados=[]
        with open ('cases-brazil-cities.csv', 'r', encoding="utf8") as f:
            with open('mun_casos.csv', 'w') as saida:
                for line in f:
                    cidade = line.strip().split(',')
                    # dados.append(cidade)
                    print('{0:s},{1:s},{2:s},{3:s}'.format(cidade[4],
                                                   cidade[3],
                                                   cidade[8],
                                                   cidade[7]), file = saida)

    # if saida.closed:
    #     print('Arquivo de saída: fechado.')

    ##############################################################
    # Le a população dos municipios
    # Cabeçalhos: "cod_mun";"pop_tcu";"pop_ans";"pop_sus"
    ##############################################################
    dic_mun_pop = {}
    # with open(DATA_DIR + '/pop_sus_mun.csv', newline='') as file:
    # with cd(pathlib.Path(__file__).parent.absolute()):
    with cd(DATA_DIR):
        with open('pop_sus_mun.csv', newline='') as file:
            csv_reader = csv.reader(file, delimiter=';')
            next(csv_reader)
            for cidade in csv_reader:
                dic_mun_pop[cidade[0]] = int(cidade[1])

    # print('dic_mun_pop: ', dic_mun_pop)

    ##############################################################
    # Dicionários dos municipios (json)
    ##############################################################
    # os.chdir(DATA_DIR)
    # os.chdir('..')
    # with cd(DATA_DIR):
    # dic_mun_list = load_municipalities()
    dic_mun_list=mun_ld


    lis_mun = []
    # with open(DATA_DIR + '/mun_casos.csv', newline='') as file:
    # with cd(pathlib.Path(__file__).parent.absolute()):
    with cd(DATA_DIR):
        with open('mun_casos.csv', newline='') as file:
            # csv_reader = csv.reader(file, delimiter=',')
            # csv_reader = csv.reader(file, quotechar='"',
            #                         delimiter=',',
            #                         quoting=csv.QUOTE_ALL,
            #                         skipinitialspace=True)

            # csv_reader = csv.reader(file,
            #                         quotechar='"',
            #                         # doublequote=True,
            #                         quoting=csv.QUOTE_ALL,
            #                         delimiter=',',
            #                         # escapechar='\\',
            #                         skipinitialspace=True)


            csv_reader = csv.reader(file,
            quotechar='"',
            delimiter=',')

            next(csv_reader)
            for cidade in csv_reader:
                for dic_munic in dic_mun_list:
                    try:
                        dic_mun = {}
                        if int(cidade[0]) == dic_munic["codigo_ibge"]:
                        # if int(dic_mun[cidade[0]]) == int(str(dic_munic["codigo_ibge"])[:-1]):
                            dic_mun["nome"] = dic_munic["nome"]
                            dic_mun["cod_ibge"] = dic_munic["codigo_ibge"]
                            dic_mun["pop"] = dic_mun_pop[str(dic_munic["codigo_ibge"])[:-1]]
                            dic_mun["casos"] = int(cidade[2])
                            dic_mun["mortes"] = int(cidade[3])
                            dic_mun["lon"] = dic_munic["longitude"]
                            dic_mun["lat"] = dic_munic["latitude"]
                            lis_mun.append(dic_mun)
                    except ValueError:
                        # Ignorando um registro CSV da internet
                        print("...")
                        continue


    # with open(DATA_DIR + '/mun_casos.json', 'w', encoding='utf8') as outfile:
    # with cd(pathlib.Path(__file__).parent.absolute()):
    with cd(DATA_DIR):
        with open('mun_casos.json', 'w', encoding='utf8') as outfile:
            json.dump(lis_mun, outfile, ensure_ascii=False)

#############################################################
# [Estados ou Municípios] Lê est_casos.json ou mun_casos.json
#############################################################
# Leitura de dados de arquivos locais (json)
def from_data_file(filename):
    fn = ("./seir/utils/" + filename)
    # url = ("https://.../%s" % filename)
    # return pd.read_json(url)
    return pd.read_json(fn, encoding='utf-8')

# Para texto de casos e mortes no Brasil
def casos_e_mortes_Brasil(imprime=False):
    br = pd.DataFrame(data=from_data_file("est_casos.json"))
    tot_casos  = br['casos'].sum()
    tot_mortes = br['mortes'].sum()
    # print('br: ', br)
    # print('tot_casos: ', tot_casos)
    # print('tot_mortes: ', tot_mortes)

    if imprime:
        st.write(
        '> O Brasil possui **',tot_casos,'** casos\
         e **', tot_mortes,'** mortes por COVID-19 \
         registrados até o momento.'
        )

# Retorna o nome do estado
# @st.cache
def get_EST_data():
    # df = pd.read_csv(".seir/utils/est_casos.csv")
    # df = pd.read_json(r'./seir/utils/est_casos.json')
    df = from_data_file('est_casos.json')
    # print('df-Estado: ', df)
    return df.set_index("nome")

# Retorna o nome do municipio
# @st.cache
def get_MUN_data():
    # df = pd.read_csv(".seir/utils/mun_casos.csv")
    # df = pd.read_json(r'./seir/utils/mun_casos.json')
    df = from_data_file('mun_casos.json')
    # print('df-Municipio: ', df)
    return df.set_index("nome")

# #############################################################
# # [Estados] Lê url e retorna casos por estado por dia
# #############################################################
# # @st.cache
# def read_EST_data_by_day():
#
#     print('Baixando os dados diários do covid-19 dos estados em csv...')
#     #######################################################################
#     # URL = "https://raw.githubusercontent.com/wcota/covid19br/master/"
#     URL = "https://github.com/wcota/covid19br/blob/master/"
#     file = pd.read_csv(URL + "cases-brazil-cities-time.csv.gz", compression = 'gzip', encoding = 'utf-8')
#
#     # file=pd.read_csv(URL + "cases-brazil-cities-time.csv")
#     # print('file: ', file)
#     with cd(DATA_DIR):
#         file.to_csv("cases-brazil-cities-time.csv")
#     print('Download completo!')
#
#     # df_est = df.copy()
#     # #######################################################################
#     #
#     # #####################################################################
#     # # Casos dos estados no tempo
#     # #####################################################################
#     #
#     # df_est.drop(columns=['country', 'city', 'ibgeID','newDeaths',
#     #                  'deaths', 'newCases'], axis=1, inplace=True)
#     #
#     # index_names = df_est[(df_est['state'] == 'TOTAL')].index
#     # df_est.drop(index_names, inplace=True)
#     #
#     # # index_names = df_est[(df_est['city'].str.contains('INDEFINIDA'))].index
#     # # df_est.drop(index_names, inplace=True)
#     # df_est.reset_index(drop=True, inplace=True)
#     # df_est.rename(columns={"state": "Estados"}, inplace=True)
#     #
#     # # https://pandas.pydata.org/docs/user_guide/reshaping.html
#     # Estados = df_est.pivot_table(index='Estados', columns='date',
#     #                       values='totalCases', aggfunc='sum').fillna(0)
#     #
#     # Estados = Estados.T.reset_index(drop=True).T
#     # # print('df_est2: ', df_est2)
#     #
#     # # print('Estados: ', Estados)
#     # Estados.to_csv('./data/est_casos_t.csv', sep=',', encoding='utf-8')
#     #
#     # df = pd.read_csv("./data/est_casos_t.csv")
#     # return df.set_index("Estados")

def get_EST_data_by_day():

    #########################################################################
    with cd(DATA_DIR):
        # df = pd.read_csv("cases-brazil-cities-time.csv.gz", compression='gzip')
        #df = pd.read_csv("cases-brazil-cities-time.csv")
        df = pd.read_csv("cases-brazil-cities.csv")
        df_est = df.copy()

        #####################################################################
        # Casos dos estados no tempo
        #####################################################################

        df_est.drop(columns=['country', 'city', 'ibgeID','newDeaths',
                         'deaths', 'newCases'], axis=1, inplace=True)

        index_names = df_est[(df_est['state'] == 'TOTAL')].index
        df_est.drop(index_names, inplace=True)

        # index_names = df_est[(df_est['city'].str.contains('INDEFINIDA'))].index
        # df_est.drop(index_names, inplace=True)
        df_est.reset_index(drop=True, inplace=True)
        df_est.rename(columns={"state": "Estados"}, inplace=True)

        # https://pandas.pydata.org/docs/user_guide/reshaping.html
        Estados = df_est.pivot_table(index='Estados', columns='date',
                              values='totalCases', aggfunc='sum').fillna(0)

        Estados = Estados.T.reset_index(drop=True).T
        # print('df_est2: ', df_est2)

    # print('Estados: ', Estados)
    Estados.to_csv('./data/est_casos_t.csv', sep=',', encoding='utf-8')

    df = pd.read_csv("./data/est_casos_t.csv")

    return df.set_index("Estados")

#############################################################
# [Municípios] Lê url e retorna casos por estado por dia
#############################################################
# @st.cache
def read_MUN_data_by_day():
    #######################################################################
    print('Baixando os dados diários do covid-19 dos municípios em csv...')

    # URL = "https://raw.githubusercontent.com/wcota/covid19br/master/"
    # df = pd.read_csv(URL + "cases-brazil-cities-time.csv", encoding='utf-8')

    URL = "https://github.com/wcota/covid19br/raw/master/"
    file = pd.read_csv(URL + "cases-brazil-cities-time.csv.gz",
                       compression='gzip', encoding='utf-8')

    # file = pd.read_csv(URL + "cases-brazil-cities-time.csv")
    # print('file: ', file)
    with cd(DATA_DIR):
        file.to_csv("cases-brazil-cities-time.csv")
    print('Download completo!')

    # df_mun = df.copy()
    # #######################################################################
    #
    # #####################################################################
    # # Casos dos municípios no tempo
    # #####################################################################
    # df_mun.drop(columns=['country', 'state', 'ibgeID','newDeaths',
    #                  'deaths', 'newCases'], axis=1, inplace=True)
    #
    # index_names = df_mun[(df_mun['city'] == 'TOTAL')].index
    # df_mun.drop(index_names, inplace=True)
    #
    # index_names = df_mun[(df_mun['city'].str.contains('INDEFINIDA'))].index
    # df_mun.drop(index_names, inplace=True)
    #
    # df_mun.reset_index(drop=True, inplace=True)
    # # df_mun.drop(columns=['date'], axis=1, inplace=True)
    # df_mun.rename(columns={"city": "Municipios"}, inplace=True)
    # df_mun.reset_index(inplace=True)
    # # print('df_mun: ', df_mun)
    #
    # # https://pandas.pydata.org/docs/user_guide/reshaping.html
    # Municipios = df_mun.pivot(index='Municipios', columns='date',
    #                       values='totalCases').fillna(0)
    #
    # Municipios = Municipios.T.reset_index(drop=True).T
    #
    # # print('Municipios: ', Municipios)
    # Municipios.to_csv('./data/mun_casos_t.csv', sep=',', encoding='utf-8')
    # #######################################################################
    # df = pd.read_csv("./data/mun_casos_t.csv")
    # return df.set_index("Municipios")


def get_MUN_data_by_day():

    #######################################################################
    with cd(DATA_DIR):
        df = pd.read_csv("cases-brazil-cities-time.csv")
        # df = pd.read_csv("cases-brazil-cities-time.csv.gz", compression='gzip')
        # df.to_csv("cases-brazil-cities-time.csv")
        df_mun = df.copy()

        #####################################################################
        # Casos dos municípios no tempo
        #####################################################################
        df_mun.drop(columns=['country', 'state', 'ibgeID','newDeaths',
                         'deaths', 'newCases'], axis=1, inplace=True)

        index_names = df_mun[(df_mun['city'] == 'TOTAL')].index
        df_mun.drop(index_names, inplace=True)

        index_names = df_mun[(df_mun['city'].str.contains('INDEFINIDA'))].index
        df_mun.drop(index_names, inplace=True)

        df_mun.reset_index(drop=True, inplace=True)
        # df_mun.drop(columns=['date'], axis=1, inplace=True)
        df_mun.rename(columns={"city": "Municipios"}, inplace=True)
        df_mun.reset_index(inplace=True)
        # print('df_mun: ', df_mun)

        # https://pandas.pydata.org/docs/user_guide/reshaping.html
        Municipios = df_mun.pivot(index='Municipios', columns='date',
                              values='totalCases').fillna(0)

        Municipios = Municipios.T.reset_index(drop=True).T

    # print('Municipios: ', Municipios)
    Municipios.to_csv('./data/mun_casos_t.csv', sep=',', encoding='utf-8')

    df = pd.read_csv("./data/mun_casos_t.csv")

    return df.set_index("Municipios")


#############################################################
# [Estados] Gera lista de pop, casos e mortes dos estados
#############################################################
def states_pop_cases_deaths(state_name):
    # Estado: [população, casos, mortes]

    # read_est_cases()
    # make_est_cases() # Já foi realizado no início

    # Carrega a lista de casos nos estados do Brasil
    # os.chdir(DATA_DIR)
    # with cd(pathlib.Path(__file__).parent.absolute()):
    with cd(DATA_DIR):
        with open('est_casos.json', 'r', encoding='utf-8-sig') as m:
            dic_state_cases = json.load(m)

    dic_est_pop_cases_deaths = {}
    for dic_est in dic_state_cases:
        if dic_est["nome"] == state_name:
            dic_est_pop_cases_deaths[state_name] = \
            [dic_est["pop"], dic_est["casos"], dic_est["mortes"]]
    # print("dic_est_pop_cases_deaths: ", dic_est_pop_cases_deaths)
    return dic_est_pop_cases_deaths.get(state_name, '** Estado inválido **')


#############################################################
# [Municipios] Gera lista de casos dos municipios
#############################################################
def mun_pop_cases_deaths(mun_name):
    # Carrega a lista de casos nos municípios do Brasil

    # read_mun_cases()
    # make_mun_cases()  # Já foi realizado no início

    # os.chdir(DATA_DIR)
    # with cd(pathlib.Path(__file__).parent.absolute()):
    with cd(DATA_DIR):
        with open('mun_casos.json', 'r', encoding='utf-8-sig') as m:
            dic_mun_cases = json.load(m)

    dic_mun_pop_cases_deaths = {}
    for dic_mun in dic_mun_cases:
        if dic_mun["nome"] == mun_name:
            dic_mun_pop_cases_deaths[mun_name] = \
            [dic_mun["pop"], dic_mun["casos"], dic_mun["mortes"]]
    # print("dic_mun_pop_cases_deaths: ", dic_mun_pop_cases_deaths)
    return dic_mun_pop_cases_deaths.get(mun_name, '** Município inválido **')


# ############################################################################
# # Códigos demo de backup
# ############################################################################
# # Turn off black formatting for this function to present the user with more
# # compact code.
# # fmt: off
# def mapping_demo():
#     import pandas as pd
#     import pydeck as pdk
#
#     @st.cache
#     def from_data_file(filename):
#         url = (
#             "https://raw.githubusercontent.com/streamlit/"
#             "example-data/master/hello/v1/%s" % filename)
#         return pd.read_json(url)
#
#     try:
#         ALL_LAYERS = {
#             "Bike Rentals": pdk.Layer(
#                 "HexagonLayer",
#                 data=from_data_file("bike_rental_stats.json"),
#                 get_position=["lon", "lat"],
#                 radius=200,
#                 elevation_scale=4,
#                 elevation_range=[0, 1000],
#                 extruded=True,
#             ),
#             "Bart Stop Exits": pdk.Layer(
#                 "ScatterplotLayer",
#                 data=from_data_file("bart_stop_stats.json"),
#                 get_position=["lon", "lat"],
#                 get_color=[200, 30, 0, 160],
#                 get_radius="[exits]",
#                 radius_scale=0.05,
#             ),
#             "Bart Stop Names": pdk.Layer(
#                 "TextLayer",
#                 data=from_data_file("bart_stop_stats.json"),
#                 get_position=["lon", "lat"],
#                 get_text="name",
#                 get_color=[0, 0, 0, 200],
#                 get_size=15,
#                 get_alignment_baseline="bottom",
#             ),
#             "Outbound Flow": pdk.Layer(
#                 "ArcLayer",
#                 data=from_data_file("bart_path_stats.json"),
#                 get_source_position=["lon", "lat"],
#                 get_target_position=["lon2", "lat2"],
#                 get_source_color=[200, 30, 0, 160],
#                 get_target_color=[200, 30, 0, 160],
#                 auto_highlight=True,
#                 width_scale=0.0001,
#                 get_width="outbound",
#                 width_min_pixels=3,
#                 width_max_pixels=30,
#             ),
#         }
#     except urllib.error.URLError as e:
#         st.error("""
#             **This demo requires internet access.**
#
#             Connection error: %s
#         """ % e.reason)
#         return
#
#     st.sidebar.markdown('### Map Layers')
#     selected_layers = [
#         layer for layer_name, layer in ALL_LAYERS.items()
#         if st.sidebar.checkbox(layer_name, True)]
#     if selected_layers:
#         st.pydeck_chart(pdk.Deck(
#             map_style="mapbox://styles/mapbox/light-v9",
#             initial_view_state={"latitude": 37.76, "longitude": -122.4, "zoom": 11, "pitch": 50},
#             layers=selected_layers,
#         ))
#     else:
#         st.error("Please choose at least one layer above.")
# # fmt: on
#
# # Turn off black formatting for this function to present the user with more
# # compact code.
# # fmt: off
# def fractal_demo():
#     import numpy as np
#
#     # Interactive Streamlit elements, like these sliders, return their value.
#     # This gives you an extremely simple interaction model.
#     iterations = st.sidebar.slider("Level of detail", 2, 20, 10, 1)
#     separation = st.sidebar.slider("Separation", 0.7, 2.0, 0.7885)
#
#     # Non-interactive elements return a placeholder to their location
#     # in the app. Here we're storing progress_bar to update it later.
#     progress_bar = st.sidebar.progress(0)
#
#     # These two elements will be filled in later, so we create a placeholder
#     # for them using st.empty()
#     frame_text = st.sidebar.empty()
#     image = st.empty()
#
#     m, n, s = 960, 640, 400
#     x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
#     y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))
#
#     for frame_num, a in enumerate(np.linspace(0.0, 4 * np.pi, 100)):
#         # Here were setting value for these two elements.
#         progress_bar.progress(frame_num)
#         frame_text.text("Frame %i/100" % (frame_num + 1))
#
#         # Performing some fractal wizardry.
#         c = separation * np.exp(1j * a)
#         Z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
#         C = np.full((n, m), c)
#         M = np.full((n, m), True, dtype=bool)
#         N = np.zeros((n, m))
#
#         for i in range(iterations):
#             Z[M] = Z[M] * Z[M] + C[M]
#             M[np.abs(Z) > 2] = False
#             N[M] = i
#
#         # Update the image placeholder by calling the image() function on it.
#         image.image(1.0 - (N / N.max()), use_column_width=True)
#
#     # We clear elements by calling empty on them.
#     progress_bar.empty()
#     frame_text.empty()
#
#     # Streamlit widgets automatically run the script from top to bottom. Since
#     # this button is not connected to any other logic, it just causes a plain
#     # rerun.
#     st.button("Re-run")
#
#
# # fmt: on
#
# # Turn off black formatting for this function to present the user with more
# # compact code.
# # fmt: off
# def plotting_demo():
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
#
# # fmt: on
#
# # Turn off black formatting for this function to present the user with more
# # compact code.
# # fmt: off
# def data_frame_demo():
#     import sys
#     import pandas as pd
#     import altair as alt
#
#     if sys.version_info[0] < 3:
#         reload(sys) # noqa: F821 pylint:disable=undefined-variable
#         sys.setdefaultencoding("utf-8")
#
#     @st.cache
#     def get_UN_data():
#         AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
#         df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
#         return df.set_index("Region")
#
#     try:
#         df = get_UN_data()
#     except urllib.error.URLError as e:
#         st.error(
#             """
#             **This demo requires internet access.**
#
#             Connection error: %s
#         """
#             % e.reason
#         )
#         return
#
#     countries = st.multiselect(
#         "Choose countries", list(df.index), ["China", "United States of America"]
#     )
#     if not countries:
#         st.error("Please select at least one country.")
#         return
#
#     data = df.loc[countries]
#     data /= 1000000.0
#     st.write("### Gross Agricultural Production ($B)", data.sort_index())
#
#     data = data.T.reset_index()
#     data = pd.melt(data, id_vars=["index"]).rename(
#         columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
#     )
#     chart = (
#         alt.Chart(data)
#         .mark_area(opacity=0.3)
#         .encode(
#             x="year:T",
#             y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
#             color="Region:N",
#         )
#     )
#     st.altair_chart(chart, use_container_width=True)
#
#
# # fmt: on
# ############################################################################
