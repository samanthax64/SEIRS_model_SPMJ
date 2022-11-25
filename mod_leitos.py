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

######################################################################
import streamlit as st
import os # Local (path) do sistema
import sys # Importa modulos do sistema
import pathlib  # Local do diretório (pasta)
import time
import numpy as np
import pandas as pd
import csv
from math import *
import urllib.error
from bokeh.plotting import figure
# from bokeh.plotting import figure, Tabs, Panel
# import altair as alt
# import plotly.figure_factory as ff

# sys.path.insert(1, './seir/')
# from seir import config

# from seir.utils.states_info import states_name
from seir.utils.states_info import states_sigla
# from seir.utils.states_info import states_pop_cases_deaths
from intro import states_pop_cases_deaths
from intro import get_EST_data
from intro import get_EST_data_by_day

from seir.utils.states_info import states_leitos_UTI
from seir.utils.states_info import states_leitos_Gerais
from seir.utils.states_info import taxa_internacao_hospitalar

from leitos import modelo_infeccao
from leitos import modelo_admissao
# from leitos import leitos_disp_por_dia

IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'', 'images')
#############################################################
# Estados
#############################################################
# @st.cache
# def get_EST_data():
#     # df = pd.read_csv(".seir/utils/est_casos.csv")
#     df = pd.read_json(r'./seir/utils/estados.json')
#     # print('df-Estado: ', df)
#     return df.set_index("nome")

# #############################################################
# # Municípios
# #############################################################
# @st.cache
# def get_MUN_data():
#     # df = pd.read_csv(".seir/utils/mun_casos.csv")
#     df = pd.read_json(r'./seir/utils/municipios.json')
#     # print('df-Municipio: ', df)
#     return df.set_index("nome")
# ########################################################################


########################################################################
# Modelo de Leitos por Estado #
########################################################################
def plotting_leitos_estado():

    # with st.spinner('Atualizando os dados...'):
    try:
        df = get_EST_data()

    except urllib.error.URLError as e:
        st.error(
            """
            **Erro de acesso aos dados dos estados.**
            Erro: %s
            """
            % e.reason
        )
        return

    estado = st.selectbox(
        # "Escolha o estado", list(df.index), ["MG"]
        "Escolha o estado", list(df.index), 0
    )
    if not estado:
        st.error("Selecione um estado.")
        return


    #############################################################
    # Execução do Modelo de Leitos para estado
    #############################################################
    # Adiciona um slider ao sidebar
    list_local = states_pop_cases_deaths(estado)

    st.write(
    '> __*',estado,'*__ possui **',list_local[1],'** casos\
     e **', list_local[2],'** mortes por COVID-19 até o momento.\
     [[+](https://covid19br.wcota.me/)]'
    )

    st.write('---')

    est_sigla = states_sigla(estado)
    Est_sigla = est_sigla
    # print('Est_sigla: ', Est_sigla)

    df = get_EST_data_by_day()
    T_dias = len(df.columns)-1

    Dsim = 500 # Duração da simulação
    N_dias = st.sidebar.number_input("Duração da simulação (dias)",
                                     int(T_dias+1), 1000, Dsim, 1)
    # Ndias = int(N_dias - T_dias)
    Ndias = int(N_dias)

    P_pop_afetada = st.sidebar.number_input("Projeção de infecções futuras  (% pop)",
                                      0.1, 10.0, 0.3, 0.01)
    Perc_pop_afetada = P_pop_afetada/100

    T_internacao_UTI = st.sidebar.number_input("Taxa de internação UTI (% das internações)",
                                      10.0, 35.0, 26.0, 1.0)

    st.sidebar.markdown(f"<font size=2>Fonte: </font>[[+](https://doi.org/10.25561/77482)]", unsafe_allow_html=True)

    Taxa_internacao_UTI = T_internacao_UTI/100
    Taxa_internacao_LG = (1-Taxa_internacao_UTI)

    # T_ocup_UTI = st.sidebar.number_input("Taxa inicial de ocupação leitos UTI (%). Leitos UTI adulto,"\
    #                                         "desconsiderando leitos UTI neonatal, queimadura e coronariana",
    #                                   0.0, 100.0, 30.0, 1.0)
    # Taxa_ocup_UTI = T_ocup_UTI/100
    Taxa_ocup_UTI = 0.0

    T_ocup_LG = st.sidebar.number_input("Taxa inicial de ocupação leitos Gerias (%). Leitos Gerais,"\
                                            "de internação. Clínicos e cirúrgicos.",
                                      0.0, 100.0, 70.0, 1.0)
    Taxa_ocup_LG = T_ocup_LG/100
    # Taxa_ocup_LG = 0.7

    # Mais_leitos_UTI_p_COVID19 = st.sidebar.number_input("Simular mais leitos UTI para COVID-19?"\
    #                                                     "(Os novos leitos recementemente adquiridos já estão incluídos)",
    #                                   0.0, 10000.0, 0.0, 1.0)
    Mais_leitos_UTI_p_COVID19 = 0
    # Mais_leitos_Gerais_p_COVID19 = st.sidebar.number_input("Simular mais leitos Gerais para COVID-19?"\
    #                                                     "(Os novos leitos recementemente adquiridos já estão incluídos)",
    #                                   0.0, 10000.0, 0.0, 1.0)
    Mais_leitos_Gerais_p_COVID19 = 0


    # T_testes = st.sidebar.number_input("Políticas de testes na quarentena (% pop). \
    #                                    Indivíduos testados e detectados positivo \
    #                                    têm a conectividade reduzida com outros \
    #                                    indivíduos da população.",
    #                                   0.0, 2.0, 0.0, 0.5)
    # Testes = T_testes/100


    # # Adiciona um slider
    # values = st.slider('Início e Fim do distanciamento (dias). \
    #                    O distanciamento produz uma redução de transmissão em 20%.',
    #                    1, max(1, Ndias), (min(1,Ndias), min(1,Ndias)))
    #
    # ini_dist = max(1, values[0])
    # fim_dist = min(values[1], Ndias)
    #
    # st.write('> Distanciamento iniciando dia ', ini_dist, 'e finalizando dia ', fim_dist)
    # st.write('---')


    #############################################################
    # Modelo Leitos: infecção
    #############################################################
    modelo_infeccao(Ndias=Ndias,
                    sigla=Est_sigla,
                    Perc_pop_afetada=Perc_pop_afetada)
    #############################################################
    # progress_bar = st.sidebar.progress(0)
    # status_text = st.sidebar.empty()

    data = pd.read_csv(
                   IMAG_DIR + "/chart_leitos_casos.csv", # Dado no seu endereço
                   sep=',',             # Dados separados por virgula
                   quotechar="'",       # Caracteres sob aspas ''
                   dtype={
                       'dia': int,
                       'Tot_casos': int,
                       'Nov_casos': int},    # Ler a coluna 'S' como inteiro
                   # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                   names=['Dias','Total de casos acumulados','Novos casos'],
                   header=0,
                   )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data (Prev. e Novos casos): ', data)
    # print(data.filter(['Previsao de novos casos']))
    # st.line_chart(data.filter(['Total de casos acumulados']))
    # st.line_chart(data.filter(['Novos casos']))

    from bokeh.plotting import figure
    title_name = 'Casos diários de COVID-19 [histórico (até hoje) e previsão]'
    TOOLS1 = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,save"
    p = figure(title=title_name,tools=TOOLS1, background_fill_color="#ffffff")
    x = list(data['Dias'])
    # print('x: ', x)
    # casos_acum = list(data['Total de casos acumulados'])
    # print('casos_acum: ', casos_acum)
    # p.line(x, casos_acum, line_color="#008080", line_width = 2, alpha = 0.7,
    #        legend_label="Casos acumulados por dia")
    casos_novos = list(data['Novos casos'])
    # print('casos_novos: ', casos_novos)
    p.line(x, casos_novos, line_color="#FF4040", line_width = 2, alpha = 0.7,
           legend_label="Novos casos por dia")
    # p.y_range.start = 0
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    # p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'Dias (desde 25/02)'
    p.yaxis.axis_label = 'Nº Casos de COVID-19 / dia'
    # p.grid.grid_line_color="white"

    st.bokeh_chart(p, use_container_width=True)


    st.write(
    '> Já se passaram ', T_dias, ' dias desde o registro do 1º caso de COVID-19.'
    )


    from bokeh.plotting import figure
    from bokeh.models.widgets import Tabs, Panel

    panels = []

    for axis_type in ["linear", "log"]:
        title_name = 'Casos acumulados de COVID-19 [histórico (até hoje) e previsão]'
        TOOLS1 = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,save"
        # p = figure(title=title_name,tools=TOOLS1, background_fill_color="#ffffff")
        p = figure(title=title_name,tools=TOOLS1, background_fill_color="#ffffff",
                   y_axis_type=axis_type)

        x = list(data['Dias'])
        # print('x: ', x)
        casos_acum = list(data['Total de casos acumulados'])
        # print('casos_acum: ', casos_acum)
        p.line(x, casos_acum, line_color="#008080", line_width = 2, alpha = 0.7,
               legend_label="Casos acumulados por dia")
        # casos_novos = list(data['Novos casos'])
        # print('casos_novos: ', casos_novos)
        # p.line(x, casos_novos, line_color="#FF4040", line_width = 2, alpha = 0.7,
        #        legend_label="Novos casos por dia")
        # p.y_range.start = 0
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        # p.legend.location = "center_right"
        p.legend.background_fill_color = "#fefefe"
        p.xaxis.axis_label = 'Dias (desde 25/02)'
        p.yaxis.axis_label = 'Nº Casos de COVID-19'
        # p.grid.grid_line_color="white"

        panel = Panel(child=p, title=axis_type)
        panels.append(panel)

    tabs = Tabs(tabs=panels)

    # st.bokeh_chart(p, use_container_width=True)
    st.bokeh_chart(tabs, use_container_width=True)

    st.write(
    '> Já se passaram ', T_dias, ' dias desde o registro do 1º caso de COVID-19.'
    )

    if st.button("Analisar curvas em conjunto"):
        from bokeh.plotting import figure
        title_name = 'Casos de COVID-19 (novos casos diários e acumulado) [histórico (até hoje) e previsão]'
        TOOLS1 = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,save"
        p = figure(title=title_name,tools=TOOLS1, background_fill_color="#ffffff")
        x = list(data['Dias'])
        # print('x: ', x)
        casos_acum = list(data['Total de casos acumulados'])
        # print('casos_acum: ', casos_acum)
        p.line(x, casos_acum, line_color="#008080", line_width = 2, alpha = 0.7,
               legend_label="Casos acumulados por dia")
        casos_novos = list(data['Novos casos'])
        # print('casos_novos: ', casos_novos)
        p.line(x, casos_novos, line_color="#FF4040", line_width = 2, alpha = 0.7,
               legend_label="Novos casos por dia")
        # p.y_range.start = 0
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        # p.legend.location = "center_right"
        p.legend.background_fill_color = "#fefefe"
        p.xaxis.axis_label = 'Dias (desde 25/02)'
        p.yaxis.axis_label = 'Nº Casos de COVID-19'
        # p.grid.grid_line_color="white"

        st.bokeh_chart(p, use_container_width=True)

        st.write(
        '> Já se passaram ', T_dias, ' dias desde o registro do 1º caso de COVID-19.'
        )

    # if st.button("Analisar curvas em conjunto"):
    #     # with st.spinner('Executando o modelo...'):
    #
    #     chart_data = pd.DataFrame(data)
    #     print('chart_data (Prev. e Novos casos): ', chart_data)
    #     # st.line_chart(chart_data)
    #     # chart = st.line_chart(chart_data)
    #     chart = st.line_chart(chart_data[:1])
    #
    #
    #     # Numero de dias (Ndias) em 100 etapas de impressao
    #     # do gráfico
    #     ch_days = int(len(data)/100)
    #     print('ch_days: ', ch_days)
    #
    #     for i in range(1, 101):
    #         # new_rows = chart_data[3*i-3:3*i]
    #         # new_rows = chart_data[i-1:i]
    #         new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
    #         # print('new_rows: ', new_rows)
    #         status_text.text("%i%% Completo" % i)
    #         chart.add_rows(new_rows)
    #         progress_bar.progress(i)
    #         time.sleep(0.01)
    #
    #     progress_bar.empty()


    #############################################################
    # Modelo Leitos: Leitos disponíveis por dia
    #############################################################
    # leitos_disp_por_dia(Ndias=Ndias, sigla=Est_sigla,
    #                     Perc_pop_afetada=Perc_pop_afetada,
    #                     Taxa_internacao_UTI=Taxa_internacao_UTI,
    #                     Taxa_internacao_LG=Taxa_internacao_LG)
    UTI_disp = []
    LG__disp = []


    st.write('---')
    st.write('> Taxa de internação hospitalar de **', estado ,'**: ', taxa_internacao_hospitalar(Est_sigla))
    # st.write('> Ajuste do percentual da taxa de internação hospitalar de **', estado, '**')
    sl_aument_internacao = st.slider('',0.0, 80.0, 0.0, 0.1)
    slider_aument_int = round((sl_aument_internacao/100),4)
    st.write('> Simule um aumento da taxa de internação hospitalar de **', estado ,'**: ', taxa_internacao_hospitalar(Est_sigla) + slider_aument_int)

    UTI_disp, LG__disp = modelo_admissao(Ndias=Ndias, sigla=Est_sigla,
                        Perc_pop_afetada=Perc_pop_afetada,
                        Taxa_internacao_UTI=Taxa_internacao_UTI,
                        # Taxa_internacao_LG=Taxa_internacao_LG,
                        Aumento_taxa_Intern = slider_aument_int,
                        Taxa_ocup_UTI=Taxa_ocup_UTI,
                        Taxa_ocup_LG=Taxa_ocup_LG,
                        Mais_leitos_UTI_p_COVID19=Mais_leitos_UTI_p_COVID19,
                        Mais_leitos_Gerais_p_COVID19=Mais_leitos_Gerais_p_COVID19
                        )


    #############################################################
    # Estatísticas do modelo de leitos
    #############################################################
    # print('UTI_disp[T_dias]: ', int(UTI_disp[T_dias]))
    # print('LG__disp[T_dias]: ', int(LG__disp[T_dias]))
    Leitos_UTI = states_leitos_UTI(Est_sigla)
    Leitos_LG = states_leitos_Gerais(Est_sigla)
    # print('Leitos_UTI: ', Leitos_UTI)
    # print('Leitos_LG: ', Leitos_LG)
    ocup_UTI = 100.0 if int(UTI_disp[T_dias]) < 0 else round((Leitos_UTI-UTI_disp[T_dias])/Leitos_UTI,2)*100
    # print('ocup_UTI: ', ocup_UTI)
    ocup_Geral = 100.0 if int(LG__disp[T_dias]) < 0 else round((Leitos_LG-LG__disp[T_dias])/Leitos_LG,2)*100
    # print('ocup_Geral: ', ocup_Geral)
    d_defit_UTI = sum(1 for i in UTI_disp if i < 0)
    # print('d_defit_UTI: ', d_defit_UTI)
    d_defit_Geral = sum(1 for i in LG__disp if i < 0)
    # print('d_defit_Geral: ', d_defit_Geral)
    defit_UTI = int(abs(min(min(UTI_disp),0)))
    # print('defit_UTI: ', defit_UTI)
    defit_LG = int(abs(min(min(LG__disp),0)))
    # print('defit_LG: ', defit_LG)
    #############################################################
    # progress_bar = st.sidebar.progress(0)
    # status_text = st.sidebar.empty()

    data = pd.read_csv(
                       IMAG_DIR + "/chart_leitos_disp_por_dia.csv", # Dado no seu endereço
                       sep=',',             # Dados separados por virgula
                       quotechar="'",       # Caracteres sob aspas ''
                       dtype={
                           'dia': int,
                           'leitos_disp_UTI_por_dia': int,
                           'leitos_disp_LG_por_dia': int},    # Ler a coluna 'S' como inteiro
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       names=['Dias', 'Leitos UTI disponiveis por dia','Leitos Gerais disponiveis por dia'],
                       header=0,
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data (Leitos disp/dia): ', data)
    # print(data.filter(['Leitos UTI disponiveis por dia']))
    # st.line_chart(data.filter(['Leitos UTI disponiveis por dia']))
    # st.line_chart(data.filter(['Leitos Gerais disponiveis por dia']))

    # st.write("""<font size=2> Em média, 13% dos casos de COVID19 _*sintomáticos*_
    # requerem hospitalização. Os percentuais são ajustados ao perfil demográfico
    # do estado. 74% dos pacientes são destinados aos leitos gerais (clínicos
    # e cirúrgicos) e 26% a leitos UTIs.
    #             <br>Fonte: \
    #             [[+](https://www.medrxiv.org/content/10.1101/2020.04.25.20077396v1.full.pdf)] \
    #             [[+](https://www.ibge.gov.br/apps/populacao/projecao/)].</font>
    #             """, unsafe_allow_html=True)

    st.write("""<font size=2> Segundo a literatura, pelo menos 1/3
                dos indivíduos infectados por COVID-19 são assintomáticos </font>
                [[+](https://doi.org/10.25561/77482)]
                [[+](https://en.wikipedia.org/wiki/Basic_reproduction_number)].<br>
                <font size=2> Nos estados brasileiros, em média 13% dos casos sintomáticos
                requerem hospitalização. Destes, 74% requerem leitos gerais (clínicos
                e cirúrgicos) e 26% requerem UTI. Estes valores são usados na
                **Modelagem de leitos**.</font>
                """, unsafe_allow_html=True)


    # if st.button("Rodar modelo de leitos hospitalares UTI e Gerais"):

        # # with st.spinner('Executando o modelo...'):
        #
        # # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
        # # chart_data = pd.DataFrame(data, columns=['S'])
        # chart_data = pd.DataFrame(data)
        # print('chart_data (Leitos disp/dia): ', chart_data)
        # # st.line_chart(chart_data)
        # # chart = st.line_chart(chart_data)
        # chart = st.line_chart(chart_data[:1])
        #
        # # print('chart_data[300]: ', chart_data[-1:])
        # # print('chart_data[1]: ', chart_data[:1])
        #
        # # Numero de dias (Ndias) em 100 etapas de impressao
        # # do gráfico
        # ch_days = int(len(data)/100)
        # print('ch_days: ', ch_days)
        #
        # for i in range(1, 101):
        #     # new_rows = chart_data[3*i-3:3*i]
        #     new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
        #     # new_rows = chart_data[i-1:i]
        #     # print('new_rows: ', new_rows)
        #     status_text.text("%i%% Completo" % i)
        #     chart.add_rows(new_rows)
        #     progress_bar.progress(i)
        #     time.sleep(0.01)
        #
        # progress_bar.empty()
        # # st.success('Ok!')


    from bokeh.plotting import figure
    title_name = 'Disponibilidade de Leitos Hospitalares UTI e Gerais [histórico (até hoje) e previsão]'
    TOOLS1 = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,save"
    p = figure(title=title_name,tools=TOOLS1, background_fill_color="#ffffff")
    x = list(data['Dias'])
    # print('x: ', x)
    leitos_UTI = list(data['Leitos UTI disponiveis por dia'])
    # print('leitos_UTI: ', leitos_UTI)
    p.line(x, leitos_UTI, line_color="#CF3F3D", line_width = 4, alpha = 0.7,
           legend_label="Leitos UTI disponiveis por dia")
    leitos_Gerais = list(data['Leitos Gerais disponiveis por dia'])
    # print('leitos_Gerais: ', leitos_Gerais)
    p.line(x, leitos_Gerais, line_color="orange", line_width = 4, alpha = 0.7,
           legend_label="Leitos Gerais disponiveis por dia")
    # p.y_range.start = 0
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    # p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'Dias (desde 25/02)'
    p.yaxis.axis_label = 'Nº Leitos disponíveis para pacientes com COVID-19'
    # p.grid.grid_line_color="white"

    st.bokeh_chart(p, use_container_width=True)


    st.write(
    '> Já se passaram ', T_dias, ' dias desde o registro do 1º caso de COVID-19.'
    )

    st.write(
    """
        | Leitos | Total (leitos) | Est. ocupação atual (%) | Déficit projetado (dias) | Demanda (novos leitos) |
        |--------|-------|----------------|--------------------------|------------------------------|
        | UTI_Cov | """,Leitos_UTI,""" | """,ocup_UTI,"""  | """,d_defit_UTI,""" | """,defit_UTI,"""|
        | Clínicos | """,Leitos_LG,"""  | """,ocup_Geral,"""| """,d_defit_Geral,""" | """,defit_LG,""" |
    """)
    st.write(
    '> Fonte: Leitos Clínicos [[+](http://cnes2.datasus.gov.br/Mod_Ind_Tipo_Leito.asp?VEstado=00)]\
     Leitos UTI Covid-19 [[+](https://covid-insumos.saude.gov.br/paineis/insumos/painel_leitos.php)]'
    )

    # import plotly.express as px
    # d1 = data.filter(['Leitos UTI disponiveis por dia'])
    # d2 = data.filter(['Leitos Gerais disponiveis por dia'])
    # df = [d1,d2]
    # group_labels = ['Leitos UTI disponiveis por dia',
    #                 'Leitos Gerais disponiveis por dia']
    # fig = px.line(df, group_labels, x='Dias')
    # st.plotly_chart(fig, use_container_width=True)

    # import altair as alt
    # source = data
    # c = alt.Chart(source).mark_bar().encode(
    # x="Dia:Q",
    # y="Leitos UTI disponiveis por dia:Q",
    # color=alt.condition(
    #     alt.datum.nonfarm_change > 0,
    #     alt.value("steelblue"),  # The positive color
    #     alt.value("orange")  # The negative color
    # ))
    #
    # st.altair_chart(c, use_container_width=True)

    # st.warning('Parâmetros de atualização recente do nº de leitos, tempos médios em  UTI e leitos gerais são customizados sob demanda.')

    st.write('---')


    st.markdown(
        """
    ## Modelo de previsão de leitos hospitalares

    **PREVISÃO DE DISPONIBILIDADE DE LEITOS NOS ESTADOS BRASILEIROS E DISTRITO FEDERAL EM FUNÇÃO DA PANDEMIA DE COVID-19**


    João Flávio de Freitas Almeida(a), Samuel Vieira Conceição(a), Luiz Ricardo Pinto(a)
    Virginia Silva Magalhães(b), Ingrid Jeber do Nascimento(b), Marcone Pereira Costa(b),
    Horácio Pereira de Faria(b), Cláudia Júlia Guimarães Horta(c), Francisco Carlos Cardoso de Campos(b)


    (a)	_Dep. de Engenharia de Produção – Universidade Federal de Minas Gerais_
    (b)	_Núcleo de Educação em Saúde Coletiva – Universidade Federal de Minas Gerais_
    (c)	_Fundação João Pinheiro_

    Notas Técnicas [+](https://labdec.nescon.medicina.ufmg.br/destaque/previsao-de-disponibilidade-de-leitos-nos-estados-brasileiros-e-distrito-federal-em-funcao-da-pandemia-covid-19/)

    Ocupação de leitos em outros países [[+](https://en.wikipedia.org/wiki/List_of_countries_by_hospital_beds)]

    Secretarias Estaduais de Saúde:
        """
                )

    st.write("""<font size=2>\
             Acre [[+](http://covid19.ac.gov.br/)]<br>\
             Alagoas [[+](http://www.alagoascontraocoronavirus.al.gov.br/)]<br>\
             Amapá [[+](http://painel.corona.ap.gov.br/)]<br>\
             Amazonas [[+](http://www.saude.am.gov.br/painel/corona/)]<br>\
             Bahia [[+](http://www.saude.ba.gov.br/temasdesaude/coronavirus/notas-tecnicas-e-boletins-epidemiologicos-covid-19/)]<br>\
             Ceará [[+](https://indicadores.integrasus.saude.ce.gov.br/indicadores/indicadores-coronavirus/coronavirus-ceara)]<br>\
             Distrito Federal [[+](http://www.saude.df.gov.br/coronavirus/)]<br>\
             Espírito Santo [[+](https://coronavirus.es.gov.br/painel-covid-19-es)]<br>\
             Goiás [[+](https://extranet.saude.go.gov.br/pentaho/api/repos/:coronavirus:paineis:painel.wcdf/generatedContent)]<br>\
             Maranhão [[+](https://painel-covid19.saude.ma.gov.br/casos)]<br>\
             Mato Grosso [[+](http://www.saude.mt.gov.br/)]<br>\
             Mato Grosso do Sul [[+](http://www.coronavirus.ms.gov.br/)]<br>\
             Minas Gerais [[+](https://www.saude.mg.gov.br/coronavirus/painel)]<br>\
             Pará [[+](https://www.covid-19.pa.gov.br/public/dashboard/41777953-93bf-4a46-b9c2-3cf4ccefb3c9)]<br>\
             Paraná [[+](http://www.coronavirus.pr.gov.br/)]<br>\
             Pernambuco [[+](https://www.pecontracoronavirus.pe.gov.br/2160-2/)]<br>\
             Piauí [[+](https://datastudio.google.com/u/0/reporting/a6dc07e9-4161-4b5a-9f2a-6f9be486e8f9/page/2itOB)]<br>\
             Rio de Janeiro [[+](http://painel.saude.rj.gov.br/monitoramento/covid19.html)]<br>\
             Rio Grande do Norte [[+](http://www.saude.rn.gov.br/Conteudo.asp?TRAN=ITEM&TARG=223456&ACT=&PAGE=&PARM=&LBL=MAT%C9RIA)]<br>\
             Rio Grande do Sul [[+](http://ti.saude.rs.gov.br/covid19/)]<br>\
             Rondônia [[+](http://covid19.sesau.ro.gov.br/#)]<br>\
             Roraima [[+](https://saude.rr.gov.br/index.php/coordenadoriasx/coronavirus-boletins)]<br>\
             São Paulo [[+](http://www.saude.sp.gov.br/ses/perfil/cidadao/homepage/outros-destaques/covid-19-plano-de-contingencia-boletins-diarios-e-outras-informacoes)]<br>\
             Santa Catarina [[+](http://www.coronavirus.sc.gov.br/boletins/)]<br>\
             Sergipe [[+](https://todoscontraocorona.net.br/)]<br>\
             Tocantins [[+](http://integra.saude.to.gov.br/covid19)]<br>\
             </font>""", unsafe_allow_html=True)

    st.write('---')
    # Video tutorial do sistema
    # st.write('### Assita um breve tutorial sobre o sistema')
    # st.video('https://youtu.be/NROBVs3Lw80')
    # st.video('https://youtu.be/lw45mKF5ITY')

    # def video_youtube(src: str, width="100%", height=315):
    #     """An extension of the video widget
    #     Arguments:
    #         src {str} -- A youtube url like https://youtu.be/NROBVs3Lw80
    #     Keyword Arguments:
    #         width {str} -- The width of the video (default: {"100%"})
    #         height {int} -- The height of the video (default: {315})
    #     """
    #     st.write(
    #         f'<iframe width="{width}" height="{height}" src="{src}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
    #         unsafe_allow_html=True,
    #     )
    #
    # video_youtube('https://youtu.be/NROBVs3Lw80')

    # st.write('---')


    # from PIL import Image
    # image = Image.open('./seir/images/SEIRStesting_diagram.png')
    # st.image(image, caption='Modelo SEIRS dinâmico com distanciamento e testes',
    #       # use_column_width=True,
    #       width = 600
    #       )



########################################################################
# Modelo de Leitos por Município #
########################################################################
# def plotting_seirs_plus_municipio():
#     # config.is_state = False
#     # print('config.is_state: ', config.is_state)
#     # from seir import seir
#
#     # with st.spinner('Atualizando os dados...'):
#     try:
#         df = get_MUN_data()
#     except urllib.error.URLError as e:
#         st.error(
#         """
#         **Erro de acesso aos dados dos municípios.**
#         Erro: %s
#         """
#         % e.reason
#         )
#         return
#
#     municipio = st.selectbox(
#     # "Escolha o município", list(df.index), ["Belo Horizonte/MG"]
#     "Escolha o município (já apresentou casos de COVID-19)",
#     list(df.index), 0
#     )
#     if not municipio:
#         st.error("Selecione um município.")
#         return
#
#     #############################################################
#     # Execução do Modelo SEIRS para município
#     #############################################################
#     # from seir import seir
#     local = municipio
#     # Ndias = seir.Ndias
#     list_local = mun_pop_cases_deaths(local)
#     # ini_dist = seir.ini_dist
#     # fim_dist = seir.fim_dist
#
#     # st.success('Ok.')
#
#
#     # Adiciona um slider ao sidebar
#     # Ndias = st.sidebar.slider('Duração da simulação (% de 5 anos)'
#     #                           ,120,1825, 365)
#     N_dias = st.sidebar.number_input("Duração da simulação (dias)",
#                                      0, 2500, 300, 100)
#     Ndias = N_dias
#
#     T_xi = st.sidebar.number_input("Taxa de re-susceptibilidade (% pop). \
#                                    Indivíduos recuperados podem se tornar \
#                                    re-susceptíveis um tempo depois da recuperação.",
#                                       0.0, 1.0, 0.0, 0.1)
#     TResus = T_xi/100
#
#     T_testes = st.sidebar.number_input("Políticas de testes na quarentena (% pop). \
#                                        Indivíduos testados e detectados positivo \
#                                        têm a conectividade reduzida com outros \
#                                        indivíduos da população.",
#                                       0.0, 2.0, 0.0, 0.5)
#     Testes = T_testes/100
#
#
#     st.write(
#     '> __*',local,'*__ possui **',list_local[1],'** casos\
#      e **', list_local[2],'** mortes por COVID-19 registrados até o momento.\n'
#      '[Fonte](https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv)'
#     )
#
#     st.write('---')
#
#     # Adiciona um slider
#     values = st.slider('Início e Fim do distanciamento (dias). \
#                        O distanciamento produz uma redução de transmissão em 20%.',
#                        1, max(1, Ndias), (min(1,Ndias), min(1,Ndias)))
#
#
#     ini_dist = max(1, values[0])
#     fim_dist = min(values[1], Ndias)
#
#     st.write('> Distanciamento iniciando dia ', ini_dist, 'e finalizando dia ', fim_dist)
#     st.write('---')
#
#     # Modelo SEIRS+
#     ref_model = modelo_SEIR(local=local, ndias=Ndias, list_local=list_local,
#                             pop_real=True)
#     modelo_SEIRS_plus(ref_model, local=local, ndias=Ndias,
#                           list_local=list_local, T_resus=TResus,
#                           id=ini_dist, fd=fim_dist, tst=Testes,
#                           imprime=False, pop_real=True)
#     #############################################################
#
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#
#     # ('..', 'images')    > Um níveil acima
#     # ('../..', 'images') > Dois níveis acima
#     IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             '', 'images')
#     # print('IMAG_DIR: ', IMAG_DIR)
#
#     data = pd.read_csv(
#                        IMAG_DIR + '/chart_seirs_plus.csv', # Dado no seu endereço
#                        sep=',',             # Dados separados por virgula
#                        quotechar="'",       # Caracteres sob aspas ''
#                        dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
#                        # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
#                        # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
#                        )
#     # Preview the first 5 lines of the loaded data
#     # print('data.head(): ', data.head())
#     # print('data: ', data)
#     # st.line_chart(data)
#
#     if st.button("Rodar modelos (Geral e Infectados) para o município"):
#
#         # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
#         # chart_data = pd.DataFrame(data, columns=['S'])
#         chart_data = pd.DataFrame(data)
#         # st.line_chart(chart_data)
#         # chart = st.line_chart(chart_data)
#         chart = st.line_chart(chart_data[:1])
#
#         # print('chart_data[300]: ', chart_data[-1:])
#         # print('chart_data[1]: ', chart_data[:1])
#
#         # Numero de dias (Ndias) em 100 etapas de impressao
#         # do gráfico
#         ch_days = int(len(data)/100)
#         print('ch_days: ', ch_days)
#
#         for i in range(1, 101):
#             # new_rows = chart_data[3*i-3:3*i]
#             new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
#             # print('new_rows: ', new_rows)
#             status_text.text("%i%% Completo" % i)
#             chart.add_rows(new_rows)
#             progress_bar.progress(i)
#             time.sleep(0.05)
#
#         progress_bar.empty()
#
#
#         plotting_seirs_plus_g2()
#
#         # st.success('Ok!')
#
#     st.write('---')
#
#     st.markdown(
#         """
#                 ## Modelo SEIRS dinâmico com a possibilidade de testes
#
#                 O [modelo epidêmico](https://github.com/ryansmcgee/seirsplus/blob/master/README.md)
#                 clássico **SEIR** considera a população dividida em indivíduos
#                 _Susceptíveis_ **(S)**, _Expostos_ **(E)**, _Infectados_ **(I)**,
#                 e _Recuperados_ **(R)**. No modelo **SEIRS**, indivíduos recuperados
#                 podem ficar novamente _susceptíveis_ após um tempo recuperado.
#                 A inclusão de efeitos dos testes na dinâmica de infecção é modelado
#                 considerando _expostos e infectados detectados_.
#                 Indivíduos com teste positivo são movidos para um estado,
#                 em que as taxas de transmissão, progressão, recuperação e mortalidade
#                 podem ser diferentes dos casos ainda não detectados.
#                 As taxas de transmissaõ entre os estados são dadas pelos parâmetros:
#
#                 * β: taxa de transmissão (pelo contato S-I por período)
#                 * σ: taxa de progressão
#                 * γ: taxa de recuperação
#                 * μ_I: taxa de mortalidade da COVID-19 (mortes por período)
#                 * ξ: taxa de re-susceptibilidade (0 se imunidade permanente)
#                 * θ_E: taxa de testes de indivíduos expostos
#                 * θ_I: taxa de testes de indivíduos infectados
#                 * ψ_E: taxa de resultados positivos de testes de indivíduos expostos
#                 * ψ_I: taxa de resultados positivos de indivíduos infectados
#                 * β_D: taxa de transmissão de casos detectados (transmissão por contato S-D_I por período)
#                 * σ_D: taxa de progressão de casos detectados
#                 * γ_D: taxa de recuperação de casos detectados
#                 * μ_D: taxa de mortalidade da COVID-19 de casos detectados (mortes por período)
#
#                 [Fonte](https://github.com/ryansmcgee/seirsplus/blob/master/docs/SEIRSplus_Model.pdf)
#
#         """
#                 )
#
#     from PIL import Image
#     image = Image.open('./seir/images/SEIRStesting_diagram.png')
#     st.image(image, caption='Modelo SEIRS dinâmico com distanciamento e testes',
#           # use_column_width=True,
#           width = 600
#           )


########################################################################
# Gráfico genérico de detalhamento de infectados
########################################################################


# ########################################################################
# # Modelo SEIR (basico)
# ########################################################################
# def plotting_seir_estado():
#     # config.is_state = True
#     # print('config.is_state: ', config.is_state)
#
#     try:
#         df = get_EST_data()
#
#     except urllib.error.URLError as e:
#         st.error(
#             """
#             **Erro de acesso aos dados dos estados.**
#             Erro: %s
#             """
#             % e.reason
#         )
#         return
#
#     estado = st.selectbox(
#         # "Escolha o estado", list(df.index), ["MG"]
#         "Escolha o estado", list(df.index), 0
#     )
#     if not estado:
#         st.error("Selecione um estado.")
#         return
#
#     #############################################################
#     # Execução do Modelo SEIR para estado
#     #############################################################
#     from seir import seir
#     local = estado
#     Ndias = seir.Ndias
#     list_local = states_pop_cases_deaths(local)
#
#     st.write(
#     '> __*',local,'*__ possui **',list_local[1],'** casos\
#      e **', list_local[2],'** mortes por COVID-19 registrados até o momento.\n'
#      '[Fonte](https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv)'
#     )
#
#     seir.modelo_SEIR(local=local, ndias=Ndias,
#                      list_local=list_local,
#                     imprime=False, pop_real=True)
#     #############################################################
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#
#     # ('..', 'images')    > Um níveil acima
#     # ('../..', 'images') > Dois níveis acima
#     IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             '', 'images')
#     # print('IMAG_DIR: ', IMAG_DIR)
#
#     data = pd.read_csv(
#                        IMAG_DIR + '/chart_seir.csv', # Dado no seu endereço
#                        sep=',',             # Dados separados por virgula
#                        quotechar="'",       # Caracteres sob aspas ''
#                        dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
#                        # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
#                        # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
#                        )
#     # Preview the first 5 lines of the loaded data
#     # print('data.head(): ', data.head())
#     # print('data: ', data)
#     # st.line_chart(data)
#
#     if st.button("Rodar modelos SEIR (Geral e Infectados) do estado"):
#
#         # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
#         # chart_data = pd.DataFrame(data, columns=['S'])
#         chart_data = pd.DataFrame(data)
#         # st.line_chart(chart_data)
#         # chart = st.line_chart(chart_data)
#         chart = st.line_chart(chart_data[:1])
#
#         # print('chart_data[300]: ', chart_data[-1:])
#         # print('chart_data[1]: ', chart_data[:1])
#
#         # Numero de dias (Ndias) em 100 etapas de impressao
#         # do gráfico
#         ch_days = int(len(data)/100)
#         print('ch_days: ', ch_days)
#
#         for i in range(1, 101):
#             # new_rows = chart_data[3*i-3:3*i]
#             new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
#             # print('new_rows: ', new_rows)
#             status_text.text("%i%% Completo" % i)
#             chart.add_rows(new_rows)
#             progress_bar.progress(i)
#             time.sleep(0.05)
#
#         progress_bar.empty()
#
#         # plotting_seir_g2_estado()
#         plotting_seir_g2()
#
#
# def plotting_seir_municipio():
#     # config.is_state = False
#     # print('config.is_state: ', config.is_state)
#     from seir import seir
#
#     try:
#         df = get_MUN_data()
#     except urllib.error.URLError as e:
#         st.error(
#         """
#         **Erro de acesso aos dados dos municípios.**
#         Erro: %s
#         """
#         % e.reason
#         )
#         return
#
#     municipio = st.selectbox(
#     # "Escolha o município", list(df.index), ["Belo Horizonte/MG"]
#     "Escolha o município (já apresentou casos de COVID-19)",
#     list(df.index), 0
#     )
#     if not municipio:
#         st.error("Selecione um município.")
#         return
#
#     #############################################################
#     # Execução do Modelo SEIR para município
#     #############################################################
#     from seir import seir
#     local = municipio
#     Ndias = seir.Ndias
#     list_local = mun_pop_cases_deaths(local)
#
#     st.write(
#     '> __*',local,'*__ possui **',list_local[1],'** casos\
#      e **', list_local[2],'** mortes por COVID-19 registrados até o momento.\n'
#      '[Fonte](https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv)'
#     )
#
#     seir.modelo_SEIR(local=local, ndias=Ndias,
#                      list_local=list_local,
#                     imprime=False, pop_real=True)
#     #############################################################
#
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#
#     # ('..', 'images')    > Um níveil acima
#     # ('../..', 'images') > Dois níveis acima
#     IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             '', 'images')
#     # print('IMAG_DIR: ', IMAG_DIR)
#
#     data = pd.read_csv(
#                        IMAG_DIR + '/chart_seir.csv', # Dado no seu endereço
#                        sep=',',             # Dados separados por virgula
#                        quotechar="'",       # Caracteres sob aspas ''
#                        dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
#                        # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
#                        # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
#                        )
#     # Preview the first 5 lines of the loaded data
#     # print('data.head(): ', data.head())
#     # print('data: ', data)
#     # st.line_chart(data)
#
#     if st.button("Rodar modelos SEIR (Geral e Infectados) do município"):
#
#         # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
#         # chart_data = pd.DataFrame(data, columns=['S'])
#         chart_data = pd.DataFrame(data)
#         # st.line_chart(chart_data)
#         # chart = st.line_chart(chart_data)
#         chart = st.line_chart(chart_data[:1])
#
#         # print('chart_data[300]: ', chart_data[-1:])
#         # print('chart_data[1]: ', chart_data[:1])
#
#         # Numero de dias (Ndias) em 100 etapas de impressao
#         # do gráfico
#         ch_days = int(len(data)/100)
#         print('ch_days: ', ch_days)
#
#         for i in range(1, 101):
#             # new_rows = chart_data[3*i-3:3*i]
#             new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
#             # print('new_rows: ', new_rows)
#             status_text.text("%i%% Completo" % i)
#             chart.add_rows(new_rows)
#             progress_bar.progress(i)
#             time.sleep(0.05)
#
#         progress_bar.empty()
#
#         # plotting_seir_g2_municipio()
#         plotting_seir_g2()
#
#
# def plotting_seir_g2():
#
#     # print('config.is_state: ', config.is_state)
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#
#     # ('..', 'images')    > Um níveil acima
#     # ('../..', 'images') > Dois níveis acima
#     IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             '', 'images')
#     # print('IMAG_DIR: ', IMAG_DIR)
#
#     data = pd.read_csv(
#                        IMAG_DIR + '/chart_seir2.csv', # Dado no seu endereço
#                        sep=',',             # Dados separados por virgula
#                        quotechar="'",       # Caracteres sob aspas ''
#                        dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
#                        # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
#                        # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
#                        )
#     # Preview the first 5 lines of the loaded data
#     # print('data.head(): ', data.head())
#     # print('data: ', data)
#     # st.line_chart(data)
#
#     # if st.button("Rodar modelo SEIR de infectados"):
#
#     # chart_data = pd.DataFrame(data, columns=['S'])
#     chart_data = pd.DataFrame(data)
#     # st.line_chart(chart_data)
#     # chart = st.line_chart(chart_data)
#     # chart = st.line_chart(chart_data[:1])
#     chart = st.area_chart(chart_data[:1])
#
#     # print('chart_data[300]: ', chart_data[-1:])
#     # print('chart_data[1]: ', chart_data[:1])
#
#     # Numero de dias (Ndias) em 100 etapas de impressao
#     # do gráfico
#     ch_days = int(len(data)/100)
#     print('ch_days: ', ch_days)
#
#     for i in range(1, 101):
#         # new_rows = chart_data[3*i-3:3*i]
#         new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
#         # print('new_rows: ', new_rows)
#         status_text.text("%i%% Completo" % i)
#         chart.add_rows(new_rows)
#         progress_bar.progress(i)
#         time.sleep(0.05)
#
#     # Streamlit widgets automatically run the script from top to bottom. Since
#     # this button is not connected to any other logic, it just causes a plain
#     # rerun.
#     # st.button("Rodar modelo Geral")
#
#     progress_bar.empty()
#
#
# ########################################################################
# # Modelo SEIRS (com re-susceptibilidade) - Ondas
# ########################################################################
# def plotting_seirs_estado():
#     # config.is_state = True
#     # print('config.is_state: ', config.is_state)
#
#     try:
#         df = get_EST_data()
#
#     except urllib.error.URLError as e:
#         st.error(
#             """
#             **Erro de acesso aos dados dos estados.**
#             Erro: %s
#             """
#             % e.reason
#         )
#         return
#
#     estado = st.selectbox(
#         # "Escolha o estado", list(df.index), ["MG"]
#         "Escolha o estado", list(df.index), 0
#     )
#     if not estado:
#         st.error("Selecione um estado.")
#         return
#
#     #############################################################
#     # Execução do Modelo SEIRS para estado
#     #############################################################
#     from seir import seir
#     local = estado
#     Ndias = seir.Ndias
#     list_local = states_pop_cases_deaths(local)
#
#     st.write(
#     '> __*',local,'*__ possui **',list_local[1],'** casos\
#      e **', list_local[2],'** mortes por COVID-19 registrados até o momento.\n'
#      '[Fonte](https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv)'
#     )
#
#     # Modelo SEIRS (com re-susceptibilidade) - Ondas
#     seir.modelo_SEIRS(local=local, ndias=Ndias,
#                      list_local=list_local,
#                     imprime=False, pop_real=True)
#     #############################################################
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#
#     # ('..', 'images')    > Um níveil acima
#     # ('../..', 'images') > Dois níveis acima
#     IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             '', 'images')
#     # print('IMAG_DIR: ', IMAG_DIR)
#
#     data = pd.read_csv(
#                        IMAG_DIR + '/chart_seirs.csv', # Dado no seu endereço
#                        sep=',',             # Dados separados por virgula
#                        quotechar="'",       # Caracteres sob aspas ''
#                        dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
#                        # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
#                        # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
#                        )
#     # Preview the first 5 lines of the loaded data
#     # print('data.head(): ', data.head())
#     # print('data: ', data)
#     # st.line_chart(data)
#
#     if st.button("Rodar modelos SEIRS Re-suscep. (Geral e Infectados) do estado"):
#
#         # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
#         # chart_data = pd.DataFrame(data, columns=['S'])
#         chart_data = pd.DataFrame(data)
#         # st.line_chart(chart_data)
#         # chart = st.line_chart(chart_data)
#         chart = st.line_chart(chart_data[:1])
#
#         # print('chart_data[300]: ', chart_data[-1:])
#         # print('chart_data[1]: ', chart_data[:1])
#
#         # Numero de dias (Ndias) em 100 etapas de impressao
#         # do gráfico
#         ch_days = int(len(data)/100)
#         print('ch_days: ', ch_days)
#
#         for i in range(1, 101):
#             # new_rows = chart_data[3*i-3:3*i]
#             new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
#             # print('new_rows: ', new_rows)
#             status_text.text("%i%% Completo" % i)
#             chart.add_rows(new_rows)
#             progress_bar.progress(i)
#             time.sleep(0.05)
#
#         progress_bar.empty()
#
#
#         plotting_seirs_g2()
#
#
# def plotting_seirs_municipio():
#     # config.is_state = False
#     # print('config.is_state: ', config.is_state)
#     from seir import seir
#
#     try:
#         df = get_MUN_data()
#     except urllib.error.URLError as e:
#         st.error(
#         """
#         **Erro de acesso aos dados dos municípios.**
#         Erro: %s
#         """
#         % e.reason
#         )
#         return
#
#     municipio = st.selectbox(
#     # "Escolha o município", list(df.index), ["Belo Horizonte/MG"]
#     "Escolha o município (já apresentou casos de COVID-19)",
#     list(df.index), 0
#     )
#     if not municipio:
#         st.error("Selecione um município.")
#         return
#
#     #############################################################
#     # Execução do Modelo SEIRS para município
#     #############################################################
#     from seir import seir
#     local = municipio
#     Ndias = seir.Ndias
#     list_local = mun_pop_cases_deaths(local)
#
#     st.write(
#     '> __*',local,'*__ possui **',list_local[1],'** casos\
#      e **', list_local[2],'** mortes por COVID-19 registrados até o momento.\n'
#      '[Fonte](https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv)'
#     )
#
#     # Modelo SEIRS (com re-susceptibilidade) - Ondas
#     seir.modelo_SEIRS(local=local, ndias=Ndias,
#                      list_local=list_local,
#                     imprime=False, pop_real=True)
#     #############################################################
#
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#
#     # ('..', 'images')    > Um níveil acima
#     # ('../..', 'images') > Dois níveis acima
#     IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             '', 'images')
#     # print('IMAG_DIR: ', IMAG_DIR)
#
#     data = pd.read_csv(
#                        IMAG_DIR + '/chart_seirs.csv', # Dado no seu endereço
#                        sep=',',             # Dados separados por virgula
#                        quotechar="'",       # Caracteres sob aspas ''
#                        dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
#                        # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
#                        # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
#                        )
#     # Preview the first 5 lines of the loaded data
#     # print('data.head(): ', data.head())
#     # print('data: ', data)
#     # st.line_chart(data)
#
#     if st.button("Rodar modelos SEIRS Re-suscep. (Geral e Infectados) do município"):
#
#         # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
#         # chart_data = pd.DataFrame(data, columns=['S'])
#         chart_data = pd.DataFrame(data)
#         # st.line_chart(chart_data)
#         # chart = st.line_chart(chart_data)
#         chart = st.line_chart(chart_data[:1])
#
#         # print('chart_data[300]: ', chart_data[-1:])
#         # print('chart_data[1]: ', chart_data[:1])
#
#         # Numero de dias (Ndias) em 100 etapas de impressao
#         # do gráfico
#         ch_days = int(len(data)/100)
#         print('ch_days: ', ch_days)
#
#         for i in range(1, 101):
#             # new_rows = chart_data[3*i-3:3*i]
#             new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
#             # print('new_rows: ', new_rows)
#             status_text.text("%i%% Completo" % i)
#             chart.add_rows(new_rows)
#             progress_bar.progress(i)
#             time.sleep(0.05)
#
#         progress_bar.empty()
#
#
#         plotting_seirs_g2()
#
#
# def plotting_seirs_g2():
#
#     # print('config.is_state: ', config.is_state)
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#
#     # ('..', 'images')    > Um níveil acima
#     # ('../..', 'images') > Dois níveis acima
#     IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             '', 'images')
#     # print('IMAG_DIR: ', IMAG_DIR)
#
#     data = pd.read_csv(
#                        IMAG_DIR + '/chart_seirs2.csv', # Dado no seu endereço
#                        sep=',',             # Dados separados por virgula
#                        quotechar="'",       # Caracteres sob aspas ''
#                        dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
#                        # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
#                        # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
#                        )
#     # Preview the first 5 lines of the loaded data
#     # print('data.head(): ', data.head())
#     # print('data: ', data)
#     # st.line_chart(data)
#
#     # if st.button("Rodar modelo SEIR de infectados"):
#
#     # chart_data = pd.DataFrame(data, columns=['S'])
#     chart_data = pd.DataFrame(data)
#     # st.line_chart(chart_data)
#     # chart = st.line_chart(chart_data)
#     # chart = st.line_chart(chart_data[:1])
#     chart = st.area_chart(chart_data[:1])
#
#     # print('chart_data[300]: ', chart_data[-1:])
#     # print('chart_data[1]: ', chart_data[:1])
#
#     # Numero de dias (Ndias) em 100 etapas de impressao
#     # do gráfico
#     ch_days = int(len(data)/100)
#     print('ch_days: ', ch_days)
#
#     for i in range(1, 101):
#         # new_rows = chart_data[3*i-3:3*i]
#         new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
#         # print('new_rows: ', new_rows)
#         status_text.text("%i%% Completo" % i)
#         chart.add_rows(new_rows)
#         progress_bar.progress(i)
#         time.sleep(0.05)
#
#     # Streamlit widgets automatically run the script from top to bottom. Since
#     # this button is not connected to any other logic, it just causes a plain
#     # rerun.
#     # st.button("Rodar modelo Geral")
#
#     progress_bar.empty()
#
# ####################################################################


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


# def get_is_state(is_state=config.is_state):
#
#     if is_state == True:
#         try:
#             df = get_EST_data()
#
#         except urllib.error.URLError as e:
#             st.error(
#                 """
#                 **Erro de acesso aos dados dos estados.**
#                 Erro: %s
#                 """
#                 % e.reason
#             )
#             return
#
#         estados = st.selectbox(
#             "Escolha o estado", list(df.index), ["MG"]
#         )
#         if not estados:
#             st.error("Selecione um estado.")
#             return
#
#     else:
#
#         try:
#             df = get_MUN_data()
#         except urllib.error.URLError as e:
#             st.error(
#             """
#             **Erro de acesso aos dados dos municípios.**
#             Erro: %s
#             """
#             % e.reason
#             )
#             return
#
#             municipios = st.selectbox(
#             "Escolha o município", list(df.index), ["Belo Horizonte/MG"]
#             )
#             if not municipios:
#                 st.error("Selecione um município.")
#                 return


###############################################################################
# Tentativas e backup de códigos antigos
###############################################################################
# def plotting_seir_g2_estado():
#
#     print('config.is_state: ', config.is_state)
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#
#     # ('..', 'images')    > Um níveil acima
#     # ('../..', 'images') > Dois níveis acima
#     IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             '', 'images')
#     # print('IMAG_DIR: ', IMAG_DIR)
#
#     data = pd.read_csv(
#                        IMAG_DIR + '/chart_seir2.csv', # Dado no seu endereço
#                        sep=',',             # Dados separados por virgula
#                        quotechar="'",       # Caracteres sob aspas ''
#                        dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
#                        # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
#                        # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
#                        )
#     # Preview the first 5 lines of the loaded data
#     # print('data.head(): ', data.head())
#     # print('data: ', data)
#     # st.line_chart(data)
#
#     # if st.button("Rodar modelo SEIR de infectados"):
#
#     # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
#     # chart_data = pd.DataFrame(data, columns=['S'])
#     chart_data = pd.DataFrame(data)
#     # st.line_chart(chart_data)
#     # chart = st.line_chart(chart_data)
#     # chart = st.line_chart(chart_data[:1])
#     chart = st.area_chart(chart_data[:1])
#
#     # print('chart_data[300]: ', chart_data[-1:])
#     # print('chart_data[1]: ', chart_data[:1])
#
#     # Numero de dias (Ndias) em 100 etapas de impressao
#     # do gráfico
#     ch_days = int(len(data)/100)
#     print('ch_days: ', ch_days)
#
#     for i in range(1, 101):
#         # new_rows = chart_data[3*i-3:3*i]
#         new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
#         # print('new_rows: ', new_rows)
#         status_text.text("%i%% Completo" % i)
#         chart.add_rows(new_rows)
#         progress_bar.progress(i)
#         time.sleep(0.05)
#
#     progress_bar.empty()
#
#     # Streamlit widgets automatically run the script from top to bottom. Since
#     # this button is not connected to any other logic, it just causes a plain
#     # rerun.
#     # st.button("Rodar modelo Infectados")



# def plotting_seir_g2_municipio():
#
#     print('config.is_state: ', config.is_state)
#
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#
#     # ('..', 'images')    > Um níveil acima
#     # ('../..', 'images') > Dois níveis acima
#     IMAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             '', 'images')
#     # print('IMAG_DIR: ', IMAG_DIR)
#
#     data = pd.read_csv(
#                        IMAG_DIR + '/chart_seir2.csv', # Dado no seu endereço
#                        sep=',',             # Dados separados por virgula
#                        quotechar="'",       # Caracteres sob aspas ''
#                        dtype={"(S) Susceptivel": int},    # Ler a coluna 'S' como inteiro
#                        # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
#                        # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
#                        )
#     # Preview the first 5 lines of the loaded data
#     # print('data.head(): ', data.head())
#     # print('data: ', data)
#     # st.line_chart(data)
#
#     # if st.button("Rodar modelo SEIR de infectados"):
#
#     # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
#     # chart_data = pd.DataFrame(data, columns=['S'])
#     chart_data = pd.DataFrame(data)
#     # st.line_chart(chart_data)
#     # chart = st.line_chart(chart_data)
#     # chart = st.line_chart(chart_data[:1])
#     chart = st.area_chart(chart_data[:1])
#
#     # print('chart_data[300]: ', chart_data[-1:])
#     # print('chart_data[1]: ', chart_data[:1])
#
#     # Numero de dias (Ndias) em 100 etapas de impressao
#     # do gráfico
#     ch_days = int(len(data)/100)
#     print('ch_days: ', ch_days)
#
#     for i in range(1, 101):
#         # new_rows = chart_data[3*i-3:3*i]
#         new_rows = chart_data[ch_days*i-ch_days:ch_days*i]
#         # print('new_rows: ', new_rows)
#         status_text.text("%i%% Completo" % i)
#         chart.add_rows(new_rows)
#         progress_bar.progress(i)
#         time.sleep(0.05)
#
#     progress_bar.empty()
#
#     # Streamlit widgets automatically run the script from top to bottom. Since
#     # this button is not connected to any other logic, it just causes a plain
#     # rerun.
#     # st.button("Rodar modelo Infectados")
