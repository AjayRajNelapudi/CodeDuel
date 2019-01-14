import pymysql
import os

if os.name == 'nt':
    separator = '\\'
else:
    separator = '/'

database = pymysql.connect('localhost', 'root', 'anitscse034')
database.autocommit(True)
conn = database.cursor()
conn.execute('USE CodeDuel')

def get_contestant_name(c_id):
    query = "SELECT c_name FROM Contestant WHERE c_id = %s" % (c_id)
    conn.execute(query)
    contestant_name = conn.fetchone()[0]
    return contestant_name

def get_directory_path(d_id):
    query = "SELECT d_path FROM Directory WHERE d_id = '%s'" % (d_id)
    conn.execute(query)
    directory_path = conn.fetchone()[0]
    return directory_path

def get_contestant_dir(c_id):
    contestant_name = get_contestant_name(c_id)
    contestant_path = contestant_name.replace(' ', '')
    src_dir = get_directory_path('src')
    contestant_dir = src_dir + separator + contestant_path
    return contestant_dir

def get_test_filenames(p_id):
    query = "SELECT t_id, t_inputfile, t_outputfile FROM Testcase WHERE p_id = %s" % (p_id)
    conn.execute(query)
    test_filenames = conn.fetchall()
    return test_filenames

def get_score(c_id):
    query = "SELECT sum(points) FROM Score WHERE c_id = %s" % (c_id)
    conn.execute(query)
    score = conn.fetchone()[0]
    return score

def update_score(c_id, t_id, points):
    existence_test_query = "SELECT * FROM Score WHERE c_id = %s AND t_id = %s" % (c_id, t_id)
    conn.execute(existence_test_query)
    existence_test = len(conn.fetchall())

    if existence_test > 1:
        query = "UPDATE Score SET points = %s WHERE c_id = %s AND t_id = %s" % (points, c_id, t_id)
    else:
        query = "INSERT INTO Score VALUES (%s, %s, %s)" % (c_id, t_id, points)
    conn.execute(query)

print(update_score(1, 1, 10))