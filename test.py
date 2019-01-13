import pymysql

db = pymysql.connect('localhost', 'root', 'anitscse034')
db.autocommit(True)
conn = db.cursor()

id = 22

conn.execute('USE CODEDUEL')
for i in range(3):
    query = '''INSERT INTO Testcase
                    VALUES
                    (%s, 8, '/Users/ajayraj/Documents/CodeDuelCursors/spec/FakeCoin', '%s', '%s')
            ''' % (id, 'input' + str(i+1), 'output' + str(i+1))
    conn.execute(query)
    id += 1 