# Plotting the ratio of two different user-provided histograms
# Intending to compare Pythia and MadGraph samples of the di-gluino system from truth.py

from ROOT import *
from FWCore.ParameterSet.VarParsing import VarParsing

#gROOT.SetBatch(True)    # Stops showing the canvases every time you run (quicker)

# def inputHistRebin(inputHist):
    # inputHistX = inputHist.Clone("inputHistX")
    # inputHistX.Rebin(2)
    # return inputHistX

def ratioPlotConvert(pythiaHist, MGHist):
    ratioPlot = TRatioPlot(MGHist, pythiaHist)
    ratioPlot.Draw()       # PROBLEM CHILD AREA
    ratioTempGraph = ratioPlot.GetLowerRefGraph()
    # ratioTempGraph.SetDirectory(0)
    # ratioTempGraph = ratioPlot.GetCalculationOutputGraph()
    # print ("hello0",type (ratioTempGraph))
    return TGraphAsymmErrors(ratioTempGraph)

def ratioHistFill(ratioTempGraph, ratioHist, xmin, xmax):
    # print type (ratioTempGraph)
    numPoints = ratioTempGraph.GetN()
    # print("numPoints in Object: ")
    # print(numPoints)
    for i in range (xmin, xmax):
        x , y = Double(), Double()
        ratioTempGraph.GetPoint(i, x, y)
        ey = ratioTempGraph.GetErrorY(i)
        ratioHist.SetBinContent(ratioHist.FindBin(x), y)
        ratioHist.SetBinError(ratioHist.FindBin(x), ey)


# Grabbing user-provided file names and mass
options = VarParsing ('python')
options.register ('mass','',VarParsing.multiplicity.singleton, VarParsing.varType.string, "mass")
# options.register ('pythiaFilename','',VarParsing.multiplicity.singleton, VarParsing.varType.string, "pythiaFilename")
# options.register ('MGFilename','',VarParsing.multiplicity.singleton, VarParsing.varType.string, "MGFilename")
options.register ('inputFilename','',VarParsing.multiplicity.singleton, VarParsing.varType.string, "inputFilename")
options.register ('outputFilename','',VarParsing.multiplicity.singleton, VarParsing.varType.string, "outputFilename")


# Sorting user arguments
options.parseArguments()
mass = options.mass
# pythiaFilename = options.pythiaFilename
# MGFilename = options.MGFilename
inputFilename = options.inputFilename
outputFilename = options.outputFilename


# Opening and creating appropriate files
# pythiaFile = TFile.Open(pythiaFilename)
# MGFile = TFile.Open(MGFilename)
inputFile = TFile.Open(inputFilename)
outputFile = TFile(outputFilename + ".root", 'RECREATE')


# Setting up the ROOT canvas & hist permissions
# Grabbing, normalizing, and recreating truth.py histograms
TH1.AddDirectory(kFALSE)
canvas1 = TCanvas("canvas1")
canvas1.cd()

# pythiaHist = pythiaFile.Get("di-glu pT;1")
# MGHist = MGFile.Get("pTsum;1")

pythiaHist = inputFile.Get("Pythia;1")
MGHist = inputFile.Get("Madgraph;1")

# print(MGHist,type)

pythiaHist.Scale(1./pythiaHist.Integral())
MGHist.Scale(1./MGHist.Integral())

# pythiaHist.SetDirectory(0)
# MGHist.SetDirectory(0)

pythiaHist.SetLineColor(kRed)
MGHist.SetLineColor(kBlue)
pythiaHist.Draw("hist")
MGHist.Draw("hist")
pythiaHist.GetXaxis().SetLimits(0.,3000.)
MGHist.GetXaxis().SetLimits(0.,3000.)
pythiaHist.SetTitle("")


# Rebinning both input histograms
# pythiaHist2 = inputHistRebin(pythiaHist)
# pythiaHist3 = inputHistRebin(pythiaHist2)
# MGHist2 = inputHistRebin(MGHist)
# MGHist3 = inputHistRebin(MGHist2)


# Converting TRatioPlot to TGraph
ratioTempGraph = ratioPlotConvert(pythiaHist, MGHist)
# print ("hello1",type (ratioTempGraph))
# ratioTempGraph2 = ratioPlotConvert(pythiaHist2, MGHist2)
# print ("hello2",type (ratioTempGraph2))
# ratioTempGraph3 = ratioPlotConvert(pythiaHist3, MGHist3)
# print ("hello3",type (ratioTempGraph3))


# Plotting original TRatioPlot
ratioPlot = TRatioPlot(pythiaHist, MGHist)
#ratioPlot.SetH2DrawOpt("hist")    #noconfint 
ratioPlot.Draw()
ratioPlot.GetLowerRefYaxis().SetRangeUser(-0.1,2.1)
ratioPlot.GetLowerRefYaxis().SetTitle("ratio")
ratioPlot.GetUpperRefYaxis().SetTitle("hists")


# Creating and Filling TH1F ratio histogram
ratioHist = MGHist.Clone("ratioHist")
ratioHist.Reset()
ratioHist.SetLineColor(kBlue+1)
ratioHist.GetYaxis().SetTitle("ratio")

ratioHistFill(ratioTempGraph, ratioHist, 0, 3000)
# ratioHistFill(ratioTempGraph2, ratioHist, 200, 600)
# ratioHistFill(ratioTempGraph3, ratioHist, 600, 3000)


# Plotting ratio histogram
canvas2 = TCanvas("canvas2")
canvas2.cd(0)
ratioHist.GetYaxis().SetRangeUser(-0.1,2.1)
ratioHist.SetTitle("")
ratioHist.SetLineColor(kBlue+1)
ratioHist.GetXaxis().SetTitle('P_{T} [GeV]')
#xbins = ratioHist.GetNbinsX()
ratioHist.Draw("hist")
    

#Adding legends
#ratioPlot.GetUpperRefObject().cd("same")
canvas1.cd()
legend1 = TLegend(0.3,0.7,0.7,0.9)
a = legend1.SetHeader("Mass = " + mass + " GeV", "C")
b = legend1.AddEntry(pythiaHist,"pythiaHist")
c = legend1.AddEntry(MGHist,"MGHist")
b.SetTextColor(kRed)
c.SetTextColor(kBlue)
legend1.Draw()
print("did the canvas change work?:", canvas1.cd())

canvas2.cd()
legend2 = TLegend(0.3,0.84,0.7,0.9)
d = legend2.SetHeader("Mass = " + mass + " GeV", "C")
legend2.Draw()

# SOMETHING IN LEGENDS AND/OR PDFS SOMETIMES CAUSING SEGFAULT ISSUES

# Closing and saving 2 pdfs (one for each canvas) 
# Saving one root file (for pythiaHist, MGHist, and ratioHist)
# canvas1.SaveAs(outputFilename + "_1.pdf")
# canvas2.SaveAs(outputFilename + "_2.pdf")
pythiaHist.Write("pythiaHist")
MGHist.Write("MGHist")
ratioHist.Write("ratioHist")
outputFile.Write()
outputFile.Close()
