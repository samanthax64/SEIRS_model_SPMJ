import streamlit as st
import os # Local (path) do sistema
import sys # Importa modulos do sistema
import pathlib  # Local do diretório (pasta)
import numpy as np
import pandas as pd
import json
import csv
from urllib import request
import urllib.error
from seir.utils.folders import cd
# from core import run_full_model, load_data, plot_rt, plot_standings
from core import run_full_model, load_data, plot_rt
from matplotlib import pyplot as plt
# import inspect
# import textwrap
# from collections import OrderedDict
# from streamlit.logger import get_logger
# from streamlit.hello import demos
from intro import get_EST_data
# import diagnostico
# import solucao
# import modelagem
# from joblib import Parallel, delayed  # importando joblib p/ rodar em paralelo


def intro():

    try:
        df = get_EST_data()
        # print('df: ', df)
        # city_df, state_df = load_data()
        state_df = load_data()
        # para a análise, vamos usar somente novos casos confirmados
        # city_df = city_df['confirmed_new']
        state_df = state_df['confirmed_new'].abs()
        # state_df.to_csv('temp.csv')

    except Exception as e:
        st.error(
            """
            **Erro de acesso >> interno << aos dados dos estados.**
            Erro: %s
            """
            % e
        )
        return

    st.markdown("## **Rt em tempo real por estado**")

    st.write("*\"Qualquer sugestão de reduzir as restrições quando Rt > 1.0 \
             é uma decisão explícita de permitir a proliferação do vírus*\". -- Kevin Systrom (2020)")

    # #################################
    # # número de cores para paralelizar modelo nos estados
    # N_JOBS = -1
    #
    # # running posteriors ###
    # with Parallel(n_jobs=N_JOBS) as parallel:
    #     results = parallel(delayed(run_full_model)(grp[1], sigma=0.01)
    #                        for grp in state_df.groupby(level='state'))
    #
    # final_results = pd.concat(results)
    #
    # # plotting - Rt vs time for all states ###
    # # number of columns and rows for plotting
    # N_COLS = 4
    # N_ROWS = int(np.ceil(len(results) / N_COLS))
    #
    # # opening figure
    # fig, axes = plt.subplots(nrows=N_ROWS, ncols=N_COLS,
    #                          figsize=(15, N_ROWS*3), dpi=90)
    #
    # # loop for several states
    # for i, (state_name, result) in enumerate(final_results.groupby('state')):
    #     plot_rt(result, axes.flat[i], state_name)
    #
    # # saving figure
    # fig.tight_layout()
    # fig.set_facecolor('w')
    # fig.savefig('./images/Rt-dos-estados.png')
    #
    # # plotting - state comparison ###
    # mr = final_results.groupby(level=0)[['ML', 'High_90', 'Low_90']].last()
    # mr.sort_values('ML', inplace=True)
    # plot_standings(mr, figsize=(13, 5))
    #
    # # ordering by worst case ##
    # mr.sort_values('High_90', inplace=True)
    # plot_standings(mr, figsize=(13, 5))    #
    # #################################

    estado = st.selectbox(
        # "Escolha o estado", list(df.index), ["MG"]
        "Escolha o estado", list(df.index), 0
    )

    if not estado:
        st.error("Selecione um estado.")
        return

    BRAZIL = {
     "Acre": 'AC',
     "Alagoas": 'AL',
     "Amapá": 'AP',
     "Amazonas": 'AM',
     "Bahia": 'BA',
     "Ceará": 'CE',
     "Distrito Federal": 'DF',
     "Espírito Santo": 'ES',
     "Goiás": 'GO',
     "Maranhão": 'MA',
     "Mato Grosso": 'MT',
     "Mato Grosso do Sul": 'MS',
     "Minas Gerais": 'MG',
     "Pará": 'PA',
     "Paraíba": 'PB',
     "Paraná": 'PR',
     "Pernambuco": 'PE',
     "Piauí": 'PI',
     "Rio de Janeiro": 'RJ',
     "Rio Grande do Norte": 'RN',
     "Rio Grande do Sul": 'RS',
     "Rondônia": 'RO',
     "Roraima": 'RR',
     "Santa Catarina": 'SC',
     "São Paulo": 'SP',
     "Sergipe": 'SE',
     "Tocantins": 'TO',
     "Brasil": 'Brazil',
    }
    # for STATE_NAME in list(BRAZIL_STATES.keys()):

    STATE_NAME = BRAZIL[estado]

    series = state_df.loc[lambda x: x.index.get_level_values(0) == STATE_NAME]

    # print('series: ', series)
    print(f'Gerando Rt de {STATE_NAME}...')

    result = run_full_model(series, sigma=0.01)
    # result = run_full_model(series)
    # result = run_full_model(series, sigma=0.01)
    fig, ax = plt.subplots(figsize=(800/72, 450/72), dpi=90)

    plot_rt(result, ax, STATE_NAME)
    fig.set_facecolor('w')
    # ax.set_title(f'Real-time $R_t$ for {STATE_NAME}')
    ax.set_title(f'$R_t$ em tempo real para {STATE_NAME}')
    rt_state = 'Rt-' + STATE_NAME
    fig.savefig('./images/' + rt_state)
    print('Ok! Gráfico Rt gerado.')
    plt.close()

    # ESTADO = [ i for i in list(BRAZIL_STATES.keys())]
    # print('ESTADO: ', ESTADO)
    # SIGLA = ESTADO[0]
    image_por_estado = './images/' + 'Rt-' + BRAZIL[estado] + '.png'
    if image_por_estado == './images/' + 'Rt-[].png':
        image_por_estado = './images/Rt-Brazil.png'
    else:
        image_por_estado = './images/' + 'Rt-' + BRAZIL[estado] + '.png'

    st.image(image_por_estado, caption='Rt do estado: ' + estado,
             use_column_width=True)

    # print('result: ', result)
    st.dataframe(result, width=5000)

    # st.write('---')
    # image_rt_estados = './images/' + 'Rt-dos-estados.png'
    # st.image(image_rt_estados, caption='Rt dos estados',
    #          use_column_width=True)

    # st.write('---')
    # image_rt_comparisson = './images/' + 'Rt-state-comparison.png'
    # st.image(image_rt_comparisson, caption='Rt comparativo dos estados',
    #          use_column_width=True)

    st.markdown("Fonte: [[+](https://github.com/loft-br/realtime_r0_brazil)]\
                [[+](http://systrom.com/blog/the-metric-we-need-to-manage-covid-19/)]\
                [[+](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0002185)]")
