import os
import glob

# The following allows a "from truculence *" to work:
modules = glob.glob(os.path.dirname(__file__) + "/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules]
__all__.extend([
	"crab",
	"physics",
])
