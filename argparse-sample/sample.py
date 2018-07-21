import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Argparse sample')
    # positional are required by default
    parser.add_argument('n1', metavar='N1',
                        help='positional, metavar, required')
    parser.add_argument('N2', nargs='*', help='positional, zero or more')

    parser.add_argument('-f', '--flag', action='store_true',
                        help='short name, store true')
    parser.add_argument('--val', required=True,
                        help='required, store arg value')
    parser.add_argument('--var', type=int, choices=[1, 3, 5], default=3,
                        help='choices (default: %(default)s)')
    parser.add_argument('--push', metavar='X', dest='opt_list', type=int, action='append',
                        help='append value, custom attribute name')

    group = parser.add_mutually_exclusive_group()  # group can also be required=
    group.add_argument('-i', action='store_true', help='can not be used with -e')
    group.add_argument('-e', action='store_false', help='can not be used with -i')

    parser.add_argument('--version', action='version', version='%(prog)s 0.1',  # version= is mandatory
                        help='prints version and exits')

    args = parser.parse_args()
    print(args)
