from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()