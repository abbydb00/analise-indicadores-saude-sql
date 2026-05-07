# Análise de Indicadores de Saúde — Previne Brasil

Projeto desenvolvido como parte das atividades de uma **Prefeitura**, onde trabalhei com extração e análise de dados de saúde para monitoramento e manutenção de indicadores federais do programa **Previne Brasil** do Ministério da Saúde.

---

## Contexto

O Previne Brasil é o modelo de financiamento da Atenção Primária à Saúde no Brasil. Parte dos repasses federais aos municípios depende do desempenho em indicadores como cobertura de pré-natal, exames preventivos e acompanhamento de pacientes hipertensos e diabéticos. O monitoramento correto desses indicadores impacta diretamente as verbas que o município recebe.

Na Prefeitura, atuei na extração e análise desses dados utilizando o sistema da empresa **MV (prontuário eletrônico)** e o **DBeaver** para elaboração de consultas SQL, além da criação de painéis de Business Intelligence e relatórios de produtividade com sistema da própria empresa, cabe destacar que o banco de dados e os indicadores já existiam, fiz um serviço de extração manutenção de querys.

---

## Sobre este repositório

Como os dados reais de saúde são protegidos pela **LGPD**, este projeto recria o ambiente de trabalho com uma base de dados **100% sintética**, gerada via Python com a biblioteca Faker.

O objetivo é demonstrar as mesmas habilidades técnicas utilizadas no trabalho real — modelagem de dados, SQL, BI — sem expor nenhuma informação de pacientes.

---

## Estrutura do projeto

```
analise-indicadores-saude-sql/
│
├── dados/
│   ├── gerador_fake_data_sus.py          # Script Python que gera os CSVs sintéticos
│   ├── pacientes.csv
│   ├── atendimentos.csv
│   ├── procedimentos.csv
│   ├── dim_equipes.csv
│   ├── dim_bairros.csv
│   ├── dim_cbo.csv
│   ├── dim_ciap.csv
│   ├── dim_sigtap.csv
│   ├── dim_profissionais.csv
│   └── README.md
│
├── sql/
│   ├── criacaobanco.sql              # Script de criação das tabelas no DBeaver
│   ├── diagrama_er.png
│   └── README.md
│
└── README.md
```

---

## Modelo de dados

O banco segue uma estrutura **Fato + Dimensão** (esquema estrela), comum em projetos de BI:

| Tabela | Tipo | Descrição |
|---|---|---|
| `pacientes` | Fato | Cadastro dos pacientes da UBS |
| `atendimentos` | Fato | Registro de cada consulta realizada |
| `procedimentos` | Fato | Exames e procedimentos por consulta |
| `dim_equipes` | Dimensão | Equipes de Saúde da Família |
| `dim_bairros` | Dimensão | Bairros de abrangência da UBS |
| `dim_profissionais` | Dimensão | Profissionais de saúde |
| `dim_cbo` | Dimensão | Classificação Brasileira de Ocupações |
| `dim_ciap` | Dimensão | Motivos de atendimento (CIAP-2) |
| `dim_sigtap` | Dimensão | Procedimentos do SUS (SIGTAP) |

---

## Como reproduzir

**1. Gerar os dados sintéticos**

```bash
pip install faker pandas
python dados/gerar_dados.py
```

**2. Criar as tabelas no DBeaver**

- Abra o DBeaver e conecte em um banco PostgreSQL
- Execute o script `sql/schema.sql`

**3. Importar os CSVs**

Importe os arquivos na seguinte ordem (por causa das chaves estrangeiras):

```
dim_equipes → dim_bairros → dim_cbo → dim_profissionais
→ dim_ciap → dim_sigtap → pacientes → atendimentos → procedimentos
```

No DBeaver: clique com botão direito na tabela → *Importar Dados* → CSV → UTF-8.

---

## Tecnologias

- Python (Faker, Pandas)
- SQL (PostgreSQL)
- DBeaver

---

## Autor

Desenvolvido por Abrão.
[LinkedIn](https://www.linkedin.com/in/abra%C3%A3o-braga-416a23403/) · [GitHub](https://github.com/abbydb00)
