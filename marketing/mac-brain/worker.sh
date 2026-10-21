#!/bin/sh
# Lightweight Mac Marketing Brain worker. No root, arbitrary shell jobs or external actions.
set -eu
umask 077
cd /opt/business-house-matrix/marketing/brain
/usr/bin/python3 brain.py recover >/dev/null
/usr/bin/python3 brain.py work-once
