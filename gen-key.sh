#!/usr/bin/env bash

# A hacky script to generate a gpg key and include it in the project
# ** NOT FOR PRODUCTION USE **

set -e

cd "$(dirname "$0")"

HAVEGED=`command -v haveged || true`

if [ x$HAVEGED != x ]; then
    echo "starting haveged service (requires root)"
    sudo systemctl start haveged
fi

GPG_OUTPUT=$(mktemp)

gpg --gen-key | tee $GPG_OUTPUT

KEY=`grep ^pub $GPG_OUTPUT | head -n 1 | awk '{ print $2 }' | sed 's/[0-9a-zA-Z]\+\///'`

echo "Using key: $KEY"

mkdir -p secrets/aptly

gpg --export-secret-keys --armor $KEY > secrets/aptly/private.key
gpg --export --armor $KEY > secrets/aptly/public.key

# XXX very hacky way to setting this variable
# TODO dynamically get this variable within the ansible role with `gpg $KEY` to
# get info
perl -pi -e "s/^aptly_secret_key_id:.*/aptly_secret_key_id: $KEY/g" group_vars/all

if [ x$HAVEGED != x ]; then
    echo "stopping havaged service (requires root)"
    sudo systemctl stop haveged
fi
