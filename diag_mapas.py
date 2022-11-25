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
import pandas as pd
import pydeck as pdk
from intro import from_data_file
from intro import casos_e_mortes_Brasil


def mapa_de_casos_covid_nos_estados():

    # ######################################################
    # # Mapa dos Municípios com casos
    # df = pd.DataFrame(data=from_data_file("mun_casos.json"),
    #                   columns=["lat", "lon"])
    #
    # st.map(df)  # Mapa de ocorrência de COVID em municípios
    # ######################################################

    # Texto de casos e mortes no Brasil
    casos_e_mortes_Brasil(imprime=True)

    ##################################################
    # Mapa de Estados
    ##################################################
    file_casos = "est_casos.json"

    try:
        ALL_LAYERS = {
            # "Estados": pdk.Layer(
            #     "HexagonLayer",
            #     data=from_data_file(file_casos),
            #     get_position=["lon", "lat"],
            #     radius=150000,
            #     elevation_scale=1000,
            #     elevation_range=[0,100],
            #     auto_highlight=True,
            #     pickable=True,
            #     extruded=True,
            #     coverage=1
            #     ),
            # "Casos": pdk.Layer(
            #      "ScatterplotLayer",
            #      data=from_data_file(file_casos),
            #      get_position=["lon", "lat"],
            #      get_color=[252, 144, 3, 160],
            #      auto_highlight=True,
            #      get_radius="[casospp]",
            #      radius_scale=100,
            #      pickable=True,
            #     ),
            "Mortes": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file(file_casos),
                get_position=["lon", "lat"],
                get_color=[250, 30, 0, 160],
                auto_highlight=True,
                get_radius="[mortes]",
                # radius_scale=5,
                pickable=True,
            ),
            "Casos": pdk.Layer(
                 "HeatmapLayer",
                 data=from_data_file(file_casos),
                 # opacity=0.9,
                 get_position=["lon", "lat"],
                 get_color=[252, 144, 3, 160],
                 aggregation='"MEAN"',
                 get_weight="casos > 0 ? casos : 0",
                ),
            # "Mortes": pdk.Layer(
            #     "HeatmapLayer",
            #     data=from_data_file(file_casos),
            #     # opacity=0.9,
            #     get_position=["lon", "lat"],
            #     get_color=[23, 3, 252, 160],
            #     aggregation='"MEAN"',
            #     get_weight="mortes > 0 ? mortes : 0",
            # ),
            # "Bart Stop Names": pdk.Layer(
            #     "TextLayer",
            #     data=from_data_file(file_casos),
            #     get_position=["lon", "lat"],
            #     get_text="nome",
            #     get_color=[0, 0, 0, 200],
            #     get_size=15,
            #     get_alignment_baseline="bottom",
            # ),
            # "Outbound Flow": pdk.Layer(
            #     "ArcLayer",
            #     data=from_data_file("bart_path_stats.json"),
            #     get_source_position=["lon", "lat"],
            #     get_target_position=["lon2", "lat2"],
            #     get_source_color=[200, 30, 0, 160],
            #     get_target_color=[200, 30, 0, 160],
            #     auto_highlight=True,
            #     width_scale=0.0001,
            #     get_width="outbound",
            #     width_min_pixels=3,
            #     width_max_pixels=30,
            # ),
        }
    except Exception as e:
        st.error(
            """
            **Erro de acesso >> interno << aos dados dos estados.**
            Erro: %s
            """
            % e.reason
        )
        return


    st.sidebar.markdown('### Camadas do mapa')
    selected_layers = [
        layer for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)]
    if selected_layers:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={"latitude": -15.83,
                                "longitude": -47.86,
                                "zoom": 3, "pitch": 50},
            layers=selected_layers,
        ))
    else:
        st.error("Escolha pelo menos uma camada do mapa.")

    st.sidebar.markdown(f"<font size=2>Fontes: </font>[[+](https://covid19br.wcota.me/)] \
    <font size=2>e </font>[[+](https://covid.saude.gov.br/)].", unsafe_allow_html=True)

def mapa_de_casos_covid_nos_municipios():

    # ######################################################
    # # Mapa dos Municípios com casos
    # file_casos = "mun_casos.json"
    # df = pd.DataFrame(data=from_data_file(file_casos),
    # columns=["casos", "mortes", "lat", "lon"])
    #
    # # st.map(df)  # Mapa de ocorrência de COVID em municípios
    # ######################################################

    # Texto de casos e mortes no Brasil
    casos_e_mortes_Brasil(imprime=True)

    ##################################################
    # Mapa de Municípios
    ##################################################

    file_casos = "mun_casos.json"

    try:
        ALL_LAYERS = {
            "Casos": pdk.Layer(
                "HexagonLayer",
                data=from_data_file(file_casos),
                get_position=["lon", "lat"],
                # radius=10000,
                elevation_scale=300,
                elevation_range=[0, 200],
                pickable=True,
                extruded=True,
                auto_highlight=True,
                # coverage=1
                # "ScatterplotLayer",
                # data=from_data_file(file_casos),
                # get_position=["lon", "lat"],
                # get_color=[252, 144, 3, 160],
                # get_radius="[casos]",
                # radius_scale=50,
            ),
            "Mortes": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file(file_casos),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[mortes]",
                # radius_scale=50,
            ),
            # "Bart Stop Names": pdk.Layer(
            #     "TextLayer",
            #     data=from_data_file(file_casos),
            #     get_position=["lon", "lat"],
            #     get_text="nome",
            #     get_color=[0, 0, 0, 200],
            #     get_size=15,
            #     get_alignment_baseline="bottom",
            # ),
            # "Outbound Flow": pdk.Layer(
            #     "ArcLayer",
            #     data=from_data_file("bart_path_stats.json"),
            #     get_source_position=["lon", "lat"],
            #     get_target_position=["lon2", "lat2"],
            #     get_source_color=[200, 30, 0, 160],
            #     get_target_color=[200, 30, 0, 160],
            #     auto_highlight=True,
            #     width_scale=0.0001,
            #     get_width="outbound",
            #     width_min_pixels=3,
            #     width_max_pixels=30,
            # ),
        }
    except Exception as e:
        st.error(
            """
            **Erro de acesso >> interno << aos dados dos municípios.**
            Erro: %s
            """
            % e.reason
        )
        return

    st.sidebar.markdown('### Camadas do mapa')
    selected_layers = [
        layer for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)]
    if selected_layers:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={"latitude": -15.83,
                                "longitude": -47.86,
                                "zoom": 5, "pitch": 50},
            layers=selected_layers,
        ))
    else:
        st.error("Escolha pelo menos uma camada do mapa.")


    st.sidebar.markdown(f"<font size=2>Fontes: </font>[[+](https://covid19br.wcota.me/)] \
    <font size=2>e </font>[[+](https://covid.saude.gov.br/)].", unsafe_allow_html=True)



#########################################################################
# Códigos de execuções anteriores
#########################################################################
# @st.cache
# def from_data_file(filename):
#     fn = filename
#     url = (
#         "https://raw.githubusercontent.com/streamlit/"
#         "streamlit/develop/examples/data/%s" % filename)
#     # return pd.read_json(url)
#     return pd.read_json(fn)
#
# try:
#     ALL_LAYERS = {
#         "Bike Rentals": pdk.Layer(
#             "HexagonLayer",
#             data=from_data_file("bike_rental_stats.json"),
#             get_position=["lon", "lat"],
#             radius=200,
#             elevation_scale=4,
#             elevation_range=[0, 1000],
#             extruded=True,
#         ),
#         "Bart Stop Exits": pdk.Layer(
#             "ScatterplotLayer",
#             data=from_data_file("bart_stop_stats.json"),
#             get_position=["lon", "lat"],
#             get_color=[200, 30, 0, 160],
#             get_radius="[exits]",
#             radius_scale=0.05,
#         ),
#         "Bart Stop Names": pdk.Layer(
#             "TextLayer",
#             data=from_data_file("bart_stop_stats.json"),
#             get_position=["lon", "lat"],
#             get_text="name",
#             get_color=[0, 0, 0, 200],
#             get_size=15,
#             get_alignment_baseline="bottom",
#         ),
#         "Outbound Flow": pdk.Layer(
#             "ArcLayer",
#             data=from_data_file("bart_path_stats.json"),
#             get_source_position=["lon", "lat"],
#             get_target_position=["lon2", "lat2"],
#             get_source_color=[200, 30, 0, 160],
#             get_target_color=[200, 30, 0, 160],
#             auto_highlight=True,
#             width_scale=0.0001,
#             get_width="outbound",
#             width_min_pixels=3,
#             width_max_pixels=30,
#         ),
#     }
# except urllib.error.URLError as e:
#     st.error("""
#         **Erro de acesso aos dados.**
#
#         Tipo de erro: %s
#     """ % e.reason)
#     return
#########################################################################

#########################################################################
# @st.cache
# def from_data_file(filename):
#     fn = filename
#     url = (
#         "https://raw.githubusercontent.com/streamlit/"
#         "streamlit/develop/examples/data/%s" % filename)
#     # return pd.read_json(url)
#     return pd.read_json(fn)
#
# try:
#     ALL_LAYERS = {
#         "Bike Rentals": pdk.Layer(
#             "HexagonLayer",
#             data=from_data_file("bike_rental_stats.json"),
#             get_position=["lon", "lat"],
#             radius=200,
#             elevation_scale=4,
#             elevation_range=[0, 1000],
#             extruded=True,
#         ),
#         "Bart Stop Exits": pdk.Layer(
#             "ScatterplotLayer",
#             data=from_data_file("bart_stop_stats.json"),
#             get_position=["lon", "lat"],
#             get_color=[200, 30, 0, 160],
#             get_radius="[exits]",
#             radius_scale=0.05,
#         ),
#         "Bart Stop Names": pdk.Layer(
#             "TextLayer",
#             data=from_data_file("bart_stop_stats.json"),
#             get_position=["lon", "lat"],
#             get_text="name",
#             get_color=[0, 0, 0, 200],
#             get_size=15,
#             get_alignment_baseline="bottom",
#         ),
#         "Outbound Flow": pdk.Layer(
#             "ArcLayer",
#             data=from_data_file("bart_path_stats.json"),
#             get_source_position=["lon", "lat"],
#             get_target_position=["lon2", "lat2"],
#             get_source_color=[200, 30, 0, 160],
#             get_target_color=[200, 30, 0, 160],
#             auto_highlight=True,
#             width_scale=0.0001,
#             get_width="outbound",
#             width_min_pixels=3,
#             width_max_pixels=30,
#         ),
#     }
# except urllib.error.URLError as e:
#     st.error("""
#         **Erro de acesso aos dados.**
#
#         Tipo de erro: %s
#     """ % e.reason)
#     return
#########################################################################
