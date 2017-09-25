TLatex* style_cms(int corner, bool pull=false) {
	TLatex* info_cms = new TLatex(0, 0, "#bf{CMS}");
	info_cms->SetNDC();		// Set text position to NDC coordinates.
//	info_cms->SetTextFont(42);
//	info_cms->SetTextSize(0.06);
	info_cms->SetTextFont(43);
	info_cms->SetTextSize(58);
	
	if (!pull) {
		if (corner == 0) {
			info_cms->SetX(0.21);
			info_cms->SetY(0.875);
		}
		else if (corner == 1) {
			info_cms->SetX(0.68);
			info_cms->SetY(0.875);
		}
		else if (corner == 2) {
			info_cms->SetX(0.68);
			info_cms->SetY(0.36);
		}
		else if (corner == 3) {
			info_cms->SetX(0.21);
			info_cms->SetY(0.36);
		}
		else if (corner == 4) {
			info_cms->SetTextSize(40);
			info_cms->SetX(0.285);
			info_cms->SetY(0.94);
		}
	}
	else {
		if (corner == 0) {
			info_cms->SetX(0.21);
			info_cms->SetY(0.86);
		}
		else if (corner == 1) {
			info_cms->SetX(0.68);
			info_cms->SetY(0.86);
		}
		else if (corner == 2) {
			info_cms->SetX(0.68);
			info_cms->SetY(0.37);
		}
		else if (corner == 3) {
			info_cms->SetX(0.21);
			info_cms->SetY(0.37);
		}
		else if (corner == 4) {
			info_cms->SetTextSize(40);
			info_cms->SetX(0.285);
			info_cms->SetY(0.945);
		}
	}
	
	return info_cms;
}

TLatex* style_lum(TString lum) {
	TLatex* info_lum = new TLatex(0, 0, lum + " fb^{-1} #scale[0.7]{(#sqrt{#it{s}} = 13 TeV)}");
	info_lum->SetNDC();
	info_lum->SetTextFont(43);
	info_lum->SetTextSize(30);
//	info_lum->SetTextFont(42);
//	info_lum->SetTextSize(0.04);
	info_lum->SetX(0.58);
	info_lum->SetY(0.94);
	
	return info_lum;
}

TLatex* style_ds_type(bool mc, int corner, bool pull) {
	TString ds = TString("#it{simulation}");
	if (not mc) ds = TString("#it{preliminary}");
	TLatex* info_ds = new TLatex(0, 0, ds);
	info_ds->SetNDC();
	info_ds->SetTextFont(43);
	info_ds->SetTextSize(30);
//	info_ds->SetTextFont(42);
//	info_ds->SetTextSize(0.035);
	if (!pull) {
		if (corner == 0) {
			info_ds->SetX(0.21);
			info_ds->SetY(0.84);
		}
		else if (corner == 1) {
			info_ds->SetX(0.67);
			if (not mc) info_ds->SetX(0.66);
			info_ds->SetY(0.84);
		}
		else if (corner == 2) {
			info_ds->SetX(0.67);
			if (not mc) info_ds->SetX(0.66);
			info_ds->SetY(0.33);
		}
		else if (corner == 3) {
			info_ds->SetX(0.21);
			info_ds->SetY(0.33);
		}
		else if (corner == 4) {
			info_ds->SetTextSize(25);
			info_ds->SetX(0.38);
			info_ds->SetY(0.94);
		}
	}
	else {
		if (corner == 0) {
			info_ds->SetX(0.21);
			info_ds->SetY(0.83);
		}
		else if (corner == 1) {
			info_ds->SetX(0.67);
			if (not mc) info_ds->SetX(0.658);
			info_ds->SetY(0.815);
		}
		else if (corner == 2) {
			info_ds->SetX(0.64);
			if (not mc) info_ds->SetX(0.62);
			info_ds->SetY(0.33);
		}
		else if (corner == 3) {
			info_ds->SetX(0.21);
			info_ds->SetY(0.33);
		}
		else if (corner == 4) {
			info_ds->SetTextSize(25);
			info_ds->SetX(0.38);
			info_ds->SetY(0.94);
		}
	}
	
	return info_ds;
}


vector<TLatex*> style_info(bool mc=true, TString lum="38.2", int corner=1, bool pull=false, double lumx=0.58, bool draw=true) {
	vector<TLatex*> results;
	results.push_back(style_cms(corner, pull));
	results.push_back(style_ds_type(mc, corner, pull));
	TLatex* lum_words = style_lum(lum);
	lum_words->SetX(lumx);
	results.push_back(lum_words);
	
	if (draw) {
		for (int i = 0; i < results.size(); i++) results[i]->Draw();
	}
	
	return results;
}


TLatex* style_write(TString text, double x=0.60, double y=0.78, double size=0.03, bool draw=true) {
	TLatex* ttext = new TLatex(0, 0, text);
	ttext->SetNDC();		// Set text position to NDC coordinates.
	ttext->SetX(x);
	ttext->SetY(y);
	ttext->SetTextFont(42);
	ttext->SetTextSize(size);
	if (draw) ttext->Draw();
	return ttext;
}

TLatex* style_write(vector<TString> texts, double x=0.60, double y=0.78, double size=0.03, bool draw=true) {
	TString text = texts[texts.size() - 1];
	for (unsigned i = texts.size() - 1; i-- > 0;) {
		text = "#splitline{" + texts[i] + "}{" + text + "}";
	}
	return style_write(text, x, y, size, draw);
	
//	TLatex* ttext = new TLatex(0, 0, text);
//	ttext->SetNDC();		// Set text position to NDC coordinates.
//	ttext->SetX(x);
//	ttext->SetY(y);
//	ttext->SetTextFont(42);
//	ttext->SetTextSize(size);
//	if (draw) ttext->Draw();
//	return ttext;
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
