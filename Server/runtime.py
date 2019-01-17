from subprocess import run, Popen
import os
try:
    from Server import database
except:
    pass

try:
    import database
except:
    pass

if os.name == 'nt':
    separator = "\\"
else:
    separator = "/"

class Run_Tests:
    def __init__(self, c_id, program_file, program_filepath, io_filepath, input_output, compiler='gcc', run_command='./a.out'):
        self.c_id = c_id
        self.program_file = program_file
        self.program_filepath = program_filepath + separator + str(self.c_id) + separator + self.program_file.split('.')[0]
        self.io_filepath = io_filepath + separator + self.program_file.split('.')[0]
        self.input_output = input_output
        self.compiler = compiler
        self.run_command = run_command

    def compile(self):
        if not self.compiler in {'python', 'python3'}:
            compile_src = Popen([self.compiler, self.program_file], cwd=self.program_filepath)
            compile_src.wait()

    def execute(self, input_data):
        file = open(self.program_filepath + separator + 'ActualOutput.txt', 'r+')
        file.truncate(0)
        file.close()

        with open(self.program_filepath + separator + 'ActualOutput.txt', 'w') as actual_output_file:
            status = run(self.run_command,
                        cwd=self.program_filepath,
                        input=input_data,
                        encoding='ascii',
                        stdout=actual_output_file
                    )

        return status.returncode

    def run_tests(self):
        self.compile()
        test_case_status = []
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
                points = 10
                test_case_status.append('P')
            else:
                points = 0
                test_case_status.append('F')
            database.update_score(self.c_id, t_id, points)

            input_file.close()
            expected_output_file.close()
            actual_output_file.close()

        return test_case_status

'''
tests = runtime.Run_Tests(1, 'SumOfN.c', '/users/ajayraj/documents/codeduelcursors2019/src', '/users/ajayraj/documents/codeduelcursors2019/tests', [(1, 'input1', 'output1'), (2, 'input2', 'output2'), (3, 'input3', 'output3')])
tests.run_tests()
'''