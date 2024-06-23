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