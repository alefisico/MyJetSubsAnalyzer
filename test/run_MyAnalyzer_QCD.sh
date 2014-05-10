#!/bin/bash

MAINDIR=`pwd`
BASEDIR="/cms/gomez/Substructure/Analyzer/CMSSW_5_3_12/src/"
run="MyAnalyzer.py"
condorFile='condor_MyAnalyzer_QCD.jdl'
tmpCondorFile='condor_MyAnalyzer_QCD_tmp.jdl'
runFile='runCondor_MyAnalyzer_QCD.jdl'
tmpRunFile='runCondor_MyAnalyzer_QCD_tmp.jdl'
condorLogDir="/cms/gomez/Files/QCD_8TeV/treeResults/condorlog/"
jetAlgo=( CA8 AK7 KT8 )
#jetAlgo=( AK4 AK5 AK7 CA4 CA8 KT4 KT8 )
mass=( 500To1000 1000ToInf 250To500 )
grooming=( MassDropFiltered Pruned Trimmed Filtered )

#################################################
cd ${MAINDIR}

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

python ${run} -s QCD -f -q \$1 -j \$2 -g \$3 -n \$4
" >> ${runFile}
chmod +x ${runFile}

###########################################
echo " Creating condor file.... "
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
			for ((l=0;l<30;l++));
			do
				echo "Output = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${grooming[${k}]}_${l}.stdout" >> $condorFile
				echo "Error = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${grooming[${k}]}_${l}.stderr" >> ${condorFile}
				echo "Log = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${grooming[${k}]}_${l}.stdlog" >> ${condorFile}
				echo "Arguments = ${mass[${i}]} ${jetAlgo[${j}]} ${grooming[${k}]} ${l}" >> ${condorFile}
				echo -e "Queue\n" >> ${condorFile}
			done
		done
	done
done


echo " Creating run file for no grooming.... "
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

python ${run} -s QCD -f -q \$1 -j \$2 -n \$3
" >> ${tmpRunFile}
chmod +x ${tmpRunFile}

echo " Creating condor file for no grooming.... "
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
		for ((l=0;l<30;l++));
		do
			echo "Output = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${l}.stdout" >> $tmpCondorFile
			echo "Error = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${l}.stderr" >> ${tmpCondorFile}
			echo "Log = \$(Outputdir)/condorlog_${mass[${i}]}_${jetAlgo[${j}]}_${l}.stdlog" >> ${tmpCondorFile}
			echo "Arguments = ${mass[${i}]} ${jetAlgo[${j}]} ${l}" >> ${tmpCondorFile}
			echo -e "Queue\n" >> ${tmpCondorFile}
		done
	done
done

echo " Submitting jobs to condor.... "
condor_submit $condorFile
condor_submit $tmpCondorFile
echo " Have a nice day :D"
