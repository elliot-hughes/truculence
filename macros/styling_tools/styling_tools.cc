vector<TLatex*> style_info(bool mc=true, TString lum="31.3", int corner=1, bool draw=true) {
	// "CMS" word:
	TLatex* info_cms = new TLatex(0, 0, "#bf{CMS}");
	info_cms->SetNDC();		// Set text position to NDC coordinates.
	info_cms->SetTextSize(0.06);
	if (corner == 0) {
		info_cms->SetX(0.21);
		info_cms->SetY(0.87);
	}
	else if (corner == 1) {
		info_cms->SetX(0.68);
		info_cms->SetY(0.87);
	}
	else if (corner == 2) {
		info_cms->SetX(0.68);
		info_cms->SetY(0.37);
	}
	else if (corner == 4) {
		info_cms->SetTextSize(0.05);
		info_cms->SetX(0.27);
		info_cms->SetY(0.945);
	}
	
	// Dataset word:
	TString ds = TString("#it{simulation}");
	if (not mc) ds = TString("#it{preliminary}");
	TLatex* info_ds = new TLatex(0, 0, ds);
	info_ds->SetNDC();
	info_ds->SetTextSize(0.035);
	if (corner == 0) {
		info_ds->SetX(0.21);
		info_ds->SetY(0.83);
	}
	else if (corner == 1) {
		info_ds->SetX(0.65);
		if (not mc) info_ds->SetX(0.64);
		info_ds->SetY(0.83);
	}
	else if (corner == 2) {
		info_ds->SetX(0.64);
		if (not mc) info_ds->SetX(0.62);
		info_ds->SetY(0.33);
	}
	else if (corner == 4) {
		info_ds->SetTextSize(0.025);
		info_ds->SetX(0.38);
		info_ds->SetY(0.945);
	}
	
	// Luminosity information:
	TLatex* info_lum = new TLatex(0, 0, lum + " fb^{-1} #scale[0.6]{(#sqrt{#it{s}} = 13 TeV)}");
	info_lum->SetNDC();
	info_lum->SetTextSize(0.04);
	info_lum->SetX(0.54);
	info_lum->SetY(0.945);
	
	vector<TLatex*> results;
	results.push_back(info_cms);
	results.push_back(info_ds);
	results.push_back(info_lum);
	
	if (draw) {
		for (int i = 0; i < results.size(); i++) results[i]->Draw();
	}
	
	return results;
}

TLatex* style_write(TString text, double x=0.60, double y=0.75, bool draw=true) {
	TLatex* ttext = new TLatex(0, 0, text);
	ttext->SetNDC();		// Set text position to NDC coordinates.
	ttext->SetX(x);
	ttext->SetY(y);
	ttext->SetTextSize(0.04);
	if (draw) ttext->Draw();
	return ttext;
}


void style_ylabel(THStack* h, TString xunit="GeV", TString yunit="Events") {
	std::ostringstream oss;
	oss << yunit << "/" << h->GetXaxis()->GetBinWidth(1) << " " << xunit;
	h->GetYaxis()->SetTitle(oss.str().c_str());
}
void style_ylabel(TH1* h, TString xunit="GeV", TString yunit="Events") {
	std::ostringstream oss;
	oss << yunit << "/" << h->GetXaxis()->GetBinWidth(1) << " " << xunit;
	h->GetYaxis()->SetTitle(oss.str().c_str());
}

void style_zlabel(TH2* h2, TString xunit="GeV", TString yunit="") {
	std::ostringstream oss;
	oss << "Events/" << h2->GetXaxis()->GetBinWidth(1) << " " << xunit << " x " << h2->GetYaxis()->GetBinWidth(1) << " " << yunit;
	h2->GetZaxis()->SetTitle(oss.str().c_str());
}

void style_ylabel_th1(TH1* h1, TString xunit="GeV") {
	std::ostringstream oss;
	oss << "Events/" << h1->GetXaxis()->GetBinWidth(1) << " " << xunit;
	h1->GetYaxis()->SetTitle(oss.str().c_str());
}
