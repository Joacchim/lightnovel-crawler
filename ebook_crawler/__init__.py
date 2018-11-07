#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interactive value input"""
import sys
import logging
import urllib3
from PyInquirer import prompt
from .lnmtl import LNMTLCrawlerApp
# from .wuxia import WuxiaCrawler
# from .wuxiac import WuxiaCoCrawler
# from .webnovel import WebNovelCrawler
# from .boxnovel import BoxNovelCrawler
# from .readln import ReadLightNovelCrawler
# from .novelplanet import NovelPlanetCrawler

def configure():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else None
    if mode == '-v' or mode == '--verbose':
        print('\33[91m 🔊 IN VERBOSE MODE\33[0m')
        print('-' * 60)
        logging.basicConfig(level=logging.DEBUG)
    else:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # end if
# end def

def headline():
    with open('VERSION', 'r') as f:
        version = f.read().strip()
    # end with
    print('-' * 60)
    print(' \33[1m\33[92m📒', 'Ebook Crawler 🍀', version, '\33[0m')
    print(' 🔗\33[94m https://github.com/dipu-bd/site-to-epub', '\33[0m')
    print(' 🙏\33[94m https://saythanks.io/to/dipu-bd', '\33[0m')
    print('-' * 60)
# end def

def main():
    headline()
    configure()

    choices = [
        'https://lnmtl.com',
        'https://boxnovel.com',
        'https://novelplanet.com',
        'https://www.webnovel.com',
        'https://www.wuxiaworld.co',
        'https://www.wuxiaworld.com',
        'https://www.readlightnovel.org'
    ]

    answer = prompt([
        {
            'type': 'list',
            'name': 'source',
            'message': 'Where is the novel from?',
            'choices': choices,
        },
    ])

    if choices[0] == answer['source']:
        LNMTLCrawlerApp().start()
    elif choices[1] == answer['source']:
        print('Not Yet Implemented: ', answer['source'])
    elif choices[2] == answer['source']:
        print('Not Yet Implemented: ', answer['source'])
    elif choices[3] == answer['source']:
        print('Not Yet Implemented: ', answer['source'])
    elif choices[4] == answer['source']:
        print('Not Yet Implemented: ', answer['source'])
    elif choices[5] == answer['source']:
        print('Not Yet Implemented: ', answer['source'])
    elif choices[6] == answer['source']:
        print('Not Yet Implemented: ', answer['source'])
    # end if
# end def

if __name__ == '__main__':
    main()
# end if
