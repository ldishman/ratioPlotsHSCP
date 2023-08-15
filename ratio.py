# Plotting the ratio of two different user-provided histograms
# Intending to compare Pythia and MadGraph samples of the di-gluino system from truth.py

from ROOT import *
from FWCore.ParameterSet.VarParsing import VarParsing

#gROOT.SetBatch(True)    # Stops showing the canvases every time you run (quicker)

# Grabbing user-provided file names and mass
options = VarParsing ('python')
options.register ('mass','',VarParsing.multiplicity.singleton, VarParsing.varType.string, "mass")
options.register ('pythiaFilename','',VarParsing.multiplicity.singleton, VarParsing.varType.string, "pythiaFilename")
options.register ('MGFilename','',VarParsing.multiplicity.singleton, VarParsing.varType.string, "MGFilename")
options.register ('outputFilename','',VarParsing.multiplicity.singleton, VarParsing.varType.string, "outputFilename")


# Sorting user arguments
options.parseArguments()
mass = options.mass
pythiaFilename = options.pythiaFilename
MGFilename = options.MGFilename
outputFilename = options.outputFilename


# Opening and creating appropriate files
pythiaFile = TFile.Open(pythiaFilename)
MGFile = TFile.Open(MGFilename)
outputFile = TFile(outputFilename + ".root", 'RECREATE')


# Setting up the ROOT canvas & hist permissions
# Grabbing, normalizing, and recreating truth.py histograms
TH1.AddDirectory(kFALSE)
canvas1 = TCanvas("canvas1")
canvas1.cd()

pythiaHist = pythiaFile.Get("di-glu pT;1")
MGHist = MGFile.Get("pTsum;1")

pythiaHist.Scale(1./pythiaHist.Integral())
MGHist.Scale(1./MGHist.Integral())

pythiaHist.SetLineColor(kRed)
MGHist.SetLineColor(kBlue)
pythiaHist.Draw("hist")
MGHist.Draw("hist")
pythiaHist.GetXaxis().SetLimits(0.,3000.)
MGHist.GetXaxis().SetLimits(0.,3000.)
pythiaHist.SetTitle("")


# Creating TRatioPlot
ratioPlot = TRatioPlot(pythiaHist, MGHist)
ratioPlot.SetH2DrawOpt("hist")    #noconfint 
ratioPlot.Draw()
ratioPlot.GetLowerRefYaxis().SetRangeUser(-0.1,2.1)
ratioPlot.GetLowerRefYaxis().SetTitle("ratio")
ratioPlot.GetUpperRefYaxis().SetTitle("hists")


# Converting TRatioPlot to TGraph, then to TH1F histogram
ratioTempGraph = ratioPlot.GetLowerRefGraph()
numPoints = ratioTempGraph.GetN()
xmin = TMath.MinElement(ratioTempGraph.GetN(), ratioTempGraph.GetX())
xmax = TMath.MaxElement(ratioTempGraph.GetN(), ratioTempGraph.GetX())
#ratioHist = TH1F('ratioHist', '', numPoints + 1, float(xmin), float(xmax))
ratioHist = pythiaHist.Clone("ratioHist")
ratioHist.Reset()
ratioHist.SetLineColor(kBlue+1)
ratioHist.GetYaxis().SetTitle("ratio")
for i in range (0, numPoints):
    x , y = Double(), Double()
    ratioTempGraph.GetPoint(i, x, y)
    ey = ratioTempGraph.GetErrorY(i)
    ratioHist.SetBinContent(ratioHist.FindBin(x), y)
    ratioHist.SetBinError(ratioHist.FindBin(x), ey)


# Plotting ratio histogram
canvas2 = TCanvas("canvas2")
canvas2.cd(0)
ratioHist.Draw()      # ("hist") for a straight line
ratioHist.GetYaxis().SetRangeUser(-0.1,2.1)
ratioHist.SetTitle("")
ratioHist.GetXaxis().SetTitle('P_{T} [GeV]')


# Adding legends
ratioPlot.GetUpperPad().cd()
legend1 = TLegend(0.3,0.7,0.7,0.9)
a = legend1.SetHeader("Mass = " + mass + " GeV", "C")
b = legend1.AddEntry(pythiaHist,"pythiaHist")
c = legend1.AddEntry(MGHist,"MGHist")
b.SetTextColor(kRed)
c.SetTextColor(kBlue)
legend1.Draw()

canvas2.cd()
legend2 = TLegend(0.3,0.84,0.7,0.9)
d = legend2.SetHeader("Mass = " + mass + " GeV", "C")
legend2.Draw()


# Closing and saving 2 pdfs (one for each canvas) 
# Saving one root file (for pythiaHist, MGHist, and ratioHist)
canvas1.SaveAs(outputFilename + "_1.pdf")
canvas2.SaveAs(outputFilename + "_2.pdf")
pythiaHist.Write("pythiaHist")
MGHist.Write("MGHist")
ratioHist.Write("ratioHist")
outputFile.Write()
outputFile.Close()



