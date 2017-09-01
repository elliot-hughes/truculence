####################################################################
# Type: SCRIPT                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
# :IMPORTS

# CLASSES:
# :CLASSES

# VARIABLES:
# :VARIABLES

# FUNCTIONS:
#def order_theta_to_minuit(mat):
#	for row in mat:
#		for value in row:

def cov_to_cor(cov):
	cor = cov
	for i, row in enumerate(cov):
		for j, value in enumerate(row):
			cor[i][j] = cov[i][j]/(cov[i][i]*cov[j][j])**(0.5)
	return cor
# :FUNCTIONS
