#!/usr/bin/env bash

echo Setting up environment variables for PyDM Charting...

source /afs/slac/g/lcls/package/pydm/setup_pydm_env.bash

export PYDM_PATH=/u/re/hbui/local/dev_test/pydm/pydm-hmbui

export EPICS_CA_AUTO_ADDR_LIST=yes
export PYEPICS_LIBCA=/afs/slac/g/lcls/epics/base/R3.15.5-1.0/lib/rhel6-x86_64/libca.s

echo Done!
