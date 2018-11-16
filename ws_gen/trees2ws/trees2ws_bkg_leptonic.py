import pandas as pd
import numpy as np
import ROOT

from root_numpy import tree2array

from optparse import OptionParser

#BDT cut
lep_BDT_cut = 0.13

#RooRealVar names to tree variable names mapping
tree_ws_var_mapping = {
	"CMS_hgg_mass":"mgg",
        "weight":"weight_LO"
}

#Define reco bins: currently configured to ttHHad (pTH)
recobins = [
	"lep_reco0",
	"lep_reco1",
	"lep_reco2",
	"lep_reco3",
	"lep_reco4",
	"lep_reco5"
]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def add_mc_vars_to_workspace(ws=None):
  IntLumi = ROOT.RooRealVar("IntLumi","IntLumi",1000)
  IntLumi.setConstant(True)
  getattr(ws, 'import')(IntLumi)

  weight = ROOT.RooRealVar("weight","weight",1)
  weight.setConstant(False)
  getattr(ws, 'import')(weight)

  CMS_hgg_mass = ROOT.RooRealVar("CMS_hgg_mass","CMS_hgg_mass",125,100,180)
  CMS_hgg_mass.setConstant(False)
  CMS_hgg_mass.setBins(160)
  getattr(ws, 'import')(CMS_hgg_mass)

  dZ = ROOT.RooRealVar("dZ","dZ",0.0,-20,20)
  dZ.setConstant(False)
  dZ.setBins(40)
  getattr(ws, 'import')(dZ)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def apply_selection(data=None,reco_name=None):
  #function to split up ttree into recobins

  #1) Split by pT reco
  if 'reco0' in reco_name: recobin_data = data[((data['pTH_reco']>=0.)&(data['pTH_reco']<45.))]
  elif 'reco1' in reco_name: recobin_data = data[((data['pTH_reco']>=45.)&(data['pTH_reco']<80.))]
  elif 'reco2' in reco_name: recobin_data = data[((data['pTH_reco']>=80.)&(data['pTH_reco']<120.))]
  elif 'reco3' in reco_name: recobin_data = data[((data['pTH_reco']>=120.)&(data['pTH_reco']<200.))]
  elif 'reco4' in reco_name: recobin_data = data[((data['pTH_reco']>=200.)&(data['pTH_reco']<350.))]
  elif 'reco5' in reco_name: recobin_data = data[(data['pTH_reco']>=350.)]
  else:
    raise ValueError("Reco bin not recognised!")

  #2) BDT selection
  recobin_data = recobin_data[(recobin_data['BDT']>=lep_BDT_cut)]

  #only use events in mass range: 100-180 GeV
  recobin_data = recobin_data[((recobin_data['mgg']>=100.)&(recobin_data['mgg']<=180.))]
  
  #DEBUG
  print "BIN:", reco_name
  print recobin_data.head()
  print ""

  return recobin_data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def add_recobin_dataset_to_workspace(data=None,ws=None,reco_name=None):

  #apply selection to extract process (e.g.ttHgen0)  x recobin
  recobin_data = apply_selection( data, reco_name )

  #define argument set  
  arg_set = ROOT.RooArgSet(ws.var("weight"))
  arg_set.add(ws.var("CMS_hgg_mass"))
  arg_set.add(ws.var("dZ"))
  #define roodataset to add to workspace
  dataset_name = '_'.join([processID,'13TeV',reco_name])
  recobin_roodataset = ROOT.RooDataSet( dataset_name, dataset_name, arg_set, "weight" )

  #Fill the dataset with values
  for index,row in recobin_data.iterrows():
    for var in ["CMS_hgg_mass"]:
      var_tree = tree_ws_var_mapping[var]
      ws.var(var).setVal( row[ var_tree ] )
    for var in ["dZ"]:
      #to ensure only one fit (i.e. all RV fit)
      ws.var(var).setVal( 0. )
      ws.var(var).setConstant();

    #!!!!! WEIGHT *3000 REQUIRED FOR BACKGROUND MODEL
    w_val = row['weight_LO']*3000
    #FOR DIPHOTON + GJET
    #w_val = row['weight_LO']*3000*1.109704641
    recobin_roodataset.add( arg_set, w_val )

  #Add to the workspace
  getattr(ws, 'import')(recobin_roodataset)

  return [dataset_name]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
def get_options():

    parser = OptionParser()
    parser.add_option('--file_path',
                       dest='file_path',
                       default='',
                       help='')
    parser.add_option('--process_id',
                       dest='process_id',
                       default='',
                       help='')
    return parser.parse_args()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

(opt,args) = get_options()
processID = opt.process_id
tfile_path = opt.file_path

#define tfile to read from
tfile = ROOT.TFile.Open( tfile_path )
#import ttree and store as pandas dataframe
data = pd.DataFrame(tree2array(tfile.Get("trilinearTree")))

#define roo fit workspace
ws = ROOT.RooWorkspace("cms_hgg_13TeV", "cms_hgg_13TeV")
#Assemble roorealvariable set
add_mc_vars_to_workspace( ws )

#Add data set to workspace: nominal dataset (no systematics)
dataset_names = []
for recobin in recobins:
  dataset_names += add_recobin_dataset_to_workspace( data, ws, recobin )

for name in dataset_names:
  print name, " ::: Entries =", ws.data(name).numEntries(), ", SumEntries =", ws.data(name).sumEntries()

#export ws to file
f_out = ROOT.TFile.Open("ttHLep_ws/bkg_separated_3000fb/output_"+processID+"_13TeV.root","RECREATE")
dir_ws = f_out.mkdir("tagsDumper")
dir_ws.cd()
ws.Write() 
