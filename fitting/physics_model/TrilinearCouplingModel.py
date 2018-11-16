from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

class TrilinearHiggs(SMLikeHiggsModel):
    "Float independently cross sections and branching ratios"
    def __init__(self):
        SMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.mHRange = []
        self.poiNames = []
    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith("higgsMassRange="):
                self.mHRange = po.replace("higgsMassRange=","").split(",")
                if len(self.mHRange) != 2:
                    raise RuntimeError, "Higgs mass range definition requires two extrema"
                elif float(self.mHRange[0]) >= float(self.mHRange[1]):
                    raise RuntimeError, "Extrema for Higgs mass range defined with inverterd order. Second must be larger the first"
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
	
	# trilinear Higgs couplings modified 
	self.modelBuilder.doVar("k_lambda[1,-20.,20.]")
	self.poiNames="k_lambda"

        # Scaling @ production: define how cross section scales for each generator pT(H) bin x Higgs production mode
        # read C1 values from file: C1 defined as interference between LO and lambda3 dependent NLO correction
        C1_ttH = []
        C1_tH = []
        C1_VH = []
        f_C1_ttH = open("C1/ttH_C1.txt","r")
	f_C1_tH = open("C1/tHj_C1.txt","r")
        f_C1_VH = open("C1/VH_C1.txt","r")
        for genbin in f_C1_ttH: C1_ttH.append( float(genbin[ genbin.find(":")+1:-2]) )
        for genbin in f_C1_tH: C1_tH.append( float(genbin[ genbin.find(":")+1:-2]) )
        for genbin in f_C1_VH: C1_VH.append( float(genbin[ genbin.find(":")+1:-2]) )
        #Use inclusive value for ggH: EWK reweighting tool not available. Taken directly from arXiv:1607.04251
        C1_ggH = 0.0066

        #Define mapping of C1 to production process
        C1_map = {}
        for i in range( len( C1_ttH ) ):
          C1_map["ttH_gen%g"%i] = C1_ttH[i]
          C1_map["tHW_gen%g"%i] = C1_tH[i]
          C1_map["tHq_gen%g"%i] = C1_tH[i]        
          C1_map["VH_gen%g"%i] = C1_VH[i]        
          #ggH at inclusive level
          C1_map["ggH_gen%g"%i] = C1_ggH
 
        #Define dZH constant variable
	dZH = -1.536e-3

        #Loop over processes*gen bins in map to define how cross-section scales
        for proc in C1_map:
          self.modelBuilder.factory_("expr::XSscal_%s(\"(1+@0*%g+%g)/((1-(@0*@0-1)*%g)*(1+%g+%g))\",k_lambda)"%(proc,C1_map[proc],dZH,dZH,C1_map[proc],dZH))

        #Scaling @ decay: define expression for how BR scales as function of klambda: h->gammagamma
        #Use following parameters taken directly from: arXiv:1607.04251
        C1_hgg = 0.0049
        C1_tot = 2.5e-3
        self.modelBuilder.factory_("expr::BRscal_hgg(\"1+(((@0-1)*(%g-%g))/(1+(@0-1)*%g))\",k_lambda)"%(C1_hgg,C1_tot,C1_tot))

        print self.poiNames
        self.modelBuilder.doSet("POI",self.poiNames)

    def getHiggsSignalYieldScale(self,production,decay,energy):
        
        #XSBR
        name = "XSBRscal_%s_%s" % (production,decay)
        #Name has not been defined in doParametersOfInterest: combine XS + BR
        if self.modelBuilder.out.function(name) == None:
          #XS
          if self.modelBuilder.out.function( "XSscal_%s"%(production) ) == None:
            print "DEBUG: proc not given XS scaling"
            raise RuntimeError, "Production mode %s not supported"%production
          else:
            XSscal = "XSscal_%s_%s"%(production,decay)
          #BR
          if self.modelBuilder.out.function( "BRscal_%s"%(decay) ) == None:
            print "DEBUG: proc not given BR scaling"
            raise RuntimeError, "Decay mode %s not supported"%decay
          else:
            BRscal = "BRscal_%s"%decay
          #XSBR
          self.modelBuilder.factory_('expr::%s(\"(@0*@1)\", XSscal_%s, BRscal_%s)'%(name,production,decay))
          print '[LHC-CMS Trilinear]', name, ": ", self.modelBuilder.out.function(name).Print("")
        return name

trilinearHiggs = TrilinearHiggs()
