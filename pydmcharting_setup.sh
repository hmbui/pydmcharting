#!/usr/bin/env bash

echo Setting up environment variables for PyDM Charting...

source /afs/slac/g/lcls/package/pydm/setup_pydm_env.bash
export PYDM_PATH=/u/re/hbui/local/dev_test/pydm/pydm-hmbui
export PYDM_STRIPTOOL_PYDM_PATH=/u/re/hbui/local/dev_test/pydm/pydm-hmbui
#export PYTHONPATH=$PYDM_PATH:/u/re/hbui/local/dev_test/pydmcharting/pydmcharting-hmbui:$PYTHONPATH
export EPICS_CA_AUTO_ADDR_LIST=yes

echo Done!
