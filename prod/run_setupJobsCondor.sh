./setupJobsCondor.sh 50 /cms/gomez/Stops/st_jj/AOD/stop_UDD312_50/
./setupJobsCondor.sh 100 /cms/gomez/Stops/st_jj/AOD/stop_UDD312_100/
./setupJobsCondor.sh 200 /cms/gomez/Stops/st_jj/AOD/stop_UDD312_200/
#./setupJobsCondor.sh stopUDD312_ISR_upto2j_50 /cms/gomez/Stops/st_jj/AOD/stop_UDD312_ISR_upto2j_50/aodsim/

#list = os.popen('ls -1 /cms/gomez/Stops/AOD/st2_h_bb_st1_jj_250_100_AOD/*.root').read().splitlines()
#list = [ '/cms/gomez/Stops/st_jj/AOD/test_QCD.root']

condor_submit condor_stopUDD312_50.jdl
condor_submit condor_stopUDD312_100.jdl
condor_submit condor_stopUDD312_200.jdl
#condor_submit condor_stopUDD312_ISR_upto2j_50.jdl
