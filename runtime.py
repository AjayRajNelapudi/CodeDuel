from subprocess import run, Popen
import os
import database

if os.name == 'nt':
    separator = "\\"
else:
    separator = "/"

class Run_Tests:
    def __init__(self, c_id, program_file, program_filepath, io_filepath, input_output, compiler='gcc', run_command='./a.out'):
        '''
        Run_Tests constructor
        :param c_id:
        :param program_file: string
        :param program_filepath: string
        :param io_filepath: string
        :param input_output: tuple of tuples
        :param compiler: string
        :param run_command: string
        '''
        self.c_id = c_id
        self.program_file = program_file
        self.program_filepath = program_filepath
        self.io_filepath = io_filepath
        self.input_output = input_output
        self.compiler = compiler
        self.run_command = run_command

    def compile(self):
        '''
        compile()
        :return: None
        '''
        if not self.compiler in {'python', 'python3'}:
            Popen([self.compiler, self.program_file], cwd=self.program_filepath).wait()


    def execute(self, input_data):
        '''
        execute()
        :param input_data: String to be passed as input to program
        :return: return value of subprocess
        '''
        file = open(self.program_filepath + separator + 'op.txt', 'r+')
        file.truncate(0)
        file.close()

        with open(self.program_filepath + '/ActualOutput.txt', 'w') as actual_output_file:
            status = run(self.run_command,
                        cwd=self.program_filepath,
                        input=input_data,
                        encoding='ascii',
                        stdout=actual_output_file
                    )

        return status.returncode

    def run_tests(self):
        self.compile()

        for t_id, input_filename, expected_output_filename in self.input_output:
            input_file = open(self.io_filepath + separator + self.program_file + separator + 'Input' + separator + input_filename, 'r')
            expected_output_file = open(self.io_filepath + separator + self.program_file + separator + 'Output' + separator + expected_output_filename, 'r')

            input_data = input_file.read()
            returncode = self.execute(input_data)
            if returncode != 0:
                return False

            actual_output_file = open(self.program_filepath + separator + 'ActualOutput.txt', 'r')

            expected_output = expected_output_file.read()
            actual_output = actual_output_file.read()

            if expected_output != actual_output:
                points = 0
            else:
                points = 25
            database.update_score(self.c_id, t_id, points)


            input_file.close()
            expected_output_file.close()
            actual_output_file.close()
