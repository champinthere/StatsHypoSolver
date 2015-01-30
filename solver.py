import numpy as np
import scipy as sp

def step2(p0, samp_size, context):
  text = "Conditions\n\n"
  text += "\\begin{enumerate}\n"
  text += "\\item Random Sample (Stated)\n"
  text += "\\item %d < 10 percent of %s\n" % (samp_size, context)
  text += "\\item \(np_0 = "
