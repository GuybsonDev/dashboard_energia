import streamlit as st
import pandas as pd 
import altair as alt
from streamlit_tags import st_tags_sidebar


#Realizando as configurações iniciais do site 
st.set_page_config(page_title= 'Dashboard', layout='wide', initial_sidebar_state='collapsed', page_icon='image.png')

#Setando um header para o dashboard
botao_dataframe = st.toggle('_Visualizar :blue[dataframe]_')

#Criando a variavel com os meses ordenados
meses_ordenados = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

#Criação da barra lateral
with st.sidebar:
    #Setando a imagem da barra lateral
    st.image('image.png')
    st.divider()

    #Selecbox para escolher a cidade que deseja visualizar
    cidade_selecionada = st.selectbox('Cidade visualizada no G1',['Ituiutaba','Monte Carmelo','Patos de Minas','Uberlândia']) 

    #Criando uma Tagbar para escolher os meses de visualização das médias
    meses_selecionados = st_tags_sidebar(
    label='_Filtragem de médias_',
    text='Selecione os meses',
    value=['Janeiro'],
    suggestions=meses_ordenados,
    maxtags = 12)

    st.divider()

#Realizando a importação de todos os dados 
dados = pd.read_csv('consumo_de_energia_eletrica_2022.csv', encoding='latin1')

#Realizando a conversão dos dados para um dataframe
df_main = pd.DataFrame(dados)
df_main = df_main['Cidade;Campus/Unidade;Ano;Mes;Quantidade'].str.split(';', expand=True)

#Criando as colunas ordenadas com ''
df_main.columns = ['Cidade', 'Campus', 'Ano', 'Mes', 'kwh']

# Converter a coluna 'kwh' para numérica
df_main['kwh'] = pd.to_numeric(df_main['kwh'], errors='coerce')

#Alterando na coluna de segunda a janeiro sem perder a ordenação
df_main['Mes'] = pd.Categorical(df_main['Mes'], categories=meses_ordenados, ordered=True)

# Agrupar os dados por 'Campus' e calcular a média de 'kwh'
df_media_kwh = df_main.groupby('Campus', as_index=False)['kwh'].mean()

#Agrupando os dados por 'Cidade e calculando a média de 'k2h'
df_media_kwh_cidade = df_main.groupby('Cidade', as_index=False)['kwh'].mean()

# Renomear a coluna do campus para refletir que é a média de 'kwh'
df_media_kwh.rename(columns={'kwh': 'media_kwh'}, inplace=True)

# Renomear a coluna  da cidade para refletir que é a média de 'kwh'
df_media_kwh_cidade.rename(columns={'kwh': 'media_kwh'}, inplace=True)

# Ajustar o número de casas decimais do daframe campus
df_media_kwh['media_kwh'] = df_media_kwh['media_kwh'].round(1)

#Ajustando o número de casas decimais do dataframe cidade
df_media_kwh_cidade['media_kwh'] = df_media_kwh_cidade['media_kwh'].round(1)

#Definindo o dataframe que sera visualizado
df_visual = df_main

num_linhas_visiveis = 5
altura_linha = 30  # Ajuste a altura da linha conforme necessário
altura_total = num_linhas_visiveis * altura_linha

if botao_dataframe:
    # Exibir tabela ajustada automaticamente
    st.dataframe(df_visual, use_container_width=True, height=altura_total)

# Filtrar o DataFrame pelos meses solicitados
df_meses = df_main[df_main['Mes'].isin(meses_selecionados)]


# Encontrar o índice da linha com o valor máximo em 'kwh'
idx_max = df_meses['kwh'].idxmax()

# Encontrar o índice da linha com o valor mínimo em 'kwh'
idx_min= df_meses['kwh'].idxmin()

# Obter a linha correspondente ao valor máximo
campus_max_kwh = df_meses.loc[idx_max]

#Obter a linha correspondente ao valor máximo
campus_min_kwh = df_meses.loc[idx_min]

# Filtrar o DataFrame com base na cidade selecionada
df_filtrado = df_main[df_main['Cidade'] == cidade_selecionada]

# Calcular a média da coluna 'quantidade' para cada mês solicitado -> apenas coluna mes e kwh
medias_geral = df_meses.groupby('Mes')['kwh'].mean()

#Calculando a media de todas cidades em todos os meses do kwh
medias_todas_cidades_kwh = df_main['kwh'].mean()

#Convertendo a media para casas decimais solicitadas
medias_todas_cidades_kwh = (round(medias_todas_cidades_kwh, 1))

#Convertendo a media das cidades para string
medias_todas_cidades_kwh_str = str(medias_todas_cidades_kwh)

# Calcular a média da coluna 'kwh' para os meses solicitados
media_kwh = medias_geral.mean()

#Convertendo a media para casas decimais solicitadas
media_kwh = (round(media_kwh, 1))

#Calculando os valores e dividindo por 100 
media_final_kwh = (media_kwh / medias_todas_cidades_kwh) * 100 -100

#Convertendo a media geral para casas decimais solicitadas
media_final_kwh = (round(media_final_kwh, 1))

#Convertendo para string para ser mostrada na coluna e adicionando a porcentagem
media_final_kwh = str(media_final_kwh) + '%'

#Tratando o kwd do campus com maior consumo para adição de %
porcentagem_campus_maior = (campus_max_kwh['kwh'] / media_kwh) * 100 -100 
porcentagem_campus_maior = (round(porcentagem_campus_maior, 1))
porcentagem_campus_maior = str(porcentagem_campus_maior) + '%'

#Tratando o kwd do campus com maior consumo para adição de %
porcentagem_campus_menor = (campus_min_kwh['kwh'] / media_kwh) * 100 -100 
porcentagem_campus_menor = (round(porcentagem_campus_menor, 1))
porcentagem_campus_menor = str(porcentagem_campus_menor) + '%'

#Injeção de CSS para configurar a largura da barra lateral
st.markdown("""
    <style>
    .st-emotion-cache-1itdyc2, .eczjsme18 {
        width: 250px !important;  
        flex-shrink: 0 !important; 
        box-sizing: border-box !important;
    }
    </style>
    """, unsafe_allow_html=True)

#Criando colunas
col1, col2, col3 = st.columns([2,2,1])

with col3:
    botao_uberlandia = st.toggle('Uberlândia')
    st.subheader('_Dados em kWh_', divider='rainbow')
    st.metric('_Media geral_', value=medias_todas_cidades_kwh, delta= '0.0%')
    st.metric('_Media meses solicitados_', value=media_kwh, delta=media_final_kwh, help='Média geral: '+ medias_todas_cidades_kwh_str )
    st.metric('Maior consumo:' + campus_max_kwh['Campus'], value=campus_max_kwh['kwh'], delta=porcentagem_campus_maior)
    st.metric('Menor consumo:' + campus_min_kwh['Campus'], value=campus_min_kwh['kwh'], delta=porcentagem_campus_menor)
    
#Configurando a primeira coluna
with col1:

    # Criar o gráfico de barras horizontal
    chart = alt.Chart(df_media_kwh_cidade).mark_bar().encode(
    y=alt.Y('Cidade:O', title='Cidade', sort='-x'),  # Ordenar pelo valor de 'media_kwh'
    x=alt.X('media_kwh:Q', title='Média')  # Usar a coluna 'media_kwh'
    ).properties(
        title='G1: Consumo médio de kwh por Cidade'
    )

    # Mostrar o gráfico no Streamlit
    st.altair_chart(chart, use_container_width=True)

    # Pivotar o DataFrame para que 'Mes' seja o índice e 'Campus/Unidade' as colunas
    df_pivot_grafico1 = df_filtrado.pivot_table(index='Mes', columns=['Campus'], values='kwh', aggfunc='sum')

     #Converter a pivot table para formato longo para usar com Altair
    df_long = df_pivot_grafico1.reset_index().melt(id_vars='Mes', var_name='Campus', value_name='kwh')

    # Definir uma paleta de cores azul para mostrar nos gráficos
    blue_palette = [
        "#0000FF",  # Azul puro
        "#1E90FF",  # Azul dodger
        "#4682B4",  # Azul aço
        "#4169E1",  # Azul royal
        "#87CEEB",  # Azul céu
        "#ADD8E6"   # Azul claro
    ]

    # Criar o gráfico de barras usando Altair
    chart = alt.Chart(df_long).mark_bar().encode(
        x=alt.X('Mes:N', sort=meses_ordenados, title= 'Mês'),
        y='kwh:Q',
        color=alt.Color('Campus:N', scale=alt.Scale(domain=df_long['Campus'].unique(), range=blue_palette), legend=alt.Legend(columns=2, title='Campus/Unidade')),
        tooltip=['Mes', 'Campus', 'kwh']
    ).properties(
        width=400,  # Ajuste a largura do gráfico conforme necessário
        height=550, # Ajuste a altura do gráfico conforme necessário
        title=f'G3: Consumo de kWh por Campus em {cidade_selecionada}'
    ).configure_axis(
        labelAngle=0
    ).configure_legend(
        orient='bottom',
        columns=2,
        titleFontSize=12,
        labelFontSize=10,
        labelLimit=100,
        symbolLimit=30,
        symbolSize=50
    )

    # Criar um gráfico de barras com o Streamlit
    st.altair_chart(chart, use_container_width=True)

with col2:

    if botao_uberlandia == False:
        # Remover 'Uberlândia' da coluna 'cidade'
        df_main = df_main[df_main['Cidade'] != 'Uberlândia']

    #Pivotar o dataframe para que mes seja o indice e 'cidade' as colunas  
    df_pivot_grafico2 = df_main.pivot_table(index='Mes', columns=['Cidade'], values='kwh', aggfunc='sum')

    # Converter a pivot table para formato longo para usar com Altair
    df_long_grafico2 = df_pivot_grafico2.reset_index().melt(id_vars='Mes', var_name='Cidade', value_name='kwh')

        # Criar o gráfico de linhas usando Altair
    line_chart = alt.Chart(df_long_grafico2).mark_line().encode(
        x=alt.X('Mes:N', sort=meses_ordenados, title='Mês', axis=alt.Axis(labelAngle=0, tickCount=2)),  # Ajusta a rotação e número de ticks no eixo X
        y=alt.Y('kwh:Q', title='kWh'),
        color=alt.Color('Cidade:N', scale=alt.Scale(domain=df_long_grafico2['Cidade'].unique(), range=blue_palette), legend=alt.Legend(columns=2, title='Cidades')),
        tooltip=['Mes', 'Cidade', 'kwh']
    ).properties(
        width=400,  # Ajuste a largura do gráfico conforme necessário
        height=400, # Ajuste a altura do gráfico conforme necessário
        title='G2: Consumo de kWh por Cidade'
    )

    # Adicionar os círculos nas pontas das linhas
    circle_chart = alt.Chart(df_long_grafico2).mark_circle(size=60).encode(
    x=alt.X('Mes:N', sort=meses_ordenados),
    y=alt.Y('kwh:Q'),
    color=alt.Color('Cidade:N', scale=alt.Scale(domain=df_long_grafico2['Cidade'].unique(), range=blue_palette)),
    tooltip=['Mes', 'Cidade', 'kwh']
    )

    # Configurações adicionais
    final_chart = (line_chart + circle_chart).configure_axis(
        labelAngle=0
    ).configure_legend(
        orient='bottom',
        columns=3,
        titleFontSize=12,
        labelFontSize=10,
        labelLimit=100,
        symbolLimit=5,
        symbolSize=50,
        labelPadding=0,
        titlePadding=0,
        padding=0
    )

    # Mostrar o gráfico ajustado ao container
    st.altair_chart(final_chart, use_container_width=True)

    # Criar o gráfico de barras horizontal
    chart1 = alt.Chart(df_media_kwh).mark_bar().encode(
    y=alt.Y('Campus:O', title='Campus', sort='-x'),  # Ordenar pelo valor de 'media_kwh'
    x=alt.X('media_kwh:Q', title='Média')  # Usar a coluna 'media_kwh'
    ).properties(
        title='G4: Consumo médio de kwh por campus',
        width=400,  # Ajuste a largura do gráfico conforme necessário
        height=300, # Ajuste a altura do gráfico conforme necessário
    )

    # Mostrar o gráfico no Streamlit
    st.altair_chart(chart1, use_container_width=True)
    

