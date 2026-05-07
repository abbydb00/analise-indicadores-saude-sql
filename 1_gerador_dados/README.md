# 1 — Gerador de Dados Sintéticos

Script Python que gera uma base de dados falsa simulando o funcionamento de uma Unidade Básica de Saúde (UBS), criado para substituir os dados reais protegidos pela **LGPD**.

---

## Por que dados sintéticos?

Os dados reais de saúde utilizados na Prefeitura são sigilosos e protegidos por lei. Este script recria um ambiente simulado e com algumas semelhanças apenas — mesmos códigos oficiais do Ministério da Saúde, mesmas regras de negócio — com nomes, datas e registros 100% fictícios.

---

## O que o script gera

| Arquivo | Registros | Descrição |
|---|---|---|
| `pacientes.csv` | 5.000 | Cadastro com CNS, nome, sexo, idade, bairro e DUM |
| `atendimentos.csv` | 20.000 | Consultas com data, profissional e motivo (CIAP) |
| `procedimentos.csv` | ~25.000 | Exames e procedimentos por consulta |
| `dim_equipes.csv` | 5 | Equipes de Saúde da Família |
| `dim_bairros.csv` | 10 | Bairros de abrangência da UBS |
| `dim_profissionais.csv` | 9 | Profissionais com nome e CBO |
| `dim_cbo.csv` | 4 | Tipos de profissional |
| `dim_ciap.csv` | 7 | Motivos de atendimento |
| `dim_sigtap.csv` | 7 | Procedimentos do SUS |

---

## Regras de negócio aplicadas

As regras abaixo foram baseadas no funcionamento real de uma UBS e nos indicadores do Previne Brasil:

- **65%** dos pacientes são do sexo feminino (foco nos indicadores femininos do programa)
- Mulheres entre 15 e 45 anos têm **25% de chance** de ter DUM registrada (gestantes)
- Médicos e enfermeiros têm **maior peso** no sorteio de atendimentos (maioria na UBS)
- Consultas de pré-natal geram **dois procedimentos** na maioria dos casos: teste rápido de sífilis + HIV
- Consultas de hipertensão têm **30% de chance** de incluir hemoglobina glicada (rastreio de diabetes)
- Técnicos em enfermagem realizam aferição de PA e aplicação de vacinas

---

## Como executar

**Instalar dependências:**

```bash
pip install faker pandas
```

**Rodar o script:**

```bash
python gerar_dados.py
```

Os 9 arquivos CSV serão gerados na mesma pasta.

---

## Dependências

| Biblioteca | Uso |
|---|---|
| `faker` | Geração de nomes brasileiros realistas |
| `pandas` | Organização e exportação dos dados em CSV |
| `random` | Sorteios e probabilidades |
| `datetime` | Geração de datas dentro dos intervalos corretos |
