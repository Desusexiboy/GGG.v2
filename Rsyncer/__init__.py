from parser_cls import Parser
from utility_cls import Utility

def main():
    data_dict = (Parser.main())
    # print ('##########final dict##########')
    # Utility.print_dict(data_dict)
    # Utility.print_client(data_dict['client'])
    Utility.rsync_all(data_dict)
