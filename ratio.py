# Plotting the ratio of two different user-provided histograms
# Intending to compare Pythia and MadGraph samples of the di-gluino system from truth.py

from ROOT import *
from FWCore.ParameterSet.VarParsing import VarParsing

#gROOT.SetBatch(True)    # Stops showing the canvases every time you run (quicker)

def inputHistRebin(inputHist):
    inputHistX = inputHist.Clone("inputHistX")
    inputHistX.Rebin(2)
    return inputHistX

def ratioPlotConvert(pythiaHist, MGHist):
    ratioPlot = TRatioPlot(pythiaHist, MGHist)
    ratioPlot.Draw()       # PROBLEM CHILD AREA
    ratioTempGraph = ratioPlot.GetLowerRefGraph()
    #ratioTempGraph.SetDirectory(0)
    #ratioTempGraph = ratioPlot.GetCalculationOutputGraph()
    print ("hello0",type (ratioTempGraph))
    return TGraphAsymmErrors(ratioTempGraph)

def ratioHistFill(ratioTempGraph, ratioHist, xmin, xmax):
    print type (ratioTempGraph)
    numPoints = ratioTempGraph.GetN()
    print("numPoints in Object: ")
    print(numPoints)
    for i in range (xmin, xmax):
        x , y = Double(), Double()
        ratioTempGraph.GetPoint(i, x, y)
        ey = ratioTempGraph.GetErrorY(i)
        ratioHist.SetBinContent(ratioHist.FindBin(x), y)
        ratioHist.SetBinError(ratioHist.FindBin(x), ey)


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
# pythiaHist2 = pythiaHist.Clone("pythiaHist2")
# pythiaHist2.Rebin(2)
# pythiaHist3 = pythiaHist2.Clone("pythiaHist3")
# pythiaHist3.Rebin(2)

# MGHist2 = MGHist.Clone("MGHist2")
# MGHist2.Rebin(2)
# MGHist3 = MGHist2.Clone("MGHist3")
# MGHist3.Rebin(2)

pythiaHist2 = inputHistRebin(pythiaHist)
pythiaHist3 = inputHistRebin(pythiaHist2)
MGHist2 = inputHistRebin(MGHist)
MGHist3 = inputHistRebin(MGHist2)


# Creating TRatioPlot(s)
# ratioPlot = TRatioPlot(pythiaHist, MGHist)
# ratioPlot.SetH2DrawOpt("hist")    #noconfint 
# ratioPlot.Draw()
# ratioPlot.GetLowerRefYaxis().SetRangeUser(-0.1,2.1)
# ratioPlot.GetLowerRefYaxis().SetTitle("ratio")
# ratioPlot.GetUpperRefYaxis().SetTitle("hists")

# ratioPlot2 = TRatioPlot(pythiaHist2, MGHist2)
# ratioPlot3 = TRatioPlot(pythiaHist3, MGHist3)


# FUNCTION FOR THIS STUFF (prior to for loop)
# Converting TRatioPlot to TGraph, then to TH1F histogram
#ratioTempGraph = ratioPlot.GetLowerRefGraph()
# ratioTempGraph2 = ratioPlot2.GetLowerRefGraph()
# ratioTempGraph3 = ratioPlot3.GetLowerRefGraph()

ratioTempGraph = ratioPlotConvert(pythiaHist, MGHist)
print ("maybe1",type (ratioTempGraph))
ratioTempGraph2 = ratioPlotConvert(pythiaHist2, MGHist2)
ratioTempGraph3 = ratioPlotConvert(pythiaHist3, MGHist3)

#numPoints = ratioTempGraph.GetN()
# xmin = TMath.MinElement(ratioTempGraph.GetN(), ratioTempGraph.GetX())
# xmax = TMath.MaxElement(ratioTempGraph.GetN(), ratioTempGraph.GetX())
#ratioHist = TH1F('ratioHist', '', numPoints + 1, float(xmin), float(xmax))
ratioHist = pythiaHist.Clone("ratioHist")
ratioHist.Reset()
ratioHist.SetLineColor(kBlue+1)
ratioHist.GetYaxis().SetTitle("ratio")

# numPoints = ratioTempGraph.GetN()
# for i in range (0, numPoints):
#     x , y = Double(), Double()
#     ratioTempGraph.GetPoint(i, x, y)
#     ey = ratioTempGraph.GetErrorY(i)
#     ratioHist1.SetBinContent(ratioHist1.FindBin(x), y)
#     ratioHist1.SetBinError(ratioHist1.FindBin(x), ey)

ratioHistFill(ratioTempGraph, ratioHist, 0, 200)
ratioHistFill(ratioTempGraph2, ratioHist, 200, 600)
ratioHistFill(ratioTempGraph3, ratioHist, 600, 3000)


# Plotting ratio histogram
canvas2 = TCanvas("canvas2")
canvas2.cd(0)
#ratioHist1.Draw()      # ("hist") for a straight line
ratioHist.GetYaxis().SetRangeUser(-0.1,2.1)
ratioHist.SetTitle("")
ratioHist.SetLineColor(kBlue+1)
ratioHist.GetXaxis().SetTitle('P_{T} [GeV]')
#xbins = ratioHist.GetNbinsX()


# Rebinning ratioHist twice
# ratioHist2 = ratioHist1.Clone("ratioHist2")
# ratioHist2.Rebin(2)
# ratioHist3 = ratioHist2.Clone("ratioHist3")
# ratioHist3.Rebin(2)


# Creating final ratioHist with variable binning
# ratioHistVarBin = ratioHist1.Clone("ratioHistVarBin")
# ratioHistVarBin.Reset()
# for i in range (0, 3000):
#     if i < 200:
#         y = ratioHist1.GetBinContent(i)
#         ey = ratioHist1.GetBinError(i)
#         ratioHistVarBin.SetBinContent(ratioHist1.FindBin(x), y)
#         ratioHistVarBin.SetBinError(ratioHist1.FindBin(x), ey)
#     elif i < 600:
#         y = ratioHist2.GetBinContent(i)
#         ey = ratioHist2.GetBinError(i)
#         ratioHistVarBin.SetBinContent(ratioHist2.FindBin(x), y)
#         ratioHistVarBin.SetBinError(ratioHist2.FindBin(x), ey)
#     elif i < 3000:
#         y = ratioHist3.GetBinContent(i)
#         ey = ratioHist3.GetBinError(i)
#         ratioHistVarBin.SetBinContent(ratioHist3.FindBin(x), y)
#         ratioHistVarBin.SetBinError(ratioHist3.FindBin(x), ey)

# ratioHistVarBin.Draw()


# Plotting each ratioHist (include section if checking)
#canvas2.Divide(1, 3)
#canvas2.cd(1)
ratioHist.Draw("hist")
#ratioHist.SetTitle("50 GeV bins")
ratioHist.GetXaxis().SetTitle('P_{T} [GeV]')

# LEGENDS AND PDFs CURRENTLY CAUSING SEGFAULT ISSUES

#canvas2.cd(2)
#ratioHist2.Draw()
#ratioHist2.SetTitle("100 GeV bins")

#canvas2.cd(3)
#ratioHist3.Draw()
#ratioHist3.SetTitle("200 GeV bins")
    

# Adding legends
# ratioPlot.GetUpperPad().cd()
# #canvas1.cd(0)
# legend1 = TLegend(0.3,0.7,0.7,0.9)
# a = legend1.SetHeader("Mass = " + mass + " GeV", "C")
# b = legend1.AddEntry(pythiaHist,"pythiaHist")
# c = legend1.AddEntry(MGHist,"MGHist")
# b.SetTextColor(kRed)
# c.SetTextColor(kBlue)
# legend1.Draw()

# canvas2.cd()
# legend2 = TLegend(0.3,0.84,0.7,0.9)
# d = legend2.SetHeader("Mass = " + mass + " GeV", "C")
# legend2.Draw()


# Closing and saving 2 pdfs (one for each canvas) 
# Saving one root file (for pythiaHist, MGHist, and ratioHist)
# canvas1.SaveAs(outputFilename + "_1.pdf")      # Causing seg fault?
# canvas2.SaveAs(outputFilename + "_2.pdf")
pythiaHist.Write("pythiaHist")
MGHist.Write("MGHist")
ratioHist.Write("ratioHist")
outputFile.Write()
outputFile.Close()



