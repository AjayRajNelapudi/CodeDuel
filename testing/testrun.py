from subprocess import run
import random
import os
import time

commands = [['python3', 'client.py', 'push', 'SumOfN.c'],
            ['python3', 'client.py', 'pull', 'SumOfN.txt'],
            ['python3', 'client.py', 'points'],
            ['python3', 'client.py', 'help']]

c_id = random.randrange(1, 4)
login_command = ['python3', 'client.py', 'config', str(c_id), 'key']
print(login_command)
try:
    process = run(login_command, cwd=os.getcwd(), timeout=10)
    process.check_returncode()
except Exception as e:
    print(e)
    print(login_command)

command = None
try:
    while True:
        command_index = random.randrange(0, 3)
        command = commands[command_index]
        process = run(command, cwd=os.getcwd(), timeout=10)
        process.check_returncode()
        time.sleep(2)
except Exception as e:
    print(e)
    print(command)