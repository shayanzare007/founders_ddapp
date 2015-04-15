#!/usr/bin/env bash
# A script to start Mindtagger for tasks under labeling/
# Author: Jaeho Shin <netj@cs.stanford.edu>
# Created: 2014-10-11
set -eu

# set up environment to run Mindtagger
cd "$(dirname "$0")"
utildir=../../../util
if [[ -d $utildir ]]; then
    # use the util directory if this script is under DeepDive source tree
    PATH="$PWD/$utildir:$PATH"
else
    # otherwise, the current working directory
    PATH="$PWD:$PATH"
    utildir=.
fi

# install Mindbender locally if not available or broken
release=${MINDBENDER_RELEASE:=v0.1.3}
if ! type mindbender &>/dev/null || [[ $(mindbender version | head -1) < "Mindbender $release" ]]; then
    tool=$utildir/mindbender
    mkdir -p "$(dirname "$tool")"
    echo >&2 "Downloading Mindbender..."
    curl --location --show-error --output $tool.download \
        https://github.com/netj/mindbender/releases/download/$release/mindbender-$release-$(uname)-$(uname -m).sh
    chmod +x $tool.download
    mv -f $tool.download $tool
fi

# start Mindtagger for all tasks available next to this script
echo >&2 "Starting Mindtagger for all tasks under $PWD/..."
shopt -s globstar 2>/dev/null || true
mindbender tagger $(ls -t **/mindtagger.conf)
