# importing core
# aqui empacotamos as funções que dá pra achar no código do Kevin Systrom
from core import run_full_model, load_data, plot_rt, plot_standings

# imports básicos
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# importando joblib para rodar em paralelo
from joblib import Parallel, delayed

# para plots com uma melhor resolução
# %config InlineBackend.figure_format = 'retina'

### parâmetros ###

# númreo de cores para paralelizar modelo nos estados
N_JOBS = -1

### reading data ###
# lendo do repositório do Wesley Cota
# city_df, state_df = load_data()
state_df = load_data()

# para a análise, vamos usar somente novos casos confirmados
# city_df = city_df['confirmed_new']
state_df = state_df['confirmed_new']

print('state_df: ', state_df)

### running posteriors ###
with Parallel(n_jobs=N_JOBS) as parallel:
    results = parallel(delayed(run_full_model)(grp[1], sigma=0.01)
                       for grp in state_df.groupby(level='state'))

final_results = pd.concat(results)


def plot_rt_states():

    ### plotting - Rt vs time for all states ###

    # number of columns and rows for plotting
    N_COLS = 4
    N_ROWS = int(np.ceil(len(results) / N_COLS))

    # opening figure
    fig, axes = plt.subplots(nrows=N_ROWS, ncols=N_COLS,
                             figsize=(15, N_ROWS*3), dpi=90)

    # loop for several states
    for i, (state_name, result) in enumerate(final_results.groupby('state')):
        plot_rt(result, axes.flat[i], state_name)

    # saving figure
    fig.tight_layout()
    fig.set_facecolor('w')
    fig.savefig('./images/Rt-dos-estados.png')
    # plt.show()


### plotting - state comparison ###
mr = final_results.groupby(level=0)[['ML', 'High_90', 'Low_90']].last()
mr.sort_values('ML', inplace=True)
plot_standings(mr, figsize=(13, 5))


### ordering by worst case ##
mr.sort_values('High_90', inplace=True)
plot_standings(mr, figsize=(13, 5))


BRAZIL_STATES = {
  'AC': 'Acre',
  'AL': 'Alagoas',
  'AP': 'Amapá',
  'AM': 'Amazonas',
  'BA': 'Bahia',
  'CE': 'Ceará',
  'DF': 'Distrito Federal',
  'ES': 'Espírito Santo',
  'GO': 'Goiás',
  'MA': 'Maranhão',
  'MT': 'Mato Grosso',
  'MS': 'Mato Grosso do Sul',
  'MG': 'Minas Gerais',
  'PA': 'Pará',
  'PB': 'Paraíba',
  'PR': 'Paraná',
  'PE': 'Pernambuco',
  'PI': 'Piauí',
  'RJ': 'Rio de Janeiro',
  'RN': 'Rio Grande do Norte',
  'RS': 'Rio Grande do Sul',
  'RO': 'Rondônia',
  'RR': 'Roraima',
  'SC': 'Santa Catarina',
  'SP': 'São Paulo',
  'SE': 'Sergipe',
  'TO': 'Tocantins',
  'Brazil': 'Brasil',
}


for STATE_NAME in list(BRAZIL_STATES.keys()):

    # STATE_NAME = 'MG'

    series = state_df.loc[lambda x: x.index.get_level_values(0) == STATE_NAME]

    result = run_full_model(series, sigma=0.01)

    fig, ax = plt.subplots(figsize=(800/72, 450/72), dpi=90)

    plot_rt(result, ax, STATE_NAME)
    fig.set_facecolor('w')
    # ax.set_title(f'Real-time $R_t$ for {STATE_NAME}')
    ax.set_title(f'$R_t$ em tempo real para {STATE_NAME}')
    rt_state = 'Rt-' + STATE_NAME
    fig.savefig('./images/' + rt_state)
    print(f'Gerando Rt de {STATE_NAME}...')
    plt.close()

    # rtAllStates = './images/' + 'Rt-dos-estados.png'
    # rtStatesComparison = './images/Rt-state-comparison.png'
    #
    # if os.path.isfile(rtAllStates):
    #     print(f"Removendo {rtAllStates}...")
    #     os.remove(rtAllStates)
    #
    # if os.path.isfile(rtStatesComparison):
    #     print(f"Removendo {rtStatesComparison}...")
    #     os.remove(rtStatesComparison)
    #
    # for STATE_NAME in list(BRAZIL_STATES.keys()):
    #     rt_state = './images/' + 'Rt-' + STATE_NAME + '.png'
    #     # print("rt_state: ", rt_state)
    #     if os.path.isfile(rt_state):
    #         print(f"Removendo {rt_state}...")
    #         os.remove(rt_state)
