import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class eventCounterHistogramProducer(Module):
    def __init__(self):
        self.passedEvents = 0
    
    def beginJob(self):
        pass
    
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_count = ROOT.TH1I("EventCounter","Event Counter",4,-0.5,3.5)
        self.h_count.GetXaxis().SetBinLabel(1,"all events")
        self.h_count.GetXaxis().SetBinLabel(2,"passed")
        self.h_count.GetXaxis().SetBinLabel(3,"sum of amc@NLO weights")
        self.h_count.GetXaxis().SetBinLabel(4,"sum of TopPt weights")
        self.h_count.SetBinContent(1,inputTree.GetEntriesFast())

        maxInt = (2**32)/2-1 # for TH1I
        entries = inputTree.GetEntriesFast()
        if entries > maxInt:
            raise RuntimeError("Had more entries in the tree ["+str(entries)+"] than we can store in the eventCounter histogram bin ["+str(maxInt)+"]!")
        self.h_count.SetBinContent(1,entries)

        eventsTree = inputFile.Get("Events")
        eventsTree.GetEntry(0)
        _LHEWeight_originalXWGTUP=1.0
        if eventsTree.GetBranch("LHEWeight_originalXWGTUP"):
            _LHEWeight_originalXWGTUP=abs(eventsTree.GetBranch("LHEWeight_originalXWGTUP").GetLeaf("LHEWeight_originalXWGTUP").GetValue())

        runsTree = inputFile.Get("Runs")
        runsTree.GetEntry(0)
        if runsTree.GetBranch("genEventSumw"):
            self.h_count.SetBinContent(3,runsTree.GetBranch("genEventSumw").GetLeaf("genEventSumw").GetValue()/_LHEWeight_originalXWGTUP)


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_count.SetBinContent(2,self.passedEvents)
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_count.Write()
        prevdir.cd()        

    def analyze(self, event):
        self.passedEvents+=1
        return True

eventCounterHistogramModule = lambda : eventCounterHistogramProducer() 

