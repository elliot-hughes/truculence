// Get a list of all tobject names in the top directory of a TFile:
vector<TString> list_tfile(TFile* tf) {
	vector<TString> list, list_norepeat;
	TList* tl = tf->GetListOfKeys();
	for(const auto&& obj: *tl) list.push_back(TString(obj->GetName()));
	
	// Get rid of duplicate entries:
	// (Probably could improve this with std::set.)
	for (unsigned i = 0; i < list.size(); ++ i) {
		bool repeat = false;
		if (list_norepeat.size() > 0) {
			for (unsigned j = 0; j < list_norepeat.size(); ++ j) {
				if (list[i] == list_norepeat[j]) repeat = true;
			}
		}
		if (!repeat) list_norepeat.push_back(list[i]);
	}
	
	return list_norepeat;
}


void normalize_th1(TH1* h) {
	h->Scale(1/h->Integral(0, h->GetNbinsX() + 1));
}

void zero_errors(TH1* h) {
	for (unsigned i = 0; i <= h->GetNbinsX() + 1; ++i) h->SetBinError(i, 0);
}

void save(TCanvas* tc) {
	tc->SaveAs(TString(tc->GetName()) + ".pdf");
}
