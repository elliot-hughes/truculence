vector<TString> list_tfile(TFile* tf) {
	vector<TString> list;
	TList* tl = tf->GetListOfKeys();
	for(const auto&& obj: *tl) list.push_back(TString(obj->GetName()));
	return list;
}

void normalize_th1(TH1* h) {
	h->Scale(1/h->Integral(0, h->GetNbinsX() + 1));
}
