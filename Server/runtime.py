from subprocess import run, Popen
import os
from contextlib import suppress
with suppress(Exception):
    from Server import database

with suppress(Exception):
    import database

if os.name == 'nt':
    separator = "\\"
else:
    separator = "/"

class Run_Tests:
    def __init__(self, c_id, program_file, program_filepath, io_filepath, input_output):
        self.c_id = c_id
        self.filename, self.extension = program_file.split('.')
        self.program_file = program_file
        self.program_filepath = program_filepath + separator + str(self.c_id) + separator + self.filename
        self.io_filepath = io_filepath + separator + self.program_file.split('.')[0]
        self.input_output = input_output

    def get_compiler_runtime_env(self):
        if self.extension == 'c':
            self.compiler = 'gcc'
        elif self.extension == 'cpp':
            self.compiler = 'g++'
        elif self.extension == 'java':
            self.compiler = 'javac'
        elif self.extension == 'py':
            self.compiler = 'python3'

        if self.compiler in {'gcc', 'g++'}:
            self.run_command = './a.out'
        elif self.compiler == 'javac':
            self.run_command = ['java', self.filename]
        elif self.compiler in {'python', 'python3'}:
            self.run_command = ['python3', self.filename]

    def compile(self):
        if not self.compiler in {'python', 'python3'}:
            compile_src = Popen([self.compiler, self.program_file], cwd=self.program_filepath)
            compile_src.wait()

    def execute(self, input_data):
        with open(self.program_filepath + separator + 'ActualOutput.txt', 'w') as actual_output_file:
            status = run(self.run_command,
                        cwd=self.program_filepath,
                        input=input_data,
                        encoding='ascii',
                        stdout=actual_output_file,
                        timeout=5
                    )

        return status.returncode

    def run_tests(self):
        self.get_compiler_runtime_env()
        self.compile()
        test_run_status = []
        for t_id, input_filename, expected_output_filename in self.input_output:
            input_file = open(self.io_filepath + separator + input_filename, 'r')
            expected_output_file = open(self.io_filepath + separator + expected_output_filename, 'r')

            input_data = input_file.read()
            returncode = self.execute(input_data)
            if returncode != 0:
                return False

            actual_output_file = open(self.program_filepath + separator + 'ActualOutput.txt', 'r')

            expected_output = expected_output_file.read()
            actual_output = actual_output_file.read()

            if expected_output.replace('\n', '') == actual_output.replace('\n', ''):
                points = database.get_testcase_points(t_id)
                test_run_status.append('P')
            else:
                points = 0
                test_run_status.append('F')
            database.update_score(self.c_id, t_id, points)

            input_file.close()
            expected_output_file.close()
            actual_output_file.close()

        return test_run_status