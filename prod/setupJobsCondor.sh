#!/bin/sh
#################################################
echo '------------------------------------------------------------------'
echo 'Input parameters:'

SAMPLE=$1
INPUTDIR=$2
OUTPUTDIR='/cms/gomez/Stops/st_jj/patTuples/'
RUNDIR='/cms/gomez/Substructure/PATTuples/CMSSW_5_3_12/src/MySubsPATtuple/MyPATtuplizer/prod/'
CMSRUNFILE='mypattuplizer_cfg.py'
JOBS=20

echo 'Output directory : '${OUTPUTDIR}
echo 'Running directory: '${RUNDIR}
echo 'cmsRun File      : '${CMSRUNFILE}
echo 'Sample           : '${SAMPLE}
echo 'Number of jobs   : '${JOBS}
echo '------------------------------------------------------------------'

condorFile=${RUNDIR}condor_${SAMPLE}.jdl
runFile=${RUNDIR}run_${SAMPLE}.sh

###################################################################
echo 'Creating output directory....'
if [ -d "${OUTPUTDIR}${SAMPLE}" ]; then 
	rm -rf "${OUTPUTDIR}${SAMPLE}" 
fi
mkdir -p ${OUTPUTDIR}${SAMPLE}/results
mkdir -p ${OUTPUTDIR}${SAMPLE}/condorlog

###################################################################
echo 'Creating condor file....'
if [ -f ${condorFile} ]; then 
	rm -rf ${condorFile}
fi
echo 'Universe = vanilla
initialdir = '${RUNDIR}'
Executable = '${runFile}'
+AccountingGroup = "group_rutgers.gomez"
Notify_User = gomez@physics.rutgers.edu
OutputDir = '${OUTPUTDIR}${SAMPLE}'/condorlog/
' >> ${condorFile}

# Appending lines to condor configuration file
for (( job = 0; job <= $JOBS; job = job+1 ))
do

echo "Output = \$(Outputdir)/${SAMPLE}__${job}_\$(Cluster)_\$(Process).stdout" >> ${condorFile}
echo "Error  = \$(Outputdir)/${SAMPLE}__${job}_\$(Cluster)_\$(Process).stderr" >>  ${condorFile}
echo "Log    = \$(Outputdir)/${SAMPLE}__${job}_\$(Cluster)_\$(Process).stdlog" >>  ${condorFile}
echo "Arguments = ${JOBS} ${job} ${INPUTDIR} ${OUTPUTDIR}${SAMPLE}/results/ ${SAMPLE}" >>  ${condorFile}
echo -e "Queue\n" >>  ${condorFile}

done

########################################################
echo 'Creating run file....'
if [ -f ${runFile} ]; then 
	rm -rf ${runFile}
fi
echo '#!/bin/sh

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
export MYRUNDIR='${RUNDIR}'

cd $MYRUNDIR
eval `scramv1 runtime -sh`
cmsRun '${RUNDIR}${CMSRUNFILE}' $1 $2 $3 $4 $5 
'>> ${runFile}
chmod a+x ${runFile}

echo 'Done. Have a nice day.'
