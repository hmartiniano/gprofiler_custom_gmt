#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pandas as pd
import argparse
from gprofiler import GProfiler


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default=None, help="Gene list. One gene per line")
    parser.add_argument("-g", "--gmt", type=str, default=None, help="GMT file")
    parser.add_argument("-t", "--token", type=str, default=None, help="Token from another invocation of the program")
    parser.add_argument("-o", "--output", type=str, default="output.csv", help="Output file name. Default: output.csv")
    return parser
    
    
def get_token_form_response(response):
    if response.status_code == 200:
        token = response.json()['organism']
    else:
        try:
            error_message = 'Error: {}'.format(response.json()['message'])
        except:
            error_message = 'Error, status code {}'.format(response.status_code)
        raise AssertionError(error_message)
    print("Token:", token)
    return token


#If you wish to upload a single GMT file.
def main(args):
    gp = GProfiler(
        user_agent='gprofiler_custom_gmt', #optional user agent
        return_dataframe=True, #return pandas dataframe or plain python structures    
    )
    genes = [line.strip() for line in open(args.filename)]

    if args.gmt is not None:
        with open(args.gmt) as f:
            response = requests.post('https://biit.cs.ut.ee/gprofiler/api/gost/custom/',
                          json={'gmt':f.read(),
                                'name': args.gmt})
        token = get_token_form_response(response)
    elif args.token is not None:
        token = args.token
    else:
         raise ValuError("Please supply either a token or a gmt file")
    res = gp.profile(genes, organism=token)
    res.to_csv(args.output)


def cli():
    import sys
    args = parser().parse_args(sys.argv[1:])
    main(args)
