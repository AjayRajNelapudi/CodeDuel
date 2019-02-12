from subprocess import run
import random
import os
import time

generate_c_id = lambda: str(random.randrange(1, 4))
commands = [['python3', 'client.py', 'config', generate_c_id(), 'key'],
            ['python3', 'client.py', 'push', 'SumOfN.c'],
            ['python3', 'client.py', 'pull', 'SumOfN.txt'],
            ['python3', 'client.py', 'points'],
            ['python3', 'client.py', 'help']]

command = None
try:
    while True:
        command_index = random.randrange(0, 4)
        command = commands[command_index]
        print('COMMAND:', command, '\nOUTPUT:')
        process = run(command, cwd=os.getcwd(), timeout=10)
        process.check_returncode()
        time.sleep(2)
except Exception as e:
    print(e)
    print(command)