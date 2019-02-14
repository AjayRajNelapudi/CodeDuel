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
        self.codeduel_db = database.CodeDuel_Database()

    def get_compiler_runtime_env(self):
        if self.extension == 'c':
            self.compiler = 'gcc'
        elif self.extension == 'cpp':
            self.compiler = 'g++'
        elif self.extension == 'java':
            self.compiler = 'javac'
        elif self.extension == 'py':
            self.compiler = 'python3'
        else:
            raise TypeError(self.extension, 'not supported\n')

        if self.compiler in {'gcc', 'g++'}:
            self.run_command = './a.out'
        elif self.compiler == 'javac':
            self.run_command = ['java', self.filename]
        elif self.compiler in {'python', 'python3'}:
            self.run_command = ['python3', self.filename]

    def set_safe_limits(self):
        # read resource module and set limits accordingly
        pass

    def compile(self):
        if not self.compiler in {'python', 'python3'}:
            compilation_errors_file = open(self.program_filepath + separator + 'CompilationErrors.txt', 'w')
            compile_src = Popen([self.compiler, self.program_file], cwd=self.program_filepath, stderr=compilation_errors_file)
            compile_src.wait()
            compilation_errors_file.close()
            if compile_src.returncode != 0:
                return False
        return True


    def execute(self, input_data):
        actual_output_file = open(self.program_filepath + separator + 'ActualOutput.txt', 'w')
        stderr_file = open(self.program_filepath + separator + 'stderr.txt', 'w')
        status = run(self.run_command,
                    cwd=self.program_filepath,
                    input=input_data,
                    encoding='ascii',
                    stdout=actual_output_file,
                    stderr=stderr_file,
                    timeout=5,
                    preexec_fn=self.set_safe_limits
                )
        actual_output_file.close()
        stderr_file.close()

        return status.returncode

    def run_tests(self):
        self.get_compiler_runtime_env()
        if not self.compile():
            compilation_errors_file = open(self.program_filepath + separator + 'CompilationErrors.txt', 'r')
            compilation_errors = compilation_errors_file.read()
            compilation_errors_file.close()
            if compilation_errors == '':
                compilation_errors = 'COMPILATION ERROR'
            return compilation_errors

        test_run_status = []
        for t_id, input_filename, expected_output_filename in self.input_output:
            input_file = open(self.io_filepath + separator + input_filename, 'r')
            expected_output_file = open(self.io_filepath + separator + expected_output_filename, 'r')

            input_data = input_file.read()
            returncode = self.execute(input_data)
            if returncode != 0:
                stderr = open(self.program_filepath + separator + 'stderr.txt', 'r')
                error = stderr.read()
                stderr.close()
                return error

            actual_output_file = open(self.program_filepath + separator + 'ActualOutput.txt', 'r')

            expected_output = expected_output_file.read()
            actual_output = actual_output_file.read()

            if expected_output.replace('\n', '') == actual_output.replace('\n', ''):
                points = self.codeduel_db.get_testcase_points(t_id)
                test_run_status.append('P')
            else:
                points = 0
                test_run_status.append('F')
            self.codeduel_db.update_score(self.c_id, t_id, points)

            input_file.close()
            expected_output_file.close()
            actual_output_file.close()

        return ' '.join(test_run_status)