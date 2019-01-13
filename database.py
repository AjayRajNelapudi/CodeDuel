import pymysql

database = pymysql.connect('localhost', 'root', 'anitscse034')
database.autocommit(True)
conn = database.cursor()

def get_contestant_dir(c_id):
    query = '''SELECT c_dir FROM Contestant WHERE c_id = %s''' % (c_id)
    conn.execute(query)
    contestant_dir = conn.fetchone()[0]
    return contestant_dir

def get_problem_dir(p_id):
    pass

def get_total_score(c_id):
    query = '''SELECT SUM(points) FROM Score WHERE c_id = %s''' % (c_id)
    conn.execute(query)
    total_score = conn.fetchone()[0]
    return total_score