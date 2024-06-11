import sqlite3


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn):
    sql_create_pools_table = """
    CREATE TABLE IF NOT EXISTS pools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        per_hour TEXT NOT NULL,
        img_src TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_pools_table)
    except sqlite3.Error as e:
        print(e)


def insert_pool(conn, pool):
    sql = ''' INSERT INTO pools(title, per_hour, img_src)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, pool)
    conn.commit()
    return cur.lastrowid


def select_pool_by_title(conn, title):
    cur = conn.cursor()
    cur.execute("SELECT * FROM pools WHERE title=?", (title,))
    rows = cur.fetchall()
    return rows



def initialize_db(db_file):
    conn = create_connection(db_file)
    create_table(conn)
    return conn
