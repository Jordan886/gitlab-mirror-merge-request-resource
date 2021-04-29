#! /usr/bin/python3
import sys
import argparse
from pprint import pprint
from load_json import LoadJson


config = LoadJson(sys.stdin)

parser = argparse.ArgumentParser(description='Argument to this python script')
parser.add_argument('--api-url', type=str, required=True, help='Gitlab API URL')
parser.add_argument('--access-token', type=str, required=True, help='The Personal/Project access token')
parser.add_argument('--source-branch', type=str, required=True, help='The Source Branch')

args = parser.parse_args()

print(f'will build {args.microservices}')


