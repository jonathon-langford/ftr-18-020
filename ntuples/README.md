#Generating ntuples

Scripts used for performing (hadronic and leptonic) pre-selection on Delphes files. Requires Delphes library, follow instructions for installation:

```
# Delphes files in eos: do following on lxplus (CERN)
# In ntuples directory, set up the CMSSW_7_4_4 environment 
export SCRAM_ARCH=slc6_amd64_gcc491
cmsrel CMSSW_7_4_4
cd CMSSW_7_4_4/src
cmsenv

# Install Delphes
git clone git@github.com:delphes/delphes.git
cd delphes
gmake
# ignore compilation errors: not unsuccessful build

# Move ntuple scripts into relevant directories
cd ${CMSSW_BASE}/src
cp -rp ../../job_* .
mv jobs_scripts/* delphes/
rmdir job_scripts
```

Now configured! In `delphes/` directory have the following scripts:

 * `tri_*_NtupleMaker_*_bacon.py`: performs pre-selection on one `.root` file: input argument. First wildcard labels hadronic or leptonic pre-selection. Second wildcard for if running on signal, background or for calc systematic uncertainty variations.
 * `tri_fiducial_NtupleMaker_bacon.py`: fiducial selection to run over ttH, THQ and THW samples. Used for calculating acceptance factors when extracting differential cross sections.
 * `tri_totalWeight_NtupleMaker_bacon.py`: determine total weight in samples (nominal, QCD scale changes)
 * `tree_merger_*.py`: merging together the ntuples from pre-selection into one .root file per process

Note the NtupleMaker scripts have the **total weight of all events in the Delphes files hardcoded**. Used for weighting by cross section. If not running over all Delphes files in folder, these will need to be changed.


