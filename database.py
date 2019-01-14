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
    query = '''SELECT c_name FROM Contestant WHERE c_id = %s''' % (c_id)
    conn.execute(query)
    contestant_name = conn.fetchone()[0]
    return contestant_name

def get_directory_path(d_id):
    query = '''SELECT d_path FROM Directory WHERE d_id = '%s' ''' % (d_id)
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
    query = '''SELECT t_inputfile, t_outputfile FROM Testcase WHERE p_id = %s''' % (p_id)
    conn.execute(query)
    test_filenames = conn.fetchall()
    return test_filenames


print(get_test_filenames(1))