'''
PyAuthomation training task: Rsync wrapper.Stage 1: Argparse.
Takes known parameters from CLI input. Returns output_dict.
All keys stored in output_dict['keys'].
All recognised files,dirrectories to copy and remote dirrectory is
stored in output_dict['host_files']
Password to remote host located in output_dict['password']
'''
import argparse
from utility_cls import Utility

logger = Utility.rsynclog.logger_init('inputparser')


class Inputparser:
    """ First stage parser. Using 'argparse' module to pull out all valid parameters."""

    @staticmethod
    def inputparse():
        """ Static method which draws out all valid parameters. Based on 'argparse' module. Returns dict,list """
        output_dict = {}
        single_param = tuple('PavSzqih')
        parser = argparse.ArgumentParser(add_help=False)
        filesgarbage = []
        unknownkeys = []
        keys = []
        parser.add_argument('-process', action="store_true", default=False)
        parser.add_argument('-e', action="store", dest='connection', type=str)
        known, unknown = parser.parse_known_args(['-Pa','-process','/dir','file','username@remote:/dirdir'])
        # ['-PavSzqi', '-process', '-pass=noOneLiveForever',
        #  '-h', '/dir', 'some', 'file',
        #  '[-pass=1234 root:port@hostname:/not\ dir -pass=123 another:2@hostname:/dir andone@more:/dir -pass=urmama69]']
        # Fill arguments in group
        unknown = unknown

        unknown, hosts = Inputparser.get_hosts(unknown)
        unknown, filesgarbage = Inputparser.get_files(unknown)
        unknown = set(unknown)
        for i in unknown:
            if i[1:] in single_param:
                keys.append(i)
            else:
                unknownkeys.append(i)

        if known.connection == 'ssh':
            print(known.connection)
            keys.append('-e ssh')
        elif known.connection == 'rsh':
            keys.append('-e rsh')

        if known.process:
            keys.append('-process')
        output_dict.update({'host_files': filesgarbage, 'keys': keys, 'hosts': hosts})

        Utility.rsynclog.debug_log(logger, output_dict)
        return output_dict, unknownkeys

    @staticmethod
    def get_hosts(some_list):
        if (some_list[-1] == ']'):
            index = some_list.index('[')
            host_list = some_list[index + 1:-1]
            some_list = some_list[:index]
        else:
            if(some_list[-1].startswith('-pass=')):
                host_list = some_list[-2:]
                some_list.remove(some_list[-1])
                some_list.remove(some_list[-1])
            else:
                host_list = [some_list[-1],]
                some_list.remove(some_list[-1])

        return some_list, host_list

    @staticmethod
    def get_files(some_list):
        unknown = filter(lambda x: x.startswith('-'), some_list)
        files = filter(lambda x: not x.startswith('-'), some_list)
        return unknown, files
