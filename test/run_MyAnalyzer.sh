#!/bin/bash

MAINDIR=`pwd`
#BASEDIR="/cms/gomez/Substructure/Analyzer/CMSSW_5_3_12/src/"
BASEDIR="/uscms_data/d3/algomez/Substructure/Analyzer/CMSSW_5_3_12/src/"
run="MyAnalyzer.py"
condorFile='condor_MyAnalyzer.jdl'
runFile='runCondor_MyAnalyzer.jdl'
#condorLogDir="/cms/gomez/Files/RPVSttojj_8TeV/treeResults/rootFiles/condorlog/"
condorLogDir=${MAINDIR}"/condorlog/"
jetAlgo=( CA8 AK7 KT8 )
#jetAlgo=( AK4 AK5 AK7 CA4 CA8 KT4 KT8 )
mass=( 100 )
job=( 0 1 2 3 4 5 6 7 8 9 )
grooming=( Pruned Trimmed FilteredN2 FilteredN3 MassDropFiltered)
#grooming=( FilteredN2  FilteredN3 )

#################################################
cd ${MAINDIR}'/condorlog'

############################################
echo " Creating run file.... "
if [ -f ${runFile} ]; then
	rm -rf $runFile
fi
echo "#!/bin/bash

# This file sets up the bash shell for condor
# If you have additional custom enhancements to your shell 
# environment, you may need to add them here

export CUR_DIR=\$PWD

export SCRAM_ARCH=\"slc5_amd64_gcc462\"
export COIN_FULL_INDIRECT_RENDERING=1
source /uscmst1/prod/sw/cms/setup/shrc prod

#export LC_ALL=\"en_US.UTF-8\"
#export SCRAM_ARCH=\"slc5_amd64_gcc462\"
#export COIN_FULL_INDIRECT_RENDERING=1
#source /uscmst1/prod/sw/cms/setup/shrc prod

# Change to your CMSSW software version
# Shown for c shell
# Also change 'username' to your username
cd ${BASEDIR}
eval \`scramv1 runtime -sh\`
date

# Switch to your working directory below
cd ${MAINDIR}

python ${run} -w -s Signal -f -m \$1 -j \$2 -g \$3 -n \$4 
" >> ${runFile}
chmod +x ${runFile}

###########################################
echo " Creating condor file.... "
if [ -f ${condorFile} ]; then
	rm -rf $condorFile
fi
echo "## To use condor
Universe = vanilla
initialdir = ${condorLogDir}
Executable = \$(initialdir)/${runFile}
Requirements = Memory >= 199 &&OpSys == \"LINUX\"&& (Arch != \"DUMMY\" )&& Disk > 1000000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Notify_User = gomez@physics.rutgers.edu

Outputdir = ${condorLogDir}
" >> ${condorFile}

numJetAlgo=${#jetAlgo[@]}
numMass=${#mass[@]}
numJob=${#job[@]}
numGromming=${#grooming[@]}

for ((i=0;i<$numMass;i++));
do
	for ((j=0;j<$numJetAlgo;j++));
	do
		for ((k=0;k<$numGromming;k++));
		do
			for ((l=0;l<$numJob;l++));
			do
				echo "Output = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${grooming[${k}]}_${job[${l}]}.stdout" >> $condorFile
				echo "Error = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${grooming[${k}]}_${job[${l}]}.stderr" >> ${condorFile}
				echo "Log = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${grooming[${k}]}_${job[${l}]}.stdlog" >> ${condorFile}
				echo "Arguments = ${mass[${i}]} ${jetAlgo[${j}]} ${grooming[${k}]} ${job[${l}]}" >> ${condorFile}
				echo -e "Queue\n" >> ${condorFile}
			done
		done
	done
done


echo " Creating run file for no grooming.... "
tmpRunFile='runCondor_MyAnalyzer_tmp.jdl'
if [ -f ${tmpRunFile} ]; then
	rm -rf $tmpRunFile
fi
echo "#!/bin/bash

# This file sets up the bash shell for condor
# If you have additional custom enhancements to your shell 
# environment, you may need to add them here

export CUR_DIR=\$PWD

export LC_ALL=\"en_US.UTF-8\"
export SCRAM_ARCH=\"slc5_amd64_gcc462\"
export COIN_FULL_INDIRECT_RENDERING=1
source /uscmst1/prod/sw/cms/setup/shrc prod

# Change to your CMSSW software version
# Shown for c shell
# Also change 'username' to your username
cd ${BASEDIR}
eval \`scramv1 runtime -sh\`
date

# Switch to your working directory below
cd ${MAINDIR}

python ${run} -w -s Signal -f -m \$1 -j \$2 -n \$3 
" >> ${tmpRunFile}
chmod +x ${tmpRunFile}

echo " Creating condor file for no grooming.... "
tmpCondorFile='condor_MyAnalyzer_tmp.jdl'
if [ -f ${tmpCondorFile} ]; then
	rm -rf $tmpCondorFile
fi
echo "## To use condor
Universe = vanilla
initialdir = ${condorLogDir}
Executable = \$(initialdir)/${tmpRunFile}
Requirements = Memory >= 199 &&OpSys == \"LINUX\"&& (Arch != \"DUMMY\" )&& Disk > 1000000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Notify_User = gomez@physics.rutgers.edu

Outputdir = ${condorLogDir}
" >> ${tmpCondorFile}

for ((i=0;i<$numMass;i++));
do
	for ((j=0;j<$numJetAlgo;j++));
	do
		for ((l=0;l<$numJob;l++));
		do
			echo "Output = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${job[${l}]}.stdout" >> $tmpCondorFile
			echo "Error = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${job[${l}]}.stderr" >> ${tmpCondorFile}
			echo "Log = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${job[${l}]}.stdlog" >> ${tmpCondorFile}
			echo "Arguments = ${mass[${i}]} ${jetAlgo[${j}]} ${job[${l}]}" >> ${tmpCondorFile}
			echo -e "Queue\n" >> ${tmpCondorFile}
		done
	done
done

echo " Submitting jobs to condor.... "
condor_submit $condorFile
condor_submit $tmpCondorFile
echo " Have a nice day :D"
