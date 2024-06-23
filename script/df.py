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
