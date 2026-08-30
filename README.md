Checkpoint - Monitoramento da Fauna
🐾 Contexto

Você faz parte de uma equipe responsável pela análise de dados de um programa de monitoramento da fauna de um parque nacional brasileiro.

O parque utiliza câmeras automáticas distribuídas em diferentes ambientes para registrar a presença de animais. As câmeras funcionam de forma contínua e geram registros quando detectam movimentação.

A equipe responsável pelo programa recebeu os registros de 30 dias de monitoramento e precisa transformá-los em informações que possam apoiar decisões relacionadas ao acompanhamento da fauna.

Seu papel neste checkpoint é atuar como analista de dados. A partir dos registros fornecidos, você deverá preparar os dados, investigar padrões e apresentar evidências que possam ajudar a equipe a responder às perguntas propostas.

    Importante: os dados utilizados neste exercício são sintéticos e foram criados exclusivamente para fins educacionais. O cenário é fictício e inspirado em características de monitoramento de fauna em unidades de conservação brasileiras.

🗺️ O parque e o monitoramento

Para este exercício, considere um parque nacional localizado em uma região de Cerrado.

O programa de monitoramento possui 12 câmeras automáticas, distribuídas em três ambientes diferentes, com quatro câmeras em cada ambiente.

As câmeras registram automaticamente os animais detectados, juntamente com informações sobre o momento do evento, duração do registro, espécie identificada, quantidade de indivíduos e condições ambientais medidas pelos sensores associados aos equipamentos.

O período analisado compreende: 01/05/2026 a 30/05/2026
📍 Áreas de monitoramento
Cerrado aberto

Ambiente caracterizado por áreas predominantemente abertas, com vegetação rasteira e regiões de passagem de animais.

Câmeras:

    CAM01
    CAM02
    CAM03
    CAM04

Mata de galeria

Área com vegetação mais densa, associada a cursos d'água e regiões de maior cobertura vegetal.

Câmeras:

    CAM05
    CAM06
    CAM07
    CAM08

Veredas e áreas úmidas

Ambientes associados a áreas úmidas, nascentes, pequenas lagoas e regiões alagáveis.

Câmeras:

    CAM09
    CAM10
    CAM11
    CAM12

🦌 Espécies monitoradas

O conjunto de dados contém registros de diferentes grupos da fauna, incluindo mamíferos, aves e anfíbios.

Entre as espécies presentes no monitoramento estão:
Espécie 	Grupo
Capivara 	Mamífero
Cervo-do-pantanal 	Mamífero
Ema 	Ave
Lobo-guará 	Mamífero
Onça-pintada 	Mamífero
Perereca-verde 	Anfíbio
Quati 	Mamífero
Rã-manteiga 	Anfíbio
Sapo-cururu 	Anfíbio
Seriema 	Ave
Tamanduá-bandeira 	Mamífero
Tatu-canastra 	Mamífero
Veado-campeiro 	Mamífero

A frequência de registros varia entre as espécies ao longo do período monitorado.
📊 Dados disponíveis

O arquivo dataset.json contém 5.000 registros.

Cada registro possui as seguintes informações:
Coluna 	Descrição
id_registro 	Identificação do registro
id_camera 	Identificação da câmera que realizou o registro
data_hora_inicio 	Data e hora em que o registro ocorreu
duracao_segundos 	Duração do registro
especie 	Espécie registrada
grupo 	Grupo faunístico ao qual a espécie pertence
individuos 	Quantidade de indivíduos registrados
temperatura_c 	Temperatura registrada pelo sensor, em °C
umidade_pct 	Umidade relativa do ar registrada pelo sensor, em %

Os dados representam os registros brutos recebidos pela equipe. Portanto, algumas variáveis podem precisar de tratamento antes de serem utilizadas nas análises.
🎯 Desafios

A equipe de pesquisadores precisa responder a diferentes questões a partir dos registros coletados.

Para cada desafio, utilize os dados para construir uma análise que responda à pergunta e apresente evidências que sustentem sua conclusão.

Não existe uma única forma correta de realizar as análises. Suas escolhas devem ser justificadas conforme o problema.
Desafio 1 - Animais solitários ou em grupo?

Durante o monitoramento, os pesquisadores querem entender como a capivara costuma ser registrada pelas câmeras.

Pergunta:

    Qual é o número médio de indivíduos por registro de capivara? A maioria dos registros envolve indivíduos isolados ou grupos?

Desafio 2 - Quando a fauna está mais ativa?

A equipe quer entender como os horários dos registros variam ao longo do dia.

Pergunta:

    Em quais períodos do dia há mais registros de animais? Escolha três espécies e compare seus horários de maior ocorrência.

Desafio 3 - Vale a pena procurar anfíbios em períodos mais úmidos?

A equipe de campo está planejando uma rotina de monitoramento de anfíbios e quer saber se a umidade pode ajudar a definir os melhores momentos para realizar esse trabalho.

Pergunta:

    Os anfíbios são registrados com maior frequência quando a umidade é mais alta? Compare a quantidade de registros em diferentes níveis de umidade e apresente sua conclusão.

Desafio 4 - Onde concentrar o monitoramento?

A equipe precisa decidir onde concentrar seus esforços no próximo período de monitoramento. Para isso, quer identificar quais câmeras apresentam maior atividade e variedade de espécies.

Pergunta:

    Quais câmeras apresentam maior quantidade de registros e maior variedade de espécies? Essas câmeras estão concentradas em alguma das três áreas do parque?

Desafio 5 - Onde procurar a onça-pintada?

Um grupo de biólogos pretende aumentar as chances de registrar uma onça-pintada no próximo período de monitoramento.

Pergunta:

    Com base nos registros deste mês, em quais câmeras, áreas e períodos do dia você recomendaria concentrar o próximo monitoramento?

⭐ Desafios bônus

Os desafios abaixo são opcionais e podem ser utilizados para aprofundar a investigação.
Bônus 1 - Preparando os dados

Antes de iniciar as análises, a equipe precisa garantir que os dados estejam adequados para serem utilizados.

Pergunta:

    Faça uma análise inicial do dataset, identifique problemas ou inconsistências que possam afetar suas análises e trate os dados da forma que considerar mais adequada. Explique brevemente as decisões tomadas.

Bônus 2 - Quanto tempo duram os registros?

A equipe quer entender se a duração dos eventos registrados varia entre as espécies e se esse comportamento pode ajudar na interpretação dos registros.

Pergunta:

    Quais espécies apresentam os registros mais longos e mais curtos? Como a duração dos registros se distribui entre as espécies e o que essa diferença pode indicar?

Bônus 3 - O comportamento do lobo-guará

A equipe quer conhecer melhor o padrão de ocorrência do lobo-guará durante o período monitorado.

Pergunta:

    Em quais horários e em quais câmeras o lobo-guará foi mais registrado? Existe algum padrão que se destaque nesses registros?

Bônus 4 - Sua própria investigação

Até aqui, você trabalhou com perguntas propostas pela equipe. Agora, pense em algo que você gostaria de investigar usando os dados.

Pergunta:

    Crie uma pergunta que possa ser respondida a partir do dataset e faça uma análise para chegar a uma conclusão.

A ideia é explorar um padrão ou situação diferente dos desafios anteriores.

Por exemplo:

    Aves, mamíferos e anfíbios possuem picos de atividade em horários claramente distintos?

Não precisa ser uma pergunta complexa. O objetivo é pensar em uma situação, formular uma pergunta e usar os dados para tentar respondê-la.
💻 Prática de Git e GitHub

A prática de Git e GitHub faz parte deste checkpoint. A ideia é utilizar o exercício para colocar em prática os conceitos estudados durante a trilha.

Crie um repositório pessoal no GitHub para desenvolver e organizar sua solução.

Sempre que possível, organize o desenvolvimento em commits que representem etapas funcionais da análise. Utilize Conventional Commits para descrever as alterações.

Por exemplo:

feat: analisar atividade da fauna
feat: analisar atividade dos anfibios
feat: analisar distribuicao por camera
feat: investigar registros de onca-pintada

Você também pode criar commits para etapas de preparação dos dados, correções ou outras evoluções relevantes.

A organização do repositório e o histórico de commits fazem parte da prática proposta neste checkpoint.
