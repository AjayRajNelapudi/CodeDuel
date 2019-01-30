import pymysql
import os

if os.name == 'nt':
    separator = '\\'
else:
    separator = '/'

class CodeDuel_Database():

    def __init__(self):
        self.database = pymysql.connect('localhost', 'root', 'anitscse034')
        self.database.autocommit(True)
        self.conn = self.database.cursor()
        self.conn.execute('USE CodeDuel')

    def validate_login(self, c_id, password):
        query = "SELECT * FROM Contestant where c_id = %s and password = '%s'" % (c_id, password)
        if self.conn.execute(query) == 1:
            return True
        return False

    def get_contestant_name(self, c_id):
        query = "SELECT c_name FROM Contestant WHERE c_id = %s" % (c_id)
        self.conn.execute(query)
        contestant_name = self.conn.fetchone()[0]
        return contestant_name

    def get_directory_path(self, d_id):
        query = "SELECT d_path FROM Directory WHERE d_id = '%s'" % (d_id)
        self.conn.execute(query)
        directory_path = self.conn.fetchone()[0]
        return directory_path

    def get_contestant_dir(self, c_id):
        contestant_name = self.conn.get_contestant_name(c_id)
        contestant_path = contestant_name.replace(' ', '')
        src_dir = self.get_directory_path('src')
        contestant_dir = src_dir + separator + contestant_path
        return contestant_dir

    def get_test_filenames(self, p_id):
        query = "SELECT t_id, t_inputfile, t_outputfile FROM Testcase WHERE p_id = %s" % (p_id)
        self.conn.execute(query)
        test_filenames = self.conn.fetchall()
        return test_filenames

    def get_score(self, c_id):
        query = "SELECT sum(points) FROM Score WHERE c_id = %s" % (c_id)
        self.conn.execute(query)
        score = self.conn.fetchone()[0]
        return score

    def update_score(self, c_id, t_id, points):
        existence_test_query = "SELECT * FROM Score WHERE c_id = %s AND t_id = %s" % (c_id, t_id)
        self.conn.execute(existence_test_query)
        existence_test = len(self.conn.fetchall())

        if existence_test != 0:
            query = "UPDATE Score SET points = %s, s_timestamp = NOW() WHERE c_id = %s AND t_id = %s" % (points, c_id, t_id)
        else:
            query = "INSERT INTO Score VALUES (%s, %s, %s, NOW())" % (c_id, t_id, points)
        self.conn.execute(query)

    def get_pid(self, p_title):
        query = "SELECT p_id FROM Problem WHERE p_title = '%s'" % (p_title)
        self.conn.execute(query)
        p_id = self.conn.fetchone()[0]
        return p_id

    query = ''' SELECT C.c_id, C.c_name, (  SELECT sum(S.points)
                                        FROM Score S
                                        WHERE C.c_id = S.c_id   ) AS Total
                    FROM Contestant C
                    ORDER BY Total DESC '''

    def make_leaderboard(self):
        leaderboard = []
        query = "SELECT c_id_A, c_id_B FROM Duel"
        self.conn.execute(query)
        duels = self.conn.fetchall()
        for duel in duels:
            score_A = self.get_score(duel[0])
            score_B = self.get_score(duel[1])

            if type(score_A).__name__ == 'NoneType' and type(score_B).__name__ != 'NoneType':
                leaderboard.append((duel[1], score_B))
                continue
            elif type(score_A).__name__ != 'NoneType' and type(score_B).__name__ == 'NoneType':
                leaderboard.append((duel[0], score_A))
                continue
            elif type(score_A).__name__ == 'NoneType' and type(score_B).__name__ == 'NoneType':
                continue

            if score_A > score_B:
                leaderboard.append((duel[0], self.get_contestant_name(duel[0]), score_A))
            elif score_B > score_A:
                leaderboard.append((duel[1], self.get_contestant_name(duel[1]), score_B))
            else:
                leaderboard.append((duel[0], self.get_contestant_name(duel[0]), score_A))
                leaderboard.append((duel[1], self.get_contestant_name(duel[1]), score_B))

        leaderboard.sort(key = lambda x: x[1])

        return leaderboard

    def get_opponent_id(self, c_id):
        query = "SELECT c_id_B FROM Duel WHERE c_id_A = %s" % (c_id)
        tuples_count = self.conn.execute(query)

        if tuples_count == 1:
            opponent_id = self.conn.fetchone()[0]
            return opponent_id

        query = "SELECT c_id_A FROM Duel WHERE c_id_B = %s" % (c_id)
        self.conn.execute(query)
        opponent_id = self.conn.fetchone()[0]
        return opponent_id

    def get_problem_names(self):
        query = "SELECT p_title FROM Problem"
        self.conn.execute(query)
        problem_names = self.conn.fetchall()
        return problem_names

    def get_all_cid(self):
        query = "SELECT c_id FROM Contestant"
        self.conn.execute(query)
        all_cid = self.conn.fetchall()
        return all_cid

    def get_testcase_points(self, t_id):
        query = "SELECT t_points FROM Testcase WHERE t_id = %s" % (t_id)
        self.conn.execute(query)
        t_points = self.conn.fetchone()[0]
        return t_points

    def get_duel_id(self, c_id):
        query = "SELECT duel_id FROM Duel WHERE c_id_A = %s OR c_id_B = %s" % (c_id, c_id)
        self.conn.execute(query)
        duel_id = self.conn.fetchone()[0]
        return duel_id

    def __del__(self):
        self.conn.close()