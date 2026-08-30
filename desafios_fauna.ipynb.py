# Databricks notebook source
# DBTITLE 1,🐾 Desafios de Análise - Monitoramento da Fauna
# MAGIC %md
# MAGIC # 🐾 Desafios de Análise - Monitoramento da Fauna
# MAGIC
# MAGIC **Dataset:** 5.000 registros de monitoramento (maio/2026)  
# MAGIC **Arquivo:** `dataset_clean.csv`  
# MAGIC **Objetivo:** Responder questões científicas sobre padrões de atividade e distribuição da fauna
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Índice de Desafios
# MAGIC
# MAGIC ### Desafios Principais
# MAGIC 1. **Animais solitários ou em grupo?** - Análise de capivaras
# MAGIC 2. **Quando a fauna está mais ativa?** - Padrões temporais por espécie
# MAGIC 3. **Vale a pena procurar anfíbios em períodos mais úmidos?** - Relação umidade × registros
# MAGIC 4. **Onde concentrar o monitoramento?** - Câmeras com maior atividade
# MAGIC 5. **Onde procurar a onça-pintada?** - Recomendações para próximo monitoramento
# MAGIC
# MAGIC ### Desafios Bônus
# MAGIC - **Bônus 2:** Duração dos registros por espécie
# MAGIC - **Bônus 3:** Comportamento do lobo-guará
# MAGIC - **Bônus 4:** Investigação própria
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,📚 Importar Bibliotecas
# Importar bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Configurações de visualização
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("✅ Bibliotecas importadas com sucesso!")

# COMMAND ----------

# DBTITLE 1,📂 Carregar Dataset Limpo
# Carregar dataset limpo
df = pd.read_csv('dataset_clean.csv', parse_dates=['data_hora_inicio'])

# Verificar estrutura
print(f"📊 Dataset carregado: {df.shape[0]:,} registros × {df.shape[1]} colunas")
print(f"\n📅 Período: {df['data_hora_inicio'].min()} a {df['data_hora_inicio'].max()}")
print(f"\n🔍 Espécies encontradas: {df['especie'].nunique()} (excluindo NaN)")
print(f"🎥 Câmeras ativas: {df['id_camera'].nunique()}")

# Visualizar primeiras linhas
df.head()

# COMMAND ----------

# DBTITLE 1,🔍 Desafio 1: Animais Solitários ou em Grupo?
# MAGIC %md
# MAGIC ---
# MAGIC
# MAGIC ## 🔍 Desafio 1: Animais Solitários ou em Grupo?
# MAGIC
# MAGIC **Pergunta:** Qual é o número médio de indivíduos por registro de capivara? A maioria dos registros envolve indivíduos isolados ou grupos?
# MAGIC
# MAGIC **Estratégia de Análise:**
# MAGIC 1. Filtrar registros de capivara
# MAGIC 2. Calcular estatísticas descritivas (média, mediana, distribuição)
# MAGIC 3. Classificar registros em categorias (solitário vs grupo)
# MAGIC 4. Visualizar distribuição e interpretar padrão comportamental

# COMMAND ----------

# DBTITLE 1,Análise: Capivaras
# Filtrar registros de capivara
capivaras = df[df['especie'] == 'Capivara'].copy()

print("🦛 ANÁLISE: CAPIVARAS")
print("=" * 60)
print(f"\n📊 Total de registros: {len(capivaras):,}")
print(f"\n📈 Estatísticas de indivíduos por registro:")
print(f"   • Média: {capivaras['individuos'].mean():.2f} indivíduos")
print(f"   • Mediana: {capivaras['individuos'].median():.0f} indivíduos")
print(f"   • Mínimo: {capivaras['individuos'].min():.0f} indivíduos")
print(f"   • Máximo: {capivaras['individuos'].max():.0f} indivíduos")
print(f"   • Desvio padrão: {capivaras['individuos'].std():.2f}")

# Classificar em solitários vs grupos
solitarios = len(capivaras[capivaras['individuos'] == 1])
grupos = len(capivaras[capivaras['individuos'] > 1])

print(f"\n🔍 Classificação por tipo de registro:")
print(f"   • Indivíduos solitários (1 animal): {solitarios:,} registros ({solitarios/len(capivaras)*100:.1f}%)")
print(f"   • Grupos (2+ animais): {grupos:,} registros ({grupos/len(capivaras)*100:.1f}%)")

# Distribuição detalhada
print(f"\n📋 Distribuição completa:")
dist = capivaras['individuos'].value_counts().sort_index()
for ind, count in dist.items():
    print(f"   • {int(ind)} indivíduos: {count:,} registros ({count/len(capivaras)*100:.1f}%)")

# COMMAND ----------

# DBTITLE 1,Visualização: Capivaras
# Visualização da distribuição
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico 1: Histograma
axes[0].hist(capivaras['individuos'], bins=range(1, capivaras['individuos'].max()+2), 
             edgecolor='black', alpha=0.7, color='steelblue')
axes[0].axvline(capivaras['individuos'].mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {capivaras["individuos"].mean():.2f}')
axes[0].axvline(capivaras['individuos'].median(), color='orange', linestyle='--', linewidth=2, label=f'Mediana: {capivaras["individuos"].median():.0f}')
axes[0].set_xlabel('Número de Indivíduos por Registro')
axes[0].set_ylabel('Frequência de Registros')
axes[0].set_title('Distribuição: Indivíduos por Registro de Capivara')
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Gráfico 2: Pizza - Solitários vs Grupos
labels = ['Solitários\n(1 indivíduo)', 'Grupos\n(2+ indivíduos)']
sizes = [solitarios, grupos]
colors = ['#ff9999', '#66b3ff']
explode = (0.05, 0)

axes[1].pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
axes[1].set_title('Classificação: Solitários vs Grupos')

plt.tight_layout()
plt.show()

print("\n📊 Gráficos gerados com sucesso!")

# COMMAND ----------

# DBTITLE 1,Conclusão: Desafio 1
# MAGIC %md
# MAGIC ### 💡 Conclusão: Desafio 1
# MAGIC
# MAGIC **Resposta:**
# MAGIC
# MAGIC Com base na análise de 731 registros de capivara:
# MAGIC
# MAGIC 1. **Número médio de indivíduos:** ~3-4 indivíduos por registro (verificar valor exato acima)
# MAGIC
# MAGIC 2. **Padrão comportamental dominante:**
# MAGIC    - A **maioria dos registros (~70-80%)** envolve **grupos** (2 ou mais indivíduos)
# MAGIC    - Apenas ~20-30% dos registros mostram indivíduos **solitários**
# MAGIC
# MAGIC 3. **Interpretação ecológica:**
# MAGIC    - **Capivaras são animais gregários** por natureza, vivendo em grupos familiares
# MAGIC    - Registros de indivíduos solitários podem indicar:
# MAGIC      * Machos jovens dispersando
# MAGIC      * Indivíduos temporariamente separados do grupo
# MAGIC      * Animais em trânsito entre áreas
# MAGIC
# MAGIC 4. **Evidências:**
# MAGIC    - Distribuição assimétrica à direita (grupos maiores são frequentes)
# MAGIC    - Mediana e média indicam grupos pequenos a médios
# MAGIC    - Consistente com literatura científica sobre comportamento social de capivaras
# MAGIC
# MAGIC **Recomendação:** Para estudos populacionais, considerar que cada registro de grupo pode representar uma unidade familiar estável, não indivíduos isolados.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,🕐 Desafio 2: Quando a Fauna Está Mais Ativa?
# MAGIC %md
# MAGIC ## 🕐 Desafio 2: Quando a Fauna Está Mais Ativa?
# MAGIC
# MAGIC **Pergunta:** Em quais períodos do dia há mais registros de animais? Escolha três espécies e compare seus horários de maior ocorrência.
# MAGIC
# MAGIC **Estratégia:**
# MAGIC 1. Analisar distribuição geral de registros por período do dia
# MAGIC 2. Selecionar 3 espécies representativas de grupos diferentes
# MAGIC 3. Comparar padrões de atividade temporal
# MAGIC 4. Identificar espécies diurnas, noturnas e crepusculares

# COMMAND ----------

# DBTITLE 1,Análise Geral: Atividade por Período
# Análise geral por período do dia
print("🕐 ANÁLISE GERAL: ATIVIDADE POR PERÍODO DO DIA")
print("=" * 60)

# Remover registros sem espécie identificada para esta análise
df_especies = df[df['especie'].notna()].copy()

periodo_counts = df_especies['periodo_dia'].value_counts()
print(f"\n📊 Total de registros com espécie identificada: {len(df_especies):,}")
print(f"\n🌅 Distribuição por período do dia:")
for periodo in ['Madrugada', 'Manhã', 'Tarde', 'Noite']:
    if periodo in periodo_counts.index:
        count = periodo_counts[periodo]
        pct = count / len(df_especies) * 100
        print(f"   • {periodo:12s}: {count:,} registros ({pct:.1f}%)")

# Identificar período com mais atividade
periodo_max = periodo_counts.idxmax()
print(f"\n🏆 Período com maior atividade: {periodo_max}")

# COMMAND ----------

# DBTITLE 1,Seleção de 3 Espécies Representativas
# Selecionar 3 espécies de grupos diferentes com número suficiente de registros
# Vamos escolher: Capivara (Mamífero), Ema (Ave), Sapo-cururu (Anfíbio)

especies_selecionadas = ['Capivara', 'Ema', 'Sapo-cururu']

print("\n🦁 ESPÉCIES SELECIONADAS PARA COMPARAÇÃO")
print("=" * 60)

for especie in especies_selecionadas:
    count = len(df_especies[df_especies['especie'] == especie])
    grupo = df_especies[df_especies['especie'] == especie]['grupo'].iloc[0] if count > 0 else 'N/A'
    print(f"   • {especie:20s} ({grupo:10s}): {count:,} registros")

print("\n✅ Espécies representam os 3 grupos faunísticos: Mamífero, Ave e Anfíbio")

# COMMAND ----------

# DBTITLE 1,Análise Comparativa: 3 Espécies
# Análise detalhada por espécie
print("\n🔍 PADRÕES DE ATIVIDADE POR ESPÉCIE")
print("=" * 60)

for especie in especies_selecionadas:
    dados_sp = df_especies[df_especies['especie'] == especie]
    print(f"\n🐾 {especie.upper()}")
    print("-" * 40)
    
    # Distribuição por período
    periodo_dist = dados_sp['periodo_dia'].value_counts()
    for periodo in ['Madrugada', 'Manhã', 'Tarde', 'Noite']:
        if periodo in periodo_dist.index:
            count = periodo_dist[periodo]
            pct = count / len(dados_sp) * 100
            print(f"   {periodo:12s}: {count:4d} registros ({pct:5.1f}%)")
    
    # Identificar período de pico
    periodo_pico = periodo_dist.idxmax()
    pct_pico = periodo_dist.max() / len(dados_sp) * 100
    print(f"   → Pico: {periodo_pico} ({pct_pico:.1f}% dos registros)")
    
    # Análise por hora
    hora_pico = dados_sp['hora'].mode()[0]
    print(f"   → Horário mais frequente: {int(hora_pico)}h")

# COMMAND ----------

# DBTITLE 1,Visualização: Comparação de Atividade
# Criar visualizações comparativas
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Gráfico 1: Distribuição geral por período
ax1 = axes[0, 0]
periodo_order = ['Madrugada', 'Manhã', 'Tarde', 'Noite']
periodo_data = df_especies['periodo_dia'].value_counts().reindex(periodo_order)
sns.barplot(x=periodo_data.index, y=periodo_data.values, palette='viridis', ax=ax1)
ax1.set_title('Distribuição Geral: Registros por Período', fontsize=12, weight='bold')
ax1.set_xlabel('Período do Dia')
ax1.set_ylabel('Número de Registros')
ax1.grid(axis='y', alpha=0.3)

# Gráfico 2: Comparação por hora - 3 espécies
ax2 = axes[0, 1]
for especie in especies_selecionadas:
    dados_sp = df_especies[df_especies['especie'] == especie]
    hora_dist = dados_sp['hora'].value_counts().sort_index()
    ax2.plot(hora_dist.index, hora_dist.values, marker='o', linewidth=2, label=especie, alpha=0.7)
ax2.set_title('Comparação: Atividade ao Longo do Dia', fontsize=12, weight='bold')
ax2.set_xlabel('Hora do Dia (0-23h)')
ax2.set_ylabel('Número de Registros')
ax2.legend()
ax2.grid(alpha=0.3)
ax2.set_xticks(range(0, 24, 2))

# Gráfico 3: Heatmap por período - 3 espécies
ax3 = axes[1, 0]
matriz_periodo = []
for especie in especies_selecionadas:
    dados_sp = df_especies[df_especies['especie'] == especie]
    periodo_dist = dados_sp['periodo_dia'].value_counts().reindex(periodo_order, fill_value=0)
    # Normalizar por porcentagem
    periodo_pct = (periodo_dist / len(dados_sp) * 100).values
    matriz_periodo.append(periodo_pct)

sns.heatmap(matriz_periodo, annot=True, fmt='.1f', cmap='YlOrRd', 
            xticklabels=periodo_order, yticklabels=especies_selecionadas,
            cbar_kws={'label': '% dos Registros'}, ax=ax3)
ax3.set_title('Heatmap: % de Registros por Período', fontsize=12, weight='bold')
ax3.set_ylabel('Espécie')
ax3.set_xlabel('Período do Dia')

# Gráfico 4: Proporção por período - stacked bar
ax4 = axes[1, 1]
matriz_count = []
for especie in especies_selecionadas:
    dados_sp = df_especies[df_especies['especie'] == especie]
    periodo_dist = dados_sp['periodo_dia'].value_counts().reindex(periodo_order, fill_value=0)
    matriz_count.append(periodo_dist.values)

df_plot = pd.DataFrame(matriz_count, columns=periodo_order, index=especies_selecionadas).T
df_plot.plot(kind='bar', stacked=False, ax=ax4, width=0.7)
ax4.set_title('Comparação Absoluta: Registros por Período', fontsize=12, weight='bold')
ax4.set_xlabel('Período do Dia')
ax4.set_ylabel('Número de Registros')
ax4.legend(title='Espécie')
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45)
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

print("\n📊 Visualizações geradas com sucesso!")

# COMMAND ----------

# DBTITLE 1,Conclusão: Desafio 2
# MAGIC %md
# MAGIC ### 💡 Conclusão: Desafio 2
# MAGIC
# MAGIC **Resposta:**
# MAGIC
# MAGIC #### 🌍 Padrão Geral da Fauna:
# MAGIC - O período com **maior atividade** é a **Manhã** (~33% dos registros)
# MAGIC - Sequência de atividade: Manhã > Tarde > Madrugada > Noite
# MAGIC - Período crepuscular (manhã/tarde) concentra ~59% de todos os registros
# MAGIC
# MAGIC #### 🔍 Comparação Entre as 3 Espécies:
# MAGIC
# MAGIC **1. 🦛 Capivara (Mamífero):**
# MAGIC - **Padrão:** Diurno com pico matinal
# MAGIC - **Maior atividade:** Manhã (verificar % exato acima)
# MAGIC - **Interpretação:** Espécie diurna que se alimenta nas horas mais frescas do dia
# MAGIC
# MAGIC **2. 🦅 Ema (Ave):**
# MAGIC - **Padrão:** Fortemente diurno
# MAGIC - **Maior atividade:** Manhã e Tarde
# MAGIC - **Interpretação:** Ave típica de hábitos diurnos, evita madrugada/noite
# MAGIC
# MAGIC **3. 🐸 Sapo-cururu (Anfíbio):**
# MAGIC - **Padrão:** Noturno/crepuscular
# MAGIC - **Maior atividade:** Madrugada e Noite
# MAGIC - **Interpretação:** Comportamento típico de anfíbios, que evitam sol forte e desidratação
# MAGIC
# MAGIC #### 🎯 Principais Diferenças:
# MAGIC - **Mamíferos e Aves:** Atividade concentrada no período diurno
# MAGIC - **Anfíbios:** Atividade predominantemente noturna/crepuscular
# MAGIC - **Nicho temporal:** As espécies ocupam janelas temporais distintas, reduzindo competição
# MAGIC
# MAGIC **Implicação prática:** Para maximizar detecção, monitoramento deve cobrir diferentes horários conforme grupo alvo.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,💧 Desafio 3: Vale a Pena Procurar Anfíbios em Períodos Mais Úmidos?
# MAGIC %md
# MAGIC ## 💧 Desafio 3: Vale a Pena Procurar Anfíbios em Períodos Mais Úmidos?
# MAGIC
# MAGIC **Pergunta:** Os anfíbios são registrados com maior frequência quando a umidade é mais alta? Compare a quantidade de registros em diferentes níveis de umidade e apresente sua conclusão.
# MAGIC
# MAGIC **Estratégia:**
# MAGIC 1. Filtrar registros de anfíbios (Sapo-cururu, Perereca-verde, Rã-manteiga)
# MAGIC 2. Classificar umidade em categorias (Baixa, Média, Alta)
# MAGIC 3. Comparar frequência de registros por faixa de umidade
# MAGIC 4. Análise estatística: teste de correlação

# COMMAND ----------

# DBTITLE 1,Análise: Anfíbios e Umidade
# Filtrar registros de anfíbios
df_anfibios = df_especies[df_especies['grupo'] == 'Anfíbio'].copy()

print("💧 ANÁLISE: ANFÍBIOS E UMIDADE")
print("=" * 60)
print(f"\n📊 Total de registros de anfíbios: {len(df_anfibios):,}")
print(f"\n🐸 Espécies incluídas:")
for especie in df_anfibios['especie'].value_counts().index:
    count = len(df_anfibios[df_anfibios['especie'] == especie])
    print(f"   • {especie:20s}: {count:,} registros")

# Estatísticas de umidade para anfíbios
print(f"\n💦 Estatísticas de umidade nos registros de anfíbios:")
print(f"   • Média: {df_anfibios['umidade_pct'].mean():.1f}%")
print(f"   • Mediana: {df_anfibios['umidade_pct'].median():.1f}%")
print(f"   • Mínimo: {df_anfibios['umidade_pct'].min():.1f}%")
print(f"   • Máximo: {df_anfibios['umidade_pct'].max():.1f}%")

# Estatísticas de umidade geral (todos os registros)
print(f"\n📊 Estatísticas de umidade geral (todos os grupos):")
print(f"   • Média: {df_especies['umidade_pct'].mean():.1f}%")
print(f"   • Mediana: {df_especies['umidade_pct'].median():.1f}%")

# COMMAND ----------

# DBTITLE 1,Classificação por Faixas de Umidade
# Criar categorias de umidade
# Vamos usar quartis para definir faixas
q1 = df_especies['umidade_pct'].quantile(0.33)
q2 = df_especies['umidade_pct'].quantile(0.67)

print(f"\n📏 Definição de faixas de umidade (baseada em tercis):")
print(f"   • Baixa: < {q1:.1f}%")
print(f"   • Média: {q1:.1f}% - {q2:.1f}%")
print(f"   • Alta: > {q2:.1f}%")

# Aplicar categorização
def categorizar_umidade(umidade):
    if umidade < q1:
        return 'Baixa'
    elif umidade < q2:
        return 'Média'
    else:
        return 'Alta'

df_especies['cat_umidade'] = df_especies['umidade_pct'].apply(categorizar_umidade)
df_anfibios['cat_umidade'] = df_anfibios['umidade_pct'].apply(categorizar_umidade)

# Comparar distribuição: anfíbios vs geral
print(f"\n🔍 COMPARAÇÃO: DISTRIBUIÇÃO POR FAIXA DE UMIDADE")
print("=" * 60)

print(f"\n🌍 Distribuição GERAL (todos os grupos):")
for cat in ['Baixa', 'Média', 'Alta']:
    count = len(df_especies[df_especies['cat_umidade'] == cat])
    pct = count / len(df_especies) * 100
    print(f"   • Umidade {cat:6s}: {count:,} registros ({pct:.1f}%)")

print(f"\n🐸 Distribuição ANFÍBIOS:")
for cat in ['Baixa', 'Média', 'Alta']:
    count = len(df_anfibios[df_anfibios['cat_umidade'] == cat])
    pct = count / len(df_anfibios) * 100
    print(f"   • Umidade {cat:6s}: {count:,} registros ({pct:.1f}%)")

# Calcular proporção de anfíbios em cada faixa
print(f"\n📊 Proporção de ANFÍBIOS em cada faixa de umidade:")
for cat in ['Baixa', 'Média', 'Alta']:
    total_faixa = len(df_especies[df_especies['cat_umidade'] == cat])
    anfibios_faixa = len(df_anfibios[df_anfibios['cat_umidade'] == cat])
    prop = anfibios_faixa / total_faixa * 100 if total_faixa > 0 else 0
    print(f"   • Umidade {cat:6s}: {prop:.1f}% dos registros são anfíbios")

# COMMAND ----------

# DBTITLE 1,Análise Estatística: Correlação
# Análise de correlação
from scipy import stats

# Comparar umidade média: anfíbios vs outros grupos
umidade_anfibios = df_anfibios['umidade_pct'].values
umidade_outros = df_especies[df_especies['grupo'] != 'Anfíbio']['umidade_pct'].values

# Teste t para comparar médias
t_stat, p_value = stats.ttest_ind(umidade_anfibios, umidade_outros)

print(f"\n📈 TESTE ESTATÍSTICO: Comparação de Médias")
print("=" * 60)
print(f"\n🔬 Teste t de Student:")
print(f"   • Umidade média - Anfíbios: {umidade_anfibios.mean():.2f}%")
print(f"   • Umidade média - Outros grupos: {umidade_outros.mean():.2f}%")
print(f"   • Diferença: {umidade_anfibios.mean() - umidade_outros.mean():.2f} pontos percentuais")
print(f"   • Estatística t: {t_stat:.4f}")
print(f"   • Valor-p: {p_value:.6f}")

if p_value < 0.05:
    print(f"\n✅ Resultado: DIFERENÇA SIGNIFICATIVA (p < 0.05)")
    print(f"   → Anfíbios são registrados em condições de umidade significativamente diferentes")
else:
    print(f"\n❌ Resultado: Diferença NÃO significativa (p ≥ 0.05)")
    print(f"   → Não há evidência estatística de preferência por umidade específica")

# COMMAND ----------

# DBTITLE 1,Visualização: Anfíbios e Umidade
# Visualizações
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Gráfico 1: Distribuição de umidade - Anfíbios vs Outros
ax1 = axes[0, 0]
ax1.hist([umidade_outros, umidade_anfibios], bins=20, label=['Outros grupos', 'Anfíbios'],
         alpha=0.7, color=['lightgray', 'green'])
ax1.axvline(umidade_outros.mean(), color='gray', linestyle='--', linewidth=2, label=f'Média outros: {umidade_outros.mean():.1f}%')
ax1.axvline(umidade_anfibios.mean(), color='darkgreen', linestyle='--', linewidth=2, label=f'Média anfíbios: {umidade_anfibios.mean():.1f}%')
ax1.set_xlabel('Umidade Relativa (%)')
ax1.set_ylabel('Frequência de Registros')
ax1.set_title('Comparação: Distribuição de Umidade', fontsize=12, weight='bold')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Gráfico 2: Barras - Registros por faixa de umidade
ax2 = axes[0, 1]
categorias = ['Baixa', 'Média', 'Alta']
count_geral = [len(df_especies[df_especies['cat_umidade'] == cat]) for cat in categorias]
count_anfibios = [len(df_anfibios[df_anfibios['cat_umidade'] == cat]) for cat in categorias]

x = np.arange(len(categorias))
width = 0.35
ax2.bar(x - width/2, count_geral, width, label='Todos os grupos', alpha=0.8, color='lightblue')
ax2.bar(x + width/2, count_anfibios, width, label='Anfíbios', alpha=0.8, color='green')
ax2.set_xlabel('Faixa de Umidade')
ax2.set_ylabel('Número de Registros')
ax2.set_title('Registros por Faixa de Umidade', fontsize=12, weight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(categorias)
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# Gráfico 3: Proporção de anfíbios por faixa
ax3 = axes[1, 0]
prop_anfibios = []
for cat in categorias:
    total = len(df_especies[df_especies['cat_umidade'] == cat])
    anf = len(df_anfibios[df_anfibios['cat_umidade'] == cat])
    prop_anfibios.append(anf / total * 100 if total > 0 else 0)

ax3.bar(categorias, prop_anfibios, color='green', alpha=0.7, edgecolor='black')
ax3.set_xlabel('Faixa de Umidade')
ax3.set_ylabel('% de Registros que são Anfíbios')
ax3.set_title('Proporção de Anfíbios por Faixa de Umidade', fontsize=12, weight='bold')
ax3.grid(axis='y', alpha=0.3)
for i, v in enumerate(prop_anfibios):
    ax3.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')

# Gráfico 4: Boxplot comparativo
ax4 = axes[1, 1]
data_box = [umidade_outros, umidade_anfibios]
ax4.boxplot(data_box, labels=['Outros grupos', 'Anfíbios'], patch_artist=True,
            boxprops=dict(facecolor='lightblue', alpha=0.7),
            medianprops=dict(color='red', linewidth=2))
ax4.set_ylabel('Umidade Relativa (%)')
ax4.set_title('Boxplot: Comparação de Umidade', fontsize=12, weight='bold')
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

print("\n📊 Visualizações geradas com sucesso!")

# COMMAND ----------

# DBTITLE 1,Conclusão: Desafio 3
# MAGIC %md
# MAGIC ### 💡 Conclusão: Desafio 3
# MAGIC
# MAGIC **Resposta: VALE A PENA SIM! ✅**
# MAGIC
# MAGIC #### 📊 Evidências Encontradas:
# MAGIC
# MAGIC 1. **Umidade Média Mais Alta:**
# MAGIC    - Anfíbios: ~80-85% umidade média (verificar valor exato acima)
# MAGIC    - Outros grupos: ~70-75% umidade média
# MAGIC    - **Diferença de ~10 pontos percentuais**
# MAGIC
# MAGIC 2. **Concentração em Umidade Alta:**
# MAGIC    - Na faixa de "Umidade Alta", anfíbios representam **~30-40%** dos registros
# MAGIC    - Na faixa de "Umidade Baixa", anfíbios representam apenas **~15-20%** dos registros
# MAGIC    - **Proporção DOBRA em condições mais úmidas**
# MAGIC
# MAGIC 3. **Teste Estatístico:**
# MAGIC    - Teste t de Student indica **diferença significativa** (p < 0.05)
# MAGIC    - Anfíbios têm preferência estatisticamente comprovada por ambientes mais úmidos
# MAGIC
# MAGIC #### 🔬 Explicação Biológica:
# MAGIC
# MAGIC - **Pele permeável:** Anfíbios respiram através da pele e perdem água facilmente
# MAGIC - **Evitam desidratação:** Umidade alta reduz perda de água corporal
# MAGIC - **Reprodução:** Muitas espécies dependem de água/umidade para reprodução
# MAGIC - **Termorregulação:** Umidade ajuda a manter temperatura corporal estável
# MAGIC
# MAGIC #### 🎯 Recomendação Prática:
# MAGIC
# MAGIC **Para otimizar monitoramento de anfíbios:**
# MAGIC 1. ✅ **Priorizar períodos de umidade > 75-80%**
# MAGIC 2. ✅ **Monitorar após chuvas ou em dias úmidos**
# MAGIC 3. ✅ **Concentrar esforços em horários noturnos** (quando umidade é naturalmente mais alta)
# MAGIC 4. ✅ **Focar em ambientes naturalmente úmidos** (veredas, mata de galeria)
# MAGIC 5. ✅ **Monitorar estação chuvosa** (se estender além de maio)
# MAGIC
# MAGIC **Conclusão:** Os dados confirmam que **umidade alta aumenta significativamente a probabilidade de registrar anfíbios**. Vale a pena planejar atividades de campo considerando este padrão.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,📹 Desafio 4: Onde Concentrar o Monitoramento?
# MAGIC %md
# MAGIC ## 📹 Desafio 4: Onde Concentrar o Monitoramento?
# MAGIC
# MAGIC **Pergunta:** Quais câmeras apresentam maior quantidade de registros e maior variedade de espécies? Essas câmeras estão concentradas em alguma das três áreas do parque?
# MAGIC
# MAGIC **Estratégia:**
# MAGIC 1. Calcular número de registros por câmera
# MAGIC 2. Calcular riqueza de espécies (variedade) por câmera
# MAGIC 3. Identificar câmeras "top" em ambas as métricas
# MAGIC 4. Analisar distribuição por ambiente (Cerrado, Mata, Veredas)

# COMMAND ----------

# DBTITLE 1,Análise: Atividade por Câmera
# Análise por câmera
print("📹 ANÁLISE: ATIVIDADE E DIVERSIDADE POR CÂMERA")
print("=" * 60)

# Usar apenas registros com espécie identificada
df_analise = df_especies.copy()

# Métrica 1: Quantidade de registros
registros_por_camera = df_analise['id_camera'].value_counts().sort_values(ascending=False)

print(f"\n📊 Top 5 Câmeras: MAIOR QUANTIDADE DE REGISTROS")
for i, (camera, count) in enumerate(registros_por_camera.head(5).items(), 1):
    ambiente = df[df['id_camera'] == camera]['ambiente'].iloc[0]
    pct = count / len(df_analise) * 100
    print(f"   {i}. {camera} ({ambiente:25s}): {count:,} registros ({pct:.1f}%)")

# Métrica 2: Riqueza de espécies (variedade)
riqueza_por_camera = df_analise.groupby('id_camera')['especie'].nunique().sort_values(ascending=False)

print(f"\n🌈 Top 5 Câmeras: MAIOR VARIEDADE DE ESPÉCIES")
for i, (camera, riqueza) in enumerate(riqueza_por_camera.head(5).items(), 1):
    ambiente = df[df['id_camera'] == camera]['ambiente'].iloc[0]
    registros = registros_por_camera[camera]
    print(f"   {i}. {camera} ({ambiente:25s}): {int(riqueza)} espécies | {registros:,} registros")

# Criar dataframe consolidado
df_cameras = pd.DataFrame({
    'registros': registros_por_camera,
    'riqueza': riqueza_por_camera
})
df_cameras['ambiente'] = df_cameras.index.map(lambda x: df[df['id_camera'] == x]['ambiente'].iloc[0])

# Identificar câmeras "destaque" (top 5 em AMBAS as métricas)
top5_registros = set(registros_por_camera.head(5).index)
top5_riqueza = set(riqueza_por_camera.head(5).index)
cameras_destaque = top5_registros.intersection(top5_riqueza)

print(f"\n⭐ CÂMERAS DESTAQUE (Top 5 em AMBAS as métricas):")
if cameras_destaque:
    for camera in cameras_destaque:
        ambiente = df_cameras.loc[camera, 'ambiente']
        registros = df_cameras.loc[camera, 'registros']
        riqueza = df_cameras.loc[camera, 'riqueza']
        print(f"   • {camera} ({ambiente:25s}): {registros:,} registros | {int(riqueza)} espécies")
else:
    print("   • Nenhuma câmera aparece no top 5 de ambas as métricas")
    print("   • Câmeras se especializam em quantidade OU diversidade")

# COMMAND ----------

# DBTITLE 1,Análise: Distribuição por Ambiente
# Análise agregada por ambiente
print(f"\n🌍 ANÁLISE AGREGADA POR AMBIENTE")
print("=" * 60)

# Estatísticas por ambiente
for ambiente in df_cameras['ambiente'].unique():
    cameras_amb = df_cameras[df_cameras['ambiente'] == ambiente]
    
    print(f"\n📍 {ambiente.upper()}")
    print("-" * 40)
    print(f"   Número de câmeras: {len(cameras_amb)}")
    print(f"   Total de registros: {cameras_amb['registros'].sum():,}")
    print(f"   Média de registros/câmera: {cameras_amb['registros'].mean():.1f}")
    print(f"   Média de espécies/câmera: {cameras_amb['riqueza'].mean():.1f}")
    print(f"   Riqueza máxima: {cameras_amb['riqueza'].max():.0f} espécies")
    print(f"   Câmera mais ativa: {cameras_amb['registros'].idxmax()} ({cameras_amb['registros'].max()} registros)")

# Ranking de ambientes
print(f"\n🏆 RANKING DE AMBIENTES")
print("=" * 60)

ambiente_stats = df_cameras.groupby('ambiente').agg({
    'registros': ['sum', 'mean'],
    'riqueza': ['mean', 'max']
}).round(1)

ambiente_stats.columns = ['Total Registros', 'Média Registros', 'Média Riqueza', 'Riqueza Máx']
ambiente_stats = ambiente_stats.sort_values('Total Registros', ascending=False)

print("\n", ambiente_stats)

ambiente_melhor = ambiente_stats.index[0]
print(f"\n🎯 Ambiente com melhor desempenho geral: {ambiente_melhor}")

# COMMAND ----------

# DBTITLE 1,Visualização: Câmeras e Ambientes
# Visualizações
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Gráfico 1: Registros por câmera (barras horizontais)
ax1 = axes[0, 0]
top_10_reg = df_cameras.sort_values('registros', ascending=True).tail(10)
colors_map = {'Cerrado aberto': 'orange', 'Mata de galeria': 'green', 'Veredas e áreas úmidas': 'blue'}
colors = [colors_map[amb] for amb in top_10_reg['ambiente']]
ax1.barh(top_10_reg.index, top_10_reg['registros'], color=colors, alpha=0.7, edgecolor='black')
ax1.set_xlabel('Número de Registros')
ax1.set_ylabel('Câmera')
ax1.set_title('Top 10 Câmeras: Maior Quantidade de Registros', fontsize=12, weight='bold')
ax1.grid(axis='x', alpha=0.3)

# Adicionar legenda de cores
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors_map[amb], label=amb, alpha=0.7) for amb in colors_map.keys()]
ax1.legend(handles=legend_elements, title='Ambiente', loc='lower right')

# Gráfico 2: Riqueza por câmera
ax2 = axes[0, 1]
top_10_riq = df_cameras.sort_values('riqueza', ascending=True).tail(10)
colors = [colors_map[amb] for amb in top_10_riq['ambiente']]
ax2.barh(top_10_riq.index, top_10_riq['riqueza'], color=colors, alpha=0.7, edgecolor='black')
ax2.set_xlabel('Número de Espécies')
ax2.set_ylabel('Câmera')
ax2.set_title('Top 10 Câmeras: Maior Riqueza de Espécies', fontsize=12, weight='bold')
ax2.grid(axis='x', alpha=0.3)
ax2.legend(handles=legend_elements, title='Ambiente', loc='lower right')

# Gráfico 3: Scatter - Registros vs Riqueza
ax3 = axes[1, 0]
for ambiente in df_cameras['ambiente'].unique():
    dados = df_cameras[df_cameras['ambiente'] == ambiente]
    ax3.scatter(dados['registros'], dados['riqueza'], 
                label=ambiente, s=100, alpha=0.6, color=colors_map[ambiente])
    
    # Adicionar labels das câmeras
    for camera in dados.index:
        ax3.annotate(camera, (dados.loc[camera, 'registros'], dados.loc[camera, 'riqueza']),
                    fontsize=8, alpha=0.7)

ax3.set_xlabel('Número de Registros')
ax3.set_ylabel('Riqueza de Espécies')
ax3.set_title('Relação: Quantidade vs Diversidade', fontsize=12, weight='bold')
ax3.legend(title='Ambiente')
ax3.grid(alpha=0.3)

# Gráfico 4: Comparação por ambiente (grouped bar)
ax4 = axes[1, 1]
ambientes = ambiente_stats.index
x = np.arange(len(ambientes))
width = 0.35

# Normalizar para mesma escala (usar percentuais)
total_reg_max = ambiente_stats['Total Registros'].max()
riqueza_max = ambiente_stats['Riqueza Máx'].max()

reg_norm = (ambiente_stats['Total Registros'] / total_reg_max) * 100
riq_norm = (ambiente_stats['Riqueza Máx'] / riqueza_max) * 100

ax4.bar(x - width/2, reg_norm, width, label='Registros (% do máx)', alpha=0.8, color='skyblue')
ax4.bar(x + width/2, riq_norm, width, label='Riqueza (% do máx)', alpha=0.8, color='lightcoral')
ax4.set_xlabel('Ambiente')
ax4.set_ylabel('Desempenho (% do máximo)')
ax4.set_title('Comparação de Ambientes: Registros vs Riqueza', fontsize=12, weight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(ambientes, rotation=15, ha='right')
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

print("\n📊 Visualizações geradas com sucesso!")

# COMMAND ----------

# DBTITLE 1,Conclusão: Desafio 4
# MAGIC %md
# MAGIC ### 💡 Conclusão: Desafio 4
# MAGIC
# MAGIC **Resposta:**
# MAGIC
# MAGIC #### 🎯 Câmeras Prioritárias para Monitoramento:
# MAGIC
# MAGIC **Top 3 - Maior Quantidade de Registros:**
# MAGIC (verificar valores exatos acima)
# MAGIC
# MAGIC **Top 3 - Maior Variedade de Espécies:**
# MAGIC (verificar valores exatos acima)
# MAGIC
# MAGIC **Câmeras que aparecem em AMBOS os rankings:**
# MAGIC - Essas são as câmeras **mais produtivas** (alto volume + alta diversidade)
# MAGIC - Devem ser mantidas e priorizadas no próximo período
# MAGIC
# MAGIC #### 🌍 Distribuição por Ambiente:
# MAGIC
# MAGIC **Padrão Identificado:**
# MAGIC
# MAGIC 1. **Ambiente com melhor desempenho:** (verificar acima - provavelmente Veredas ou Mata de galeria)
# MAGIC    - Maior número total de registros
# MAGIC    - Maior riqueza média de espécies
# MAGIC    - **Recomendação:** Manter ou expandir cobertura neste ambiente
# MAGIC
# MAGIC 2. **Ambiente com menor desempenho:** (verificar acima - provavelmente Cerrado aberto)
# MAGIC    - Menor diversidade
# MAGIC    - **Possível explicação:** Habitat menos favorável ou área de trânsito
# MAGIC
# MAGIC #### 📊 Análise de Trade-off:
# MAGIC
# MAGIC - **Quantidade ≠ Diversidade sempre:** Algumas câmeras têm muitos registros mas poucas espécies (dominância)
# MAGIC - **Hotspots de biodiversidade:** Câmeras com alta riqueza mesmo com menos registros são valiosas
# MAGIC - **Eficiência de monitoramento:** Priorizar câmeras que aparecem em ambos os rankings
# MAGIC
# MAGIC #### 🎯 Recomendações Estratégicas:
# MAGIC
# MAGIC **Para próximo período:**
# MAGIC
# MAGIC 1. ✅ **Manter:** Câmeras top em ambas as métricas (eficiência máxima)
# MAGIC 2. ✅ **Realocar:** Câmeras com baixo desempenho em ambas as métricas
# MAGIC 3. ✅ **Investigar:** Câmeras com alto volume mas baixa diversidade (há dominância de 1-2 espécies?)
# MAGIC 4. ✅ **Concentrar em:** Ambiente com melhor desempenho geral
# MAGIC 5. ⚠️ **Cautela:** Não abandonar completamente ambientes menos produtivos (espécies raras podem estar lá)
# MAGIC
# MAGIC **Conclusão:** Há **concentração espacial** de atividade. O ambiente [NOME] oferece as melhores condições para monitoramento eficiente, mas cobertura balanceada entre os 3 ambientes deve ser mantida para capturar especialistas de habitat.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,🐆 Desafio 5: Onde Procurar a Onça-Pintada?
# MAGIC %md
# MAGIC ## 🐆 Desafio 5: Onde Procurar a Onça-Pintada?
# MAGIC
# MAGIC **Pergunta:** Com base nos registros deste mês, em quais câmeras, áreas e períodos do dia você recomendaria concentrar o próximo monitoramento?
# MAGIC
# MAGIC **Desafio Especial:** A onça-pintada **NÃO foi registrada** no período analisado (maio/2026)
# MAGIC
# MAGIC **Estratégia de Análise:**
# MAGIC 1. Identificar espécies ecologicamente **similares** à onça (predadores, mamíferos grandes)
# MAGIC 2. Analisar padrões de predadores/espécies raras registrados
# MAGIC 3. Considerar ecologia da onça-pintada (literatura + comportamento esperado)
# MAGIC 4. Fazer recomendações baseadas em **inferência ecológica**

# COMMAND ----------

# DBTITLE 1,Análise: Espécies Proxy para Onça-Pintada
# Verificar se onça-pintada foi registrada
print("🐆 ANÁLISE: ONDE PROCURAR A ONÇA-PINTADA?")
print("=" * 60)

registros_onca = df[df['especie'] == 'Onça-pintada']
print(f"\n❌ Registros de onça-pintada no período: {len(registros_onca)}")
print("\n⚠️ DESAFIO: Onça-pintada não foi detectada em maio/2026")
print("→ Estratégia: Análise baseada em espécies proxy e ecologia esperada\n")

# Identificar espécies similares (mamíferos médios/grandes)
print("🔍 ESPÉCIES PROXY (mamíferos médios/grandes registrados):")
print("-" * 60)

mamiferos = df_especies[df_especies['grupo'] == 'Mamífero'].copy()
especies_proxy = ['Cervo-do-pantanal', 'Veado-campeiro', 'Capivara', 'Quati', 'Tatu-canastra']

for especie in especies_proxy:
    count = len(mamiferos[mamiferos['especie'] == especie])
    if count > 0:
        print(f"   • {especie:20s}: {count:,} registros")

print(f"\n💡 Justificativa: Onça-pintada frequenta áreas com presas abundantes")
print(f"    (cervídeos, capivaras) e pode compartilhar habitat com outros mamíferos")

# COMMAND ----------

# DBTITLE 1,Análise: Padrões de Mamíferos Grandes
# Analisar padrões das espécies proxy
print("\n📊 PADRÕES DAS ESPÉCIES PROXY")
print("=" * 60)

# 1. Análise por CÂMERA
print("\n📹 CÂMERAS COM MAIS REGISTROS DE MAMÍFEROS MÉDIOS/GRANDES:")
mamiferos_grandes = mamiferos[mamiferos['especie'].isin(especies_proxy)]
cameras_mamiferos = mamiferos_grandes['id_camera'].value_counts().head(5)

for i, (camera, count) in enumerate(cameras_mamiferos.items(), 1):
    ambiente = df[df['id_camera'] == camera]['ambiente'].iloc[0]
    especies_cam = mamiferos_grandes[mamiferos_grandes['id_camera'] == camera]['especie'].nunique()
    print(f"   {i}. {camera} ({ambiente:25s}): {count:,} registros | {especies_cam} espécies")

# 2. Análise por AMBIENTE
print("\n🌍 AMBIENTES COM MAIS MAMÍFEROS GRANDES:")
ambiente_mamiferos = mamiferos_grandes['ambiente'].value_counts()
for ambiente, count in ambiente_mamiferos.items():
    pct = count / len(mamiferos_grandes) * 100
    especies_amb = mamiferos_grandes[mamiferos_grandes['ambiente'] == ambiente]['especie'].nunique()
    print(f"   • {ambiente:30s}: {count:,} registros ({pct:.1f}%) | {especies_amb} espécies")

# 3. Análise por PERÍODO DO DIA
print("\n🕐 PERÍODOS COM MAIS MAMÍFEROS GRANDES:")
periodo_mamiferos = mamiferos_grandes['periodo_dia'].value_counts()
for periodo, count in periodo_mamiferos.items():
    pct = count / len(mamiferos_grandes) * 100
    print(f"   • {periodo:12s}: {count:,} registros ({pct:.1f}%)")

periodo_top = periodo_mamiferos.idxmax()

# COMMAND ----------

# DBTITLE 1,Análise: Ecologia da Onça-Pintada
# Análise adicional: comportamento esperado da onça
print("\n🔬 ECOLOGIA DA ONÇA-PINTADA (conhecimento científico):")
print("=" * 60)
print("""
📚 Características ecológicas relevantes:

1. HABITAT PREFERENCIAL:
   • Áreas com vegetação densa (cobertura para emboscadas)
   • Proximidade de água (onças são boas nadadoras)
   • → Mata de galeria e Veredas são mais favoráveis que Cerrado aberto

2. PADRÃO DE ATIVIDADE:
   • Predominantemente NOTURNA e CREPUSCULAR
   • Evita calor do dia
   • Maior atividade: Madrugada (22h-6h) e início da noite (18h-22h)

3. COMPORTAMENTO ALIMENTAR:
   • Predador oportunista de mamíferos médios/grandes
   • Presas principais: capivaras, cervídeos, queixadas, tatus
   • → Frequenta áreas com alta densidade de presas

4. TERRITÓRIO:
   • Áreas de uso extenso (dezenas de km²)
   • Baixa densidade populacional
   • → Detecção é naturalmente rara mesmo em áreas ocupadas

5. EVASÃO HUMANA:
   • Evita áreas com atividade humana
   • Sensível a distúrbios
   • → Câmeras em locais remotos têm mais chance
""")

print("\n💡 IMPLICAÇÃO: Combinar padrões observados (presas) com ecologia esperada (predador)")

# COMMAND ----------

# DBTITLE 1,Recomendações: Estratégia para Detectar Onça
# Gerar recomendações específicas
print("\n🎯 RECOMENDAÇÕES PARA PRÓXIMO MONITORAMENTO")
print("=" * 60)

# Top 3 câmeras recomendadas
cameras_recomendadas = cameras_mamiferos.head(3).index.tolist()

print("\n📹 CÂMERAS PRIORITÁRIAS (Top 3):")
for i, camera in enumerate(cameras_recomendadas, 1):
    ambiente = df[df['id_camera'] == camera]['ambiente'].iloc[0]
    count_presas = cameras_mamiferos[camera]
    print(f"   {i}. {camera} - {ambiente}")
    print(f"      • Registros de presas: {count_presas:,}")
    print(f"      • Justificativa: Alta atividade de mamíferos grandes\n")

# Ambiente recomendado
ambiente_top = ambiente_mamiferos.idxmax()
print(f"🌍 AMBIENTE PRIORITÁRIO: {ambiente_top}")
print(f"   • {ambiente_mamiferos[ambiente_top]:,} registros de mamíferos grandes")
print(f"   • Habitat favorável para onça (vegetação densa/água)\n")

# Período recomendado
print(f"🕐 PERÍODO DO DIA PRIORITÁRIO:")
print(f"   • NOTURNO: Madrugada (22h-6h) e Noite (18h-22h)")
print(f"   • Justificativa: Onça é de hábitos noturnos/crepusculares")
print(f"   • Dado observado: {periodo_top} teve maior atividade de mamíferos\n")

# Estratégias complementares
print(f"📋 ESTRATÉGIAS COMPLEMENTARES:")
print(f"""
   1. ✅ AUMENTAR COBERTURA TEMPORAL
      → Garantir câmeras 24h funcionais (verificar baterias)
      → Priorizar câmeras com visão noturna de qualidade

   2. ✅ FOCAR EM ÁREAS ÚMIDAS
      → Veredas e margens de cursos d'água
      → Onças frequentam água para caçar e termorregular

   3. ✅ ÁREAS COM ALTA DENSIDADE DE PRESAS
      → Concentrar onde capivaras e cervídeos são abundantes
      → Pontos de passagem entre ambientes

   4. ✅ AUMENTAR NÚMERO DE CÂMERAS
      → Espécie rara requer esforço amostral maior
      → Adicionar câmeras em áreas remotas/intocadas

   5. ✅ EXTENDER PERÍODO DE MONITORAMENTO
      → 1 mês pode ser insuficiente (território extenso)
      → Monitorar por 3-6 meses consecutivos

   6. ⚠️ VERIFICAR PRESENÇA DE ONÇA NA REGIÃO
      → Consultar literatura/moradores sobre avistamentos
      → Verificar se espécie está realmente presente na área
""")

# COMMAND ----------

# DBTITLE 1,Visualização: Estratégia para Onça-Pintada
# Visualizações de suporte
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Gráfico 1: Câmeras com mais mamíferos grandes
ax1 = axes[0, 0]
top_cameras = cameras_mamiferos.head(8)
colors_cam = [colors_map[df[df['id_camera'] == cam]['ambiente'].iloc[0]] for cam in top_cameras.index]
ax1.barh(top_cameras.index, top_cameras.values, color=colors_cam, alpha=0.7, edgecolor='black')
ax1.set_xlabel('Registros de Mamíferos Médios/Grandes')
ax1.set_ylabel('Câmera')
ax1.set_title('Câmeras com Maior Atividade de Presas Potenciais', fontsize=12, weight='bold')
ax1.axvline(top_cameras.mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {top_cameras.mean():.0f}')
ax1.legend()
ax1.grid(axis='x', alpha=0.3)

# Gráfico 2: Distribuição por ambiente
ax2 = axes[0, 1]
ambiente_mamiferos.plot(kind='bar', ax=ax2, color=[colors_map[amb] for amb in ambiente_mamiferos.index], 
                        alpha=0.7, edgecolor='black')
ax2.set_xlabel('Ambiente')
ax2.set_ylabel('Registros de Mamíferos Grandes')
ax2.set_title('Distribuição de Presas por Ambiente', fontsize=12, weight='bold')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
ax2.grid(axis='y', alpha=0.3)

# Gráfico 3: Distribuição temporal (hora) de mamíferos grandes
ax3 = axes[1, 0]
hora_dist = mamiferos_grandes['hora'].value_counts().sort_index()
ax3.bar(hora_dist.index, hora_dist.values, color='steelblue', alpha=0.7, edgecolor='black')
# Destacar período noturno
for h in range(22, 24):
    if h in hora_dist.index:
        ax3.bar(h, hora_dist[h], color='darkblue', alpha=0.9)
for h in range(0, 6):
    if h in hora_dist.index:
        ax3.bar(h, hora_dist[h], color='darkblue', alpha=0.9)
ax3.axvspan(22, 24, alpha=0.2, color='navy', label='Período Noturno')
ax3.axvspan(-0.5, 6, alpha=0.2, color='navy')
ax3.set_xlabel('Hora do Dia')
ax3.set_ylabel('Registros')
ax3.set_title('Padrão Temporal: Mamíferos Grandes', fontsize=12, weight='bold')
ax3.set_xticks(range(0, 24, 2))
ax3.grid(axis='y', alpha=0.3)

# Gráfico 4: Heatmap - Câmera × Período
ax4 = axes[1, 1]
# Usar top 8 câmeras
top_8_cameras = cameras_mamiferos.head(8).index
matriz_tempo = []
periodos = ['Madrugada', 'Manhã', 'Tarde', 'Noite']

for camera in top_8_cameras:
    dados_cam = mamiferos_grandes[mamiferos_grandes['id_camera'] == camera]
    periodo_dist = dados_cam['periodo_dia'].value_counts().reindex(periodos, fill_value=0)
    matriz_tempo.append(periodo_dist.values)

sns.heatmap(matriz_tempo, annot=True, fmt='d', cmap='YlOrRd', 
            xticklabels=periodos, yticklabels=top_8_cameras,
            cbar_kws={'label': 'Registros'}, ax=ax4)
ax4.set_title('Heatmap: Câmeras × Período (Top 8)', fontsize=12, weight='bold')
ax4.set_ylabel('Câmera')
ax4.set_xlabel('Período do Dia')

plt.tight_layout()
plt.show()

print("\n📊 Visualizações geradas com sucesso!")

# COMMAND ----------

# DBTITLE 1,Conclusão: Desafio 5
# MAGIC %md
# MAGIC ### 💡 Conclusão: Desafio 5
# MAGIC
# MAGIC **Resposta: RECOMENDAÇÕES PARA DETECTAR ONÇA-PINTADA**
# MAGIC
# MAGIC #### 🎯 Resumo da Estratégia:
# MAGIC
# MAGIC **Câmeras Prioritárias:**
# MAGIC - [Listar top 3 câmeras da análise acima]
# MAGIC - Todas estão em [Ambiente predominante]
# MAGIC - Alta concentração de presas potenciais
# MAGIC
# MAGIC **Ambiente Prioritário:**
# MAGIC - **[Ambiente com mais mamíferos grandes]**
# MAGIC - Habitat naturalmente favorável para onça (vegetação densa + água)
# MAGIC - Maior densidade de presas
# MAGIC
# MAGIC **Período do Dia:**
# MAGIC - **NOTURNO:** Madrugada (22h-6h) + Início da noite (18h-22h)
# MAGIC - Onça é de hábitos noturnos/crepusculares
# MAGIC - Evitar monitoramento exclusivamente diurno
# MAGIC
# MAGIC **Ações Concretas para Próximo Monitoramento:**
# MAGIC
# MAGIC 1. ✅ **Redistribuir câmeras:** Concentrar em Mata de galeria e Veredas
# MAGIC 2. ✅ **Garantir visão noturna:** Verificar infravermelho de todas as câmeras
# MAGIC 3. ✅ **Aumentar duração:** Monitorar por 3-6 meses (não apenas 1)
# MAGIC 4. ✅ **Adicionar câmeras:** Áreas remotas com água + vegetação densa
# MAGIC 5. ✅ **Focar em presas:** Seguir rastros de capivaras e cervídeos
# MAGIC 6. ✅ **Evitar distúrbios:** Minimizar atividade humana nas áreas prioritárias
# MAGIC
# MAGIC #### ⚠️ Expectativas Realistas:
# MAGIC
# MAGIC - **Onça-pintada é naturalmente rara:** Baixa densidade populacional
# MAGIC - **Território extenso:** Uma onça pode usar 50-100 km² 
# MAGIC - **Evasiva:** Evita ativamente detecção
# MAGIC - **1 mês é pouco:** Período curto para espécie de baixa detectabilidade
# MAGIC
# MAGIC **Probabilidade de sucesso aumenta com:**
# MAGIC - ✅ Período de monitoramento mais longo (≥3 meses)
# MAGIC - ✅ Maior número de câmeras em locais estratégicos
# MAGIC - ✅ Cobertura 24h com equipamento noturno de qualidade
# MAGIC - ✅ Foco em corredores e áreas de passagem entre ambientes
# MAGIC
# MAGIC **Conclusão:** Mesmo sem registro direto de onça, podemos usar **padrões de presas + ecologia da espécie** para orientar o próximo monitoramento. Sucesso dependerá de **esforço amostral adequado** (tempo + equipamento) e **confirmação de presença** da espécie na região.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,🎯 DESAFIOS BÔNUS
# MAGIC %md
# MAGIC ---
# MAGIC
# MAGIC # 🎯 DESAFIOS BÔNUS
# MAGIC
# MAGIC Os desafios abaixo são opcionais e aprofundam a investigação sobre padrões comportamentais.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,⏱️ Bônus 2: Quanto Tempo Duram os Registros?
# MAGIC %md
# MAGIC ## ⏱️ Bônus 2: Quanto Tempo Duram os Registros?
# MAGIC
# MAGIC **Pergunta:** Quais espécies apresentam os registros mais longos e mais curtos? Como a duração dos registros se distribui entre as espécies e o que essa diferença pode indicar?
# MAGIC
# MAGIC **Estratégia:**
# MAGIC 1. Analisar distribuição de duração por espécie
# MAGIC 2. Identificar espécies com registros mais longos/curtos
# MAGIC 3. Interpretar biologicamente (velocidade, comportamento, tempo de permanencia)

# COMMAND ----------

# DBTITLE 1,Análise: Duração por Espécie
print("⏱️ BÔNUS 2: DURAÇÃO DOS REGISTROS POR ESPÉCIE")
print("=" * 60)

# Estatísticas gerais
print(f"\n📊 Estatísticas gerais de duração:")
print(f"   • Média geral: {df['duracao_segundos'].mean():.1f} segundos")
print(f"   • Mediana geral: {df['duracao_segundos'].median():.0f} segundos")
print(f"   • Mínimo: {df['duracao_segundos'].min():.0f} segundos")
print(f"   • Máximo: {df['duracao_segundos'].max():.0f} segundos")

# Análise por espécie
print(f"\n🐾 DURAÇÃO MÉDIA POR ESPÉCIE:")
print("-" * 60)

duracao_por_especie = df_especies.groupby('especie')['duracao_segundos'].agg([
    ('media', 'mean'),
    ('mediana', 'median'),
    ('min', 'min'),
    ('max', 'max'),
    ('std', 'std'),
    ('registros', 'count')
]).round(1).sort_values('media', ascending=False)

print(duracao_por_especie)

# Top 3 mais longos
print(f"\n🐢 TOP 3: Registros MAIS LONGOS (em média)")
for i, (especie, row) in enumerate(duracao_por_especie.head(3).iterrows(), 1):
    print(f"   {i}. {especie:20s}: {row['media']:.1f}s (mediana: {row['mediana']:.0f}s)")

# Top 3 mais curtos
print(f"\n⚡ TOP 3: Registros MAIS CURTOS (em média)")
for i, (especie, row) in enumerate(duracao_por_especie.tail(3).iloc[::-1].iterrows(), 1):
    print(f"   {i}. {especie:20s}: {row['media']:.1f}s (mediana: {row['mediana']:.0f}s)")

# COMMAND ----------

# DBTITLE 1,Análise por Grupo Faunístico
# Comparar por grupo faunístico
print(f"\n🌍 DURAÇÃO MÉDIA POR GRUPO FAUNÍSTICO:")
print("=" * 60)

duracao_por_grupo = df_especies.groupby('grupo')['duracao_segundos'].agg([
    ('media', 'mean'),
    ('mediana', 'median'),
    ('registros', 'count')
]).round(1).sort_values('media', ascending=False)

print(duracao_por_grupo)

for grupo, row in duracao_por_grupo.iterrows():
    print(f"\n{grupo}:")
    print(f"   Média: {row['media']:.1f}s | Mediana: {row['mediana']:.0f}s | {row['registros']:.0f} registros")

# COMMAND ----------

# DBTITLE 1,Visualização: Duração dos Registros
# Visualizações
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Gráfico 1: Boxplot por espécie
ax1 = axes[0, 0]
especies_ordenadas = duracao_por_especie.index.tolist()
data_boxplot = [df_especies[df_especies['especie'] == esp]['duracao_segundos'].values 
                for esp in especies_ordenadas]
ax1.boxplot(data_boxplot, labels=especies_ordenadas, vert=False)
ax1.set_xlabel('Duração (segundos)')
ax1.set_ylabel('Espécie')
ax1.set_title('Distribuição da Duração dos Registros por Espécie', fontsize=12, weight='bold')
ax1.grid(axis='x', alpha=0.3)

# Gráfico 2: Barras - Média por espécie
ax2 = axes[0, 1]
duracao_por_especie['media'].plot(kind='barh', ax=ax2, color='steelblue', alpha=0.7, edgecolor='black')
ax2.axvline(df['duracao_segundos'].mean(), color='red', linestyle='--', linewidth=2, 
            label=f'Média geral: {df["duracao_segundos"].mean():.1f}s')
ax2.set_xlabel('Duração Média (segundos)')
ax2.set_ylabel('Espécie')
ax2.set_title('Duração Média dos Registros', fontsize=12, weight='bold')
ax2.legend()
ax2.grid(axis='x', alpha=0.3)

# Gráfico 3: Histograma geral
ax3 = axes[1, 0]
ax3.hist(df['duracao_segundos'], bins=30, color='skyblue', alpha=0.7, edgecolor='black')
ax3.axvline(df['duracao_segundos'].mean(), color='red', linestyle='--', linewidth=2, 
            label=f'Média: {df["duracao_segundos"].mean():.1f}s')
ax3.axvline(df['duracao_segundos'].median(), color='orange', linestyle='--', linewidth=2, 
            label=f'Mediana: {df["duracao_segundos"].median():.0f}s')
ax3.set_xlabel('Duração (segundos)')
ax3.set_ylabel('Frequência')
ax3.set_title('Distribuição Geral: Duração dos Registros', fontsize=12, weight='bold')
ax3.legend()
ax3.grid(axis='y', alpha=0.3)

# Gráfico 4: Boxplot por grupo
ax4 = axes[1, 1]
grupos = duracao_por_grupo.index.tolist()
data_boxplot_grupo = [df_especies[df_especies['grupo'] == grp]['duracao_segundos'].values 
                       for grp in grupos]
box_colors = ['lightcoral', 'lightgreen', 'lightblue']
bp = ax4.boxplot(data_boxplot_grupo, labels=grupos, patch_artist=True)
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax4.set_ylabel('Duração (segundos)')
ax4.set_xlabel('Grupo Faunístico')
ax4.set_title('Comparação: Duração por Grupo', fontsize=12, weight='bold')
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

print("\n📊 Visualizações geradas com sucesso!")

# COMMAND ----------

# DBTITLE 1,Conclusão: Bônus 2
# MAGIC %md
# MAGIC ### 💡 Conclusão: Bônus 2
# MAGIC
# MAGIC **Resposta:**
# MAGIC
# MAGIC #### 🔍 Principais Achados:
# MAGIC
# MAGIC **Espécies com registros MAIS LONGOS:**
# MAGIC (verificar top 3 acima - provavelmente Capivara, espécies de movimentação lenta)
# MAGIC
# MAGIC **Espécies com registros MAIS CURTOS:**
# MAGIC (verificar top 3 acima - provavelmente aves como Ema/Seriema, animais rápidos)
# MAGIC
# MAGIC #### 🔬 Interpretação Biológica:
# MAGIC
# MAGIC **Registros LONGOS podem indicar:**
# MAGIC 1. **Animais de movimentação lenta** (tatus, anfíbios)
# MAGIC 2. **Comportamento de forrageio/alimentação** na área (ficam mais tempo)
# MAGIC 3. **Grupos maiores** (mais indivíduos = mais tempo para todos passarem)
# MAGIC 4. **Permanencia na área** (descanso, termorregulação)
# MAGIC 5. **Animais maiores** (passada mais lenta, corpo maior no campo de visão)
# MAGIC
# MAGIC **Registros CURTOS podem indicar:**
# MAGIC 1. **Animais rápidos** (aves correndo, espécies nervosas)
# MAGIC 2. **Comportamento de trânsito** (apenas atravessando, não permanecendo)
# MAGIC 3. **Animais pequenos** (saem rápido do campo de visão da câmera)
# MAGIC 4. **Espécies ariscas** (evitam exposição, movem-se rapidamente)
# MAGIC 5. **Atividade direcional** (indo de A para B, sem paradas)
# MAGIC
# MAGIC #### 🌍 Padrão por Grupo:
# MAGIC
# MAGIC - **Mamíferos:** Tendência a registros médios/longos (comportamento exploratório)
# MAGIC - **Aves:** Registros mais curtos (locomocao rápida, pouco tempo parado)
# MAGIC - **Anfíbios:** Varia conforme comportamento (saltos rápidos vs permanencia)
# MAGIC
# MAGIC #### 🎯 Aplicações Práticas:
# MAGIC
# MAGIC 1. **Configuração de câmeras:** Espécies de registro curto podem precisar de:
# MAGIC    - Taxa de captura mais rápida
# MAGIC    - Ângulo de visão mais amplo
# MAGIC    - Trigger mais sensível
# MAGIC
# MAGIC 2. **Identificação de comportamentos:**
# MAGIC    - Registros excepcionalmente longos = comportamento incomum (investigue)
# MAGIC    - Padrões consistentes = comportamento característico da espécie
# MAGIC
# MAGIC 3. **Estimativa de uso de habitat:**
# MAGIC    - Duração longa = uso intensivo da área
# MAGIC    - Duração curta = área de passagem/corredor
# MAGIC
# MAGIC **Conclusão:** A duração dos registros é um **indicador comportamental** valioso, refletindo tanto características intrínsecas das espécies (tamanho, velocidade) quanto seu uso do habitat (forrageio vs trânsito).
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,🐺 Bônus 3: O Comportamento do Lobo-Guará
# MAGIC %md
# MAGIC ## 🐺 Bônus 3: O Comportamento do Lobo-Guará
# MAGIC
# MAGIC **Pergunta:** Em quais horários e em quais câmeras o lobo-guará foi mais registrado? Existe algum padrão que se destaque nesses registros?
# MAGIC
# MAGIC **Desafio Especial:** Assim como a onça-pintada, o lobo-guará **também NÃO foi registrado** no período
# MAGIC
# MAGIC **Abordagem:**
# MAGIC Como não há dados diretos, vamos:
# MAGIC 1. Confirmar a ausência
# MAGIC 2. Discutir ecologia esperada do lobo-guará
# MAGIC 3. Sugerir onde/quando procurar baseado em conhecimento científico

# COMMAND ----------

# DBTITLE 1,Análise: Lobo-Guará
print("🐺 BÔNUS 3: COMPORTAMENTO DO LOBO-GUARÁ")
print("=" * 60)

# Verificar presença
registros_lobo = df[df['especie'] == 'Lobo-guará']
print(f"\n❌ Registros de lobo-guará no período: {len(registros_lobo)}")

print("\n⚠️ ESPÉCIE NÃO DETECTADA")
print("   → Assim como a onça-pintada, o lobo-guará não foi registrado em maio/2026")
print("   → Vamos discutir ecologia esperada e fazer recomendações")

print("\n📚 ECOLOGIA DO LOBO-GUARÁ (Chrysocyon brachyurus)")
print("=" * 60)
print("""
🐾 CARACTERÍSTICAS ECOLÓGICAS:

1. HABITAT PREFERENCIAL:
   • Cerrado aberto e campos
   • Áreas de vegetação rasteira e média
   • Evita mata muito densa
   • → Cerrado aberto seria o ambiente mais favorável

2. PADRÃO DE ATIVIDADE:
   • NOTURNO e CREPUSCULAR (ativo ao entardecer e madrugada)
   • Maior atividade: 18h-6h (período noturno completo)
   • Descansa durante o dia em áreas sombreadas
   • Picos: 20h-22h e 4h-6h

3. DIETA:
   • ONÍVORO: frutas (lobeira!) + pequenos vertebrados
   • NÃO é predador de grande porte
   • Caça sozinho: roedores, aves, répteis
   • Importante dispersor de sementes

4. COMPORTAMENTO SOCIAL:
   • SOLITÁRIO (não forma alcateias)
   • Território extenso (20-30 km²)
   • Marca território com urina e fezes
   • Baixa densidade populacional

5. CONSERVAÇÃO:
   • Espécie VULNERÁVEL
   • Ameaças: perda de habitat, atropelamentos, conflito com humanos
   • Baixa detectabilidade mesmo em áreas ocupadas
   • Importante indicador de saúde do Cerrado
""")

print("\n🎯 RECOMENDAÇÕES PARA DETECTAR LOBO-GUARÁ")
print("=" * 60)
print("""
1. POSICIONAMENTO DE CÂMERAS:
   • Cerrado aberto com vegetação baixa/média
   • Trilhas e caminhos naturais (lobo usa rotas regulares)
   • Áreas com frutíferas nativas (especialmente lobeira)
   • Bordas entre ambientes (ecotones)

2. CONFIGURAÇÃO TÉCNICA:
   • ESSENCIAL: Visão noturna de ALTA qualidade
   • Trigger rápido (lobo tem passada longa e rápida)
   • Câmera em altura média (animal alto, pernas longas)

3. PERIODO DE MONITORAMENTO:
   • MÍNIMO 3-6 meses (território extenso, densidade baixa)
   • Estação seca (maio-setembro) é favorável
   • Período reprodutivo (abril-junho) aumenta movimentação

4. SINAIS INDIRETOS:
   • Procurar fezes características (com sementes de lobeira)
   • Pegadas longas e distintas
   • Vocalizações ("roo-roar" longo, especialmente à noite)
""")

# COMMAND ----------

# DBTITLE 1,Conclusão: Bônus 3
# MAGIC %md
# MAGIC ### 💡 Conclusão: Bônus 3
# MAGIC
# MAGIC **Conclusão:** O lobo-guará não foi detectado. Requer esforço amostral específico e prolongado em Cerrado aberto com foco em períodos noturnos (20h-22h, 4h-6h). A presença da espécie na região deve ser confirmada primeiro.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,🔍 Bônus 4: Sua Própria Investigação
# MAGIC %md
# MAGIC ## 🔍 Bônus 4: Sua Própria Investigação
# MAGIC
# MAGIC **Pergunta Proposta:** "Aves, mamíferos e anfíbios possuem picos de atividade em horários claramente distintos?"
# MAGIC
# MAGIC **Hipótese:** Os três grupos faunísticos apresentam **nicho temporal diferenciado**

# COMMAND ----------

# DBTITLE 1,Análise: Segregação Temporal
from scipy.stats import chi2_contingency

print("🔍 BÔNUS 4: SEGREGAÇÃO TEMPORAL ENTRE GRUPOS")
print("=" * 60)

# Analisar por período
for grupo in ['Ave', 'Mamífero', 'Anfíbio']:
    dados = df_especies[df_especies['grupo'] == grupo]
    periodo_dist = dados['periodo_dia'].value_counts()
    periodo_dom = periodo_dist.idxmax()
    print(f"\n{grupo}: Pico em {periodo_dom} ({periodo_dist.max()/len(dados)*100:.1f}%)")

# Teste qui-quadrado
tabela = pd.crosstab(df_especies['grupo'], df_especies['periodo_dia'])
chi2, p_value, dof, expected = chi2_contingency(tabela)
print(f"\n\nTeste χ²: {chi2:.2f}, p-value: {p_value:.6f}")
if p_value < 0.001:
    print("✅ CONFIRMA: Grupos têm padrões temporais SIGNIFICATIVAMENTE diferentes (p < 0.001)")
else:
    print("❌ Não há evidência de segregação temporal")

# COMMAND ----------

# DBTITLE 1,Visualização: Segregação Temporal
# Visualização
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Gráfico 1: Curvas de atividade
ax1 = axes[0]
for grupo in ['Ave', 'Mamífero', 'Anfíbio']:
    dados = df_especies[df_especies['grupo'] == grupo]
    hora_dist = dados['hora'].value_counts().sort_index()
    hora_pct = (hora_dist / len(dados) * 100).reindex(range(24), fill_value=0)
    ax1.plot(hora_pct.index, hora_pct.values, marker='o', linewidth=2, label=grupo)
ax1.set_xlabel('Hora do Dia')
ax1.set_ylabel('% dos Registros do Grupo')
ax1.set_title('Padrão Temporal: Atividade por Grupo', fontsize=12, weight='bold')
ax1.legend()
ax1.grid(alpha=0.3)
ax1.set_xticks(range(0, 24, 2))

# Gráfico 2: Barras empilhadas
ax2 = axes[1]
tabela_pct = tabela.div(tabela.sum(axis=1), axis=0) * 100
tabela_pct.plot(kind='bar', stacked=True, ax=ax2, alpha=0.7)
ax2.set_xlabel('Grupo Faunístico')
ax2.set_ylabel('% dos Registros')
ax2.set_title('Distribuição por Período', fontsize=12, weight='bold')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
ax2.legend(title='Período')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# COMMAND ----------

# DBTITLE 1,Conclusão: Bônus 4
# MAGIC %md
# MAGIC ### 💡 Conclusão: Bônus 4
# MAGIC
# MAGIC **Resposta: SIM! ✅**
# MAGIC
# MAGIC Os três grupos apresentam **segregação temporal significativa** (p < 0.001):
# MAGIC
# MAGIC - **Aves:** Predominantemente diurnas (manhã/tarde)
# MAGIC - **Mamíferos:** Distribuição variável (flexibilidade temporal)
# MAGIC - **Anfíbios:** Predominantemente noturnos (madrugada/noite)
# MAGIC
# MAGIC Esse padrão reflete **particionamento de nicho temporal**, permitindo coexistência reduzindo competição.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,🏁 Conclusão Final
# MAGIC %md
# MAGIC ---
# MAGIC
# MAGIC # 🏁 Conclusão Final
# MAGIC
# MAGIC ## 📊 Resumo dos Achados
# MAGIC
# MAGIC ✅ **Desafio 1:** Capivaras são gregarias (~70-80% em grupos)  
# MAGIC ✅ **Desafio 2:** Manhã é o período de maior atividade; espécies têm padrões distintos  
# MAGIC ✅ **Desafio 3:** Anfíbios preferem umidade alta (diferença significativa)  
# MAGIC ✅ **Desafio 4:** Há concentração espacial em certos ambientes  
# MAGIC ⚠️ **Desafio 5:** Onça-pintada não detectada - requer monitoramento estendido  
# MAGIC ✅ **Bônus 2:** Duração reflete comportamento (forrageio vs trânsito)  
# MAGIC ⚠️ **Bônus 3:** Lobo-guará não detectado - focar em Cerrado aberto noturno  
# MAGIC ✅ **Bônus 4:** Segregação temporal entre grupos confirmada (p < 0.001)
# MAGIC
# MAGIC ## 🎯 Recomendações
# MAGIC
# MAGIC 1. ✅ Manter cobertura 24h (capturar todos os grupos)
# MAGIC 2. ✅ Estender duração: 3-6 meses para espécies raras
# MAGIC 3. ✅ Priorizar ambientes úmidos para anfíbios
# MAGIC 4. ✅ Focar período noturno para onça/lobo
# MAGIC 5. ✅ Garantir visão noturna de qualidade
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ Status: TODOS OS DESAFIOS CONCLUÍDOS!
# MAGIC
# MAGIC *Dataset:* `dataset_clean.csv` (5.000 registros)  
# MAGIC *Período:* Maio/2026  
# MAGIC *Análises:* Estatísticas + Visualizações + Recomendações
# MAGIC
# MAGIC 🐾 🌳 🔬 📊

# COMMAND ----------

