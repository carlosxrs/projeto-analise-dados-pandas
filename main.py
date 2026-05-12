#%%
import pandas as pd

df_orders = pd.read_csv('data/olist_orders_dataset.csv')
df_orders.head()

#%%
df_orders.shape
#%%
df_orders.columns
#%%
df_orders.info()
#%%
df_orders.isnull().sum()
#%%
# CONVERSAO DAS COLUNAS DE DATA PARA DATETIME
colunas_data = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

for coluna in colunas_data:
    df_orders[coluna] = pd.to_datetime(df_orders[coluna])
df_orders.info()

#%%
## CALCULO DO TEMPO DE ENTREGA EM DIAS
df_orders['tempo_entrega_dias'] = (
    df_orders['order_delivered_customer_date'] 
    - df_orders['order_purchase_timestamp']
    ).dt.days

df_orders[['order_purchase_timestamp', 
           'order_delivered_customer_date', 
           'tempo_entrega_dias']]

#%%
# CONVERTENDO A COLUNA PARA INT64
df_orders['tempo_entrega_dias'] =(
    df_orders['tempo_entrega_dias']
    .astype('Int64')
    )
df_orders[['tempo_entrega_dias']]

#%%
df_orders['tempo_entrega_dias'].describe()

#%%
#PEDIDOS SEM ENTREGA
df_orders[
    df_orders['tempo_entrega_dias'].isnull()
]

#%%
# PEDIDOS COM TEMPO DE ENTREGA ACIMA DE 30 DIAS
df_orders[
    df_orders['tempo_entrega_dias'] > 30
] [[
    'order_id',
    'order_purchase_timestamp',
    'tempo_entrega_dias'
]]

#%%
# MÉDIA DE TEMPO DE ENTREGA
media_entrega = df_orders['tempo_entrega_dias'].mean()
round(media_entrega, 2)

#%%
#IDENTIFICANDO PEDIDOS ATRASADOS
df_orders ['pedido_atrasado'] = (
    df_orders['order_delivered_customer_date'] 
    > df_orders['order_estimated_delivery_date']
)
# SUBSTITUINDO TRUE/FALSE POR TEXTOS MAIS VISUAIS
df_orders['pedido_atrasado'] = (
    df_orders['pedido_atrasado']
    .map ({True: 'Atrasou',
            False: 'Chegou no prazo'})

)

df_orders[[
    'order_delivered_customer_date',
    'order_estimated_delivery_date',
    'pedido_atrasado'
]]

#%%
df_orders['pedido_atrasado'].value_counts()

#%%
# PORCENTAGEM DE PEDIDOS ATRASADOS
percentual_atraso = (
    df_orders['pedido_atrasado'].value_counts(normalize=True) * 100
)

round(percentual_atraso, 2)

# %%
#QUANTIDADE DE PEDIDOS POR STATUS
df_orders.groupby('order_status').size().sort_values(ascending=False)

#%%
df_orders['mes_compra'] = (
    df_orders['order_purchase_timestamp']
    .dt.month
)
df_orders[['order_purchase_timestamp', 'mes_compra']]

#%%
mes = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}
df_orders['nome_mes_compra'] = (
    df_orders['mes_compra']
    .map(mes)
)
df_orders[['mes_compra', 'nome_mes_compra']]

#%%
## QUANTIDADE DE PEDIDOS POR MÊS
pedidos_por_mes = (df_orders
.groupby('nome_mes_compra')
.size()
.sort_values(ascending=False)
)

pedidos_por_mes

#%%
## ORGANIZANDO OS MESES EM ORDEM CRONOLÓGICA
ordem_mes = [
    'Janeiro',
    'Fevereiro',
    'Março',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro'
]
pedidos_por_mes = (
    df_orders['nome_mes_compra']
    .value_counts()
    .reindex(ordem_mes)
)

pedidos_por_mes

#%%
# LEITURA DO DATASET DE CLIENTES
df_customers = pd.read_csv('data/olist_customers_dataset.csv')
df_customers.head()

#%%
df_customers.info()

#%%
# JOIN ENTRE PEDIDOS E CLIENTES
df_orders_customers = pd.merge(
    df_orders,
    df_customers,
    on='customer_id',
    how='inner'
)
df_orders_customers.head()

#%%
# REMOVENDO COLUNA REDUNDANTE
df_orders_customers = (
    df_orders_customers
    .drop(columns=['mes_compra'])
)
df_orders_customers.head()

#%% 
## QUANTIDADE DE PEDIDOS POR ESTADO
pedidos_por_estado = (
    df_orders_customers
    .groupby('customer_state')
    .size()
    .sort_values(ascending=False)
)

pedidos_por_estado

#%%
# MÉDIA DE TEMPO DE ENTREGA POR ESTADO
media_entrega_por_estado = (
    df_orders_customers
    .groupby('customer_state')['tempo_entrega_dias']
    .mean()
    .sort_values(ascending=False)
)
round(media_entrega_por_estado, 2)

#%%
# TOP 10 CIDADES COM MAIS PEDIDOS
top_cidades = (
    df_orders_customers
    .groupby('customer_city')
    .size()
    .sort_values(ascending=False)
    .head(10)
)
top_cidades

#%%
# QUANTIDADE DE PEDIDOS ATRASADOS POR ESTADO
atraso_por_estado = (
    df_orders_customers[
        df_orders_customers['pedido_atrasado'] == 'Atrasou'
    ]
    .groupby('customer_state')
    .size()
    .sort_values(ascending=False)
)

atraso_por_estado

#%%
## TAXA DE ATRASO POR ESTADO
total_pedidos_estado = (
    df_orders_customers
    .groupby('customer_state')
    .size()
)

pedidos_atrasados_estado = (
    df_orders_customers[
        df_orders_customers['pedido_atrasado'] == 'Atrasou'
    ]
    .groupby('customer_state')
    .size()
)

taxa_atraso_estado = (
    (pedidos_atrasados_estado / total_pedidos_estado) * 100
)

round(taxa_atraso_estado.sort_values(ascending=False), 2)

#%%
# SELECIONANDO COLUNAS IMPORTANTES PARA ANÁLISE
df_final = df_orders_customers[[
    'order_id',
    'customer_id',
    'customer_city',
    'customer_state',
    'order_status',
    'order_purchase_timestamp',
    'order_delivered_customer_date',
    'order_estimated_delivery_date',
    'tempo_entrega_dias',
    'pedido_atrasado',
    'nome_mes_compra'
]]

df_final.head()

#%%
# EXPORTANDO DATASET FINAL TRATADO
df_final.to_csv('DataSet_Final/df_final.csv', index=False)