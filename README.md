# e-SUS PEC API

O Sistema [e-SUS APS PEC](https://sisaps.saude.gov.br/esus/) é composto de uma estrutura complexa de banco de dados contendo colunas defasadas e atuais para retrocompatibilidade, é um probgrama amplamente utilizado na atenção básica ao redor do Brasil, porém pobre em exibição de métricas e análise inteligente dos dados, por isso o desenvolvimento dessa camada dem anipulação de dados para exposição dos mesmos em API com autenticação a fim de cálculo de métricas de desempenho dentre outras utilidades.

## COnfigurando variáveis de ambiente

Criar arquivo .env com base na estrutura de variáveis exposto em .env.example 

```bash
# Porta onde será exposta aplicação web que expõe a estrutura de tabelas, somente leitura
PGWEB_PORT=8098
# Porta que expõe a aplicação principal, é possível acessar a área de testes (playground) com http://localhost:8072/api/v1/graphql
API_PORT=8072
# É a senha mestra usado quando da criação de usuários pelo playground
MASTER_KEY='passw@rd'
# Chave de criptografia
SECRET=
# URL tcp do banco de dados que teremos acesso
DATABASE_URL='postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@psql:5432/${POSTGRES_DB}?sslmode=disable'
```

## Gerando secret key

Para preencher a variável `SECRET`, que identificada como chave de criptografia, tenha instalado o Python em sua máquina e rode em terminal o seguinte comando

```sh
python -c 'import secrets; print(secrets.token_hex())'
```

## Reset app

As seguintes linhas de código executam os comandos expressos nos respectivos blocos identificados em `Makefile`

```sh
make run
make migrate
```

## Comandos de migrations

```sh
make migrate
make m="update some table" makemigrations
```

## Utilizando o alembic no ambiente de desenvolvimento

```sh
docker exec -it esus_dashboard_api bash
flask db init --multidb
flask db migrate -m "Initial migration"
flask db upgrade
```

## Dicas de navegação no banco de dados do PEC

O banco de dados, na versão `4.2.8` em que essa documentação foi escrita continha 919 tabelas com relacionamentos abundantes e aparente repetição de dados. Não existe uma documentação do banco, porém segue algumas dicas que uso para poder navegar.

### Reiniciando nginx após alterar arquivo de conf

```sh
docker exec esus_dashboard_api nginx -s reload
```

### [ Recomendável ] Criando usuário read-only 

Para que seja impossível por meio dessa API editar os dados por acidente, permitindo apenas a leitura por parte da API.

**Atualização** Após entrar em contato com a equipe de suporte do Laboratório Bridge /CTC / UFSC, recebi a seguinte informação de Wagner J. Nascimento:

> Na criação do banco de dados é criado um usuário para leitura sim, mas só é possível ter acesso a essa informação na máquina onde o servidor do PEC está instalado. 
Acessando a pasta webserver > config do PEC há um arquivo com o nome "credenciais" onde são exibidas as informações (usuário e senha) do usuário com acesso completo ao banco e do usuário com acesso de leitura.  


```sql
-- Criando Role (Função)
CREATE ROLE readaccess;
ALTER ROLE readaccess LOGIN;
-- Criando grupo de permissões para a Função
GRANT CONNECT ON DATABASE esus TO readaccess;
GRANT USAGE ON SCHEMA public TO readaccess;
GRANT SELECT ON ALL TABLES IN SCHEMA "public" TO readaccess;
-- Criando o usuário com a Função
CREATE USER esus_reader WITH PASSWORD 'esus';
-- Dando a possibilidade de realizar login para visualizar tabelas
GRANT readaccess TO esus_reader;
```

Aparentemente alguns comando não funcionam diretamente na linha de comando `psql`, mas funcionaram com o `dbeaver` para parte de rodar comando sql. That's odd! 😖

### Verificando mais sobre uma tabela para apromorar API

```sh
docker exec -it esus_psql bash
psql -U postgres
\c esus
\dt
\d+ tb_proced
```

### Encontrando nome da tabela

```sql
select t.table_schema,
       t.table_name
from information_schema.tables t
inner join information_schema.columns c on c.table_name = t.table_name
                                and c.table_schema = t.table_schema
where c.column_name = 'co_principio_ativo'
      and t.table_schema not in ('information_schema', 'pg_catalog')
      and t.table_type = 'BASE TABLE'
order by t.table_schema;
```
