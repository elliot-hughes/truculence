#include "styling_tools/styling_tools.cc"

void example_styling() {
	gStyle->SetOptStat(0);		// Remove the statbox.
	
	TH1F* h1 = new TH1F("h1", "h1 title", 20, -4, 6);
	h1->FillRandom("gaus", 2000);
	TH1F* h2 = new TH1F("h2", "h2 title", 20, -5, 5);
	for (int i = 0; i < 1000; i++) h2->Fill(gRandom->Gaus(0,2) + 1);
	
	// Basic styling:
	h1->SetTitle("");		// Remove h1's title. Generally titles are too ugly.
	h1->SetLineWidth(2);
	h1->SetFillColor(kRed - 4);
	h1->SetFillStyle(3003);
	h1->GetXaxis()->SetNdivisions(406);
	h1->GetXaxis()->SetTitle("Something (units)");
	style_ylabel_th1(h1, "units");		// Add h1's y-axis label. (Uses a custom styling function.)
	h2->SetLineWidth(2);
	h2->SetLineStyle(2);
	h2->SetFillStyle(0);
	
	// Draw things:
	h1->Draw();
	h2->Draw("same");
	style_info(false);		// Write some basic info on the canvas.
	
	
	// Make a legend:
	TLegend* leg = new TLegend(0.50, 0.65, 0.80, 0.80);
	leg->AddEntry(h1, "A gaussian", "fl");
	leg->AddEntry(h2, "Another gaussian", "lf");
	leg->Draw();
}
