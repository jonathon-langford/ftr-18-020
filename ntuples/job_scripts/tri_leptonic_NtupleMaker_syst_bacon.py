#!/usr/bin/env python

# Author: Jonathon Langford
#         Imperial College London
#         CMS, Hgg IC group

# Description: To perform trilinear analysis on ttHHadronic tagged events for signal samples
###############################################################################
#	PRELIMINARIES

#Import Libraries
import sys
import ROOT
import math
from array import array
from optparse import OptionParser

#Define efficiecny and uncertainty dict for btagging systematic
eff_dict = {0:[0.000,1.500,20.000,30.000],1:[0.000,1.500,30.000,40.000],2:[0.000,1.500,40.000,50.000],3:[0.000,1.500,50.000,60.000],4:[0.000,1.500,60.000,70.000],5:[0.000,1.500,70.000,80.000],6:[0.000,1.500,80.000,90.000],7:[0.000,1.500,90.000,100.000],8:[0.000,1.500,100.000,120.000],9:[0.000,1.500,120.000,140.000],10:[0.000,1.500,140.000,160.000],11:[0.000,1.500,160.000,180.000],12:[0.000,1.500,180.000,200.000],13:[0.000,1.500,200.000,250.000],14:[0.000,1.500,250.000,300.000],15:[0.000,1.500,300.000,350.000],16:[0.000,1.500,350.000,400.000],17:[0.000,1.500,400.000,500.000],18:[0.000,1.500,500.000,600.000],19:[0.000,1.500,600.000,700.000],20:[0.000,1.500,700.000,800.000],21:[0.000,1.500,800.000,1000.000],22:[0.000,1.500,1000.000,1400.000],23:[0.000,1.500,1400.000,2000.000],24:[0.000,1.500,2000.000,3000.000],25:[0.000,1.500,3000.000,99999999.000],26:[1.500,2.500,20.000,30.000],27:[1.500,2.500,30.000,40.000],28:[1.500,2.500,40.000,50.000],29:[1.500,2.500,50.000,60.000],30:[1.500,2.500,60.000,70.000],31:[1.500,2.500,70.000,80.000],32:[1.500,2.500,80.000,90.000],33:[1.500,2.500,90.000,100.000],34:[1.500,2.500,100.000,120.000],35:[1.500,2.500,120.000,140.000],36:[1.500,2.500,140.000,160.000],37:[1.500,2.500,160.000,180.000],38:[1.500,2.500,180.000,200.000],39:[1.500,2.500,200.000,250.000],40:[1.500,2.500,250.000,300.000],41:[1.500,2.500,300.000,350.000],42:[1.500,2.500,350.000,400.000],43:[1.500,2.500,400.000,500.000],44:[1.500,2.500,500.000,600.000],45:[1.500,2.500,600.000,700.000],46:[1.500,2.500,700.000,800.000],47:[1.500,2.500,800.000,1000.000],48:[1.500,2.500,1000.000,1400.000],49:[1.500,2.500,1400.000,2000.000],50:[1.500,2.500,2000.000,3000.000],51:[1.500,2.500,3000.000,99999999.000],52:[2.500,3.500,20.000,30.000],53:[2.500,3.500,30.000,40.000],54:[2.500,3.500,40.000,50.000],55:[2.500,3.500,50.000,60.000],56:[2.500,3.500,60.000,70.000],57:[2.500,3.500,70.000,80.000],58:[2.500,3.500,80.000,90.000],59:[2.500,3.500,90.000,100.000],60:[2.500,3.500,100.000,120.000],61:[2.500,3.500,120.000,140.000],62:[2.500,3.500,140.000,160.000],63:[2.500,3.500,160.000,180.000],64:[2.500,3.500,180.000,200.000],65:[2.500,3.500,200.000,250.000],66:[2.500,3.500,250.000,300.000],67:[2.500,3.500,300.000,350.000],68:[2.500,3.500,350.000,400.000],69:[2.500,3.500,400.000,500.000],70:[2.500,3.500,500.000,600.000],71:[2.500,3.500,600.000,700.000],72:[2.500,3.500,700.000,800.000],73:[2.500,3.500,800.000,1000.000],74:[2.500,3.500,1000.000,1400.000],75:[2.500,3.500,1400.000,2000.000],76:[2.500,3.500,2000.000,3000.000],77:[2.500,3.500,3000.000,99999999.000]}

eff_list = [0.6880,0.7430,0.7680,0.7800,0.7870,0.7900,0.7890,0.7920,0.7860,0.7800,0.7730,0.7660,0.7550,0.7390,0.7110,0.6900,0.6610,0.6310,0.6000,0.5540,0.5370,0.4880,0.4490,0.4060,0.3680,0.3680,0.5720,0.6570,0.6950,0.7100,0.7120,0.7130,0.7070,0.7030,0.6940,0.6790,0.6640,0.6400,0.6270,0.6040,0.5640,0.5440,0.5300,0.5090,0.4690,0.4430,0.4210,0.3890,0.3890,0.3890,0.3890,0.3890,0.3820,0.4680,0.5030,0.5150,0.5200,0.5190,0.5190,0.5140,0.5020,0.4950,0.4750,0.4790,0.4520,0.4490,0.4030,0.3990,0.3710,0.3990,0.3990,0.3990,0.3990,0.3990,0.3990,0.3990,0.3990,0.3990]

sigma_dict = {0:[20.,30.],1:[30.,50.],2:[50.,70.],3:[70.,100.],4:[100.,140.],5:[140.,200.],6:[200.,300.],7:[300.,600.],8:[600.,1000.],9:[1000.,3000.],10:[3000.,9999999999.]}
sigma_list = [0.017, 0.01, 0.01, 0.01, 0.01, 0.01, 0.016, 0.018, 0.023, 0.046, 0.08]

#for JES: define mapping of pT bin to uncertainty
JES_dict = {0:[15.00,15.20],1:[15.20,15.61],2:[15.61,16.03],3:[16.03,16.46],4:[16.46,16.90],5:[16.90,17.35],6:[17.35,17.82],7:[17.82,18.30],8:[18.30,18.79],9:[18.79,19.29],10:[19.29,19.81],11:[19.81,20.34],12:[20.34,20.89],13:[20.89,21.45],14:[21.45,22.03],15:[22.03,22.62],16:[22.62,23.23],17:[23.23,23.85],18:[23.85,24.49],19:[24.49,25.15],20:[25.15,25.82],21:[25.82,26.51],22:[26.51,27.23],23:[27.23,27.96],24:[27.96,28.71],25:[28.71,29.48],26:[29.48,30.27],27:[30.27,31.08],28:[31.08,31.92],29:[31.92,32.77],30:[32.77,33.65],31:[33.65,34.56],32:[34.56,35.49],33:[35.49,36.44],34:[36.44,37.42],35:[37.42,38.42],36:[38.42,39.45],37:[39.45,40.51],38:[40.51,41.60],39:[41.60,42.72],40:[42.72,43.86],41:[43.86,45.04],42:[45.04,46.25],43:[46.25,47.49],44:[47.49,48.77],45:[48.77,50.07],46:[50.07,51.42],47:[51.42,52.80],48:[52.80,54.22],49:[54.22,55.67],50:[55.67,57.17],51:[57.17,58.70],52:[58.70,60.28],53:[60.28,61.89],54:[61.89,63.56],55:[63.56,65.26],56:[65.26,67.01],57:[67.01,68.81],58:[68.81,70.66],59:[70.66,72.56],60:[72.56,74.51],61:[74.51,76.51],62:[76.51,78.56],63:[78.56,80.67],64:[80.67,82.83],65:[82.83,85.06],66:[85.06,87.34],67:[87.34,89.69],68:[89.69,92.09],69:[92.09,94.57],70:[94.57,97.11],71:[97.11,99.71],72:[99.71,102.39],73:[102.39,105.14],74:[105.14,107.96],75:[107.96,110.86],76:[110.86,113.83],77:[113.83,116.89],78:[116.89,120.03],79:[120.03,123.25],80:[123.25,126.56],81:[126.56,129.96],82:[129.96,133.45],83:[133.45,137.03],84:[137.03,140.71],85:[140.71,144.48],86:[144.48,148.36],87:[148.36,152.35],88:[152.35,156.44],89:[156.44,160.64],90:[160.64,164.95],91:[164.95,169.38],92:[169.38,173.92],93:[173.92,178.59],94:[178.59,183.39],95:[183.39,188.31],96:[188.31,193.36],97:[193.36,198.56],98:[198.56,203.89],99:[203.89,209.36],100:[209.36,214.98],101:[214.98,220.75],102:[220.75,226.68],103:[226.68,232.76],104:[232.76,239.01],105:[239.01,245.43],106:[245.43,252.02],107:[252.02,258.78],108:[258.78,265.73],109:[265.73,272.86],110:[272.86,280.19],111:[280.19,287.71],112:[287.71,295.43],113:[295.43,303.36],114:[303.36,311.51],115:[311.51,319.87],116:[319.87,328.46],117:[328.46,337.28],118:[337.28,346.33],119:[346.33,355.63],120:[355.63,365.17],121:[365.17,374.98],122:[374.98,385.04],123:[385.04,395.38],124:[395.38,405.99],125:[405.99,416.89],126:[416.89,428.09],127:[428.09,439.58],128:[439.58,451.38],129:[451.38,463.50],130:[463.50,475.94],131:[475.94,488.72],132:[488.72,501.84],133:[501.84,515.31],134:[515.31,529.14],135:[529.14,543.35],136:[543.35,557.93],137:[557.93,572.91],138:[572.91,588.29],139:[588.29,604.08],140:[604.08,620.30],141:[620.30,636.95],142:[636.95,654.05],143:[654.05,671.61],144:[671.61,689.64],145:[689.64,708.16],146:[708.16,727.17],147:[727.17,746.69],148:[746.69,766.73],149:[766.73,787.32],150:[787.32,808.45],151:[808.45,830.16],152:[830.16,852.44],153:[852.44,875.33],154:[875.33,898.82],155:[898.82,922.95],156:[922.95,947.73],157:[947.73,973.17],158:[973.17,999.30],159:[999.30,1026.13],160:[1026.13,1053.67],161:[1053.67,1081.96],162:[1081.96,1111.01],163:[1111.01,1140.83],164:[1140.83,1171.46],165:[1171.46,1202.91],166:[1202.91,1235.20],167:[1235.20,1268.36],168:[1268.36,1302.41],169:[1302.41,1337.37],170:[1337.37,1373.27],171:[1373.27,1410.14],172:[1410.14,1448.00],173:[1448.00,1486.87],174:[1486.87,1526.79],175:[1526.79,1567.77],176:[1567.77,1609.86],177:[1609.86,1653.08],178:[1653.08,1697.46],179:[1697.46,1743.03],180:[1743.03,1789.82],181:[1789.82,1837.87],182:[1837.87,1887.21],183:[1887.21,1937.87],184:[1937.87,1989.89],185:[1989.89,2043.31],186:[2043.31,2098.17],187:[2098.17,2154.49],188:[2154.49,2212.33],189:[2212.33,2271.72],190:[2271.72,2332.71],191:[2332.71,2395.33],192:[2395.33,2459.64],193:[2459.64,2525.67],194:[2525.67,2593.47],195:[2593.47,2663.09],196:[2663.09,2734.58],197:[2734.58,2808.00],198:[2808.00,2883.38],199:[2883.38,2960.78],200:[2960.78,3000.00]}

JES_unc_lightjets = {0:0.0352,1:0.0346,2:0.0341,3:0.0336,4:0.0332,5:0.0326,6:0.0318,7:0.0310,8:0.0302,9:0.0294,10:0.0286,11:0.0278,12:0.0270,13:0.0263,14:0.0255,15:0.0247,16:0.0239,17:0.0231,18:0.0223,19:0.0216,20:0.0208,21:0.0201,22:0.0194,23:0.0188,24:0.0182,25:0.0177,26:0.0172,27:0.0167,28:0.0162,29:0.0158,30:0.0153,31:0.0149,32:0.0145,33:0.0141,34:0.0136,35:0.0132,36:0.0128,37:0.0124,38:0.0121,39:0.0117,40:0.0114,41:0.0110,42:0.0107,43:0.0104,44:0.0101,45:0.0098,46:0.0095,47:0.0093,48:0.0091,49:0.0089,50:0.0087,51:0.0085,52:0.0083,53:0.0081,54:0.0079,55:0.0077,56:0.0076,57:0.0074,58:0.0072,59:0.0071,60:0.0069,61:0.0068,62:0.0067,63:0.0065,64:0.0064,65:0.0062,66:0.0061,67:0.0059,68:0.0058,69:0.0057,70:0.0056,71:0.0055,72:0.0054,73:0.0053,74:0.0052,75:0.0051,76:0.0050,77:0.0049,78:0.0048,79:0.0048,80:0.0047,81:0.0046,82:0.0045,83:0.0045,84:0.0044,85:0.0044,86:0.0043,87:0.0043,88:0.0042,89:0.0042,90:0.0042,91:0.0042,92:0.0042,93:0.0042,94:0.0042,95:0.0042,96:0.0042,97:0.0042,98:0.0042,99:0.0043,100:0.0043,101:0.0043,102:0.0043,103:0.0044,104:0.0044,105:0.0044,106:0.0045,107:0.0045,108:0.0045,109:0.0045,110:0.0045,111:0.0045,112:0.0045,113:0.0045,114:0.0045,115:0.0044,116:0.0044,117:0.0044,118:0.0044,119:0.0044,120:0.0044,121:0.0044,122:0.0044,123:0.0044,124:0.0044,125:0.0044,126:0.0044,127:0.0044,128:0.0044,129:0.0045,130:0.0045,131:0.0045,132:0.0045,133:0.0045,134:0.0046,135:0.0046,136:0.0046,137:0.0046,138:0.0047,139:0.0047,140:0.0047,141:0.0048,142:0.0048,143:0.0048,144:0.0049,145:0.0049,146:0.0050,147:0.0051,148:0.0051,149:0.0052,150:0.0052,151:0.0053,152:0.0053,153:0.0054,154:0.0054,155:0.0055,156:0.0055,157:0.0056,158:0.0056,159:0.0057,160:0.0057,161:0.0058,162:0.0058,163:0.0059,164:0.0059,165:0.0059,166:0.0060,167:0.0060,168:0.0061,169:0.0061,170:0.0062,171:0.0062,172:0.0063,173:0.0063,174:0.0064,175:0.0064,176:0.0064,177:0.0065,178:0.0065,179:0.0066,180:0.0066,181:0.0067,182:0.0067,183:0.0067,184:0.0068,185:0.0068,186:0.0068,187:0.0068,188:0.0068,189:0.0068,190:0.0068,191:0.0068,192:0.0068,193:0.0068,194:0.0068,195:0.0068,196:0.0068,197:0.0068,198:0.0068,199:0.0068,200:0.0068}

JES_unc_bjets = {0:0.0346,1:0.0341,2:0.0336,3:0.0331,4:0.0326,5:0.0320,6:0.0312,7:0.0304,8:0.0296,9:0.0288,10:0.0280,11:0.0272,12:0.0264,13:0.0256,14:0.0248,15:0.0240,16:0.0232,17:0.0224,18:0.0216,19:0.0208,20:0.0200,21:0.0193,22:0.0186,23:0.0180,24:0.0174,25:0.0169,26:0.0163,27:0.0158,28:0.0153,29:0.0148,30:0.0144,31:0.0139,32:0.0135,33:0.0130,34:0.0126,35:0.0123,36:0.0119,37:0.0115,38:0.0112,39:0.0108,40:0.0105,41:0.0102,42:0.0100,43:0.0097,44:0.0094,45:0.0092,46:0.0089,47:0.0087,48:0.0084,49:0.0082,50:0.0080,51:0.0078,52:0.0076,53:0.0074,54:0.0072,55:0.0070,56:0.0069,57:0.0067,58:0.0065,59:0.0064,60:0.0062,61:0.0061,62:0.0060,63:0.0059,64:0.0058,65:0.0057,66:0.0056,67:0.0055,68:0.0054,69:0.0053,70:0.0052,71:0.0051,72:0.0050,73:0.0049,74:0.0048,75:0.0047,76:0.0046,77:0.0045,78:0.0045,79:0.0044,80:0.0043,81:0.0042,82:0.0042,83:0.0041,84:0.0041,85:0.0040,86:0.0040,87:0.0040,88:0.0039,89:0.0039,90:0.0039,91:0.0039,92:0.0039,93:0.0039,94:0.0039,95:0.0040,96:0.0040,97:0.0040,98:0.0041,99:0.0041,100:0.0042,101:0.0042,102:0.0043,103:0.0043,104:0.0043,105:0.0044,106:0.0044,107:0.0044,108:0.0044,109:0.0045,110:0.0045,111:0.0045,112:0.0045,113:0.0045,114:0.0045,115:0.0044,116:0.0044,117:0.0044,118:0.0044,119:0.0044,120:0.0044,121:0.0044,122:0.0044,123:0.0044,124:0.0044,125:0.0044,126:0.0044,127:0.0044,128:0.0044,129:0.0045,130:0.0045,131:0.0045,132:0.0045,133:0.0045,134:0.0045,135:0.0045,136:0.0046,137:0.0046,138:0.0046,139:0.0046,140:0.0047,141:0.0047,142:0.0048,143:0.0048,144:0.0049,145:0.0049,146:0.0050,147:0.0050,148:0.0051,149:0.0051,150:0.0052,151:0.0052,152:0.0053,153:0.0053,154:0.0054,155:0.0054,156:0.0055,157:0.0055,158:0.0055,159:0.0056,160:0.0056,161:0.0057,162:0.0057,163:0.0057,164:0.0058,165:0.0058,166:0.0059,167:0.0059,168:0.0059,169:0.0060,170:0.0060,171:0.0061,172:0.0061,173:0.0062,174:0.0062,175:0.0063,176:0.0063,177:0.0064,178:0.0064,179:0.0065,180:0.0065,181:0.0065,182:0.0066,183:0.0066,184:0.0066,185:0.0067,186:0.0067,187:0.0067,188:0.0067,189:0.0067,190:0.0067,191:0.0067,192:0.0067,193:0.0067,194:0.0067,195:0.0067,196:0.0067,197:0.0067,198:0.0067,199:0.0067,200:0.0067}

def get_options():
  parser = OptionParser()
  parser = OptionParser( usage="usage: python %prog [input file] [signal type]" )
  parser.add_option("-i", "--inp", dest="input_file", default='', help="Input file to analyse")
  parser.add_option("-s", "--signal", dest="signal", default='ttH', help="Define which signal process running over, for correct XS")
  parser.add_option("-u","--systematic", dest="systematic", default='JES', help="Define which systematic uncertainty")
  parser.add_option("-d","--direction",dest="direction", default='up',help="[UP/DOWN]")
  return parser.parse_args()

(opt,args) = get_options()
f_input = opt.input_file
signal_type = opt.signal
syst_type = opt.systematic
syst_direction = opt.direction

#Extract number from output file: remove ".root" 
f_split = f_input.split("_")
nOut = "ERROR"
if( f_split[-2].isdigit() ):
  nOut = f_split[-2] + "_" + f_split[-1][:-5]
else:
  nOut = f_split[-1][:-5]

#Load delphes ROOT libraries
ROOT.gSystem.Load("libDelphes")

#Including packages to read TTree
try:
  ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass

# Create chain of root trees
chain = ROOT.TChain("Delphes")
chain.Add( f_input )

# Create objects of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()
#numberOfEntries = 100

# Get pointers to branches used in this analysis
branchEvent = treeReader.UseBranch("Event")
branchWeight = treeReader.UseBranch("Weight")
branchGenParticle = treeReader.UseBranch("Particle")
branchPhoton =  treeReader.UseBranch("PhotonTight")
branchElectron = treeReader.UseBranch("Electron")
branchMuon = treeReader.UseBranch("MuonTight")
branchJet = treeReader.UseBranch("JetPUPPI")
branchMET = treeReader.UseBranch("PuppiMissingET")
branchScalarHT = treeReader.UseBranch("ScalarHT")

#Define cross sections [fb] for various processes and uncomment required one
#also calc total weight (check == numberOfEntries)
if( signal_type == "ttH" ):
  if( syst_type == 'QCDscale_inc' ):
    if( syst_direction == 'up' ): Xsection = 1.477
    else: Xsection = 1.279
  elif( syst_type == 'PDF_inc' ):
    if( syst_direction == 'up' ): Xsection = 1.408
    else: Xsection = 1.378
  else: Xsection = 1.393
  #CHange total weight if looking for renormShape/factorShape
  if( syst_type == 'renormShape' ):
    if( syst_direction == 'up' ): totalWeight = 50162.28
    else: totalWeight = 86877.5488
  elif( syst_type == 'factorShape' ):
    if( syst_direction == 'up' ): totalWeight = 60388.3448
    else: totalWeight = 63037.2652
  else: totalWeight = 61505.9956

elif( signal_type == "ggH" ):
  Xsection = 124.1
  totalWeight = 85889211
  print "ggH: totalWeight = 85889211 (Mean x entries)"

elif( signal_type == "THQ" ):
  if( syst_type == 'QCDscale_inc' ):
    if( syst_direction == 'up' ): Xsection = 0.226
    else: Xsection = 0.181
  elif( syst_type == 'PDF_inc' ):
    if( syst_direction == 'up' ): Xsection = 0.219
    else: Xsection = 0.205
  else: Xsection = 0.212
  #CHange total weight if looking for renormShape/factorShape
  if( syst_type == 'renormShape' ):
    if( syst_direction == 'up' ): totalWeight = 1674103.283
    else: totalWeight = 2152176.417
  elif( syst_type == 'factorShape' ):
    if( syst_direction == 'up' ): totalWeight = 1745842.297
    else: totalWeight = 2037318.358
  #BUGGED: FILE_38 server error
  else: totalWeight = 1882919
  #print "THQ: totalWeight = 1906318 (Mean x Entries)"  

elif( signal_type == "THW" ):
  if( syst_type == 'QCDscale_inc' ):
    if( syst_direction == 'up' ): Xsection = 0.0442
    else: Xsection = 0.0392
  elif( syst_type == 'PDF_inc' ):
    if( syst_direction == 'up' ): Xsection = 0.0446
    else: Xsection = 0.0396
  else: Xsection = 0.0421
  #CHange total weight if looking for renormShape/factorShape
  if( syst_type == 'renormShape' ):
    if( syst_direction == 'up' ): totalWeight = 691518.3
    else: totalWeight = 891955
  elif( syst_type == 'factorShape' ):
    if( syst_direction == 'up' ): totalWeight = 818729
    else: totalWeight = 687311.7
  #BUGGED: FILE_6 server error
  else: totalWeight = 779000

elif( signal_type == "VH" ):
  Xsection = 5.660
  totalWeight = 7937535.474
  print "VH: totalWeight = 7937535.474 (Mean x Entries)"
##############################################################################
#	CONFIGURE OUTPUT

print "Configuring output Ntuple..."
# Initialise TTree and open files to write to
#Main variables
pTH_gen_v = array( 'f', [-1.] )
pTH_reco_v = array( 'f', [-1.] )
mgg_v = array( 'f', [-1.] )
LO_w = array( 'f', [-1.] )
#Reco photon variables
pho1_pT = array( 'f', [-1.] )
pho1_eta = array( 'f', [-1.] )
pho1_phi = array( 'f', [-1.] )
pho1_E = array( 'f', [-1.] )
pho1_IsolationVar = array( 'f', [-1.] )
pho2_pT = array( 'f', [-1.] )
pho2_eta = array( 'f', [-1.] )
pho2_phi = array( 'f', [-1.] )
pho2_E = array( 'f', [-1.] )
pho2_IsolationVar = array( 'f', [-1.] )
#Gen photon variables
pho1_gen_pT = array( 'f', [-1.] )
pho1_gen_eta = array( 'f', [-1.] )
pho1_gen_phi = array( 'f', [-1.] )
pho1_gen_E = array( 'f', [-1.] )
pho2_gen_pT = array( 'f', [-1.] )
pho2_gen_eta = array( 'f', [-1.] )
pho2_gen_phi = array( 'f', [-1.] )
pho2_gen_E = array( 'f', [-1.] )
#First six jets info
jet1_pT = array( 'f', [-1.] )
jet1_eta = array( 'f', [-1.] )
jet1_phi = array( 'f', [-1.] )
jet1_mass = array( 'f', [-1.] )
jet1_btag = array( 'i', [-1] )
jet2_pT = array( 'f', [-1.] )
jet2_eta = array( 'f', [-1.] )
jet2_phi = array( 'f', [-1.] )
jet2_mass = array( 'f', [-1.] )
jet2_btag = array( 'i', [-1] )
jet3_pT = array( 'f', [-1.] )
jet3_eta = array( 'f', [-1.] )
jet3_phi = array( 'f', [-1.] )
jet3_mass = array( 'f', [-1.] )
jet3_btag = array( 'i', [-1] )
#Global jet variables
Njets = array( 'i', [0] )
Nbjets = array( 'i', [0] )
#Lepton variables
Nleptons = array( 'i', [0] )
lep_pT = array( 'f', [-1.] )
lep_eta = array( 'f', [-1.] )
lep_phi = array( 'f', [-1.] )
#Other
MET = array( 'f', [-1.] )
MET_eta = array( 'f', [-1.] )
MET_phi = array( 'f', [-1.] )
scalarHT = array( 'f', [-1.] )

#Save one tree, can split into different gen pT trees later
#if( signal_type == "ttH" ): filename = "ttHHad_tri_ntuples/ttHHad_signal_ttH_M125.root"
if( signal_type == "ttH" ): filename = "ttHLep_tri_ntuples_syst/" + syst_type + "/ttH/ttH_" + nOut  + "_" + syst_direction +".root"
elif( signal_type == "ggH" ): filename = "ttHLep_tri_ntuples_syst/" + syst_type + "/ggH/ggH_" + nOut  + "_" + syst_direction +".root"
elif( signal_type == "THQ" ): filename = "ttHLep_tri_ntuples_syst/" + syst_type + "/THQ/THQ_" + nOut  + "_" + syst_direction + ".root"
elif( signal_type == "THW" ): filename = "ttHLep_tri_ntuples_syst/" + syst_type + "/THW/THW_" + nOut  + "_" + syst_direction + ".root"
elif( signal_type == "VH" ): filename = "ttHLep_tri_ntuples_syst/" + syst_type + "/VH/VH_" + nOut  + "_" + syst_direction + ".root"

f_0 = ROOT.TFile.Open( filename ,"RECREATE")
tree_0 = ROOT.TTree("trilinearTree","trilinearTree")

tree_0.Branch("pTH_gen", pTH_gen_v, 'pTH_gen/F')
tree_0.Branch("pTH_reco", pTH_reco_v, 'pTH_reco/F')
tree_0.Branch("mgg", mgg_v, 'mgg/F')
tree_0.Branch("weight_LO", LO_w, 'weight_LO/F')
#Reco photon info
tree_0.Branch("pho1_pT", pho1_pT, 'pho1_pT/F')
tree_0.Branch("pho1_eta", pho1_eta, 'pho1_eta/F')
tree_0.Branch("pho1_phi", pho1_phi, 'pho1_phi/F')
tree_0.Branch("pho1_E", pho1_E, 'pho1_E/F')
tree_0.Branch("pho1_IsolationVar", pho1_IsolationVar, 'pho1_IsolationVar/F')
tree_0.Branch("pho2_pT", pho2_pT, 'pho2_pT/F')
tree_0.Branch("pho2_eta", pho2_eta, 'pho2_eta/F')
tree_0.Branch("pho2_phi", pho2_phi, 'pho2_phi/F')
tree_0.Branch("pho2_E", pho2_E, 'pho2_E/F')
tree_0.Branch("pho2_IsolationVar", pho2_IsolationVar, 'pho2_IsolationVar/F')
#Gen photon info
tree_0.Branch("pho1_gen_pT", pho1_gen_pT, 'pho1_gen_pT/F')
tree_0.Branch("pho1_gen_eta", pho1_gen_eta, 'pho1_gen_eta/F')
tree_0.Branch("pho1_gen_phi", pho1_gen_phi, 'pho1_gen_phi/F')
tree_0.Branch("pho1_gen_E", pho1_gen_E, 'pho1_gen_E/F')
tree_0.Branch("pho2_gen_pT", pho2_gen_pT, 'pho2_gen_pT/F')
tree_0.Branch("pho2_gen_eta", pho2_gen_eta, 'pho2_gen_eta/F')
tree_0.Branch("pho2_gen_phi", pho2_gen_phi, 'pho2_gen_phi/F')
tree_0.Branch("pho2_gen_E", pho2_gen_E, 'pho2_gen_E/F')
#First six jet into
tree_0.Branch("jet1_pT", jet1_pT, 'jet1_pT/F')
tree_0.Branch("jet1_eta", jet1_eta, 'jet1_eta/F')
tree_0.Branch("jet1_phi", jet1_phi, 'jet1_phi/F')
tree_0.Branch("jet1_mass", jet1_mass, 'jet1_mass/F')
tree_0.Branch("jet1_btag", jet1_btag, 'jet1_btag/I')
tree_0.Branch("jet2_pT", jet2_pT, 'jet2_pT/F')
tree_0.Branch("jet2_eta", jet2_eta, 'jet2_eta/F')
tree_0.Branch("jet2_phi", jet2_phi, 'jet2_phi/F')
tree_0.Branch("jet2_mass", jet2_mass, 'jet2_mass/F')
tree_0.Branch("jet2_btag", jet2_btag, 'jet2_btag/I')
tree_0.Branch("jet3_pT", jet3_pT, 'jet3_pT/F')
tree_0.Branch("jet3_eta", jet3_eta, 'jet3_eta/F')
tree_0.Branch("jet3_phi", jet3_phi, 'jet3_phi/F')
tree_0.Branch("jet3_mass", jet3_mass, 'jet3_mass/F')
tree_0.Branch("jet3_btag", jet3_btag, 'jet3_btag/I')
#Global jet variables
tree_0.Branch("Njets", Njets, 'Njets/I')
tree_0.Branch("Nbjets", Nbjets, 'Nbjets/I')
#Lepton Variables
tree_0.Branch("Nleptons", Nleptons, 'Nleptons/I')
tree_0.Branch("lep_pT", lep_pT, 'lep_pT/F')
tree_0.Branch("lep_eta", lep_eta, 'lep_eta/F')
tree_0.Branch("lep_phi", lep_phi, 'lep_phi/F')
#Other
tree_0.Branch("MET", MET, 'MET/F')
tree_0.Branch("MET_eta", MET_eta, 'MET_eta/F')
tree_0.Branch("MET_phi", MET_phi, 'MET_phi/F')
tree_0.Branch("scalarHT", scalarHT, 'scalarHT/F')

######################################################################
#	FUNCTIONS FOR KINEMATICS

def deltaR( eta1, phi1, eta2, phi2 ):
  return math.sqrt( (eta1-eta2)*(eta1-eta2) + (phi1-phi2)*(phi1-phi2) )

def pT_vector_calc( part1, part2 ):
  Px1 = part1.PT*math.cos( part1.Phi )
  Px2 = part2.PT*math.cos( part2.Phi )
  Py1 = part1.PT*math.sin( part1.Phi )
  Py2 = part2.PT*math.sin( part2.Phi )
  return math.sqrt( (Px1+Px2)*(Px1+Px2) + (Py1+Py2)*(Py1+Py2) )

def JetPermutationEtaCalc( bjet, ljet1, ljet2 ):
  q_perm = bjet.P4()+ljet1.P4()+ljet2.P4()
  return q_perm.Eta()

def JetPermutationPhiCalc( bjet, ljet1, ljet2 ):
  q_perm = bjet.P4()+ljet1.P4()+ljet2.P4()
  return q_perm.Phi()

###############################################################################
#	FUNCTIONS FOR EVENT SELECTION

def SelectPhoton( _photon, photonPtThreshold, photonEtaThresholds, phoIsoChRelThreshold ):
  photon_pass = True
  if( _photon.PT < photonPtThreshold ): photon_pass = False
  #Eta: inc outside transition region between barrel and endcap 
  if( ( abs( _photon.Eta ) > photonEtaThresholds[2] ) | ( ( abs( _photon.Eta ) > photonEtaThresholds[0] ) & ( abs( _photon.Eta ) < photonEtaThresholds[1] ) ) ): photon_pass = False
  #Isolation: currently only using Ich, need Ipho and Itrk
  if( (_photon.SumPtCharged/_photon.PT) > phoIsoChRelThreshold ): photon_pass = False
  #SHOWER SHAPE VARIABLES: R9, sigma_etaeta, need to access from Delphes in some way

  return photon_pass


def SelectDiPhoton( _leadPhoton, _subleadPhoton, leadPhoPTOverMassThreshold, subleadPhoPTOverMassThreshold, deltaRLeadPhoSubleadPhoThreshold ):
  diphoton_pass = True
  q_gg = _leadPhoton.P4()+_subleadPhoton.P4()
  m_gg = math.sqrt( q_gg*q_gg )
  if( _leadPhoton.PT/m_gg < leadPhoPTOverMassThreshold ) | ( _subleadPhoton.PT/m_gg < subleadPhoPTOverMassThreshold ): diphoton_pass = False
  #DIPHOTON MVA EQUIVALENT
  #Require diphoton mass to be between 100 and 180 GeV
  if( m_gg < 100 )|(m_gg > 180 ): diphoton_pass = False

  #Make sure photons are seperated in dR
  dR_gg = deltaR( _leadPhoton.Eta, _leadPhoton.Phi, _subleadPhoton.Eta, _subleadPhoton.Phi )
  if dR_gg < deltaRLeadPhoSubleadPhoThreshold: diphoton_pass = False
  return diphoton_pass


def SelectMuon( _muon, _dipho, muonPtThreshold, muonEtaThreshold, muPFIsoSumRelThreshold, deltaRMuonPhoThreshold ):
  muon_pass = True
  if( _muon.PT < muonPtThreshold ): muon_pass = False
  if( abs( _muon.Eta ) > muonEtaThreshold ): muon_pass = False
  #Vertex: missing, require vertex info in CMS card, copy isTightMuon() (see implementation on git)
  #Isolation: using sumPt variable: assuming same as hard sum in flashgg::LeptonSelection.cc
  if( (_muon.SumPt/_muon.PT) > muPFIsoSumRelThreshold ): muon_pass = False
  
  #if muon passed then calc dR between leadPho and subleadPho
  if muon_pass:
    dR_Muon_LeadPho = deltaR( _dipho[0][0].Eta, _dipho[0][0].Phi, _muon.Eta, _muon.Phi )
    dR_Muon_SubleadPho = deltaR( _dipho[0][1].Eta, _dipho[0][1].Phi, _muon.Eta, _muon.Phi )
    if( dR_Muon_LeadPho < deltaRMuonPhoThreshold ) | ( dR_Muon_SubleadPho < deltaRMuonPhoThreshold ): muon_pass = False

  return muon_pass


def SelectElectron( _electron, _dipho, electronPtThreshold , electronEtaThresholds, electronPhoMassThreshold , deltaRElectronPhoThreshold ):
  electron_pass = True
  if( _electron.PT < electronPtThreshold ): electron_pass = False
  #Eta: inc outside transition region between barrel and endcap 
  if( ( abs( _electron.Eta ) > electronEtaThresholds[2] ) | ( ( abs( _electron.Eta ) > electronEtaThresholds[0] ) & ( abs( _electron.Eta ) < electronEtaThresholds[1] ) ) ): electron_pass = False 
  #Vertex: missing, require vertex info
  #ID: flashgg::passLooseID()

  #mass of electron+photon not close to Z mass: fasely recon electrons
  if electron_pass:
    m_eLeadPho = math.sqrt( abs((_dipho[0][0].P4()+_electron.P4())*(_dipho[0][0].P4()+_electron.P4())) )
    m_eSubleadPho = math.sqrt( abs((_dipho[0][1].P4()+_electron.P4())*(_dipho[0][1].P4()+_electron.P4())) )
    if( abs( m_eLeadPho-91.2 ) < 5. ) | ( abs( m_eSubleadPho-91.2 ) < 5. ): electron_pass = False

  #if electron passed then calc dR between leadPho and subleadPho
  if electron_pass:
    dR_Electron_LeadPho = deltaR( _dipho[0][0].Eta, _dipho[0][0].Phi, _electron.Eta, _electron.Phi )
    dR_Electron_SubleadPho = deltaR( _dipho[0][1].Eta, _dipho[0][1].Phi, _electron.Eta, _electron.Phi )
    if( dR_Electron_LeadPho < deltaRElectronPhoThreshold ) | ( dR_Electron_SubleadPho < deltaRElectronPhoThreshold ): electron_pass = False

  return electron_pass


def SelectJet_alpha( _alpha, _jet, _dipho, jetPtThreshold, jetEtaThreshold, deltaRJetPhoThreshold, isBtagged ):
  jet_pass = True
  if( (_jet.PT*_alpha) < jetPtThreshold ): jet_pass = False
  if( abs( _jet.Eta ) > jetEtaThreshold ): jet_pass = False
  
  #if jet passed then calc dR between it and leadPho and subleadPho
  if jet_pass:
    dR_Jet_LeadPho = deltaR( _dipho[0][0].Eta, _dipho[0][0].Phi, _jet.Eta, _jet.Phi )
    dR_Jet_SubleadPho = deltaR( _dipho[0][1].Eta, _dipho[0][1].Phi, _jet.Eta, _jet.Phi )
    if( dR_Jet_LeadPho < deltaRJetPhoThreshold ) | ( dR_Jet_SubleadPho < deltaRJetPhoThreshold ): jet_pass = False

  #B tagging: set isBtagged=1 to output b-jets only
  #Using medium w/ MTD as working point: extract the write bit
  if( isBtagged == 0 ):
    if( _jet.BTag & 0b010000 ): jet_pass = False
  else:
    if( not _jet.BTag & 0b010000 ): jet_pass = False

  return jet_pass

###############################################################################
#For effect of systematic

#b-tagging
#function to calculate weight modifier
def btag_weight_multiplier( direction, _bjets_gen ):
  eff = []
  sigma = []
  for bjet in _bjets_gen:
    eff_found = False
    sigma_found = False
    for key, value in eff_dict.iteritems():
      if( not eff_found ):
        if( abs(bjet.Eta) > value[0] )&( abs(bjet.Eta) <= value[1] )&( bjet.PT > value[2] )&( bjet.PT <= value[3] ):

          eff_value = eff_list[key] 
          eff_found = True
    if( not eff_found ): eff_value = 0.
    eff.append( eff_value )
    for key, value in sigma_dict.iteritems():
      if( bjet.PT > value[0] )&( bjet.PT <= value[1] ): sigma.append( sigma_list[key]*eff_value )
  #Calc probability of selection given bjets in event
  P_nominal = 1
  P_syst = 1
  for i in range( len( _bjets_gen ) ):
    P_nominal *= (1-eff[i])
    if( direction == 'up' ): P_syst *= (1-(eff[i]+sigma[i]))
    else: P_syst *= (1-(eff[i]-sigma[i]))
  P_nominal = 1-P_nominal
  P_syst = 1-P_syst
  #Return modifier
  if( P_nominal == 0. ): return 1.
  else: return abs(P_syst/P_nominal) 
  
#For JES
#JES: define jet pT multiplier: alpha
alpha = 1.
#if( syst_type == 'JES' ):
#  if( syst_direction == 'up' ): alpha = 1.02
#  else: alpha = 0.98

#JER
#elif( syst_type == 'JER' ): alpha = 1.

#btag
#else: alpha = 1.

#For ggH 2017 LHCHXSWG uncertainty
def interpol( x, x1, y1, x2, y2 ):
  if x<x1: return y1
  elif x>x2: return y2
  else: return y1-(y2-y1)*(x-x1)/(x2-x1)

def qcd_ggH_uncert_2017( N_jets, pTH, N_sigma ):
  #Njet uncertainties
  sig = [30.117,12.928,4.845]
  yieldUnc = [1.12,0.66,0.42]
  resUnc = [0.03,0.57,0.42]
  cut01Unc = [-1.22,1.00,0.21]
  cut12Unc = [0,-0.86,0.86]
  #scaling BLPTW total cross section to N3LO
  sf = 48.52/47.4
  if N_jets > 1: jetBin = 2
  else: jetBin = N_jets
  normFact = sf/sig[jetBin]
  result = [yieldUnc[jetBin]*normFact,resUnc[jetBin]*normFact,cut01Unc[jetBin]*normFact, cut12Unc[jetBin]*normFact]
  #Not in VBF phase space therefore add zero for STXS uncertainties
  result.append(0.)
  result.append(0.)
  #pTH uncertainties
  #60 GeV
  if N_jets == 0: result.append(0.)
  elif N_jets == 1: result.append( interpol( pTH,20,-0.1,100,0.1) )
  else: result.append( interpol( pTH,0,-0.1,180,0.1) )
  #120 GeV
  if N_jets == 0: result.append( 0. )
  else: result.append( interpol( pTH, 90, -0.016, 160, 0.14 ) )
  #top mass uncertainty
  result.append( interpol( pTH, 160, 0.0, 500, 0.37 ) )
  #determine scale factors
  sfs = []
  for unc in result: sfs.append(1.0+N_sigma*unc)
  return sfs
 
#Factorisation/Renormalisation shape
w_ID = -1
if( syst_type == "factorShape" ):
  if( syst_direction == "up" ): w_ID = 1
  else: w_ID = 2
elif( syst_type == "renormShape" ):
  if( syst_direction == "up" ): w_ID = 3
  else: w_ID = 6

###############################################################################
#	EVENTS LOOP

# Loop over all events
for entry in range(0, numberOfEntries ):
 
  if entry % 10000 == 0: print "Processing event: (", entry, "/", numberOfEntries, ")"

  #Define boolean for event passing selection
  event_pass = False
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)


  #Event branch: get event weight
  _event = branchEvent.At(0)
  LO_weight = (_event.Weight/totalWeight)*Xsection

  #Extract genLevel higgs
  #Some events do not have gen-level higgs: remove these events
  hasHiggs = False
  Higgs_gen_idx = -1
  if( branchGenParticle.GetEntries > 0 ):
    for i in range( branchGenParticle.GetEntries() ):
      genPart = branchGenParticle.At(i)
      if( genPart.PID == 25 )&( genPart.Status == 22 ): 
        hasHiggs = True
        Higgs_gen_idx = i

  if( not hasHiggs ): continue 
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #Perform event selection: ttHHad
  if( branchPhoton.GetEntries() < 2 ): continue

  #list to hold photon and lepton candidates
  photons = []
  diphotons = []
  photon_pair = []
  muons = []
  electrons = []
  jets = []
  bjets = []

  #booleans describing event passing different stages of selection
  photons_pass = False
  lepton_pass = False
  top_pass = False

  #------------------------------------------------------------------------------------
  #Photon Selection
  if branchPhoton.GetEntries() > 0:

    #Loop over photons in event and apply photon selection
    for i in range( branchPhoton.GetEntries() ):
      photon = branchPhoton.At(i)
      #Apply selection on single photons
      if( SelectPhoton( photon, photonPtThreshold=20., photonEtaThresholds=[1.4442,1.566,2.5], phoIsoChRelThreshold=0.3 ) ): photons.append( photon )
  
    #if atleast 2 photons in event
    if len( photons ) >= 2:
    
      #sort photons according to pT (descending)
      photons.sort( key=lambda g: g.PT, reverse=True )

      #Loop over photon pairs in event and apply diphoton selection
      for leadPho_idx in range( len( photons ) ):
        for subleadPho_idx in range( len( photons ) ):
          #Only once for each pair
          if subleadPho_idx > leadPho_idx:
            if( SelectDiPhoton( photons[leadPho_idx], photons[subleadPho_idx], leadPhoPTOverMassThreshold=0.333, subleadPhoPTOverMassThreshold=0.25, deltaRLeadPhoSubleadPhoThreshold=0.4) ): diphotons.append( [photons[leadPho_idx],photons[subleadPho_idx]] )
      
      #If atleast one diphoton pair passing selection: choose pair with mass closest to Higgs mass
      if( len( diphotons ) > 1 ):
        mgg_opt = -999.
        dipho_idx_opt = -999
        for dipho_idx in range( len(diphotons) ):
          m_gg = math.sqrt( abs((diphotons[dipho_idx][0].P4()+diphotons[dipho_idx][1].P4())*(diphotons[dipho_idx][0].P4()+diphotons[dipho_idx][1].P4())) )
          if( abs( m_gg - 125.0 ) < abs( mgg_opt - 125.0 ) ):
            mgg_opt = m_gg
            dipho_idx_opt = dipho_idx
        photon_pair.append( diphotons[ dipho_idx_opt ] )
        photons_pass = True
      #else if one pair, then set
      elif( len( diphotons ) == 1 ):
        photon_pair.append( diphotons[0] )
        photons_pass = True

  #-------------------------------------------------------------------------------------------------
  #Lepton VETO: only perform if photon pair selected
  if( photons_pass ):
    #Muons
    if branchMuon.GetEntries() > 0:
      #loop over Muons in event and extract those which satisfy criteria
      for i in range( branchMuon.GetEntries() ):
        muon = branchMuon.At(i)
        if( SelectMuon( muon, photon_pair, muonPtThreshold=20., muonEtaThreshold=3., muPFIsoSumRelThreshold=0.25, deltaRMuonPhoThreshold=0.35 ) ):
          muons.append( muon )

    #Electron
    if branchElectron.GetEntries() > 0:
      #loop over Electrons in event and extract those which satisfy criteria
      for i in range( branchElectron.GetEntries() ):
        electron = branchElectron.At(i)
        if( SelectElectron( electron, photon_pair, electronPtThreshold=20., electronEtaThresholds=[1.4442,1.566,3.], electronPhoMassThreshold=5., deltaRElectronPhoThreshold=0.35 ) ):
          electrons.append( electron )
  
    #Sort electrons and muons according to pT
    electrons.sort( key=lambda e: e.PT, reverse=True )
    muons.sort( key=lambda mu: mu.PT, reverse=True )

    #check for size of lists: If greater than zero then lepton tagged and veto event
    if( len(muons) > 0 ) | ( len(electrons) > 0 ): lepton_pass = True

  #-------------------------------------------------------------------------------------------------
  #Top reconstruction:
  if( photons_pass ) & ( lepton_pass ):
    if branchJet.GetEntries() > 0:
      #loop over jets in event and extract those which satisfy criteria
      for i in range( branchJet.GetEntries() ):
        jet = branchJet.At(i)

        #Determine alpha for current jet from dictionary
        if( syst_type == "JES" ):
          #if b-tagged jet
          if( jet.BTag & 0b010000 ):
            bin_found = False
            for unc_v in JES_dict:
              if( not bin_found ):
                if( jet.PT > JES_dict[unc_v][0] )&( jet.PT <= JES_dict[unc_v][1] ):
                  if( syst_direction == 'up' ): alpha = 1+JES_unc_bjets[unc_v]
                  else: alpha = 1-JES_unc_bjets[unc_v]
                  bin_found = True
            if( not bin_found ):
              alpha = 1.0068
          #for light jet
          else:
            bin_found = False
            for unc_v in JES_dict:
              if( not bin_found ):
                if( jet.PT > JES_dict[unc_v][0] )&( jet.PT <= JES_dict[unc_v][1] ):
                  if( syst_direction == 'up' ): alpha = 1+JES_unc_lightjets[unc_v]
                  else: alpha = 1-JES_unc_lightjets[unc_v]
                  bin_found = True
            if( not bin_found ):
              alpha = 1.0068

        #Jet selection: without b tag
        #UPDATE: CMS-PHASE II TRACKER IMPROVEMENTS, change jet eta threshold to 4
        if( SelectJet_alpha( alpha, jet, photon_pair, jetPtThreshold=25., jetEtaThreshold=4, deltaRJetPhoThreshold=0.4, isBtagged=0 ) ): jets.append( jet )
        #Jet selection: with b tag
        elif( SelectJet_alpha( alpha, jet, photon_pair, jetPtThreshold=25., jetEtaThreshold=4, deltaRJetPhoThreshold=0.4, isBtagged=1 ) ): bjets.append( jet )

      #Require >=2 jets in events and that atleast one of jets is b-tagged
      if( len(jets)+len(bjets) >= 2 ) & ( len(bjets) >= 1 ):

        #Order jets according to pT (descending)
        jets.sort( key=lambda J: J.PT, reverse=True )
        bjets.sort( key=lambda bJ: bJ.PT, reverse=True )
        #Set top pass to true
        top_pass = True

 
##############################################################################
#	EVENTS PASSING SELECTION
  if( hasHiggs ) & (photons_pass) & (lepton_pass) & (top_pass):

    ##############################################################################
    #For b-tagging systematic: change weight of event according to gen b-jets
    btag_modifier = 1.
    #If syst - b-tagging
    #Determine number of true b-jets in event: add to list
    if( syst_type == 'btag' ):
      all_jets = jets + bjets
      bjets_gen = []
      for jet in all_jets:
        if abs(jet.Flavor) == 5: bjets_gen.append( jet ) 
      #Extract weight modifier
      btag_modifier = btag_weight_multiplier( syst_direction, bjets_gen )
        
    #Define final photons
    leadPhoton = photon_pair[0][0]
    subleadPhoton = photon_pair[0][1]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # GEN PARTICLE EXTRACTION

    #Higgs
    higgs_gen = branchGenParticle.At( Higgs_gen_idx )

    #Photons from Higgs decay
    mass_pass = False
    dR_pass = False
    higgsPhotons_Found = False
    genPhotons = []
    higgsPhotons_gen = []
    #Define hash table to save unique ID of genParticles and respective position in branch
    hash_ID = {}
    if branchGenParticle.GetEntries() > 0:
      baseUniqueID = branchGenParticle.At(0).GetUniqueID()
      for i in range( branchGenParticle.GetEntries() ):
        #Only save the ID of top quarks as this is where photons originate
        if( abs( branchGenParticle.At(i).PID ) == 6 ):
          hash_ID[ branchGenParticle.At(i).GetUniqueID() - baseUniqueID ] = i
        
        #extract gen Photons
        if( branchGenParticle.At(i).PID == 22 ):
          genPhotons.append( branchGenParticle.At(i) )

      #Extract PID of genPhotons mothers
      for i in range( len( genPhotons ) ):
        motherPID = -999
        if genPhotons[i].M1 in hash_ID.keys():
          motherPID = branchGenParticle.At( hash_ID[ genPhotons[i].M1 ] ).PID
        if abs( motherPID ) == 6:
          higgsPhotons_gen.append( genPhotons[i] )

      if( len( higgsPhotons_gen ) > 1 ):
        #Checks on genPhotons: 
        #dR between genPhotons and one of reco photons is > 0.2
        gen_leadPhoton_idx = -999
        dR_leadPho_min = 999
        for i in range( len( higgsPhotons_gen ) ):
          dR = deltaR( higgsPhotons_gen[i].Eta, higgsPhotons_gen[i].Phi, leadPhoton.Eta, leadPhoton.Phi )
          if( dR < dR_leadPho_min ):
            dR_leadPho_min = dR
            gen_leadPhoton_idx = i
      
        gen_subleadPhoton_idx = -999
        dR_subleadPho_min = 999
        for i in range( len( higgsPhotons_gen ) ):
          dR = deltaR( higgsPhotons_gen[i].Eta, higgsPhotons_gen[i].Phi, subleadPhoton.Eta, subleadPhoton.Phi )
          if( dR < dR_subleadPho_min ):
            dR_subleadPho_min = dR
            gen_subleadPhoton_idx = i

        #Demand criteria and two photons are different
        if( dR_leadPho_min < 0.2 )&( dR_subleadPho_min < 0.2 )&( gen_leadPhoton_idx != gen_subleadPhoton_idx ):
          dR_pass = True
          gen_leadPhoton = higgsPhotons_gen[ gen_leadPhoton_idx ]
          gen_subleadPhoton = higgsPhotons_gen[ gen_subleadPhoton_idx ]

        #Mass criteria: within 3GeV of Higgs mass
        if( dR_pass ):
          m_gg = math.sqrt( abs( (gen_leadPhoton.P4()+gen_subleadPhoton.P4())*(gen_leadPhoton.P4()+gen_subleadPhoton.P4()) ) )
          if( abs( m_gg -125.0 ) < 3. ): mass_pass = True

        if( dR_pass )&( mass_pass ): higgsPhotons_Found = True
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    #If theory systematic for ggH
    ggH_modifier = 1.
    #First calc jet multiplicity for jets > 30 GeV
    Njets30 = 0
    for i in range( branchJet.GetEntries() ):
      jet = branchJet.At(i)
      if( jet.PT > 30. ): Njets30 += 1
    if "THU_ggH" in syst_type:
      #calculate scale factors
      if( syst_direction == "up" ): ggH_sf = qcd_ggH_uncert_2017(Njets30,higgs_gen.PT,1.0)
      else: ggH_sf = qcd_ggH_uncert_2017(Njets30,higgs_gen.PT,-1.0)
      #extract relevant scale factor
      if syst_type == "THU_ggH_Mu": ggH_modifier = ggH_sf[0]
      elif syst_type == "THU_ggH_Res": ggH_modifier = ggH_sf[1]
      elif syst_type == "THU_ggH_Mig01": ggH_modifier = ggH_sf[2]
      elif syst_type == "THU_ggH_Mig12": ggH_modifier = ggH_sf[3]
      elif syst_type == "THU_ggH_PT60": ggH_modifier = ggH_sf[6]
      elif syst_type == "THU_ggH_PT120": ggH_modifier = ggH_sf[7]
      elif syst_type == "THU_ggH_qmtop": ggH_modifier = ggH_sf[8]

    #Reset var that need resetting
    jet3_pT[0] = -1.
    jet3_eta[0] = -999.
    jet3_phi[0] = -999.
    jet3_mass[0] = -1.
    jet3_btag[0] = -1
    pho1_gen_pT[0] = -1. 
    pho1_gen_eta[0] = -999.
    pho1_gen_phi[0] = -999. 
    pho1_gen_E[0] = -1. 
    pho2_gen_pT[0] = -1.
    pho2_gen_eta[0] = -999.
    pho2_gen_phi[0] = -999.
    pho2_gen_E[0] = -1.

    #Fill Ntuples with relevant variables
    pTH_gen_v[0] = higgs_gen.PT
    pTH_reco_v[0] = pT_vector_calc( leadPhoton, subleadPhoton )
    mgg_v[0] = math.sqrt( (leadPhoton.P4()+subleadPhoton.P4())*(leadPhoton.P4()+subleadPhoton.P4()) )
    if "THU_ggH" in syst_type: LO_w[0] = LO_weight*ggH_modifier
    elif( syst_type == "factorShape" )|( syst_type == "renormShape" ):
      if( branchWeight.At(0).Weight == 0 ):
        LO_w[0] = LO_weight
      elif( (branchWeight.At(w_ID).Weight/branchWeight.At(0).Weight) > 2. )|( (branchWeight.At(w_ID).Weight/branchWeight.At(0).Weight) < 0. ):
        LO_w[0] = LO_weight
      else:
        LO_w[0] = LO_weight*(branchWeight.At(w_ID).Weight/branchWeight.At(0).Weight)
    else: LO_w[0] = LO_weight*btag_modifier
    pho1_pT[0] = leadPhoton.PT
    pho1_eta[0] = leadPhoton.Eta
    pho1_phi[0] = leadPhoton.Phi
    pho1_E[0] = leadPhoton.E
    pho1_IsolationVar[0] = leadPhoton.IsolationVarRhoCorr
    pho2_pT[0] = subleadPhoton.PT
    pho2_eta[0] = subleadPhoton.Eta
    pho2_phi[0] = subleadPhoton.Phi
    pho2_E[0] = subleadPhoton.E
    pho2_IsolationVar[0] = subleadPhoton.IsolationVarRhoCorr

    if( higgsPhotons_Found ):
      pho1_gen_pT[0] = gen_leadPhoton.PT
      pho1_gen_eta[0] = gen_leadPhoton.Eta
      pho1_gen_phi[0] = gen_leadPhoton.Phi
      pho1_gen_E[0] = gen_leadPhoton.E
      pho2_gen_pT[0] = gen_subleadPhoton.PT
      pho2_gen_eta[0] = gen_subleadPhoton.Eta
      pho2_gen_phi[0] = gen_subleadPhoton.Phi
      pho2_gen_E[0] = gen_subleadPhoton.E

    #jet variables
    #create list combining jets w/ bjets, order by pT
    merged_jets = jets + bjets
    merged_jets.sort( key=lambda J: J.PT, reverse=True )
    #Detemine alpha values for jets in merged_jets
    alphas = []
    for jet in merged_jets:
      #If JES uncertainty
      #Determine alpha for current jet from dictionary
      if( syst_type == "JES" ):
        #if b-tagged jet
        if( jet.BTag & 0b010000 ):
          bin_found = False
          for unc_v in JES_dict:
            if( not bin_found ):
              if( jet.PT > JES_dict[unc_v][0] )&( jet.PT <= JES_dict[unc_v][1] ):
                if( syst_direction == 'up' ): alphas.append(1+JES_unc_bjets[unc_v])
                else: alphas.append(1-JES_unc_bjets[unc_v])
                bin_found = True
          if( not bin_found ):
            alphas.append(1.0068)
        #for light jet
        else:
          bin_found = False
          for unc_v in JES_dict:
            if( not bin_found ):
              if( jet.PT > JES_dict[unc_v][0] )&( jet.PT <= JES_dict[unc_v][1] ):
                if( syst_direction == 'up' ): alphas.append(1+JES_unc_lightjets[unc_v])
                else: alphas.append(1-JES_unc_lightjets[unc_v])
                bin_found = True
          if( not bin_found ):
            alphas.append(1.0068)
      #If not set all alphas to 1
      else: alphas.append(1.) 
    #first jet
    jet1_pT[0] = merged_jets[0].PT*alphas[0]
    jet1_eta[0] = merged_jets[0].Eta
    jet1_phi[0] = merged_jets[0].Phi
    jet1_mass[0] = merged_jets[0].Mass
    jet1_btag[0] = merged_jets[0].BTag
    #second jet
    jet2_pT[0] = merged_jets[1].PT*alphas[1]
    jet2_eta[0] = merged_jets[1].Eta
    jet2_phi[0] = merged_jets[1].Phi
    jet2_mass[0] = merged_jets[1].Mass
    jet2_btag[0] = merged_jets[1].BTag
    #third jet
    if( len( merged_jets ) > 2 ):
      jet3_pT[0] = merged_jets[2].PT*alphas[2]
      jet3_eta[0] = merged_jets[2].Eta
      jet3_phi[0] = merged_jets[2].Phi
      jet3_mass[0] = merged_jets[2].Mass
      jet3_btag[0] = merged_jets[2].BTag

    #Global jet variables
    Njets[0] = len( merged_jets )
    Nbjets[0] = len( bjets )

    #create list combining electrons and muons
    merged_lep = electrons + muons
    merged_lep.sort( key=lambda lep: lep.PT, reverse=True )
    Nleptons[0] = len( merged_lep )
    lep_pT[0] = merged_lep[0].PT
    lep_eta[0] = merged_lep[0].Eta
    lep_phi[0] = merged_lep[0].Phi

    #Other variables
    MET[0] = branchMET.At(0).MET
    MET_eta[0] = branchMET.At(0).Eta
    MET_phi[0] = branchMET.At(0).Phi 
    scalarHT[0] = branchScalarHT.At(0).HT
    tree_0.Fill()

    #END OF EVENT LOOP
##############################################################################
f_0.Write()
f_0.Close()
#raw_input("Press Enter to continue...")
