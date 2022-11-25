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
import os # Local (path) do sistema
import sys # Importa modulos do sistema
import pathlib  # Local do diretório (pasta)

from diag_graf_casos import graficos_de_casos_covid_nos_estados
from diag_graf_casos import graficos_de_casos_covid_nos_municipios
from diag_mapas import mapa_de_casos_covid_nos_estados
from diag_mapas import mapa_de_casos_covid_nos_municipios


def mapa_grafico_de_casos_estado():
    mapa_de_casos_covid_nos_estados()
    graficos_de_casos_covid_nos_estados()


def mapa_grafico_de_casos_municipio():
    # mapa_de_casos_covid_nos_municipios()
    graficos_de_casos_covid_nos_municipios()
