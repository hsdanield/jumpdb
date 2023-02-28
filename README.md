# jumpdb

### Objetivo: 
1. Inspeção/investigação de tabelas e automatização para criação de scripts de banco de dados relacionais. OBS: Compativel com oracle e mysql. 
2. Extração, Transformação e Carregamento de dados através de banco de dados relacionais e arquivos.




A seguir temos a descrição dos parâmetros utilizados e alguns exemplos utilizados no console jumpdb

| **columns**                  | Buscar Colunas e inspecionar seus tipos e comentarios no banco de dados                     |
|------------------------------|---------------------------------------------------------------------------------------------|
| database (obrigatorio)       | informar dialect (por exemplo mysql ou oracle)                                              |
| name (obrigatorio)           | informar o nome cadastros em settings.toml                                                  |
| --table-name (obrigatorio)   | nome da tabela para busca filter_columns: caso não informado ira recuperar todas as colunas |
| --filter-columns (opicional) | utilizar para recuperar apenas coluans especificas                                          |

Exemplo utilizando o parâmetro columns:

```
jumpdb columns <database> <name> --table-name <table_name> --filter-columns
```

| **pks**                    | Buscar Primary Keys no banco de dados          |
|----------------------------|------------------------------------------------|
| database (obrigatorio)     | informar dialect (por exemplo mysql ou oracle) |
| name (obrigatorio)         | informar o nome cadastros em settings.toml     |
| --table-name (obrigatorio) | nome da tabela para busca                      |

Exemplo utilizando o parâmetro pks:

```
jumpdb pks <database> <name> --table-name <table_name>
```

| **fks**                    | Buscar Foreign Keys no banco de dados          |
|----------------------------|------------------------------------------------|
| database (obrigatorio)     | informar dialect (por exemplo mysql ou oracle) |
| name (obrigatorio)         | informar o nome cadastros em settings.toml     |
| --table-name (obrigatorio) | nome da tabela para busca                      |

Exemplo utilizando o parâmetro fks:

```
jumpdb fks <database> <name> --table-name <table_name>
```

| **indexes**                | Buscar Indexes de uma tabela no banco de dados                                              |
|----------------------------|---------------------------------------------------------------------------------------------|
| database (obrigatorio)     | informar dialect (por exemplo mysql ou oracle)                                              |
| name (obrigatorio)         | informar o nome cadastros em settings.toml                                                  |
| --table-name (obrigatorio) | nome da tabela para busca filter_columns: caso não informado ira recuperar todas as colunas |

Exemplo utilizando o parâmetro mapping:

```
jumpdb mapping <database> <name> --table-name <table_name> --path-file<caminho_do_arquivo>
```

| **mapping**               | Gerar script de criação de tabela de acordo com uma select |
|---------------------------|------------------------------------------------------------|
| database (obrigatorio)    | informar dialect (por exemplo mysql ou oracle)             |
| name (obrigatorio)        | informar o nome cadastros em settings.toml                 |
| --new-table (obrigatorio) | nome da nova tabela                                        |
| --path-file (obrigatorio) | caminho do arquivo do     SELECT                           |   

Exemplo utilizando o parâmetro mapping:

```
jumpdb mapping <database> <name> --table-name <table_name> --path-file<caminho_do_arquivo>
```

Exemplo 2: Suponha que temos um banco de dados **oracle** com o nome **practical** com duas tabelas
ORDERS e CUSTOMERS com a seguinte SELECT separada em um arquivo chamado **select.sql**.

**select.sql**

```sql
    SELECT
    O.ID AS ID_ORDER,
    C.ID AS ID_CUSTOMER,
    O.ORDERED AS ORDERED_ALIAS,
    O.DELIVERY AS DELIVERY_ALIAS,
    C.NAME AS NAME_ALIAS
    FROM ORDERS O
    INNER JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.ID
    ORDER BY ID_ORDER;
```

Rodamos o seguinte comando:

```commandline
jumpdb mapping oracle practical --new-table customer_ordered --path-file D:\ws_python\jumpdb\jumpdb\jumpdb\select.sql
```

Obtemos o seguintes resultado no console:

```sql
CREATE TABLE CUSTOMER_ORDERED (
        ID VARCHAR2(32) NOT NULL,
        ID_ORDER INTEGER, --ORDERS.ID
        ORDERED_ALIAS DATETIME, --ORDERS.ORDERED
        DELIVERY_ALIAS DATETIME, --ORDERS.DELIVERY
        ID_CUSTOMER INTEGER, --CUSTOMERS.ID
        NAME_ALIAS VARCHAR(20), --CUSTOMERS.NAME,
        DTC_INICIO DATE,
        DTC_FIM DATE,
        STS_CORRENTE VARCHAR2(1)
);

ALTER TABLE CUSTOMER_ORDERED ADD CONSTRAINT PK_CUSTOMER_ORDERED PRIMARY KEY (ID);

```

Para gerar esse script os seguintes passos são seguidos:

Os campos ID, DTC_INICIO, DTC_FIM, STS_CORRENTE são obrigatórios e ja incluidos.

1. Localiza todos os Alias (AS)
2. Localiza no banco de dados os tipos dessas colunas nas suas respectivas tabelas
3. É adicionado a coluna com o nome de acordo com o AS e em seguida comentado da origem da tabela e coluna.
4. Por fim é adicionado uma constraint primary key






