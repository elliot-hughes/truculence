{
	const int FONTSCALE = 42;		// "4" is Helvetica ("5" is Helvetica italic), "2" is the precision (font size scales with pad).
	const float FONTSCALESIZE = 0.06;
	const int FONT = 43;		// "4" is Helvetica ("5" is Helvetica italic), "3" is the precision (font size is fixed in pixels).
	const float FONTSIZE = 50;
	
	gROOT->SetStyle("Plain");
	
	// Canvas: default plain and square
	gStyle->SetCanvasBorderMode(0);		// -1: down, 0: no border, 1: up
	gStyle->SetCanvasBorderSize(0);
	gStyle->SetCanvasColor(kWhite);
	gStyle->SetCanvasDefH(1000);		// Height of canvas
	gStyle->SetCanvasDefW(1000);		// Width of canvas
	
	// Pad and margins:
	gStyle->SetPadBorderMode(0);		// -1: down, 0: no border, 1: up
	gStyle->SetPadColor(kWhite);
	gStyle->SetPadBottomMargin(0.29);		// 161020: Used to be 0.18, but corrected for right margin change to keep a square.
	gStyle->SetPadTopMargin(0.07);
	gStyle->SetPadLeftMargin(0.17);
	gStyle->SetPadRightMargin(0.19);		// 161020: Used to be 0.08, but changed to accomodate powers of ten for large x-axis values.
	
	// Frames:
	/// Frames are the squares around plots, under the axes.
	gStyle->SetFrameLineWidth(1);
	gStyle->SetFrameLineColor(1);
	gStyle->SetFrameLineStyle(1);
	gStyle->SetFrameBorderMode(0);		// -1: down, 0: no border, 1: up
	gStyle->SetFrameBorderSize(0);
	gStyle->SetFrameFillColor(0);
	gStyle->SetFrameFillStyle(0);
	
	// Grid:
//	gStyle->SetPadGridX(false);
//	gStyle->SetPadGridY(false);
//	gStyle->SetGridColor(0);
//	gStyle->SetGridStyle(3);
//	gStyle->SetGridWidth(1);
	
	// Text:
	gStyle->SetTextFont(FONT);
	gStyle->SetTextSize(FONTSIZE);
	gStyle->SetTitleFont(FONT, "xyz");
	gStyle->SetTitleFont(FONT, "bla");
	gStyle->SetTitleSize(FONTSIZE, "xy");
	gStyle->SetTitleSize(FONTSIZE*0.87, "z");
	gStyle->SetLabelFont(FONT, "xyz");
	gStyle->SetLabelSize(FONTSIZE*0.83, "xyz");
	gStyle->SetLabelSize(FONTSIZE*0.67, "z");
	/// Plot titles:
	gStyle->SetTitleBorderSize(0);
//	gStyle->SetTitleColor(1);
//	gStyle->SetTitleAlign(13);
	gStyle->SetTitleX(0.00f);
	gStyle->SetTitleY(0.99);
	gStyle->SetTitleW(0.5);
	gStyle->SetTitleH(0.0);
	gStyle->SetTitleFontSize(FONTSCALESIZE*0.83);
//	gStyle->SetTitleY(1.0);
//	gStyle->SetTitleX(FONTSIZE);
	
	// Axes:
	gStyle->SetLabelOffset(0.015, "x");
	gStyle->SetLabelOffset(0.007, "yz");
	gStyle->SetTitleOffset(1.25, "x");
	gStyle->SetTitleOffset(1.6, "y");
	gStyle->SetTitleOffset(1.6, "z");
	
	// Statbox:
	gStyle->SetOptStat(1111110);		// "ksiourmen" (right-to-left)
	gStyle->SetStatFont(FONTSCALE);
	gStyle->SetStatFontSize(FONTSCALESIZE*0.67);
	gStyle->SetStatX(0.80);
	gStyle->SetStatY(0.80);
	gStyle->SetStatW(0.30);
	gStyle->SetStatH(0.50);
	gStyle->SetStatBorderSize(0);
	gStyle->SetStatColor(0);
	gStyle->SetStatStyle(0);
	
	// Histograms:
	gStyle->SetHistLineWidth(2);
	gStyle->SetHistFillColor(kRed-10);		// Salmon
	
	// Markers:
	gStyle->SetMarkerStyle(20);
	gStyle->SetMarkerSize(1.2);
	
	// Legend:
	gStyle->SetLegendBorderSize(0);
	gStyle->SetLegendFont(FONT);
	
	// Colors:
	Int_t MyPalette[100];
//	Double_t Red[]    = {0.0, 1.0};
//	Double_t Green[]  = {0.0, 0.0};
//	Double_t Blue[]   = {1.0, 0.0};
	Double_t Red[]    = {0.0, 0.0, 1.0};
	Double_t Green[]  = {0.0, 0.6, 1.0};
	Double_t Blue[]   = {0.4, 0.6, 0.0};
	Double_t Length[] = {0.0, 0.5, 1.0};
	Int_t FI = TColor::CreateGradientColorTable(3, Length, Red, Green, Blue, 100);
	for (int i=0;i<100;i++) MyPalette[i] = FI+i;
	gStyle->SetPalette(100, MyPalette);
//	gStyle->SetPalette(kViridis);
//	gStyle->SetPalette(71);		// Only starts working in ROOT 6.04
	
	gROOT->ForceStyle();
}
