import datetime

info = {}

info['exe'] = "metrics"
info['name'] = "Metrics"
info['description'] = "A Metrics Logger"

info['author'] = "Peter Klein"
info['company_name'] = "Peter Klein"
info['copyright'] = "(c) {0}, {1}".format(datetime.datetime.now().year, info['company_name'])

info['version'] = "1.0"


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Get the software information.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-v', '--value', help='gets the value associated with the variable VAR',metavar="VAR")
    group.add_argument('-c', '--candle', help='display software info formatted as candle arguments', action='store_true')
    args = parser.parse_args()

    if args.candle:
        print("".join([" -dsi_{0}=\"{1}\"".format(*x) for x in info.items()]))
    if args.value:
        print(info.get(args.value, None))
