import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Projeto BI - Visualização de Dados")

try:
    df = pd.read_csv('dataset_contabio.csv', sep=';', encoding='latin1')
    #st.write(df.head(15))  # mostra as primeiras 15 linhas 
except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {e}")

if 'df' in locals():
    # coluna 'Data do Contrato ContaBio' esteja no formato datetime
    try:
        df['Data do Contrato ContaBio'] = pd.to_datetime(df['Data do Contrato ContaBio'], errors='coerce')
    except Exception as e:
        st.error(f"Erro ao converter datas: {e}")

    # Removendo valores inválidos 
    df = df.dropna(subset=['Data do Contrato ContaBio'])

    # Criando os dados para os gráficos
    regimes_mais_usados = df.groupby('Regime Tributário')['ID Cliente'].count().sort_values(ascending=True)
    novos_clientes = df.groupby(df['Data do Contrato ContaBio'].dt.year)['ID Cliente'].count().sort_values(ascending=True)
    tipo_negocio = df.groupby('Tipo de Negócio')['ID Cliente'].count().sort_values(ascending=False)

    col1, col2, col3 = st.columns(3)

    with col1:
        grafico1 = px.pie(
            regimes_mais_usados, 
            values=regimes_mais_usados.values, 
            names=regimes_mais_usados.index, 
            title="Clientes por Regime Tributário",
            color_discrete_sequence=['skyblue', 'lightgreen', 'coral', 'gold']
        )
        st.plotly_chart(grafico1, use_container_width=True)

    with col2:
        grafico2 = px.pie(
            novos_clientes, 
            values=novos_clientes.values, 
            names=novos_clientes.index, 
            title="Novos Clientes por Ano",
            color_discrete_sequence=['pink', 'coral', 'gold']
        )
        st.plotly_chart(grafico2, use_container_width=True)

    with col3:
        grafico3 = px.pie(
            tipo_negocio, 
            values=tipo_negocio.values, 
            names=tipo_negocio.index, 
            title="Tipos de Negócio",
            color_discrete_sequence=['orange', 'lightgreen', 'red', 'gold']
        )
        st.plotly_chart(grafico3, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    # Gráfico 1: Clientes por Tipo de Empresa
    with col1:
        empresas_saude = [
            'Clínica Médica', 'Clínica Médica Especializada', 'Clínica Odontológica', 
            'Clinica de Estética', 'Influencer Area da Saúde', 
            'Clínica de Fisioterapia', 'Clínica de Psicologia', 'Laboratório de Exames Clínicos'
        ]
        replacements = {categoria: 'Saúde' for categoria in empresas_saude}
        df['Tipo de Empresa'] = df['Tipo de Empresa'].replace(replacements)
        clientes_por_empresa = df.groupby('Tipo de Empresa')['ID Cliente'].count().sort_values(ascending=True)
        grafico1 = px.bar(
            clientes_por_empresa, 
            x=clientes_por_empresa.values, 
            y=clientes_por_empresa.index, 
            orientation='h', 
            title="Total de Clientes por Tipo de Empresa",
            labels={'x': 'Total de Clientes', 'y': ' '},
            color_discrete_sequence=['purple']
        )
        st.plotly_chart(grafico1, use_container_width=True)

    # Gráfico 2: Leads 
    with col2:
        leads = df.groupby('Fonte do Lead')['ID Cliente'].count().sort_values(ascending=True)
        grafico4 = px.bar(
            leads, 
            x=leads.values, 
            y=leads.index, 
            orientation='h', 
            title="Leads",
            labels={'x': 'Total de Leads', 'y': 'Fonte'},
            color_discrete_sequence=['gray']
        )
        st.plotly_chart(grafico4, use_container_width=True)

    # Gráfico 3:
    with col3:
        df['Endereço de cobrança'] = df['Endereço de cobrança'].str.strip().str.title()
        # Correção 'Sao Paulo' para 'São Paulo'
        df['Endereço de cobrança'] = df['Endereço de cobrança'].replace('Sao Paulo', 'São Paulo')
        cobrancas_por_cidade = df.groupby('Endereço de cobrança').size()
        grafico7 = px.pie(
            cobrancas_por_cidade, 
            values=cobrancas_por_cidade.values, 
            names=cobrancas_por_cidade.index, 
            title="Cobranças por Cidade",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(grafico7, use_container_width=True)
