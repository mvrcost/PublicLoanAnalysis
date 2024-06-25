#%% Frameworks
import pandas as pd
import numpy as np

# Gráficas
import matplotlib.pyplot as plt
import seaborn as sns

# Avisos
import warnings
warnings.filterwarnings('ignore')

#%% Ajustes casas decimais no pandas
pd.options.display.float_format = '{:,.2f}'.format

#%% Layout
sns.set_theme( style='whitegrid')

#%% Leitdura dos dados
Base_Credito = pd.read_csv('../database/Base_Dados - Operacoes Uniao.csv', encoding='latin1', sep=';')
Base_Credito.head()


#%% Info dados
Base_Credito.info()

#%% Transform columns
Base_Credito.columns = [loop.replace(' ', '_' ) for loop in Base_Credito.columns]
Base_Credito.columns


#%% Convert string to number
Base_Credito.Valor = Base_Credito.Valor.apply(lambda loop : loop.replace('.',''))
Base_Credito.Valor = Base_Credito.Valor.apply(lambda loop : loop.replace(',','.'))
Base_Credito.Valor = pd.to_numeric( Base_Credito.Valor )
Base_Credito.Valor.head()

#%% Convert string to date
Base_Credito.Data = pd.to_datetime( Base_Credito.Data )
Base_Credito.Data 

#%% Campos únicos
Base_Credito.nunique()



#%% Enriquecimento

# Dicionario De Para
uf_to_regiao = {
    'AC': 'Norte',
    'AL': 'Nordeste',
    'AM': 'Norte',
    'AP': 'Norte',
    'BA': 'Nordeste',
    'CE': 'Nordeste',
    'DF': 'Centro-Oeste',
    'ES': 'Sudeste',
    'GO': 'Centro-Oeste',
    'MA': 'Nordeste',
    'MG': 'Sudeste',
    'MS': 'Centro-Oeste',
    'MT': 'Centro-Oeste',
    'PA': 'Norte',
    'PB': 'Nordeste',
    'PE': 'Nordeste',
    'PI': 'Nordeste',
    'PR': 'Sul',
    'RJ': 'Sudeste',
    'RN': 'Nordeste',
    'RO': 'Norte',
    'RR': 'Norte',
    'RS': 'Sul',
    'SC': 'Sul',
    'SE': 'Nordeste',
    'SP': 'Sudeste',
    'TO': 'Norte'
}



Base_Credito['Região'] = Base_Credito['UF'].map(uf_to_regiao)

Base_Credito.head()


#%% Gerando datas

Base_Credito['Ano'] = Base_Credito['Data'].dt.year
Base_Credito['Mês'] = Base_Credito['Data'].dt.month
Base_Credito['Dia'] = Base_Credito['Data'].dt.day

#%% Describe
Base_Credito.describe(include='all').transpose()

#%% Análise Descritiva
Base_Credito.columns
#%% Concentração Cidade
Base_Credito.Interessado.value_counts(normalize=True).cumsum()


#%% Concentração UF

Base_Credito.UF.value_counts(normalize=True)


#%% Concentração Região
Base_Credito.Região.value_counts(normalize=True)

#%% Tipo de interessado
Base_Credito.Tipo_de_interessado.value_counts()

#%% Finalidade
Base_Credito.Finalidade.value_counts()

#%% Análise crédito Pernambuco nos anos de 2020 a 2024
fitlro_pe = (Base_Credito['UF'] == 'PE') & (Base_Credito['Ano'] > 2020) #importante criar o filtro, para facilitar nas buscas
Base_Credito.loc[fitlro_pe].Finalidade.value_counts()

#%% Finalidade do emprestimo por região
Base_Credito.groupby('UF').Finalidade.value_counts().head(10)


#%% Credor do emprestimo

Base_Credito.Credor.value_counts(normalize=True).head(10)

#%%Filtros Status
Filtro_Status = [ 'Deferido', 'Deferido (PVL-IF)', 'Regularizado' ]

Base_Concesao = Base_Credito.loc[ Base_Credito.Status.isin( Filtro_Status ) ]
Base_Concesao.shape
# %% Entender Por UF:Quantidade de emprestimos, Total Liberado, Ticker médio

Anl_1 = Base_Concesao[ (Base_Concesao.Tipo_de_interessado == 'Estado') & ( Base_Concesao.Ano >= 2014 ) ].groupby( by=['Região', 'Interessado'] ).agg(
    Quantidade = ('Interessado', 'count'),
    Total_Liberado = ('Valor', 'sum'),
    Ticket_Medio = ('Valor', 'median')
).reset_index()

Anl_1


#%%----------------GRÁFICOS---------------
# Definindo a paleta de cores
Paleta = ['#183FFE', '#00D100', '#FFD000','#FE0002', '#f5f5f5']
sns.palplot( Paleta )
plt.title('Ministério da Fazenda - paleta de cores', loc='left',fontfamily='serif',fontsize=15, y=1.2)
#%%

Anl_Emprestimo = Base_Concesao.groupby('Ano').agg(Sum = ('Valor', 'sum')).tail(7)/10 ** 9.
Anl_Emprestimo.index
Anl_Emprestimo.sum


#%%
plt.figure( figsize=(12, 5) )
plt.title('Gráfico de barra')
plt.bar( Anl_Emprestimo.index, Anl_Emprestimo.Sum)

# Tamanho da figura
fig, ax = plt.subplots(figsize=(12, 5))

# Título e subtítulo
fig.text(0.09, 1, 'Investindo no Progresso: Evolução Anual dos Pedidos de Empréstimos Municipais/UFs', fontsize=15, fontweight='bold', fontfamily='serif')
fig.text(0.09, 0.95, 'Análise das Tendências e Necessidades de Financiamento ao Longo dos Anos.', fontsize=12, fontweight='light', fontfamily='serif')

# Gráfico de barras
bars = ax.bar(
    Anl_Emprestimo.index, Anl_Emprestimo.Sum,
    width=0.5, edgecolor='darkgray', linewidth=1.6, color=Paleta[3]
)

# Remover todas as spines (bordas)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Linha horizontal no eixo y=0
ax.axhline( y=0, color='black', linewidth=5.3, alpha=0.7)

# Configurar grid apenas no eixo y
ax.grid(axis='y', linestyle='-', alpha=0.4)
ax.grid(axis='x', alpha=0)

# Adicionar rótulo ao eixo y
ax.set_ylabel('Valores em bilhões (bi)', size=10)

# Configurar o tamanho das marcas dos eixos
ax.tick_params(axis='both', which='major', labelsize=12)

# Adicionar os valores em cima das barras
# Iterando sobre cada barra do gráfico
for bar in bars:

    # Obtendo a altura da barra atual
    height = bar.get_height()

    # Adicionando uma anotação (valor da barra) no topo de cada barra
    ax.annotate(
        # Formato do texto: 'R$' seguido do valor da barra com separadores de milhares e uma casa decimal
        'R$ {:,.1f}'.format(height),
        # Posição da anotação: centro da barra
        xy=(bar.get_x() + bar.get_width() / 2, height),
        # Deslocamento vertical e horizontal da anotação
        xytext=(0, 3),
        # Especificando o sistema de coordenadas do deslocamento da anotação
        textcoords="offset points",
        # Alinhamento horizontal e vertical do texto
        ha='center', va='bottom',
        # Tamanho da fonte do texto
        fontsize=10,
        # Peso da fonte (leve)
        fontweight='light',
        # Família da fonte (serif)
        fontfamily='serif'
    )

# insiths
fig.text(
    0.09, -0.1,
    '''
    Considerando a tendência de crescimento observada nos últimos anos,
    há uma perspectiva de que o volume de pedidos de empréstimo para o ano de 2024 não ultrapasse o registrado em 2018 ,
    que foi o maior da série histórica até o momento
    ''',
    fontsize=10, fontweight='light', fontfamily='serif'
)

plt.savefig('Analise-Anual.png', dpi=500, bbox_inches='tight')