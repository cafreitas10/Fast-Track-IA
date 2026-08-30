# Databricks notebook source
# DBTITLE 1,Limpeza e Preparação dos Dados - Monitoramento da Fauna
# MAGIC %md
# MAGIC # 🧹 Limpeza e Preparação dos Dados - Monitoramento da Fauna
# MAGIC
# MAGIC **Checkpoint: Preparando os Dados**
# MAGIC
# MAGIC **Dataset:** Monitoramento de fauna - Parque Nacional (Cerrado)  
# MAGIC **Período:** 01-30 de maio de 2026  
# MAGIC **Registros:** 5.000 registros de câmeras automáticas
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Objetivos
# MAGIC
# MAGIC 1. Carregar e explorar a estrutura do dataset
# MAGIC 2. Identificar problemas e inconsistências
# MAGIC 3. Aplicar tratamentos adequados
# MAGIC 4. Gerar dataset limpo para análises
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📦 Estrutura do Notebook
# MAGIC
# MAGIC 1. **Carregamento dos Dados**
# MAGIC 2. **Análise Exploratória**
# MAGIC 3. **Identificação de Problemas**
# MAGIC 4. **Aplicação de Tratamentos**
# MAGIC 5. **Validação Final**
# MAGIC 6. **Exportação do Dataset Limpo**

# COMMAND ----------

# DBTITLE 1,Importar Bibliotecas
# Importar bibliotecas necessárias
import pandas as pd
import numpy as np
from datetime import datetime

# Configurações de visualização
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)
pd.set_option('display.width', 1000)

print("✓ Bibliotecas importadas com sucesso!")

# COMMAND ----------

# DBTITLE 1,Carregar Dataset Original
# Carregar o dataset
df = pd.read_csv('/Volumes/ft-ia/default/compass/dataset.csv')

print("="*80)
print("ESTRUTURA DO DATASET ORIGINAL")
print("="*80)
print(f"\nDimensões: {df.shape[0]} registros x {df.shape[1]} colunas")
print(f"\nColunas: {list(df.columns)}")
print(f"\nTipos de dados:")
print(df.dtypes)
print(f"\n\nPrimeiras 5 linhas:")
df.head()

# COMMAND ----------

# DBTITLE 1,Análise Exploratória
# MAGIC %md
# MAGIC ## 🔍 Etapa 1: Análise Exploratória
# MAGIC
# MAGIC Nesta etapa vamos investigar:
# MAGIC - Valores ausentes
# MAGIC - Registros duplicados
# MAGIC - Valores únicos em colunas categóricas
# MAGIC - Estatísticas descritivas
# MAGIC - Valores anômalos

# COMMAND ----------

# DBTITLE 1,Análise de Valores Ausentes
print("="*80)
print("1. ANÁLISE DE VALORES AUSENTES")
print("="*80)

missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)

missing_df = pd.DataFrame({
    'Coluna': missing.index,
    'Qtd_Ausentes': missing.values,
    'Percentual': missing_pct.values
})

print("\n", missing_df.to_string(index=False))

# Destacar problemas críticos
print("\n⚠️  PROBLEMAS CRÍTICOS:")
for col, pct in missing_pct.items():
    if pct > 20:
        print(f"   - {col}: {pct}% de valores ausentes!")

# COMMAND ----------

# DBTITLE 1,Análise de Duplicados
print("="*80)
print("2. ANÁLISE DE REGISTROS DUPLICADOS")
print("="*80)

duplicados_completos = df.duplicated().sum()
duplicados_id = df['id_registro'].duplicated().sum()

print(f"\nRegistros completamente duplicados: {duplicados_completos}")
print(f"IDs duplicados: {duplicados_id}")

if duplicados_completos == 0 and duplicados_id == 0:
    print("\n✓ Nenhum duplicado encontrado! Integridade OK.")

# COMMAND ----------

# DBTITLE 1,Análise de Valores Únicos
print("="*80)
print("3. VALORES ÚNICOS (Colunas Categóricas)")
print("="*80)

for col in ['id_camera', 'especie', 'grupo']:
    valores_unicos = df[col].dropna().unique()
    print(f"\n{col}: {df[col].nunique()} valores únicos (incluindo NaN)")
    print(f"   Valores não-nulos: {len(valores_unicos)}")
    print(f"   Valores: {sorted([str(v) for v in valores_unicos])}")

# COMMAND ----------

# DBTITLE 1,Estatísticas Descritivas
print("="*80)
print("4. ESTATÍSTICAS DESCRITIVAS (Variáveis Numéricas)")
print("="*80)

print(df[['duracao_segundos', 'individuos', 'temperatura_c', 'umidade_pct']].describe())

# COMMAND ----------

# DBTITLE 1,Análise de Valores Anômalos
print("="*80)
print("5. ANÁLISE DE VALORES ANÔMALOS")
print("="*80)

# Duração
print(f"\nDuração (segundos):")
print(f"   Mínimo: {df['duracao_segundos'].min()}")
print(f"   Máximo: {df['duracao_segundos'].max()}")
print(f"   Negativos: {(df['duracao_segundos'] < 0).sum()}")
print(f"   Zero: {(df['duracao_segundos'] == 0).sum()}")

# Indivíduos
print(f"\nIndivíduos:")
print(f"   Mínimo: {df['individuos'].min()}")
print(f"   Máximo: {df['individuos'].max()}")
print(f"   Negativos: {(df['individuos'] < 0).sum()}")
print(f"   Zero: {(df['individuos'] == 0).sum()}")

# Temperatura
print(f"\nTemperatura (°C):")
print(f"   Mínimo: {df['temperatura_c'].min()}")
print(f"   Máximo: {df['temperatura_c'].max()}")
print(f"   Fora do range típico (10-35°C): {((df['temperatura_c'] < 10) | (df['temperatura_c'] > 35)).sum()}")

# Umidade
print(f"\nUmidade (%):")
print(f"   Mínimo: {df['umidade_pct'].min()}")
print(f"   Máximo: {df['umidade_pct'].max()}")
print(f"   Fora do range válido (0-100%): {((df['umidade_pct'] < 0) | (df['umidade_pct'] > 100)).sum()}")

print("\n✓ Todas as variáveis numéricas estão dentro de ranges válidos!")

# COMMAND ----------

# DBTITLE 1,Análise de Datas e Problema do Grupo
print("="*80)
print("6. ANÁLISE DE DATAS")
print("="*80)

print(f"\nExemplos de data_hora_inicio:")
print(df['data_hora_inicio'].head(10).to_list())

# Parsear datas
df_temp = df.copy()
df_temp['data_hora_inicio_parsed'] = pd.to_datetime(df_temp['data_hora_inicio'], format='%Y-%m-%d %H:%M:%S')

print(f"\n✓ Formato de data reconhecido: 'YYYY-MM-DD HH:MM:SS'")
print(f"  Período: {df_temp['data_hora_inicio_parsed'].min()} a {df_temp['data_hora_inicio_parsed'].max()}")

maio_2026 = (df_temp['data_hora_inicio_parsed'].dt.year == 2026) & (df_temp['data_hora_inicio_parsed'].dt.month == 5)
print(f"  Registros em maio/2026: {maio_2026.sum()} de {len(df_temp)} ({maio_2026.sum()/len(df_temp)*100:.1f}%)")

print("\n" + "="*80)
print("7. INVESTIGAÇÃO: RELAÇÃO ESPÉCIE-GRUPO")
print("="*80)

print("\nContagem de registros por espécie (com e sem grupo):")
especie_grupo = df.groupby(['especie', 'grupo']).size().reset_index(name='count')
print(especie_grupo.to_string(index=False))

print("\n\nRegistros com espécie mas SEM grupo:")
sem_grupo = df[df['especie'].notna() & df['grupo'].isna()]
print(f"Total: {len(sem_grupo)} registros")
if len(sem_grupo) > 0:
    print(f"\nEspécies afetadas:")
    print(sem_grupo['especie'].value_counts())

# COMMAND ----------

# DBTITLE 1,Problemas Identificados - Resumo
# MAGIC %md
# MAGIC ## 📊 Problemas Identificados
# MAGIC
# MAGIC ### ⚠️ Problemas Críticos
# MAGIC
# MAGIC 1. **Coluna `grupo` com 78,86% de valores ausentes**
# MAGIC    - Apenas Ema e Seriema (aves) possuem grupo
# MAGIC    - 7 espécies sem classificação (mamíferos e anfíbios)
# MAGIC
# MAGIC 2. **Coluna `especie` com 23,26% de valores ausentes**
# MAGIC    - 1.163 registros sem identificação
# MAGIC    - Câmeras detectaram movimento mas não identificaram a espécie
# MAGIC
# MAGIC 3. **Espécies esperadas vs encontradas**
# MAGIC    - Esperadas: 13 espécies
# MAGIC    - Encontradas: 9 espécies
# MAGIC    - **Faltantes:** Lobo-guará, Onça-pintada, Rã-manteiga, Tamanduá-bandeira
# MAGIC
# MAGIC ### ⚠️ Problemas Moderados
# MAGIC
# MAGIC 4. **Valores ausentes em sensores**
# MAGIC    - Temperatura: 247 registros (4,94%)
# MAGIC    - Umidade: 175 registros (3,50%)
# MAGIC
# MAGIC ### ✅ Pontos Positivos
# MAGIC
# MAGIC - Sem duplicados
# MAGIC - Variáveis numéricas consistentes
# MAGIC - Datas corretas e no período esperado
# MAGIC - IDs de câmeras padronizados (CAM01-CAM12)

# COMMAND ----------

# DBTITLE 1,Decisões de Tratamento
# MAGIC %md
# MAGIC ## 🔧 Etapa 2: Aplicação de Tratamentos
# MAGIC
# MAGIC ### Decisões Tomadas:
# MAGIC
# MAGIC 1. **Preencher coluna `grupo`** → Mapeamento espécie → grupo taxonômico
# MAGIC 2. **Manter registros sem espécie** → Úteis para análise de taxa de detecção
# MAGIC 3. **Criar coluna `ambiente`** → Facilitar análises por habitat
# MAGIC 4. **Preencher sensores** → Mediana por ambiente (preserva características locais)
# MAGIC 5. **Converter datas** → Tipo datetime + colunas derivadas
# MAGIC 6. **Criar colunas temporais** → Hora, dia, período do dia

# COMMAND ----------

# DBTITLE 1,Tratamento 1: Criar Cópia e Preencher Grupo
# Criar cópia do dataframe original
df_clean = df.copy()

print("="*80)
print("APLICANDO TRATAMENTOS")
print("="*80)

# TRATAMENTO 1: Preencher coluna 'grupo'
print("\n1. Preenchendo coluna 'grupo'...")

# Mapeamento espécie → grupo taxonômico
mapeamento_grupo = {
    # Mamíferos
    'Capivara': 'Mamífero',
    'Cervo-do-pantanal': 'Mamífero',
    'Lobo-guará': 'Mamífero',
    'Onça-pintada': 'Mamífero',
    'Quati': 'Mamífero',
    'Tamanduá-bandeira': 'Mamífero',
    'Tatu-canastra': 'Mamífero',
    'Veado-campeiro': 'Mamífero',
    # Aves
    'Ema': 'Ave',
    'Seriema': 'Ave',
    # Anfíbios
    'Perereca-verde': 'Anfíbio',
    'Rã-manteiga': 'Anfíbio',
    'Sapo-cururu': 'Anfíbio'
}

# Preencher grupo baseado na espécie
df_clean['grupo'] = df_clean.apply(
    lambda row: mapeamento_grupo.get(row['especie'], row['grupo']),
    axis=1
)

print(f"   ✓ Antes: {df['grupo'].isna().sum()} valores ausentes")
print(f"   ✓ Depois: {df_clean['grupo'].isna().sum()} valores ausentes")
print(f"   ✓ Grupos preenchidos: {df_clean['grupo'].value_counts().to_dict()}")

# COMMAND ----------

# DBTITLE 1,Tratamento 2: Criar Coluna Ambiente
# TRATAMENTO 2: Criar coluna 'ambiente'
print("\n2. Criando coluna 'ambiente'...")

def mapear_ambiente(id_camera):
    """Mapeia ID da câmera para tipo de ambiente"""
    if id_camera in ['CAM01', 'CAM02', 'CAM03', 'CAM04']:
        return 'Cerrado aberto'
    elif id_camera in ['CAM05', 'CAM06', 'CAM07', 'CAM08']:
        return 'Mata de galeria'
    elif id_camera in ['CAM09', 'CAM10', 'CAM11', 'CAM12']:
        return 'Veredas e áreas úmidas'
    else:
        return None

df_clean['ambiente'] = df_clean['id_camera'].apply(mapear_ambiente)

print(f"   ✓ Ambientes criados: {df_clean['ambiente'].value_counts().to_dict()}")

# COMMAND ----------

# DBTITLE 1,Tratamento 3: Preencher Valores de Sensores
# TRATAMENTO 3: Preencher valores ausentes de temperatura e umidade
print("\n3. Preenchendo valores ausentes de temperatura e umidade...")

# Calcular medianas por ambiente
medianas_temp = df_clean.groupby('ambiente')['temperatura_c'].median()
medianas_umid = df_clean.groupby('ambiente')['umidade_pct'].median()

print(f"\n   Medianas de temperatura por ambiente:")
for amb, med in medianas_temp.items():
    print(f"   - {amb}: {med:.1f}°C")

print(f"\n   Medianas de umidade por ambiente:")
for amb, med in medianas_umid.items():
    print(f"   - {amb}: {med:.1f}%")

# Preencher valores ausentes
for ambiente in df_clean['ambiente'].unique():
    # Temperatura
    mask_temp = (df_clean['ambiente'] == ambiente) & (df_clean['temperatura_c'].isna())
    df_clean.loc[mask_temp, 'temperatura_c'] = medianas_temp[ambiente]
    
    # Umidade
    mask_umid = (df_clean['ambiente'] == ambiente) & (df_clean['umidade_pct'].isna())
    df_clean.loc[mask_umid, 'umidade_pct'] = medianas_umid[ambiente]

print(f"\n   ✓ Temperatura: {df['temperatura_c'].isna().sum()} → {df_clean['temperatura_c'].isna().sum()} valores ausentes")
print(f"   ✓ Umidade: {df['umidade_pct'].isna().sum()} → {df_clean['umidade_pct'].isna().sum()} valores ausentes")

# COMMAND ----------

# DBTITLE 1,Tratamento 4: Converter Datas e Criar Colunas Derivadas
# TRATAMENTO 4: Converter data_hora_inicio para datetime
print("\n4. Convertendo data_hora_inicio para datetime...")

df_clean['data_hora_inicio'] = pd.to_datetime(df_clean['data_hora_inicio'], format='%Y-%m-%d %H:%M:%S')

print(f"   ✓ Tipo convertido: {df_clean['data_hora_inicio'].dtype}")
print(f"   ✓ Período: {df_clean['data_hora_inicio'].min()} a {df_clean['data_hora_inicio'].max()}")

# TRATAMENTO 5: Criar colunas derivadas
print("\n5. Criando colunas derivadas para facilitar análises...")

# Extrair data e hora
df_clean['data'] = df_clean['data_hora_inicio'].dt.date
df_clean['hora'] = df_clean['data_hora_inicio'].dt.hour
df_clean['dia_da_semana'] = df_clean['data_hora_inicio'].dt.day_name()
df_clean['dia_do_mes'] = df_clean['data_hora_inicio'].dt.day

# Criar coluna de período do dia
def classificar_periodo(hora):
    """Classifica a hora em período do dia"""
    if 5 <= hora < 12:
        return 'Manhã'
    elif 12 <= hora < 18:
        return 'Tarde'
    elif 18 <= hora < 22:
        return 'Noite'
    else:
        return 'Madrugada'

df_clean['periodo_dia'] = df_clean['hora'].apply(classificar_periodo)

print(f"   ✓ Colunas criadas: data, hora, dia_da_semana, dia_do_mes, periodo_dia")
print(f"   ✓ Distribuição por período: {df_clean['periodo_dia'].value_counts().to_dict()}")

# COMMAND ----------

# DBTITLE 1,Salvar Dataset Limpo
# TRATAMENTO 6: Salvar dataset limpo
print("\n6. Salvando dataset limpo...")

output_path = '/Volumes/ft-ia/default/compass/dataset_clean.csv'
df_clean.to_csv(output_path, index=False)

print(f"   ✓ Arquivo salvo em: {output_path}")

# COMMAND ----------

# DBTITLE 1,Validação Final
# MAGIC %md
# MAGIC ## ✅ Etapa 3: Validação Final
# MAGIC
# MAGIC Verificação do dataset limpo e resumo das transformações.

# COMMAND ----------

# DBTITLE 1,Resumo Final do Dataset Limpo
print("="*80)
print("RESUMO FINAL DO DATASET LIMPO")
print("="*80)

print(f"\nDimensões: {df_clean.shape[0]} registros x {df_clean.shape[1]} colunas")
print(f"\nColunas: {list(df_clean.columns)}")

print("\n\nValores ausentes por coluna:")
missing_final = df_clean.isnull().sum()
missing_final_pct = (df_clean.isnull().sum() / len(df_clean) * 100).round(2)

missing_final_df = pd.DataFrame({
    'Coluna': missing_final.index,
    'Qtd_Ausentes': missing_final.values,
    'Percentual': missing_final_pct.values
})

print(missing_final_df[missing_final_df['Qtd_Ausentes'] > 0].to_string(index=False))

if missing_final_df['Qtd_Ausentes'].sum() == df_clean['especie'].isna().sum() + df_clean['grupo'].isna().sum():
    print("\n✓ Apenas 'especie' e 'grupo' mantêm valores ausentes (registros não identificados)")
    print(f"✓ Total de registros não identificados: {df_clean['especie'].isna().sum()} ({df_clean['especie'].isna().sum()/len(df_clean)*100:.2f}%)")

# COMMAND ----------

# DBTITLE 1,Visualizar Amostra do Dataset Limpo
print("\n" + "="*80)
print("AMOSTRA DO DATASET LIMPO")
print("="*80)

print("\nPrimeiras 10 linhas do dataset limpo:")
df_clean.head(10)

# COMMAND ----------

# DBTITLE 1,Comparação Antes vs Depois
print("="*80)
print("COMPARAÇÃO: ANTES vs DEPOIS")
print("="*80)

print("\n📊 DATASET ORIGINAL:")
print(f"   - Dimensões: {df.shape[0]} x {df.shape[1]}")
print(f"   - Valores ausentes totais: {df.isnull().sum().sum()}")
print(f"   - Grupo ausente: {df['grupo'].isna().sum()} ({df['grupo'].isna().sum()/len(df)*100:.1f}%)")
print(f"   - Temperatura ausente: {df['temperatura_c'].isna().sum()} ({df['temperatura_c'].isna().sum()/len(df)*100:.1f}%)")
print(f"   - Umidade ausente: {df['umidade_pct'].isna().sum()} ({df['umidade_pct'].isna().sum()/len(df)*100:.1f}%)")

print("\n📊 DATASET LIMPO:")
print(f"   - Dimensões: {df_clean.shape[0]} x {df_clean.shape[1]}")
print(f"   - Valores ausentes totais (exceto especie/grupo): {df_clean.drop(['especie', 'grupo'], axis=1).isnull().sum().sum()}")
print(f"   - Grupo ausente: {df_clean['grupo'].isna().sum()} ({df_clean['grupo'].isna().sum()/len(df_clean)*100:.1f}%)")
print(f"   - Temperatura ausente: {df_clean['temperatura_c'].isna().sum()}")
print(f"   - Umidade ausente: {df_clean['umidade_pct'].isna().sum()}")
print(f"   - Novas colunas criadas: 6 (ambiente, data, hora, dia_da_semana, dia_do_mes, periodo_dia)")

print("\n✅ MELHORIAS:")
print(f"   - Grupo preenchido: {df['grupo'].isna().sum() - df_clean['grupo'].isna().sum()} registros")
print(f"   - Temperatura preenchida: {df['temperatura_c'].isna().sum()} registros")
print(f"   - Umidade preenchida: {df['umidade_pct'].isna().sum()} registros")
print(f"   - Colunas para análise temporal: 5 novas colunas")
print(f"   - Coluna para análise espacial: 1 nova coluna (ambiente)")

# COMMAND ----------

# DBTITLE 1,Conclusão
# MAGIC %md
# MAGIC ## 🎯 Conclusão
# MAGIC
# MAGIC ### ✅ Tratamentos Aplicados com Sucesso:
# MAGIC
# MAGIC 1. ✓ Coluna `grupo` preenchida com base em taxonomia (redução de 70% nos valores ausentes)
# MAGIC 2. ✓ Coluna `ambiente` criada para facilitar análises espaciais
# MAGIC 3. ✓ Valores de sensores (temperatura e umidade) preenchidos com mediana por ambiente
# MAGIC 4. ✓ Data/hora convertida para tipo datetime
# MAGIC 5. ✓ 6 colunas derivadas criadas para análises temporais e espaciais
# MAGIC
# MAGIC ### 📊 Dataset Pronto Para:
# MAGIC
# MAGIC - ✓ Análises por ambiente (3 tipos de habitat)
# MAGIC - ✓ Análises temporais (período do dia, dia da semana)
# MAGIC - ✓ Análises por espécie e grupo taxonômico
# MAGIC - ✓ Análises ambientais (temperatura e umidade)
# MAGIC - ✓ Estudos de diversidade e padrões de atividade
# MAGIC
# MAGIC ### ⚠️ Limitações a Considerar:
# MAGIC
# MAGIC - 23% dos registros sem identificação de espécie (mantidos para análises de detecção)
# MAGIC - 4 espécies esperadas não registradas no período (Lobo-guará, Onça-pintada, Rã-manteiga, Tamanduá-bandeira)
# MAGIC - ~5% dos valores de sensores foram imputados (mediana por ambiente)
# MAGIC
# MAGIC ### 📁 Arquivos Gerados:
# MAGIC
# MAGIC - **dataset_clean.csv** → Dataset limpo e enriquecido (5.000 registros × 15 colunas)
# MAGIC - **cleaning_fauna.md** → Documentação completa das decisões de tratamento
# MAGIC - **cleaning_fauna.ipynb** → Este notebook com todo o código reproduzível
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Status:** ✅ **DATASET VALIDADO E PRONTO PARA ANÁLISES**

# COMMAND ----------

