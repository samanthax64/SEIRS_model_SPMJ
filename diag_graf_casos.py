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

import urllib.error
import streamlit as st
import os
import sys
import pandas as pd
import altair as alt
from intro import get_EST_data_by_day
from intro import get_MUN_data_by_day


def graficos_de_casos_covid_nos_estados():

    if sys.version_info[0] < 3:
        reload(sys) # noqa: F821 pylint:disable=undefined-variable
        sys.setdefaultencoding("utf-8")

    #############################################################
    # Estados
    #############################################################
    # @st.cache
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
    #     Estados.to_csv('./data/est_casos_t.csv', sep=',', encoding='utf-8')
    #
    #     df = pd.read_csv("./data/est_casos_t.csv")
    #     return df.set_index("Estados")


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

    estados = st.multiselect(
        "Escolha o(s) estado(s)", list(df.index), ["MG"]
    )
    if not estados:
        st.error("Selecione pelo menos um estado.")
        return

    # print('list(df.index): ', list(df.index))
    data = df.loc[estados]
    # print('data: ', data)

    # st.write("### Casos de COVID-19 (notificados)", data.sort_index())

    t_dias = pd.date_range('2020-02-25', periods=T_dias, freq='1D')
    # print(t_dias)
    # print('data: ', data)

    data = data.T.reset_index()
    # print('data: ', data)

    data = pd.melt(data, id_vars=["index"]).rename(
        columns={"index": "Dias", "value": "Casos de COVID-19 (desde 25 Fev)"}
    )
    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.3)
        .encode(
            x="Dias:Q",
            y=alt.Y("Casos de COVID-19 (desde 25 Fev):Q", stack=None),
            color="Estados:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)
    st.write(
    '> Já se passaram ', T_dias, ' dias desde o registro do 1º caso de COVID-19.')
    st.write(
    '> Casos de COVID-19 registrados desde 25/02/2020 até o momento\n'
     '[[+](https://covid19br.wcota.me/)].'
    )
    st.write('---')


def graficos_de_casos_covid_nos_municipios():

    if sys.version_info[0] < 3:
        reload(sys) # noqa: F821 pylint:disable=undefined-variable
        sys.setdefaultencoding("utf-8")

    #############################################################
    # Municipios
    #############################################################
    # @st.cache
    # def get_MUN_data_by_day():
    #     #######################################################################
    #     URL = "https://raw.githubusercontent.com/wcota/covid19br/master/"
    #     df = pd.read_csv(URL + "cases-brazil-cities-time.csv", encoding='utf-8')
    #     df_mun = df.copy()
    #     #######################################################################
    #
    #     #####################################################################
    #     # Casos dos municípios no tempo
    #     #####################################################################
    #     df_mun.drop(columns=['country', 'state', 'ibgeID','newDeaths',
    #                      'deaths', 'newCases'], axis=1, inplace=True)
    #
    #     index_names = df_mun[(df_mun['city'] == 'TOTAL')].index
    #     df_mun.drop(index_names, inplace=True)
    #
    #     index_names = df_mun[(df_mun['city'].str.contains('INDEFINIDA'))].index
    #     df_mun.drop(index_names, inplace=True)
    #
    #     df_mun.reset_index(drop=True, inplace=True)
    #     # df_mun.drop(columns=['date'], axis=1, inplace=True)
    #     df_mun.rename(columns={"city": "Municipios"}, inplace=True)
    #     df_mun.reset_index(inplace=True)
    #     # print('df_mun: ', df_mun)
    #
    #     # https://pandas.pydata.org/docs/user_guide/reshaping.html
    #     Municipios = df_mun.pivot(index='Municipios', columns='date',
    #                           values='totalCases').fillna(0)
    #
    #     Municipios = Municipios.T.reset_index(drop=True).T
    #
    #     # print('Municipios: ', Municipios)
    #     Municipios.to_csv('./data/mun_casos_t.csv', sep=',', encoding='utf-8')
    #     #######################################################################
    #     df = pd.read_csv("./data/mun_casos_t.csv")
    #     return df.set_index("Municipios")


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

    # countries = st.multiselect(
    #     "Choose countries", list(df.index), ["China", "United States of America"]
    # )
    municipios = st.multiselect(
        # "Escolha o(s) município(s)", list(df.index), ["Belo Horizonte/MG","São Paulo/SP"]
        "Escolha o(s) município(s)", list(df.index), ["Belo Horizonte/MG"]

    )
    if not municipios:
        st.error("Selecione pelo menos um município.")
        return

    data = df.loc[municipios]

    # st.write("### Casos de COVID-19 (notificados)", data.sort_index())

    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["index"]).rename(
        columns={"index": "Dias", "value": "Casos de COVID-19 (desde 25 Fev)"}
    )
    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.3)
        .encode(
            x="Dias:Q",
            y=alt.Y("Casos de COVID-19 (desde 25 Fev):Q", stack=None),
            color="Municipios:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)
    st.write(
    '> Já se passaram ', T_dias, ' dias desde o registro do 1º caso de COVID-19.'
    )
    st.write(
    '> Casos de COVID-19 registrados desde 25/02/2020 até o momento\n'
     '[[+](https://covid19br.wcota.me/)].'
    )
    st.write('---')


##################################################################
#
# import sys
# import pandas as pd
# import altair as alt
#
# if sys.version_info[0] < 3:
#     reload(sys) # noqa: F821 pylint:disable=undefined-variable
#     sys.setdefaultencoding("utf-8")
#
# @st.cache
# def get_UN_data():
#     AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
#     df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
#     return df.set_index("Region")
#
# try:
#     df = get_UN_data()
# except urllib.error.URLError as e:
#     st.error(
#         """
#         **This demo requires internet access.**
#
#         Connection error: %s
#     """
#         % e.reason
#     )
#     return
#
# countries = st.multiselect(
#     "Choose countries", list(df.index), ["China", "United States of America"]
# )
# if not countries:
#     st.error("Please select at least one country.")
#     return
#
# data = df.loc[countries]
# data /= 1000000.0
# st.write("### Gross Agricultural Production ($B)", data.sort_index())
#
# data = data.T.reset_index()
# data = pd.melt(data, id_vars=["index"]).rename(
#     columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
# )
# chart = (
#     alt.Chart(data)
#     .mark_area(opacity=0.3)
#     .encode(
#         x="year:T",
#         y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
#         color="Region:N",
#     )
# )
# st.altair_chart(chart, use_container_width=True)
##################################################################

##################################################################
#
# import sys
# import pandas as pd
# import altair as alt
#
# if sys.version_info[0] < 3:
#     reload(sys) # noqa: F821 pylint:disable=undefined-variable
#     sys.setdefaultencoding("utf-8")
#
# @st.cache
# def get_UN_data():
#     AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
#     df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
#     return df.set_index("Region")
#
# try:
#     df = get_UN_data()
# except urllib.error.URLError as e:
#     st.error(
#         """
#         **This demo requires internet access.**
#
#         Connection error: %s
#     """
#         % e.reason
#     )
#     return
#
# countries = st.multiselect(
#     "Choose countries", list(df.index), ["China", "United States of America"]
# )
# if not countries:
#     st.error("Please select at least one country.")
#     return
#
# data = df.loc[countries]
# data /= 1000000.0
# st.write("### Gross Agricultural Production ($B)", data.sort_index())
#
# data = data.T.reset_index()
# data = pd.melt(data, id_vars=["index"]).rename(
#     columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
# )
# chart = (
#     alt.Chart(data)
#     .mark_area(opacity=0.3)
#     .encode(
#         x="year:T",
#         y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
#         color="Region:N",
#     )
# )
# st.altair_chart(chart, use_container_width=True)
##################################################################
