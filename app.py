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

import inspect
import textwrap
from collections import OrderedDict

import streamlit as st
from streamlit.logger import get_logger
# from streamlit.hello import demos
import intro
import rt
# import realtimert
import diagnostico
import solucao
import modelagem

LOGGER = get_logger(__name__)

# Dictionary of
# demo_name -> (demo_function, demo_description)
OPCAOGERAL = OrderedDict(
    [
        ("-", (intro.intro, None)),
        ("Casos de COVID-19",(diagnostico.mapa_grafico_de_casos_estado,
                    """Diagnóstico Mapa e Grafico dos Estados""",),),
        ("Modelagem da transmissão", (solucao.seir_hosp_estado,
                    """Proposta de Solução SEIRS e Modelo Dinâmico de Leitos""",),),
        ("Modelagem de leitos", (modelagem.leitos_estado,
                    """Proposta de Modelagem de Leitos para Planejamento
                    de Capacidade Hospitalar""",),),
        # ("No Reprodução efetivo Rt", (realtimert.run_rt, None)),
        ("No Reprodução efetivo Rt", (rt.intro, None)),
    ]
)

DIAGESTMUN = OrderedDict(
    [
        ("Estados",(diagnostico.mapa_grafico_de_casos_estado,
                    """Diagnóstico Mapa e Grafico dos Estados""",),),
        # ("Municípios",(diagnostico.mapa_grafico_de_casos_municipio,
        #                """Diagnóstico Mapa e Grafico dos Municípios""",),),
        ("Municípios",(diagnostico.mapa_grafico_de_casos_municipio,
                       """Diagnóstico Grafico dos Municípios""",),),
    ]
)

SOLESTMUN = OrderedDict(
    [
        ("Estados",(solucao.seir_hosp_estado,
                    """Proposta de Solução SEIRS para Estados""",),),
        ("Municípios",(solucao.seir_hosp_municipio,
                       """Proposta de Solução SEIRS para Municípios""",),),
    ]
)

LEIESTMUN = OrderedDict(
    [
        ("Estados",(modelagem.leitos_estado,
                    """Modelagem de leitos para Estados""",),),
        # ("Municípios",(modelagem.leitos_municipio,
        #                """Modelagem de leitos Municípios""",),),
    ]
)

def run():

    option_name = st.sidebar.selectbox("Selecione uma opção",
                                     list(OPCAOGERAL.keys()), 0)
    opcao = OPCAOGERAL[option_name][0]

    # show_code = st.sidebar.checkbox("Show code", False)
    # if option_name == "No Reprodução efetivo Rt":
    if option_name == "-":
        show_code = False
        st.write("# Combate ao Coronavírus no Brasil")

    # else:
    #     show_code = st.sidebar.checkbox("Show code", True)
    #     st.markdown("# %s" % option_name)
    #     description = OPCAOGERAL[option_name][1]
    #     if description:
    #         st.write(description)
    #     # Clear everything from the intro page.
    #     # We only have 4 elements in the page so this is intentional overkill.
    #     for i in range(10):
    #         st.empty()


    elif option_name == 'Casos de COVID-19':
        option_name = st.sidebar.selectbox("Selecione uma opção",
                                         list(DIAGESTMUN.keys()), 0)
        opcao = DIAGESTMUN[option_name][0]

        show_code = False
        # show_code = st.sidebar.checkbox("Show code", True)

        st.markdown("# %s" % option_name)
        description = DIAGESTMUN[option_name][1]
        if description:
            st.write(description)
        # Clear everything from the intro page.
        # We only have 4 elements in the page so this is intentional overkill.
        for i in range(10):
            st.empty()

    elif option_name == 'Modelagem da transmissão':
        option_name = st.sidebar.selectbox("Selecione uma opção",
                                         list(SOLESTMUN.keys()), 0)
        opcao = SOLESTMUN[option_name][0]

        show_code = False
        # show_code = st.sidebar.checkbox("Show code", True)

        st.markdown("# %s" % option_name)
        description = SOLESTMUN[option_name][1]
        if description:
            st.write(description)
        # Clear everything from the intro page.
        # We only have 4 elements in the page so this is intentional overkill.
        for i in range(10):
            st.empty()

    elif option_name == 'Modelagem de leitos':
        option_name = st.sidebar.selectbox("Selecione uma opção",
                                         list(LEIESTMUN.keys()), 0)
        opcao = LEIESTMUN[option_name][0]

        show_code = False
        # show_code = st.sidebar.checkbox("Show code", True)

        st.markdown("# %s" % option_name)
        description = LEIESTMUN[option_name][1]
        if description:
            st.write(description)
        # Clear everything from the intro page.
        # We only have 4 elements in the page so this is intentional overkill.
        for i in range(10):
            st.empty()

    elif option_name == "No Reprodução efetivo Rt":
        show_code = False

    opcao()

    if show_code:
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(opcao)
        st.code(textwrap.dedent("".join(sourcelines[1:])))

    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style,
                unsafe_allow_html=True)

if __name__ == "__main__":
    run()


#######################################################################
# Código demo de backup
#######################################################################
# def run():
#     demo_name = st.sidebar.selectbox("Selecione uma opção",
#                                      list(OPCAOGERAL.keys()), 0)
#     demo = OPCAOGERAL[demo_name][0]
#
#     if demo_name == "—":
#         show_code = False
#         st.write("# Combate ao Coronavírus no Brasil")
#     # else:
#     #     show_code = st.sidebar.checkbox("Show code", True)
#     #     st.markdown("# %s" % demo_name)
#     #     description = OPCAOGERAL[demo_name][1]
#     #     if description:
#     #         st.write(description)
#     #     # Clear everything from the intro page.
#     #     # We only have 4 elements in the page so this is intentional overkill.
#     #     for i in range(10):
#     #         st.empty()
#
#     elif demo_name == 'Diagnóstico':
#         demo_name = st.sidebar.selectbox("Selecione uma opção",
#                                          list(DIAGESTMUN.keys()), 0)
#         demo = DIAGESTMUN[demo_name][0]
#
#         show_code = False
#         # show_code = st.sidebar.checkbox("Show code", True)
#
#         st.markdown("# %s" % demo_name)
#         description = DIAGESTMUN[demo_name][1]
#         if description:
#             st.write(description)
#         # Clear everything from the intro page.
#         # We only have 4 elements in the page so this is intentional overkill.
#         for i in range(10):
#             st.empty()
#
#     elif demo_name == 'Solução':
#         demo_name = st.sidebar.selectbox("Selecione uma opção",
#                                          list(SOLESTMUN.keys()), 0)
#         demo = SOLESTMUN[demo_name][0]
#
#         show_code = False
#         # show_code = st.sidebar.checkbox("Show code", True)
#
#         st.markdown("# %s" % demo_name)
#         description = SOLESTMUN[demo_name][1]
#         if description:
#             st.write(description)
#         # Clear everything from the intro page.
#         # We only have 4 elements in the page so this is intentional overkill.
#         for i in range(10):
#             st.empty()
#
#     demo()
#
#     if show_code:
#         st.markdown("## Code")
#         sourcelines, _ = inspect.getsourcelines(demo)
#         st.code(textwrap.dedent("".join(sourcelines[1:])))
#
#
# if __name__ == "__main__":
#     run()
#######################################################################
