import sys
class Error(object):
    def __init__(self):
        self.error_table = {0: '[Warining] Input File does not exist\n\n',
                            1: '[Warining] Multiple input files detected\n\n',
                            2: '[Warining] Multiple command line arguments\n\n',
                            3: '[Warining] Invalid command line argument\n\n'}

        self.error_record = []

    def check_error(self, error_code):
        if error_code in self.error_table.keys():
            sys.stdout.write(self.error_table[error_code])

