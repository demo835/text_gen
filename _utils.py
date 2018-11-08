import logging

def startup():
    print('Would you like to run in verbose mode? y/n')
    i = str(input())
    if i == 'y':
        verbose = True
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
    else:
        verbose = False
        logging.disable(logging.CRITICAL)