import MySQLdb
from config import load_config

config = load_config()
db = MySQLdb.connect(
    host = config['database']['host'],
    user = config['database']['user'],
    password = config['database']['password'],
    database = config['database']['name']
)

async def load_words():
    cursor = db.cursor()
    cursor.execute("""SELECT word from word""")
    list = cursor.fetchall()
    flat_list = [item for sublist in list for item in sublist]
    return flat_list
