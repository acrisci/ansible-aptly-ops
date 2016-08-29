#!/usr/bin/env python3

import sys
from os import path
from argparse import ArgumentParser
from subprocess import call
import json

PUBLISH_REPOS = 'publish-repos'

def do_publish_repos(args):
    debs = args.debs

    extra_vars = { 'aptly_debs': [] }

    for d in debs:
        if not path.exists(d):
            print('Could not find package: %s' % d)
            sys.exit(1)

        extra_vars['aptly_debs'].append(d)

    call(['ansible-playbook', '-i', 'hosts', '--ask-become-pass', '--extra-vars', json.dumps(extra_vars), 'site.yml'])


parser = ArgumentParser(description='Manage aptly repositories and repos')

subparsers = parser.add_subparsers(help='Publish the configured repos with the given debian packages', dest='command')

publish_repos_cmd = subparsers.add_parser(PUBLISH_REPOS)
publish_repos_cmd.add_argument('debs', metavar='DEBS', nargs='+', help='The Debian packages to publish')

args = parser.parse_args()

if not args.command:
    parser.print_help()
    sys.exit(0)

if args.command == PUBLISH_REPOS:
    do_publish_repos(args)
