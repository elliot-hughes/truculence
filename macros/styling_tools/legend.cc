void legend() {return;}

TLegend* get_legend(int corner=1, int entries=4, double scale = 1.0) {
	double height = 0.05*entries*scale;
	TLegend* leg;
	if (corner == 0) leg = new TLegend(0.20, 0.92-height, 0.40, 0.92);			// 0: Top-left
	else if (corner == 1) leg = new TLegend(0.59, 0.83-height, 0.80, 0.83);		// 1: Top-right
	else if (corner == 2) leg = new TLegend(0.59, 0.66, 0.80, 0.83);			// 2: Bottom-right
	else if (corner == 3) leg = new TLegend(0.59, 0.66, 0.80, 0.83);			// 3: Bottom-left
		
	leg->SetFillColor(0);
	return leg;
}
