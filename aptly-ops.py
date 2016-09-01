#!/usr/bin/env python3

import sys
import os
from os import path
from argparse import ArgumentParser
from subprocess import call
import json

script_dir = os.path.dirname(path.realpath(__file__))

CREATE_REPOS = 'create-repos'
ADD_DEBS = 'add-debs'
CLEAN_REPOS = 'clean-repos'

def run_playbook(playbook, debs=[]):
    extra_vars = { 'aptly_debs': [] }

    for d in debs:
        if not path.exists(d):
            print('Could not find package: %s' % d)
            sys.exit(1)

        extra_vars['aptly_debs'].append(path.realpath(d))

    call(['ansible-playbook', '-i', path.join(script_dir, 'hosts'), '--ask-become-pass', '--extra-vars', json.dumps(extra_vars), path.join(script_dir, playbook)])

def do_clean_repos(args):
    run_playbook('clean-repos.yml')

def do_create_repos(args):
    run_playbook('site.yml')

def do_add_debs(args):
    run_playbook('add-debs.yml', debs=args.debs)

parser = ArgumentParser(description='Manage aptly repositories and repos')

subparsers = parser.add_subparsers(help='Publish the configured repos with the given debian packages', dest='command')

create_repos_cmd = subparsers.add_parser(CREATE_REPOS)

add_debs_cmd = subparsers.add_parser(ADD_DEBS)
add_debs_cmd.add_argument('debs', metavar='DEBS', nargs='+', help='The Debian packages to update the repo with')

clean_repos_cmd = subparsers.add_parser(CLEAN_REPOS)

args = parser.parse_args()

if not args.command:
    parser.print_help()
    sys.exit(0)

if args.command == CREATE_REPOS:
    do_create_repos(args)
elif args.command == ADD_DEBS:
    do_add_debs(args)
elif args.command == CLEAN_REPOS:
    do_clean_repos(args)
