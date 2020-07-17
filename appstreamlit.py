# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 13:22:53 2020

"""


import pandas as pd
import streamlit as st
import altair as alt
from altair.expr import datum


@st.cache
def load_data():
    df = pd.read_csv("dados_covid.zip" , sep=",")
    return df

def countsintomas(sintomas_selected, sintomas):
    dados = dados_covid
    for i in sintomas:
        if i in sintomas_selected:
            dados = dados[dados[i]==1]
        else:
            dados = dados[dados[i]==0]   
    return dados

st.title ("Análise Exploratória - Casos Covid")
st.write("Esta análise consite em analisar a relação entre sintomas e possíveis outros parâmetros com casos confirmados, a fim detentar predizer através de algoritmo de machine learning qual a chance de uma pessoa estar contaminada com coronavírus.")
st.write("O dataset utilizado foi a base de dados epidemiológicos de SG (Síndrome Gripal) de casos suspeitos de COVID-19, disponibilizados no endereço: https://opendatasus.saude.gov.br/dataset/casos-nacionais")
st.image('imagem_covid19.png')

dados_covid = load_data()

def main():

    #st.write(pd.value_counts(dados_covid["resultadoTeste"]))

    st.sidebar.title('HACKATHON 1')
    st.sidebar.subheader('Análise dados COVID-19')


    filtro_coluna = st.sidebar.selectbox('Selecione o filtro', ('Dados Gerais' , 'Idade', 'Sexo', 'Sintomas'))

    if filtro_coluna:

        if filtro_coluna == 'Dados Gerais':
            st.write(dados_covid.head(1000))
            if st.checkbox("Mostrar colunas"):
                  st.write(dados_covid.count())
              
        
        if filtro_coluna == 'Sexo':
            st.subheader('Sexo por resultado do teste')
            sexo_barras = alt.Chart(dados_covid ,  width = 200).mark_bar().encode(
            alt.X('sexo:O' , axis=alt.Axis(title='')),
            alt.Y('count():Q'),
            alt.Column('resultadoTeste:O'),
            color = alt.Color('sexo:N', scale=alt.Scale(range=["#EA98D2", "#659CCA"])),
            tooltip = 'count()'
            ).interactive()
            st.altair_chart(sexo_barras)
    #        count_sexo = pd.value_counts(dados_covid['sexo'])color=alt.Color('gender:N', scale=alt.Scale(range=["#EA98D2", "#659CCA"]))
    #        st.write(count_sexo)
    #        st.bar_chart(count_sexo)


        if filtro_coluna == 'Idade':
            st.markdown('Describe da coluna Idade')
            st.write(dados_covid.idade.describe())
            st.subheader('Idade por resultado teste')
            idade_barras = alt.Chart(dados_covid ,  width = 200).mark_bar().encode(
            alt.X('idade' , bin=alt.Bin(maxbins=20)),
            alt.Y('count():Q') , alt.Column('resultadoTeste:O') , color='resultadoTeste', 
            tooltip = ['idade' , 'count()']
            ).transform_filter(
            alt.FieldRangePredicate(field='idade', range=[0, 120])
            ).interactive()
            st.altair_chart(idade_barras , use_container_width=True)

            idade_line = alt.Chart(dados_covid , width = 600).mark_line().encode(
            x = 'idade',
            y = 'count():Q',
            color='resultadoTeste:O'
            ).transform_filter(
            alt.FieldRangePredicate(field='idade', range=[0, 100])
            )
            st.altair_chart(idade_line)
            
            
        if filtro_coluna == 'Sintomas':
            st.subheader('Sintomas relatados')
            sintomas = dados_covid.columns[4:]
            df_sintomas = dados_covid[sintomas].sum().reset_index()
            df_sintomas.columns = ['sintoma', 'count']
            st.write(df_sintomas)
            sintomas_bar = alt.Chart(df_sintomas , width= 700).mark_bar().encode(x = 'sintoma' , y = 'count', 
            tooltip = ['count']
            ).interactive()
            st.write("\n\n")
            st.altair_chart(sintomas_bar)
            
            st.subheader('Sintomas por resultado do teste')
            grouped = dados_covid.groupby(['resultadoTeste'])[sintomas].sum()
            st.write(grouped)
            st.write("\n\n\n")
            st.bar_chart(grouped)
            
            select = st.multiselect("Selecione combinação de sintomas apresentados", dados_covid.columns[4:].tolist() , default = ["Febre"])
            df_select = countsintomas(select , sintomas)
            df_select
#            st.write("Numero de ocorrências: ", len(df_select.index))
            st.write(df_select.groupby(['resultadoTeste'])[sintomas].sum())
            
            st.markdown('->Número de pessoas que aprensentaram apenas os sintomas selecionados')
                
    st.sidebar.subheader('Grupo 1')
    st.sidebar.markdown('Daniel Santos Pereira')
    st.sidebar.markdown('Fernando Henrique De Brito Borges')
    st.sidebar.markdown('Gláucio Ribeiro Santos')
    st.sidebar.markdown('Rafael Rodrigues dos Santos')

if __name__ == '__main__':
    main()               
