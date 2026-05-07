"""
=============================================================================
GERADOR DE DADOS SINTÉTICOS - PREVINE BRASIL / UBS
=============================================================================
Esse script gera uma base de dados falsa para simular o funcionamento
de uma Unidade Básica de Saúde (UBS) e testar os indicadores do programa
Previne Brasil do Ministério da Saúde.

Os dados são 100% fictícios e servem para proteger a privacidade dos
pacientes reais, seguindo as diretrizes da LGPD.


=============================================================================
"""

# --- Bibliotecas que vamos precisar ---
import random
from datetime import date
from faker import Faker
import pandas as pd

# Configuração do gerador de nomes em português do Brasil
fake = Faker('pt_BR')

# Aqui definimos quantos registros queremos gerar
# Quanto maior o número, mais robusto fica o banco para testar queries SQL
NUM_PACIENTES    = 5000
NUM_ATENDIMENTOS = 20000

print("Iniciando a geração de dados... isso pode demorar alguns segundos.")


# =============================================================================
# PARTE 1 - CÓDIGOS OFICIAIS DO MINISTÉRIO DA SAÚDE
# =============================================================================
# Guardei os códigos em variáveis com nomes legíveis para não ter que
# ficar decorando os números na hora de usar lá embaixo.

# CBO = Classificação Brasileira de Ocupações (identifica o tipo de profissional)
cbo_medico     = '225125'
cbo_enfermeiro = '223505'
cbo_dentista   = '223208'
cbo_tecnico    = '322230'   # Técnico em Enfermagem

# CIAP-2 = Motivo do atendimento (Classificação Internacional de Atenção Primária)
ciap_gravidez    = 'W78'
ciap_diabetes    = 'T90'
ciap_hipertensao = 'K86'
ciap_preventivo  = 'X86'
ciap_rotina      = 'A98'
ciap_odontologia = 'D83'
ciap_crianca     = 'A93'   # Consulta de puericultura (acompanhamento de criança)

# SIGTAP = Código do procedimento realizado (tabela do SUS)
sigtap_sifilis    = '0214010874'
sigtap_hiv        = '0214010840'
sigtap_glicada    = '0202010503'
sigtap_pa         = '0301100039'
sigtap_preventivo = '0203010086'
sigtap_odonto     = '0307010015'
sigtap_vacina     = '0301010153'   # Consulta de vacinação


# =============================================================================
# PARTE 2 - TABELAS DE APOIO (Dimensões)
# Essas listas viram tabelas separadas no CSV 
# =============================================================================

# Equipes de Saúde da Família que existem na UBS
# Cada equipe é responsável por uma área da cidade
lista_equipes = [
    [1, 'Equipe A - Centro',          'ESF'],
    [2, 'Equipe B - Vila Verde',       'ESF'],
    [3, 'Equipe C - Jardim das Flores','ESF'],
    [4, 'Equipe D - Santo André',      'ESF'],
    [5, 'Equipe E - Montanha',         'ESF'],
]

# Bairros onde os pacientes moram
lista_bairros = [
    [1,  'Centro',           'ESF', 1],
    [2,  'Vila Verde',       'ESF', 2],
    [3,  'Jardim das Flores','ESF', 3],
    [4,  'Santo André',      'ESF', 4],
    [5,  'Montanha',         'ESF', 5],
    [6,  'Alto da Boa Vista','ESF', 1],
    [7,  'Pinheiros',        'ESF', 2],
    [8,  'Santa Cruz',       'ESF', 3],
    [9,  'Novo Horizonte',   'ESF', 4],
    [10, 'Vila Esperança',   'ESF', 5],
]

# Tabela de profissionais que trabalham na UBS
lista_profissionais = [
    [1, 'Dr. Carlos Mendes',      cbo_medico,     1],
    [2, 'Dra. Ana Paula Ramos',   cbo_medico,     2],
    [3, 'Dra. Fernanda Costa',    cbo_medico,     3],
    [4, 'Enf. Ricardo Oliveira',  cbo_enfermeiro, 4],
    [5, 'Enf. Juliana Martins',   cbo_enfermeiro, 5],
    [6, 'Dr. Marcos Alves',       cbo_dentista,   1],
    [7, 'Dra. Patrícia Lima',     cbo_dentista,   2],
    [8, 'Téc. Sandra Souza',      cbo_tecnico,    3],
    [9, 'Téc. Paulo Henrique',    cbo_tecnico,    4],
]


# =============================================================================
# PARTE 3 - GERAÇÃO DOS PACIENTES
# =============================================================================
# Criamos listas vazias que vão receber os dados um por um dentro do loop
pacientes = []

for id_paciente in range(1, NUM_PACIENTES + 1):

    # CNS começa com 7 (padrão do cartão emitido em UBS)
    cns = "7" + str(random.randint(10000000000000, 99999999999999))

    # 65% de chance de ser mulher (os indicadores do Previne têm muito foco feminino)
    if random.randint(1, 100) <= 65:
        sexo = 'F'
        nome = fake.name_female()
    else:
        sexo = 'M'
        nome = fake.name_male()

    # Data de nascimento entre 0 e 85 anos
    data_nascimento = fake.date_of_birth(minimum_age=0, maximum_age=85)
    idade = 2023 - data_nascimento.year

    # Cada paciente mora em um bairro da lista
    id_bairro = random.randint(1, len(lista_bairros))

    # Campo de DUM começa vazio. Só vai ter valor se for gestante.
    dum = ""

    # Regra de negócio: mulheres entre 15 e 45 anos têm 25% de chance de estar grávidas
    if sexo == 'F' and 15 <= idade <= 45:
        if random.randint(1, 100) <= 25:
            dum = fake.date_between(start_date=date(2022, 8, 1), end_date=date(2023, 3, 31))

    pacientes.append([id_paciente, cns, nome, data_nascimento, sexo, idade, id_bairro, dum])


# =============================================================================
# PARTE 4 - GERAÇÃO DOS ATENDIMENTOS E PROCEDIMENTOS
# Um atendimento pode ter mais de um procedimento (relação 1:N)
# =============================================================================
atendimentos  = []
procedimentos = []

id_procedimento_atual = 1

for id_atendimento in range(1, NUM_ATENDIMENTOS + 1):

    # Sorteia um paciente e uma data dentro do 1º semestre de 2023
    id_paciente       = random.randint(1, NUM_PACIENTES)
    data_atendimento  = fake.date_between(start_date=date(2023, 1, 1), end_date=date(2023, 6, 30))

    # Sorteia qual profissional fez o atendimento
    # Médicos e enfermeiros têm mais peso porque são maioria na UBS
    id_profissional = random.choice([1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9])
    cbo_do_profissional = lista_profissionais[id_profissional - 1][2]

    cbo_escolhido   = cbo_do_profissional
    ciap_escolhido  = ""
    sigtap_escolhido = ""

    # --- Lógica por tipo de profissional ---

    if cbo_do_profissional == cbo_dentista:
        # Dentista sempre faz atendimento odontológico
        ciap_escolhido   = ciap_odontologia
        sigtap_escolhido = sigtap_odonto

    elif cbo_do_profissional == cbo_tecnico:
        # Técnico em enfermagem costuma fazer vacinas e aferição de PA
        ciap_escolhido   = ciap_rotina
        sigtap_escolhido = random.choice([sigtap_pa, sigtap_vacina])

    else:
        # Médico ou Enfermeiro: sorteia o motivo da consulta
        # Deixei rotina com peso maior porque é o mais comum no dia a dia
        motivos = [
            ciap_rotina, ciap_rotina, ciap_rotina,
            ciap_hipertensao, ciap_hipertensao,
            ciap_diabetes,
            ciap_gravidez,
            ciap_preventivo,
            ciap_crianca,
        ]
        ciap_escolhido = random.choice(motivos)

        # Define o procedimento conforme o motivo da consulta
        if ciap_escolhido == ciap_gravidez:
            sigtap_escolhido = random.choice([sigtap_sifilis, sigtap_hiv])
        elif ciap_escolhido == ciap_diabetes:
            sigtap_escolhido = sigtap_glicada
        elif ciap_escolhido == ciap_hipertensao:
            sigtap_escolhido = sigtap_pa
        elif ciap_escolhido == ciap_preventivo:
            sigtap_escolhido = sigtap_preventivo
        elif ciap_escolhido == ciap_crianca:
            sigtap_escolhido = sigtap_vacina
        else:
            sigtap_escolhido = sigtap_pa  # Consulta de rotina geralmente afere a PA

    # Salva o atendimento
    atendimentos.append([
        id_atendimento,
        id_paciente,
        id_profissional,
        cbo_escolhido,
        ciap_escolhido,
        data_atendimento
    ])

    # Salva o procedimento principal
    procedimentos.append([id_procedimento_atual, id_atendimento, sigtap_escolhido])
    id_procedimento_atual += 1

    # Regra especial: gestantes quase sempre fazem sífilis E HIV na mesma consulta
    if ciap_escolhido == ciap_gravidez:
        if random.randint(1, 100) <= 75:  # 75% de chance de ter o segundo exame
            outro_exame = sigtap_hiv if sigtap_escolhido == sigtap_sifilis else sigtap_sifilis
            procedimentos.append([id_procedimento_atual, id_atendimento, outro_exame])
            id_procedimento_atual += 1

    # Pacientes hipertensos às vezes fazem glicemia junto com a PA (rastreio de diabetes)
    if ciap_escolhido == ciap_hipertensao:
        if random.randint(1, 100) <= 30:
            procedimentos.append([id_procedimento_atual, id_atendimento, sigtap_glicada])
            id_procedimento_atual += 1


# =============================================================================
# PARTE 5 - TABELAS DIMENSÃO
# =============================================================================

dim_cbo = [
    [cbo_medico,     'Medico Clinico Geral'],
    [cbo_enfermeiro, 'Enfermeiro'],
    [cbo_dentista,   'Cirurgiao Dentista'],
    [cbo_tecnico,    'Tecnico em Enfermagem'],
]

dim_ciap = [
    [ciap_gravidez,    'Gravidez / Pre-Natal'],
    [ciap_diabetes,    'Diabetes'],
    [ciap_hipertensao, 'Hipertensao'],
    [ciap_preventivo,  'Exame Preventivo (Papanicolau)'],
    [ciap_rotina,      'Consulta de Rotina'],
    [ciap_odontologia, 'Consulta Odontologica'],
    [ciap_crianca,     'Puericultura (Consulta Infantil)'],
]

dim_sigtap = [
    [sigtap_sifilis,    'Teste Rapido para Sifilis'],
    [sigtap_hiv,        'Teste Rapido para HIV'],
    [sigtap_glicada,    'Hemoglobina Glicada'],
    [sigtap_pa,         'Afericao de Pressao Arterial'],
    [sigtap_preventivo, 'Exame Citopatologico Cervico-Vaginal'],
    [sigtap_odonto,     'Atendimento Odontologico Basico'],
    [sigtap_vacina,     'Aplicacao de Vacina'],
]


# =============================================================================
# PARTE 6 - EXPORTAÇÃO - transformamos tudo em tabelas e salvamos como CSV
# =============================================================================

# --- Tabelas de Fatos ---
df_pacientes = pd.DataFrame(pacientes, columns=[
    'id_paciente', 'cns', 'nome', 'data_nascimento', 'sexo', 'idade', 'id_bairro', 'dum'
])
df_atendimentos = pd.DataFrame(atendimentos, columns=[
    'id_atendimento', 'id_paciente', 'id_profissional', 'codigo_cbo', 'codigo_ciap', 'data_atendimento'
])
df_procedimentos = pd.DataFrame(procedimentos, columns=[
    'id_procedimento', 'id_atendimento', 'codigo_sigtap'
])

# --- Tabelas Dimensão ---
df_dim_cbo          = pd.DataFrame(dim_cbo,          columns=['codigo_cbo',    'nome_profissao'])
df_dim_ciap         = pd.DataFrame(dim_ciap,         columns=['codigo_ciap',   'motivo_atendimento'])
df_dim_sigtap       = pd.DataFrame(dim_sigtap,       columns=['codigo_sigtap', 'nome_procedimento'])
df_dim_bairros      = pd.DataFrame(lista_bairros,    columns=['id_bairro',     'nome_bairro', 'tipo_equipe', 'id_equipe'])
df_dim_equipes      = pd.DataFrame(lista_equipes,    columns=['id_equipe',     'nome_equipe', 'tipo'])
df_dim_profissionais = pd.DataFrame(lista_profissionais, columns=['id_profissional', 'nome_profissional', 'codigo_cbo', 'id_equipe'])

# --- Salvando os arquivos ---
df_pacientes.to_csv('pacientes.csv',               index=False, encoding='utf-8')
df_atendimentos.to_csv('atendimentos.csv',         index=False, encoding='utf-8')
df_procedimentos.to_csv('procedimentos.csv',       index=False, encoding='utf-8')
df_dim_cbo.to_csv('dim_cbo.csv',                   index=False, encoding='utf-8')
df_dim_ciap.to_csv('dim_ciap.csv',                 index=False, encoding='utf-8')
df_dim_sigtap.to_csv('dim_sigtap.csv',             index=False, encoding='utf-8')
df_dim_bairros.to_csv('dim_bairros.csv',           index=False, encoding='utf-8')
df_dim_equipes.to_csv('dim_equipes.csv',           index=False, encoding='utf-8')
df_dim_profissionais.to_csv('dim_profissionais.csv', index=False, encoding='utf-8')

print(f"Concluído! 9 arquivos CSV gerados.")
print(f"  - {len(df_pacientes)} pacientes")
print(f"  - {len(df_atendimentos)} atendimentos")
print(f"  - {len(df_procedimentos)} procedimentos")