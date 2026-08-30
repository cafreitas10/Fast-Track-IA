# 🧹 Limpeza e Preparação dos Dados - Monitoramento da Fauna

**Checkpoint: Preparando os Dados**  
**Analista:** Assistente IA  
**Data:** Maio/2026  
**Dataset:** 5.000 registros de monitoramento de fauna (01-30/maio/2026)

---

## 📋 Sumário Executivo

Este documento detalha o processo de análise exploratória, identificação de problemas e decisões de tratamento aplicadas ao dataset de monitoramento da fauna do parque nacional.

**Principais achados:**
- ✅ Dataset estruturado com 5.000 registros e 9 colunas
- ⚠️ 78,86% de valores ausentes na coluna `grupo`
- ⚠️ 23,26% de valores ausentes na coluna `especie`
- ⚠️ 4 espécies esperadas não encontradas no período
- ✅ Sem duplicados ou valores anômalos nas variáveis numéricas

---

## 1️⃣ Análise Exploratória Inicial

### 1.1 Estrutura do Dataset

**Dimensões originais:** 5.000 registros × 9 colunas

**Colunas disponíveis:**

| Coluna | Tipo | Descrição |
|--------|------|----------|
| `id_registro` | int64 | Identificação única do registro |
| `id_camera` | object | ID da câmera (CAM01 a CAM12) |
| `data_hora_inicio` | object | Data e hora do registro |
| `duracao_segundos` | int64 | Duração do registro em segundos |
| `especie` | object | Nome da espécie registrada |
| `grupo` | object | Grupo faunístico (Mamífero, Ave, Anfíbio) |
| `individuos` | int64 | Quantidade de indivíduos |
| `temperatura_c` | float64 | Temperatura em °C |
| `umidade_pct` | float64 | Umidade relativa em % |

### 1.2 Período de Monitoramento

- **Início:** 01/05/2026 00:04:00
- **Fim:** 30/05/2026 23:58:00
- **Duração:** 30 dias completos ✅
- **Conformidade:** 100% dos registros dentro do período esperado

---

## 2️⃣ Problemas Identificados

### 🚨 Problema 1: Coluna `grupo` Incompleta (CRÍTICO)

**Descrição:**  
Apenas 1.057 registros (21,14%) possuem o grupo faunístico preenchido. Os demais 3.943 registros (78,86%) estão com valores ausentes.

**Investigação:**
- Apenas registros de **Ema** e **Seriema** (aves) possuem grupo preenchido
- Todas as outras 7 espécies (mamíferos e anfíbios) estão sem classificação
- Isso indica falha no processo de registro ou exportação dos dados

**Impacto:**
- Impossibilita análises por grupo faunístico sem tratamento
- Análises de diversidade ficam comprometidas

**Espécies afetadas:**

| Espécie | Grupo Esperado | Registros sem Grupo |
|---------|----------------|---------------------|
| Capivara | Mamífero | 731 |
| Sapo-cururu | Anfíbio | 564 |
| Perereca-verde | Anfíbio | 389 |
| Quati | Mamífero | 378 |
| Veado-campeiro | Mamífero | 292 |
| Tatu-canastra | Mamífero | 273 |
| Cervo-do-pantanal | Mamífero | 153 |
| **Total** | - | **2.780** |

---

### ⚠️ Problema 2: Valores Ausentes na Coluna `especie`

**Descrição:**  
1.163 registros (23,26%) não possuem identificação de espécie.

**Interpretação:**
- Câmeras detectaram movimento mas não conseguiram identificar a espécie
- Pode indicar:
  - Registros de animais muito rápidos
  - Má qualidade da imagem
  - Falso positivo (vento, vegetação)
  - Espécies não catalogadas no sistema

**Decisão de Tratamento:**  
✅ **MANTER** esses registros no dataset

**Justificativa:**
- São úteis para análise de taxa de detecção por câmera
- Permitem avaliar eficiência do sistema de identificação
- Úteis para análises temporais e ambientais independentes de espécie

---

### ⚠️ Problema 3: Espécies Esperadas vs Encontradas

**Espécies esperadas no monitoramento:** 13  
**Espécies encontradas no dataset:** 9  
**Espécies ausentes:** 4

#### Espécies Encontradas (9):
✅ Capivara (Mamífero) - 731 registros  
✅ Cervo-do-pantanal (Mamífero) - 153 registros  
✅ Ema (Ave) - 551 registros  
✅ Perereca-verde (Anfíbio) - 389 registros  
✅ Quati (Mamífero) - 378 registros  
✅ Sapo-cururu (Anfíbio) - 564 registros  
✅ Seriema (Ave) - 506 registros  
✅ Tatu-canastra (Mamífero) - 273 registros  
✅ Veado-campeiro (Mamífero) - 292 registros

#### Espécies Ausentes (4):
❌ **Lobo-guará** (Mamífero)  
❌ **Onça-pintada** (Mamífero)  
❌ **Rã-manteiga** (Anfíbio)  
❌ **Tamanduá-bandeira** (Mamífero)

**Interpretação:**
- Espécies raras ou de difícil detecção
- Possível ausência na área monitorada durante o período
- Lobo-guará e onça-pintada são de hábitos noturnos e território amplo
- Importante documentar para relatórios de biodiversidade

---

### ⚠️ Problema 4: Valores Ausentes em Sensores Ambientais

**Temperatura:**
- 247 registros ausentes (4,94%)
- Possível falha intermitente dos sensores

**Umidade:**
- 175 registros ausentes (3,50%)
- Falhas não coincidem totalmente com as de temperatura

**Análise de Padrão:**
- Valores ausentes distribuídos ao longo do período
- Não concentrados em câmeras específicas
- Indica falhas pontuais, não sistemáticas

---

## 3️⃣ Análise de Qualidade dos Dados

### ✅ Pontos Positivos

1. **Sem duplicados**
   - 0 registros completamente duplicados
   - 0 IDs duplicados
   - Integridade referencial preservada ✓

2. **Variáveis numéricas consistentes**
   - `duracao_segundos`: 3 a 167 segundos (sem valores negativos ou zero)
   - `individuos`: 1 a 14 indivíduos (valores plausíveis)
   - `temperatura_c`: 12,3 a 34,1°C (dentro do esperado para o Cerrado)
   - `umidade_pct`: 44,3 a 99,0% (range válido 0-100%)

3. **IDs de câmeras padronizados**
   - 12 câmeras identificadas: CAM01 a CAM12 ✓
   - Distribuição equilibrada entre ambientes

4. **Datas no formato correto**
   - Formato: `YYYY-MM-DD HH:MM:SS`
   - 100% dos registros em maio/2026
   - Parseamento sem erros

---

## 4️⃣ Decisões de Tratamento

### 🔧 Tratamento 1: Preencher Coluna `grupo`

**Método:** Mapeamento espécie → grupo baseado em taxonomia

**Mapeamento aplicado:**

```python
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
```

**Resultado:**
- ✅ 3.943 → 1.163 valores ausentes (redução de 70%)
- ✅ Apenas registros sem espécie ficam sem grupo (consistência lógica)
- ✅ Distribuição final:
  - Mamífero: 1.827 registros
  - Ave: 1.057 registros
  - Anfíbio: 953 registros

---

### 🔧 Tratamento 2: Criar Coluna `ambiente`

**Justificativa:**  
Facilitar análises por tipo de ambiente sem precisar mapear IDs de câmeras manualmente.

**Mapeamento:**

| Câmeras | Ambiente |
|---------|----------|
| CAM01, CAM02, CAM03, CAM04 | Cerrado aberto |
| CAM05, CAM06, CAM07, CAM08 | Mata de galeria |
| CAM09, CAM10, CAM11, CAM12 | Veredas e áreas úmidas |

**Resultado:**
- ✅ Nova coluna criada com 3 categorias
- ✅ Distribuição equilibrada:
  - Veredas e áreas úmidas: 1.817 registros (36,3%)
  - Cerrado aberto: 1.624 registros (32,5%)
  - Mata de galeria: 1.559 registros (31,2%)

---

### 🔧 Tratamento 3: Preencher Valores Ausentes de Sensores

**Método:** Imputação pela **mediana por ambiente**

**Justificativa:**
- Mediana é robusta a outliers
- Cada ambiente tem características climáticas próprias
- Preserva a distribuição natural dos dados

**Medianas calculadas:**

#### Temperatura (°C):
| Ambiente | Mediana |
|----------|--------|
| Cerrado aberto | 25,0°C |
| Mata de galeria | 22,0°C |
| Veredas e áreas úmidas | 22,4°C |

#### Umidade (%):
| Ambiente | Mediana |
|----------|--------|
| Cerrado aberto | 67,9% |
| Mata de galeria | 79,3% |
| Veredas e áreas úmidas | 82,0% |

**Resultado:**
- ✅ Temperatura: 247 → 0 valores ausentes
- ✅ Umidade: 175 → 0 valores ausentes
- ✅ Padrões ambientais preservados (Cerrado mais quente e seco, Veredas mais frias e úmidas)

---

### 🔧 Tratamento 4: Converter `data_hora_inicio` para Datetime

**Justificativa:**
- Facilitar análises temporais
- Permitir extração de componentes (hora, dia, semana)
- Melhorar performance em filtros e ordenações

**Conversão:**
- Formato original: `object` (string)
- Formato final: `datetime64[ns]`
- Parseamento: 100% de sucesso

---

### 🔧 Tratamento 5: Criar Colunas Derivadas

**Novas colunas criadas para facilitar análises:**

1. **`data`**: Data isolada (tipo: date)
2. **`hora`**: Hora do registro (0-23)
3. **`dia_da_semana`**: Nome do dia (Monday, Tuesday, etc.)
4. **`dia_do_mes`**: Dia do mês (1-31)
5. **`periodo_dia`**: Período do dia classificado como:
   - **Madrugada** (22h-5h): 1.152 registros (23%)
   - **Manhã** (5h-12h): 1.662 registros (33%)
   - **Tarde** (12h-18h): 1.317 registros (26%)
   - **Noite** (18h-22h): 869 registros (17%)

**Utilidade:**
- Análise de padrões de atividade por período
- Identificação de espécies diurnas vs noturnas
- Estudos de sazonalidade temporal

---

## 5️⃣ Dataset Final

### Estrutura do Dataset Limpo

**Arquivo gerado:** `dataset_clean.csv`  
**Dimensões:** 5.000 registros × 15 colunas

**Colunas:**
1. `id_registro` - ID único do registro
2. `id_camera` - ID da câmera
3. `data_hora_inicio` - Data/hora (datetime)
4. `duracao_segundos` - Duração do registro
5. `especie` - Nome da espécie
6. `grupo` - Grupo faunístico (preenchido)
7. `individuos` - Quantidade de indivíduos
8. `temperatura_c` - Temperatura (sem ausentes)
9. `umidade_pct` - Umidade (sem ausentes)
10. **`ambiente`** - Tipo de ambiente (nova)
11. **`data`** - Data isolada (nova)
12. **`hora`** - Hora do registro (nova)
13. **`dia_da_semana`** - Nome do dia (nova)
14. **`dia_do_mes`** - Dia do mês (nova)
15. **`periodo_dia`** - Período classificado (nova)

### Resumo de Valores Ausentes

| Coluna | Valores Ausentes | Percentual |
|--------|------------------|------------|
| `especie` | 1.163 | 23,26% |
| `grupo` | 1.163 | 23,26% |
| **Demais colunas** | **0** | **0,00%** |

**Nota:** Os 1.163 registros sem espécie foram mantidos intencionalmente para análises de detecção.

---

## 6️⃣ Recomendações para Análises Futuras

### ✅ Dataset Pronto Para:

1. **Análises por ambiente**
   - Diversidade de espécies por tipo de habitat
   - Condições climáticas por ambiente
   - Eficiência de detecção por local

2. **Análises temporais**
   - Padrões de atividade por período do dia
   - Tendências ao longo do mês
   - Comportamento diurno vs noturno

3. **Análises por espécie**
   - Distribuição espacial
   - Tamanho de grupos
   - Preferências de habitat

4. **Análises ambientais**
   - Relação temperatura/umidade com presença de fauna
   - Condições ideais por espécie

### ⚠️ Limitações a Considerar:

1. **Espécies ausentes**: 4 espécies esperadas não foram registradas no período
2. **Registros não identificados**: 23% dos registros sem espécie
3. **Período único**: Apenas maio/2026 (1 mês) - sazonalidade limitada
4. **Dados de sensores imputados**: ~5% de valores preenchidos por mediana

---

## 7️⃣ Metadados do Processo

**Ferramenta:** Python 3.x + Pandas  
**Data de processamento:** Maio/2026  
**Arquivo de entrada:** `dataset.csv`  
**Arquivo de saída:** `dataset_clean.csv`  
**Registros processados:** 5.000  
**Taxa de sucesso:** 100%  
**Tempo de processamento:** < 1 segundo

---

## 📚 Referências

### Classificação Taxonômica
- **Mamíferos**: Capivara, Cervo-do-pantanal, Lobo-guará, Onça-pintada, Quati, Tamanduá-bandeira, Tatu-canastra, Veado-campeiro
- **Aves**: Ema, Seriema
- **Anfíbios**: Perereca-verde, Rã-manteiga, Sapo-cururu

### Ambientes
- **Cerrado aberto**: Vegetação rasteira, áreas de passagem
- **Mata de galeria**: Vegetação densa, cursos d'água
- **Veredas e áreas úmidas**: Nascentes, lagoas, regiões alagáveis

---

## 🎯 Conclusão

O dataset passou por um processo rigoroso de limpeza e enriquecimento, resultando em um conjunto de dados robusto e pronto para análises ecológicas. Os principais problemas (valores ausentes em `grupo` e sensores ambientais) foram tratados de forma conservadora, preservando a integridade dos dados originais sempre que possível.

**Status:** ✅ **DATASET LIMPO E VALIDADO**

---

*Documento gerado automaticamente como parte do Checkpoint: Preparando os Dados*  
*Para dúvidas sobre as decisões de tratamento, consulte o código em `cleaning_fauna.ipynb`*