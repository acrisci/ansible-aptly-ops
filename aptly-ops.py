#!/usr/bin/env python3

import sys
import os
from os import path
from argparse import ArgumentParser
from subprocess import call
import json

script_dir = os.path.dirname(path.realpath(__file__))

PUBLISH_REPOS = 'publish-repos'
UPDATE_REPOS = 'update-repos'
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

def do_publish_repos(args):
    run_playbook('site.yml', debs=args.debs)

def do_update_repos(args):
    run_playbook('add-debs.yml', debs=args.debs)

parser = ArgumentParser(description='Manage aptly repositories and repos')

subparsers = parser.add_subparsers(help='Publish the configured repos with the given debian packages', dest='command')

publish_repos_cmd = subparsers.add_parser(PUBLISH_REPOS)
publish_repos_cmd.add_argument('debs', metavar='DEBS', nargs='+', help='The Debian packages to publish')

update_repos_cmd = subparsers.add_parser(UPDATE_REPOS)
update_repos_cmd.add_argument('debs', metavar='DEBS', nargs='+', help='The Debian packages to update the repo with')

clean_repos_cmd = subparsers.add_parser(CLEAN_REPOS)

args = parser.parse_args()

if not args.command:
    parser.print_help()
    sys.exit(0)

if args.command == PUBLISH_REPOS:
    do_publish_repos(args)
elif args.command == UPDATE_REPOS:
    do_update_repos(args)
elif args.command == CLEAN_REPOS:
    do_clean_repos(args)
