import pymysql

database = pymysql.connect('localhost', 'root', 'anitscse034')
database.autocommit(True)
conn = database.cursor()

def get_contestant_dir(c_id):
    query = '''SELECT c_dir FROM Contestant WHERE c_id = %s''' % (c_id)
    conn.execute(query)
    dir = conn.fetchone()[0]
    return dir

