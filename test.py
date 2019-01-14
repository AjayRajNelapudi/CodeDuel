import pymysql

db = pymysql.connect('localhost', 'root', 'anitscse034')
db.autocommit(True)
conn = db.cursor()

id = 1

conn.execute('USE CODEDUEL')
for i in range(3):
    query = '''insert into testcase values (%s, 1, '%s', '%s')
            ''' % (id, 'input' + str(i+1), 'output' + str(i+1))
    print(query)
    id += 1 