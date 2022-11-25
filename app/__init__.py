#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys # Importa modulos do sistema
import os # Local (path) do sistema
import pathlib  # Local do diretório (pasta)

# from pathlib import Path
# print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

# For relative imports to work in Python 3.6
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from utils.states_info import states_codes
from utils.states_info import states_mun
from utils.states_info import states_pop
from utils.states_info import states_name
from utils.states_info import load_states
from utils.states_info import read_est_cases
from utils.states_info import states_pop_cases_deaths

from utils.mun_info import load_municipalities
from utils.mun_info import read_mun_cases
from utils.mun_info import mun_pop_cases_deaths
from utils.folders import cd

from seir.models import custom_exponential_graph
from seir.models import plot_degree_distn

from seir.seirsbr import modelo_SEIR
from seir.seirsbr import modelo_SEIRS
from seir.seirsbr import modelo_SEIRS_plus
from seir.seirsbr import modelo_SEIR_Network_base
from seir.seirsbr import modelo_SEIRS_network

import config

from utils.file_info import file_info

__all__ = ['states_codes', 'states_mun', 'states_pop', \
           'states_pop_cases_deaths', 'states_name', \
           'load_states', 'read_est_cases', 'load_municipalities',\
           'read_mun_cases', 'mun_pop_cases_deaths', \
           'custom_exponential_graph', 'plot_degree_distn', 'cd',\
           'modelo_SEIR', 'modelo_SEIRS', 'modelo_SEIRS_plus', \
           'modelo_SEIR_Network_base', 'modelo_SEIRS_network', \
           'config', 'file_info']
