void legend() {return;}

TLegend* get_legend(int corner=1, int entries=4, double yscale=1.0, double xscale=1.0, bool pull=false) {
	double height = 0.05*entries*yscale;
	double yadjust = 0;
	if (pull) yadjust -= 0.03;
	TLegend* leg;
	if (corner == 0) leg = new TLegend(0.20, 0.92-height, 0.40, 0.92);			// 0: Top-left
	else if (corner == 1) leg = new TLegend(0.59*xscale, 0.83-height+yadjust, 0.80, 0.83+yadjust);		// 1: Top-right
	else if (corner == 2) leg = new TLegend(0.59, 0.66, 0.80, 0.83);			// 2: Bottom-right
	else if (corner == 3) leg = new TLegend(0.59, 0.66, 0.80, 0.83);			// 3: Bottom-left
		
	leg->SetFillColor(0);
	return leg;
}
