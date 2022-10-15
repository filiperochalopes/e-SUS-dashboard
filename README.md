# eSUS Dashboard

O Sistema [e-SUS APS PEC](https://sisaps.saude.gov.br/esus/) é composto de uma estrutura complexa de banco de dados contendo colunas defasadas e atuais para retrocompatibilidade, é um probgrama amplamente utilizado na atenção básica ao redor do Brasil, porém pobre em exibição de métricas e análise inteligente dos dados, por isso o desenvolvimento dessa camada dem anipulação de dados para exposição dos mesmos em API com autenticação a fim de cálculo de métricas de desempenho dentre outras utilidades.

## COnfigurando variáveis de ambiente

```bash
DATABASE_URL='postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@psql:5432/${POSTGRES_DB}?sslmode=disable'
```

## Gerando secret key

```sh
python -c 'import secrets; print(secrets.token_hex())'
```

## Reset app

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
flask db init --multidb
flask db migrate -m "Initial migration"
flask db upgrade
```

## Dicas de navegação no banco de dados do PEC

O banco de dados, na versão `4.2.8` em que essa documentação foi escrita continha 919 tabelas com relacionamentos abundantes e aparente repetição de dados. Não existe uma documentação do banco, porém segue algumas dicas que uso para poder navegar.

### [ Recomendável ] Criando usuário read-only 

Para que seja impossível por meio dessa API editar os dados por acidente, permitindo apenas a leitura por parte da API.

```sql
-- Criando Role (Função)
CREATE ROLE readaccess;
-- Criando grupo de permissões para a Função
GRANT CONNECT ON DATABASE esus TO readaccess;
GRANT USAGE ON SCHEMA public TO readaccess;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readaccess;
-- Criando o usuário com a Função
CREATE USER esus_reader WITH PASSWORD 'esus';
GRANT readaccess TO esus_reader;
```

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
