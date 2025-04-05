import psycopg2
from psycopg2 import sql

def drop_all_tables(database, user, password, host='localhost', port=5432):
    try:
        # Conectar ao banco de dados
        connection = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Obter todas as tabelas do esquema público
        cursor.execute("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public';
        """)
        tables = cursor.fetchall()

        # Apagar todas as tabelas
        for table in tables:
            table_name = table[0]
            cursor.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(sql.Identifier(table_name)))
            print(f"Tabela '{table_name}' apagada com sucesso.")

        print("Todas as tabelas foram apagadas.")
    except Exception as e:
        print(f"Erro ao apagar tabelas: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Configurações do banco de dados
db_config = {
    'database': 'cuidar_plus_db',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost',  # Altere se necessário
    'port': 5432          # Altere se necessário
}

# Executar a função
drop_all_tables(
    database=db_config['database'],
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    port=db_config['port']
)