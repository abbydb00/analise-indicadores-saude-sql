-- Criando a estrutura do banco de dados UBS / Previne Brasil

-- 1. Tabelas de Apoio (Dimensões)

CREATE TABLE dim_equipes (
    id_equipe INT PRIMARY KEY,
    nome_equipe VARCHAR(100),
    tipo VARCHAR(50)
);

CREATE TABLE dim_bairros (
    id_bairro INT PRIMARY KEY,
    nome_bairro VARCHAR(100),
    tipo_equipe VARCHAR(50),
    id_equipe INT REFERENCES dim_equipes(id_equipe)
);

CREATE TABLE dim_cbo (
    codigo_cbo VARCHAR(10)  PRIMARY KEY,
    nome_profissao VARCHAR(100)
);

CREATE TABLE dim_profissionais (
    id_profissional INT PRIMARY KEY,
    nome_profissional VARCHAR(100),
    codigo_cbo VARCHAR(10) REFERENCES dim_cbo(codigo_cbo),
    id_equipe INT REFERENCES dim_equipes(id_equipe)
);

CREATE TABLE dim_ciap (
    codigo_ciap VARCHAR(10) PRIMARY KEY,
    motivo_atendimento VARCHAR(100)
);

CREATE TABLE dim_sigtap (
    codigo_sigtap VARCHAR(15) PRIMARY KEY,
    nome_procedimento VARCHAR(200)
);

-- 2. Tabelas Principais (Fatos)

CREATE TABLE pacientes (
    id_paciente INT PRIMARY KEY,
    cns VARCHAR(15),
    nome VARCHAR(100),
    data_nascimento DATE,
    sexo CHAR(1),
    idade INT,
    id_bairro INT REFERENCES dim_bairros(id_bairro),
    dum DATE
);

CREATE TABLE atendimentos (
    id_atendimento INT PRIMARY KEY,
    id_paciente INT REFERENCES pacientes(id_paciente),
    id_profissional INT REFERENCES dim_profissionais(id_profissional),
    codigo_cbo VARCHAR(10) REFERENCES dim_cbo(codigo_cbo),
    codigo_ciap VARCHAR(10) REFERENCES dim_ciap(codigo_ciap),
    data_atendimento DATE
);

CREATE TABLE procedimentos (
    id_procedimento INT PRIMARY KEY,
    id_atendimento INT REFERENCES atendimentos(id_atendimento),
    codigo_sigtap VARCHAR(15) REFERENCES dim_sigtap(codigo_sigtap)
);