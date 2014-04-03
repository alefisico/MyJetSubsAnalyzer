#!/bin/bash

MAINDIR=`pwd`
BASEDIR="/cms/gomez/Substructure/Analyzer/CMSSW_5_3_12/src/"
run="MyAnalyzer.py"
condorFile='condor_MyAnalyzer.jdl'
runFile='runCondor_MyAnalyzer.jdl'
condorLogDir="/cms/gomez/Stops/st_jj/treeResults/rootFiles/condorlog/"
#jetAlgo=( AK5 AK7 CA8 )
jetAlgo=( AK4 AK5 AK7 CA4 CA8 KT4 KT8 )
mass=( 50 100 200 )
grooming=( _NOJEC Pruned Trimmed Filtered MassDropFiltered)

cd ${MAINDIR}

if [ -f ${runFile} ]; then
	rm -rf $runFile
fi
echo "#!/bin/bash

# This file sets up the bash shell for condor
# If you have additional custom enhancements to your shell 
# environment, you may need to add them here

export CUR_DIR=\$PWD

export SCRAM_ARCH=\"slc5_amd64_gcc462\"
export VO_CMS_SW_DIR=\"/cms/base/cmssoft\"
export COIN_FULL_INDIRECT_RENDERING=1
source /cms/base/cmssoft/cmsset_default.sh

# Change to your CMSSW software version
# Shown for c shell
# Also change 'username' to your username
cd ${BASEDIR}
eval \`scramv1 runtime -sh\`
date

# Switch to your working directory below
cd  \$CUR_DIR

python ${run} -f -m \$1 -j \$2 -g \$3 
" >> ${runFile}
chmod +x ${runFile}

if [ -f ${condorFile} ]; then
	rm -rf $condorFile
fi
echo "## To use condor
Universe = vanilla
initialdir = ${MAINDIR}
Executable = \$(initialdir)/${runFile}
+AccountingGroup = "group_rutgers.gomez"
Notify_User = gomez@physics.rutgers.edu

Outputdir = ${condorLogDir}
" >> ${condorFile}

numJetAlgo=${#jetAlgo[@]}
numMass=${#mass[@]}
numGromming=${#grooming[@]}

for ((i=0;i<$numMass;i++));
do
	for ((j=0;j<$numJetAlgo;j++));
	do
		for ((k=0;k<$numGromming;k++));
		do
			echo "Output = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${grooming[${k}]}.stdout" >> $condorFile
			echo "Error = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${grooming[${k}]}.stderr" >> ${condorFile}
			echo "Log = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${grooming[${k}]}.stdlog" >> ${condorFile}
			echo "Arguments = ${mass[${i}]} ${jetAlgo[${j}]} ${grooming[${k}]}" >> ${condorFile}
			echo -e "Queue\n" >> ${condorFile}
		done
	done
done

tmpRunFile='runCondor_MyAnalyzer_tmp.jdl'
if [ -f ${tmpRunFile} ]; then
	rm -rf $tmpRunFile
fi
echo "#!/bin/bash

# This file sets up the bash shell for condor
# If you have additional custom enhancements to your shell 
# environment, you may need to add them here

export CUR_DIR=\$PWD

export SCRAM_ARCH=\"slc5_amd64_gcc462\"
export VO_CMS_SW_DIR=\"/cms/base/cmssoft\"
export COIN_FULL_INDIRECT_RENDERING=1
source /cms/base/cmssoft/cmsset_default.sh

# Change to your CMSSW software version
# Shown for c shell
# Also change 'username' to your username
cd ${BASEDIR}
eval \`scramv1 runtime -sh\`
date

# Switch to your working directory below
cd  \$CUR_DIR

python ${run} -f -m \$1 -j \$2 
" >> ${tmpRunFile}
chmod +x ${tmpRunFile}

tmpCondorFile='condor_MyAnalyzer_tmp.jdl'
if [ -f ${tmpCondorFile} ]; then
	rm -rf $tmpCondorFile
fi
echo "## To use condor
Universe = vanilla
initialdir = ${MAINDIR}
Executable = \$(initialdir)/${tmpRunFile}
+AccountingGroup = "group_rutgers.gomez"
Notify_User = gomez@physics.rutgers.edu

Outputdir = ${condorLogDir}
" >> ${tmpCondorFile}

for ((i=0;i<$numMass;i++));
do
	for ((j=0;j<$numJetAlgo;j++));
	do
		echo "Output = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_.stdout" >> $tmpCondorFile
		echo "Error = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_.stderr" >> ${tmpCondorFile}
		echo "Log = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_.stdlog" >> ${tmpCondorFile}
		echo "Arguments = ${mass[${i}]} ${jetAlgo[${j}]} " >> ${tmpCondorFile}
		echo -e "Queue\n" >> ${tmpCondorFile}
	done
done

condor_submit $condorFile
condor_submit $tmpCondorFile
