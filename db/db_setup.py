import duckdb

def initialize_db(database=':memory:'):
    con = duckdb.connect(database=database, read_only=False)
    con.execute("INSTALL vss; LOAD vss;")
    con.execute(
        '''
            CREATE OR REPLACE TABLE embeddings (
                doc_id INTEGER, 
                page_num INTEGER, 
                vec FLOAT[384],
                sentence TEXT
            );
        ''')
    return con
