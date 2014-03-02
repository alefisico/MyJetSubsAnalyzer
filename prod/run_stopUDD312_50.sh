#!/bin/sh

# This file sets up the bash shell for condor
# If you have additional custom enhancements to your shell 
# environment, you may need to add them here


export SCRAM_ARCH="slc5_amd64_gcc462"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1
#source $VO_CMS_SW_DIR/cmsset_default.sh
#source /uscmst1/prod/sw/cms/shrc prod
source /cms/base/cmssoft/cmsset_default.sh

# Change to your CMSSW software version
export MYRUNDIR=/cms/gomez/Substructure/PATTuples/CMSSW_5_3_12/src/MySubsPATtuple/MyPATtuplizer/prod/

cd $MYRUNDIR
eval `scramv1 runtime -sh`
cmsRun /cms/gomez/Substructure/PATTuples/CMSSW_5_3_12/src/MySubsPATtuple/MyPATtuplizer/prod/mypattuplizer_cfg.py $1 $2 $3 $4 $5 

