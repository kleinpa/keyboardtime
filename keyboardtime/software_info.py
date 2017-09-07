import datetime
import sys
import os

info = {}

info['exe'] = "keyboardtime"
info['name'] = "KeyboardTime"
info['description'] = "Keyboard Time Monitor"

info['author'] = "Peter Klein"
info['company_name'] = "Peter Klein"
info['copyright'] = "{0} {1}".format(datetime.datetime.now().year, info['company_name'])

info['upgrade_code'] = "92891133-407C-43FE-874C-D28945F58DEE"

info['port'] = 63874

version_data = (1, 7, 0)
info['version'] = "{0}.{1}.{2}".format(*version_data)
info['version4'] = "{0}.{1}.{2}.0".format(*version_data)

# Some utility functions for accessing data from outside python
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Get the software information.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-v', '--value', help='gets the value associated with the variable VAR', metavar="VAR")
    group.add_argument('-c', '--candle', help='display software info formatted as candle arguments', action='store_true')
    parser.add_argument('-o', help='output file for pickled version info', metavar="FILE")
    args = parser.parse_args()

    if args.candle:
        print("".join([" -dsi_{0}=\"{1}\"".format(*x) for x in info.items()]))
    if args.value:
        print(info.get(args.value, None))
