'''
Arquivo para guardar funções
'''
import Samantha_estimator as estimator
import ipdb
import pandas as pd
import plotly.graph_objects as go

def export_BR(casosEstimados, casosBR):
    writer = pd.ExcelWriter('casos_BR.xlsx', engine='xlsxwriter')
    casosEstimados.to_excel(writer, sheet_name='Casos Estados')
    casosBR.to_excel(writer, sheet_name='Casos País')
    writer.save()
    
def plot_BR(casosBR):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=casosBR.index, y=casosBR['Media_Movel'],
                        mode='lines',
                        name='Historical Cases of Infection'))
    fig.add_trace(go.Scatter(x=casosBR.index, y=casosBR['casos previstos'],
                        mode='lines',
                        name='Estimated cases of infection (SEIRS Model)'))
    fig.update_layout(legend_font_size=30, legend = dict(yanchor="top",
    y=0.99,xanchor="left",x=0.01))
    fig.update_xaxes(showgrid=False, gridwidth=0, gridcolor='White')
    fig.update_yaxes(showgrid=False, gridwidth=0, gridcolor='White')
    fig.update_layout(font_size=30)
    fig.update_layout(title_font_family = 'Times New Roman', xaxis_title="Days",
    yaxis_title="Confirmed Cases")
    fig.update_xaxes(title_font_family="Times New Roman")
    fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

   
    
    fig.show()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=casosBR.index, y=casosBR['Media_Movel_Mortes'],
                        mode='lines',
                        name='Historical Cases of Deaths'))
    fig.add_trace(go.Scatter(x=casosBR.index, y=casosBR['Mortes_Previstas_CALC'],
                        mode='lines',
                        name='Estimated Cases of Deaths'))
    fig.update_layout(legend_font_size=30, legend = dict(yanchor="top",
    y=0.99,xanchor="left",x=0.01))
    fig.update_layout(legend_font_size=30)
    fig.update_layout(font_size=30)
    fig.show()