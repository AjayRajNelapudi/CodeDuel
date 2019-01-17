from Server import database
import os

os.chdir('/users/ajayraj/documents/CodeDuelCursors2019')
os.mkdir('spec')
os.mkdir('src')
os.mkdir('test')

pwd = os.getcwd()

os.chdir(pwd + '/spec')
for problem in database.get_problem_names():
    os.mkdir(problem[0])

for c_id in database.get_all_cid():
    os.chdir(pwd + '/src')
    os.mkdir(str(c_id[0]))
    os.chdir(pwd + '/src' + '/' + str(c_id[0]))
    for problem in database.get_problem_names():
        os.mkdir(problem[0])

os.chdir(pwd + '/test')
for problem in database.get_problem_names():
    os.mkdir(problem[0])