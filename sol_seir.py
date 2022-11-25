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
import time
import numpy as np
import pandas as pd
import csv
import os # Local (path) do sistema
import sys # Importa modulos do sistema
from math import *
import urllib.error
import pathlib  # Local do diretório (pasta)
import ipdb

from intro import states_pop_cases_deaths
from intro import mun_pop_cases_deaths

# from seir.seirsbr import modelo_SEIR
# from seir.seirsbr import modelo_SEIRS
from seir.seirsbr import modelo_SEIRS_plus
from seir.seirsbr import taxa_de_transmissao_beta

from intro import get_EST_data
from intro import get_MUN_data

import pandas as pd
from intro import get_EST_data_by_day
from intro import get_MUN_data_by_day

from seir.utils.states_info import states_codes
from seir.utils.states_info import states_sigla
from seir.utils.states_info import states_pop

#############################################################
# Estados
#############################################################
# @st.cache
# def get_EST_data():
#     # df = pd.read_csv(".seir/utils/est_casos.csv")
#     df = pd.read_json(r'./seir/utils/est_casos.json')
#     # print('df-Estado: ', df)
#     return df.set_index("nome")

#############################################################
# Municípios
#############################################################
# @st.cache
# def get_MUN_data():
#     # df = pd.read_csv(".seir/utils/mun_casos.csv")
#     df = pd.read_json(r'./seir/utils/mun_casos.json')
#     # print('df-Municipio: ', df)
#     return df.set_index("nome")
########################################################################


########################################################################
# Modelo SEIRS+ #
########################################################################
def plotting_seirs_plus_estado():
    # config.is_state = True
    # print('config.is_state: ', config.is_state)

    # with st.spinner('Atualizando os dados...'):
    try:
        df = get_EST_data()

    except Exception as e:
        st.error(
            """
            **Erro de acesso >> interno << aos dados dos estados.**
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
    # Execução do Modelo SEIRS+ para estado
    #############################################################
    # from seir import seir
    local = estado
    # print('local: ', local)
    # print('sigla: ', states_sigla(local))
    # print('cod: ', states_codes(states_sigla(local)))

    # Ndias = seir.Ndias
    list_local = states_pop_cases_deaths(local)
    # ini_dist = seir.ini_dist
    # fim_dist = seir.fim_dist
    # ini_dist = 2
    # fim_dist = 180

    # st.success('Ok.')

    try:
        df = get_EST_data_by_day()
        T_dias = len(df.columns)-1
    except Exception as e:
        st.error(
            """
            **Erro de acesso >> interno << aos dados dos estados.**
            Erro: %s
            """
            % e.reason
        )
        return


    # Adiciona um slider ao sidebar
    # Ndias = st.sidebar.slider('Duração da simulação (% de 5 anos)'
    #                           ,120,1825, 365)
    Dsim = 500 # Duração da simulação
    N_dias = st.sidebar.number_input("Duração da simulação desde o início da \
                                     pandemia (Nº de dias deve ser maior que \
                                     os dias já decorridos).",
                                     int(T_dias), 2500, Dsim, 1)
    Ndias = max(T_dias, N_dias)

    # N_iso_social = st.sidebar.number_input("Nível de isolamento social (%).\
    #                                        O isolamento social pode provocar\
    #                                        uma redução de até 74% da transmissão\
    #                                        do COVID-19.", 30.0, 100.0, 60.0, 1.0)

    N_iso_social = 60

    st.sidebar.markdown(f"<font size=2>Índice: </font>[[+](https://mapabrasileirodacovid.inloco.com.br/pt/)] \
    <font size=2>e Fonte: </font>[[+](https://bmcmedicine.biomedcentral.com/track/pdf/10.1186/s12916-020-01597-8)]", unsafe_allow_html=True)

    # Historicamente o índice de isolamento social oscila entre
    # 20% e 30 % (https://mapabrasileirodacovid.inloco.com.br/pt/)
    # Assim, este Percentual deve ser deduzido.
    N_isolamento = float(N_iso_social - 30)/100
    # N_transmissao = round((1 - N_isolamento*0.74),2)
    N_transmissao = round((1 - N_isolamento*0.94),2)
    # print('N_transmissao: ', N_transmissao)

    # T_testes = st.sidebar.number_input("Políticas de testes na quarentena (% pop). \
    #                                    Indivíduos testados e detectados positivo \
    #                                    têm a conectividade reduzida com outros \
    #                                    indivíduos da população.",
    #                                   0.0, 20.0, 0.0, 0.1)

    T_testes = 2.0
    Testes = round((T_testes/100),4)

    st.sidebar.markdown("<font size=2>Testes: </font>[[+](https://covid-insumos.saude.gov.br/paineis/insumos/painel.php)]\
                        [[+](https://www.saude.gov.br/noticias/agencia-saude/46868-ministerio-da-saude-ja-distribuiu-6-9-milhoes-de-testes-para-covid-19)]\
                        /<font size=2> População: </font>[[+](https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_popula%C3%A7%C3%A3o)].",
                        unsafe_allow_html=True)

    # T_xi = st.sidebar.number_input("Taxa de re-susceptibilidade (% pop). \
    #                                Indivíduos recuperados podem se tornar \
    #                                re-suscetíveis um tempo depois da recuperação.",
    #                                   0.0, 20.0, 10.0, 0.1)

    T_xi = 5.0
    TResus = round((T_xi/100),4)


    st.write(
    '> __*',local,'*__ possui **',list_local[1],'** casos acumulados\
     e **', list_local[2],'** mortes por COVID-19 até o momento.\
     [[+](https://covid19br.wcota.me/)]'
    )


    st.write('---')


    # Adiciona um slider
    values = st.slider('Início e Fim do distanciamento (dias). \
                       De forma geral, o distanciamento iniciou-se aproximadamente 1 mês após o primeiro caso \
                       de COVID-19 e produz uma redução de transmissão segundo\
                       o nível de isolamento social.',
                       # início, fim, (ini_dist, fim_dist)
                       # 1, max(1, Ndias), (min(1,Ndias), min(1,Ndias)))
                       # 1, max(1, Ndias), (min(30,Ndias), int(T_dias/2)))
                       1, max(1, Ndias), (min(30,Ndias), 300))

    ini_dist = max(1, values[0])
    # fim_dist = min(values[1], int(T_dias/2))
    fim_dist = min(values[1], 300)

    st.write('> Política de distanciamento aplicada entre os dias ',
             ini_dist, ' e ', fim_dist, ' após o primeiro dia de COVID-19.')
    st.write(
    '> Já se passaram ', T_dias, ' dias desde o registro do 1º caso de COVID-19.')
    st.write('---')


    st.write('<font size=2>Registros de infectados (% da população). \
    Ajuste o percentual da população afetada para que o número \
    **mortes** (acumulado) seja próximo ao valor ', list_local[2], " \
    reportado hoje.</font>",unsafe_allow_html=True)

    # Estima-se que pelo menos 1/3 dos infectados sejam assintomáticos\
    # [[+](https://doi.org/10.25561/77482)]. \

    # st.write('<font size=2>Estimativa da população afetada (%). \
    # Considere países que estão aparentemente ao final da pandemia \
    # [[+](https://flattening-the-curve.commutatus.com/)]. \
    # Estima-se que pelo menos 1/3 dos infectados sejam assintomáticos\
    # [[+](https://doi.org/10.25561/77482)]. \
    # Assim, ajuste o percentual da população afetada para que o número \
    # **máximo** de infectados seja aproximadamente ',
    # int(states_pop(states_sigla(local))*0.0023),".</font>",unsafe_allow_html=True)

    sl_pop = st.slider('',0.0, 10.0, 3.0, 0.1)

    slider_pop = round((sl_pop/100),4)


    # if st.button("Rodar modelo SEIRS para o estado"):

    #############################################################
    # Modelo SEIRS+
    #############################################################
    # ref_model = modelo_SEIR(local=local, ndias=Ndias, list_local=list_local,
    #                         pop_real=True)
    # modelo_SEIRS_plus(ref_model, local=local, ndias=Ndias,
    #                       list_local=list_local, T_resus=TResus,
    #                       id=ini_dist, fd=fim_dist, tst=Testes,
    #                       imprime=False, pop_real=True)

    #ipdb.set_trace()
    modelo_SEIRS_plus(local=local, tdias=T_dias, ndias=Ndias,
                      list_local=list_local, T_resus=TResus,
                      id=ini_dist, fd=fim_dist, tst=Testes,
                      ntrans=N_transmissao,
                      sl_pop=slider_pop,
                      imprime=False, pop_real=True)

    # print('modelo_SEIRS_plus: ', modelo_SEIRS_plus(local=local, tdias=T_dias, ndias=Ndias,
    #                   list_local=list_local, T_resus=TResus,
    #                   id=ini_dist, fd=fim_dist, tst=Testes,
    #                   ntrans=N_transmissao,
    #                   sl_pop=slider_pop,
    #                   imprime=False, pop_real=True))
    #############################################################

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
                       dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
                       # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data: ', data)
    # st.line_chart(data)

    # with st.spinner('Parâmetros da literatura internacional. Customizados ao estado sob demanda.'):

    # chart_data = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'D_E', 'D_I', 'F']) (Erro)
    # chart_data = pd.DataFrame(data, columns=['S'])
    # chart_data = pd.DataFrame(data).rename(columns={'(S) Suscetiveis':'(S) Susceptible',
    #                                                 '(E) Expostos':'(E) Exposed',
    #                                                 '(I) Infectados':'(I) Infected',
    #                                                 '(R) Recuperados':'(R) Recovered',
    #                                                 '(D_E) Expostos detectados':'(D_E) Detected Exposed',
    #                                                 '(D_I) Infectados detectados':'(D_I) Detected Infected',
    #                                                 '(M) Mortes':'(D) Deaths'})
    chart_data = pd.DataFrame(data)
    # print('chart_data: ', chart_data)
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
        time.sleep(0.001)

    progress_bar.empty()


    plotting_seirs_plus_g2()


    K = taxa_de_transmissao_beta(local)      # taxa de transmissão - Beta
    t = 5.2         # período médio de infecção
    Ro = exp(K*t)    # Número básico de reprodução (Ro = e^(K.t))
    # https://www.medrxiv.org/content/10.1101/2020.04.25.20077396v1.full.pdf

    st.write("<font size=2>R<sub>0</sub>: </font>",round(Ro,2)," \
            <font size=2> (Número esperado de casos secundários gerados por um caso \
            na população.) \
            </font>[[+](https://en.wikipedia.org/wiki/Basic_reproduction_number)].",
            unsafe_allow_html=True)

    st.write('---')

    st.write("<font size=2>Taxa de mortalidade de "+ local +" pelo COVID-19 foi ajustada " + \
             "ao perfil demográfico nacional em 2020.<br>Fonte: Imperial College " + \
             "[[+](https://doi.org/10.25561/77482)] e IBGE: " + \
             "[[+](https://www.ibge.gov.br/apps/populacao/projecao/)].</font>",
                        unsafe_allow_html=True)



    # PIRÂMIDE ETÁRIA IBGE (e projetção até 2060)

    # sc = states_codes(states_sigla(local))
    # # print('sc: ', str(sc))
    # pyramid = "<iframe id=\"iframeAGPOP_uf\" src=\"https://www.ibge.gov.br/" + \
    # "apps/populacao/projecao/box_piramideplay.php?ag=" + str(sc) + \
    # "\" width=\"700\" height=\"560\" frameborder=\"0\"></iframe>"
    # st.write(pyramid, unsafe_allow_html=True)


    st.markdown(
        """
                ## Modelo SEIRS dinâmico com a possibilidade de testes

                O [modelo epidêmico](https://github.com/ryansmcgee/seirsplus/blob/master/README.md)
                clássico **SEIR** considera a população dividida em indivíduos
                _Susceptíveis_ **(S)**, _Expostos_ **(E)**, _Infectados_ **(I)**,
                e _Recuperados_ **(R)**. No modelo **SEIRS**, indivíduos recuperados
                podem ficar novamente _susceptíveis_ após um tempo recuperado.
                A inclusão de efeitos dos testes na dinâmica de infecção é modelado
                considerando _expostos e infectados detectados_.
                Indivíduos com teste positivo são movidos para um estado,
                em que as taxas de transmissão, progressão, recuperação e mortalidade
                podem ser diferentes dos casos ainda não detectados.
        """
                )

    # As taxas de transmissaõ entre os estados são dadas pelos parâmetros:
    #
    # * β: taxa de transmissão (pelo contato S-I por período)
    # * σ: taxa de progressão
    # * γ: taxa de recuperação
    # * μ_I: taxa de mortalidade da COVID-19 (mortes por período)
    # * ξ: taxa de re-susceptibilidade (0 se imunidade permanente)
    # * θ_E: taxa de testes de indivíduos expostos
    # * θ_I: taxa de testes de indivíduos infectados
    # * ψ_E: taxa de resultados positivos de testes de indivíduos expostos
    # * ψ_I: taxa de resultados positivos de indivíduos infectados
    # * β_D: taxa de transmissão de casos detectados (transmissão por contato S-D_I por período)
    # * σ_D: taxa de progressão de casos detectados
    # * γ_D: taxa de recuperação de casos detectados
    # * μ_D: taxa de mortalidade da COVID-19 de casos detectados (mortes por período)

    # from PIL import Image
    # image = Image.open('./seir/images/SEIRStesting_diagram.png')
    # st.image(image, caption='Modelo SEIRS dinâmico com distanciamento e testes',
    # # use_column_width=True,
    # width = 400)

    st.markdown("Fonte: [[+](https://github.com/ryansmcgee/seirsplus/blob/master/docs/SEIRSplus_Model.pdf)]")


    # st.write(">Adote ",sl_pop,"% da população no **Modelo de leitos**.")

    st.write("""<font size=2> Curvas de casos COVID-19 outros países
                [[+](https://flattening-the-curve.commutatus.com/)]
                População total de outros países </font>
                [[+](https://www.worldometers.info/world-population/population-by-country/)]
                """, unsafe_allow_html=True)

    st.write("""<font size=2> Índice de Gini
             [[+](https://pt.wikipedia.org/wiki/Lista_de_pa%C3%ADses_por_igualdade_de_riqueza)]
                </font>""", unsafe_allow_html=True)











def plotting_seirs_plus_municipio():
    # config.is_state = False
    # print('config.is_state: ', config.is_state)
    # from seir import seir

    # with st.spinner('Atualizando os dados...'):
    try:
        df = get_MUN_data()
    except Exception as e:
        st.error(
            """
            **Erro de acesso >> interno << aos dados dos municípios.**
            Erro: %s
            """
            % e.reason
        )
        return

    municipio = st.selectbox(
    # "Escolha o município", list(df.index), ["Belo Horizonte/MG"]
    "Escolha o município (já apresentou casos de COVID-19)",
    list(df.index), 0
    )
    if not municipio:
        st.error("Selecione um município.")
        return

    #############################################################
    # Execução do Modelo SEIRS para município
    #############################################################
    # from seir import seir
    local = municipio
    # Ndias = seir.Ndias
    list_local = mun_pop_cases_deaths(local)
    # ini_dist = seir.ini_dist
    # fim_dist = seir.fim_dist

    # st.success('Ok.')

    try:
        df = get_MUN_data_by_day()
        T_dias = len(df.columns)-1
    except Exception as e:
        st.error(
            """
            **Erro de acesso >> interno << aos dados dos municípios.**
            Erro: %s
            """
            % e.reason
        )
        return


    # Adiciona um slider ao sidebar
    # Ndias = st.sidebar.slider('Duração da simulação (% de 5 anos)'
    #                           ,120,1825, 365)
    Dsim = 500 # Duração da simulação
    N_dias = st.sidebar.number_input("Duração da simulação desde o início da \
                                     pandemia (Nº de dias deve ser maior que \
                                     os dias já decorridos).",
                                     int(T_dias), 2500, Dsim, 1)
    Ndias = max(T_dias, N_dias)


    # N_iso_social = st.sidebar.number_input("Nível de isolamento social (%).\
    #                                        O isolamento social pode provocar\
    #                                        uma redução de até 74% da transmissão\
    #                                        do COVID-19.", 30.0, 100.0, 60.0, 1.0)

    N_iso_social = 60

    st.sidebar.markdown(f"<font size=2>Índice: </font>[[+](https://mapabrasileirodacovid.inloco.com.br/pt/)] \
    <font size=2>e Fonte: </font>[[+](https://bmcmedicine.biomedcentral.com/track/pdf/10.1186/s12916-020-01597-8)]", unsafe_allow_html=True)

    # Historicamente o índice de isolamento social oscila entre
    # 20% e 30 % (https://mapabrasileirodacovid.inloco.com.br/pt/)
    # Assim, este Percentual deve ser deduzido.
    N_isolamento = float(N_iso_social - 30)/100
    N_transmissao = round((1 - N_isolamento*0.94),2)
    # print('N_transmissao: ', N_transmissao)


    # T_testes = st.sidebar.number_input("Políticas de testes na quarentena (% pop). \
    #                                    Indivíduos testados e detectados positivo \
    #                                    têm a conectividade reduzida com outros \
    #                                    indivíduos da população.",
    #                                   0.0, 2.0, 0.0, 0.5)

    T_testes = 2.0
    Testes = round((T_testes/100),4)

    st.sidebar.markdown("<font size=2>Testes: </font>[[+](https://covid-insumos.saude.gov.br/paineis/insumos/painel.php)]\
                        /<font size=2> População: </font>[[+](https://cidades.ibge.gov.br/brasil/panorama)].",
                        unsafe_allow_html=True)


    # T_xi = st.sidebar.number_input("Taxa de re-susceptibilidade (% pop). \
    #                                Indivíduos recuperados podem se tornar \
    #                                re-suscetíveis um tempo depois da recuperação.",
    #                                   0.0, 20.0, 10.0, 0.1)

    T_xi = 5.0
    TResus = round((T_xi/100),4)


    st.write(
    '> __*',local,'*__ possui **',list_local[1],'** casos acumulados\
     e **', list_local[2],'** mortes por COVID-19 até o momento\
     [[+](https://covid19br.wcota.me/)].'
    )

    st.write('---')


    # Adiciona um slider
    values = st.slider('Início e Fim do distanciamento (dias). \
                       De forma geral, o distanciamento iniciou-se aproximadamente 1 mês após o primeiro caso \
                       de COVID-19 e produz uma redução de transmissão segundo\
                       o nível de isolamento social.',
                       # 1, max(1, Ndias), (min(1,Ndias), min(1,Ndias)))
                       # 1, max(1, Ndias), (min(30,Ndias),int(T_dias/2)))
                       1, max(1, Ndias), (min(30,Ndias),300))

    ini_dist = max(1, values[0])
    # fim_dist = min(values[1], Ndias)
    # fim_dist = min(values[1], int(T_dias/2))
    fim_dist = min(values[1], 300)

    st.write('> Política de distanciamento aplicada entre os dias ',
             ini_dist, ' e ', fim_dist, ' após o primeiro dia de COVID-19.')
    st.write(
    '> Já se passaram ', T_dias, ' dias desde o registro do 1º caso de COVID-19.')
    st.write('---')

    # sl_pop = st.slider('Estimativa da população do município infectada (%).',
    #                    0.0, 10.0, 2.0, 0.1)
    #
    # st.write('<font size=2>Estima-se que pelo menos 1/3 dos infectados sejam assintomáticos.\
    #          Assim, ajuste a taxa de transmissão para que o modelo se ajuste \
    #          ao número de casos em </font> **',int(list_local[1]/0.67),'** \
    #     <font size=2> até o momento.</font>', unsafe_allow_html=True)

    st.write('<font size=2>Registros de infectados (% da população). \
    Ajuste o percentual da população afetada para que o número \
    **mortes** (acumulado) seja próximo ao valor ', list_local[2], " \
    reportado hoje.</font>",unsafe_allow_html=True)

    # Estima-se que pelo menos 1/3 dos infectados sejam assintomáticos\
    # [[+](https://doi.org/10.25561/77482)]. \

    # Considere países que estão aparentemente ao final da pandemia \
    # [[+](https://flattening-the-curve.commutatus.com/)]. \
    # Assim, ajuste o percentual da população afetada para o número \
    # **máximo** de infectados seja aproximadamente ',
    # int(mun_pop_cases_deaths(local)[0]*0.0023),

    sl_pop = st.slider('',0.0, 10.0, 3.0, 0.1)

    slider_pop = round((sl_pop/100),4)

    # # Adiciona um slider
    # values = st.slider('Início e Fim do distanciamento (dias). \
    #                    O distanciamento produz uma redução de transmissão em 20%.',
    #                    1, max(1, Ndias), (min(1,Ndias), min(1,Ndias)))
    #
    #
    # ini_dist = max(1, values[0])
    # fim_dist = min(values[1], Ndias)
    #
    # st.write('> Distanciamento iniciando dia ', ini_dist, 'e finalizando dia ', fim_dist)
    # st.write('---')


    # if st.button("Rodar modelo SEIRS para o município"):

    # Modelo SEIRS+
    #############################################################
    # ref_model = modelo_SEIR(local=local, ndias=Ndias, list_local=list_local,
    #                         pop_real=True)
    # modelo_SEIRS_plus(ref_model, local=local, ndias=Ndias,
    #                       list_local=list_local, T_resus=TResus,
    #                       id=ini_dist, fd=fim_dist, tst=Testes,
    #                       imprime=False, pop_real=True)
    modelo_SEIRS_plus(local=local, tdias=T_dias, ndias=Ndias,
                      list_local=list_local, T_resus=TResus,
                      id=ini_dist, fd=fim_dist, tst=Testes,
                      ntrans=N_transmissao,
                      sl_pop=slider_pop,
                      imprime=False, pop_real=True)

    #############################################################


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
                       dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
                       # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data: ', data)
    # st.line_chart(data)


    # with st.spinner('Parâmetros da literatura internacional. Customizados ao município sob demanda.'):

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
        time.sleep(0.001)

    progress_bar.empty()

    plotting_seirs_plus_g2()

    K = taxa_de_transmissao_beta(local)      # taxa de transmissão - Beta
    t = 5.2         # período médio de infecção
    Ro = exp(K*t)    # Número básico de reprodução (Ro = e^(K.t))

    st.write("<font size=2>R<sub>0</sub>: </font>",round(Ro,2)," \
            <font size=2> (Número esperado de casos secundário gerados por um caso \
            na população)\
            </font>[[+](https://en.wikipedia.org/wiki/Basic_reproduction_number)].",
            unsafe_allow_html=True)

    st.write('---')

    st.markdown(
        """
                ## Modelo SEIRS dinâmico com a possibilidade de testes

                O [modelo epidêmico](https://github.com/ryansmcgee/seirsplus/blob/master/README.md)
                clássico **SEIR** considera a população dividida em indivíduos
                _Susceptíveis_ **(S)**, _Expostos_ **(E)**, _Infectados_ **(I)**,
                e _Recuperados_ **(R)**. No modelo **SEIRS**, indivíduos recuperados
                podem ficar novamente _susceptíveis_ após um tempo recuperado.
                A inclusão de efeitos dos testes na dinâmica de infecção é modelado
                considerando _expostos e infectados detectados_.
                Indivíduos com teste positivo são movidos para um estado,
                em que as taxas de transmissão, progressão, recuperação e mortalidade
                podem ser diferentes dos casos ainda não detectados.
        """
                )

    # As taxas de transmissaõ entre os estados são dadas pelos parâmetros:
    #
    # * β: taxa de transmissão (pelo contato S-I por período)
    # * σ: taxa de progressão
    # * γ: taxa de recuperação
    # * μ_I: taxa de mortalidade da COVID-19 (mortes por período)
    # * ξ: taxa de re-susceptibilidade (0 se imunidade permanente)
    # * θ_E: taxa de testes de indivíduos expostos
    # * θ_I: taxa de testes de indivíduos infectados
    # * ψ_E: taxa de resultados positivos de testes de indivíduos expostos
    # * ψ_I: taxa de resultados positivos de indivíduos infectados
    # * β_D: taxa de transmissão de casos detectados (transmissão por contato S-D_I por período)
    # * σ_D: taxa de progressão de casos detectados
    # * γ_D: taxa de recuperação de casos detectados
    # * μ_D: taxa de mortalidade da COVID-19 de casos detectados (mortes por período)
    
    # from PIL import Image
    # image = Image.open('./seir/images/SEIRStesting_diagram.png')
    # st.image(image, caption='Modelo SEIRS dinâmico com distanciamento e testes',
    # # use_column_width=True,
    # width = 400)

    st.markdown("Fonte: [[+](https://github.com/ryansmcgee/seirsplus/blob/master/docs/SEIRSplus_Model.pdf)]")

    st.write("""<font size=2> Segundo a literatura, pelo menos 1/3
                dos indivíduos infectados por COVID-19 são assintomáticos </font>
                [[+](https://doi.org/10.25561/77482)]
                [[+](https://en.wikipedia.org/wiki/Basic_reproduction_number)].<br>
                <font size=2> Nos estados brasileiros, em média 13% dos casos sintomáticos
                requerem hospitalização. Destes, 74% requerem leitos gerais (clínicos
                e cirúrgicos) e 26% requerem UTI. Estes valores são usados na
                **Modelagem de leitos**.</font>
                """, unsafe_allow_html=True)


    st.write("""<font size=2> Curvas de casos COVID-19 outros países </font>
                [[+](https://flattening-the-curve.commutatus.com/)]
                """, unsafe_allow_html=True)



########################################################################
# Gráfico genérico de detalhamento de infectados
########################################################################
def plotting_seirs_plus_g2():

    # print('config.is_state: ', config.is_state)

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
                       dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
                       # dtype={"E": int},    # Ler a coluna 'E' como inteiro (Erro)
                       # usecols=['S','E', 'I'],  # Ler apenas essas colunas (Erro)
                       )
    # Preview the first 5 lines of the loaded data
    # print('data.head(): ', data.head())
    # print('data: ', data)
    # st.line_chart(data)

    # if st.button("Rodar modelo SEIR de infectados"):

    # chart_data = pd.DataFrame(data, columns=['S'])
    chart_data = pd.DataFrame(data)
    # st.line_chart(chart_data)
    # chart = st.line_chart(chart_data)
    chart = st.line_chart(chart_data[:1]) # < Tipo de gráfico: Linha
    # chart = st.area_chart(chart_data[:1]) # < Tipo de gráfico: Área

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
        time.sleep(0.001)

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    # st.button("Rodar modelo Geral")

    progress_bar.empty()



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
#                        dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
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
#                        dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
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
#                        dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
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
#                        dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
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
#                        dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
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
#                        dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
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
#                        dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
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
#                        dtype={"(S) Suscetiveis": int},    # Ler a coluna 'S' como inteiro
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
