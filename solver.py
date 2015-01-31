import numpy as np
from scipy.stats import norm

def step1(p0, context, symbol):
    text = "1-proportion \\(z\\) test for \\(p\\) = proportion of %s.\n\n" % (context,)
    text += "\\(H_0\\): \\(p = %.5f\\)\n\n" % (p0,)
    text += "\\(H_a\\): \\( p %s %.5f\\)\n\n" % (symbol, p0)
    return text


def step2(p0, samp_size, context):
  text = "\\textbf{Conditions}\n\n"
  text += "\\begin{enumerate}\n"
  text += "\\item Random Sample (Stated)\n"
  text += "\\item %d < 10 percent of %s\n" % (samp_size, context)
  text += "\\item \\(np_0 = (%d)(%.5f) = %.2f \\geq 10\\)\n\n" % (samp_size, p0, samp_size * p0)
  text += "\\(nq_0 = (%d)(%.5f) = %.2f \\geq 10\\)\n" % (samp_size, 1 - p0, samp_size * (1 - p0))
  text += "\\end{enumerate}"
  return text


def step3(p0, samp_size):
    text = 'The distribution of \(\hat{p}\) is approximately given by' + "\n"
    text += "\\[ N\\left(%.5f, \\sqrt{\\frac{(%.5f)(%.5f)}{%d}} \\approx %.6f\\right)\\]\n\n" \
                % (p0, p0, 1 - p0, samp_size, np.sqrt(p0 * (1 - p0) / samp_size))
    return text

def step4(p0, ps, samp_size, sig_level, diagram_type="one_sided_right"):
    sigma = np.sqrt(p0 * (1 - p0) / samp_size)
    text = "\\includegraphics[scale=.25]{diagram}\n"
    zscore = (ps - p0) / sigma
    rv = norm()
    text += "\\[z = \\frac{%.5f - %.5f}{%.6f} = %.4f\\]\n" % (ps, p0, sigma, zscore)
    pvalue = 0.0
    prob = 0.0
    raster_symbol = ">"
    if diagram_type == 'one_sided_right':
        prob = 1 - rv.cdf(zscore)
        pvalue = prob
    text += "\\[ P(\\hat{p} %s %.5f) = %.7f\\]\n" % (raster_symbol, ps, prob)
    symbol = '>' if pvalue >= sig_level else '<'
    text += "\\[ \\text{p-value} = %.7f %s %.2f = \\alpha\\]" % (pvalue, symbol, sig_level)
    return (text, pvalue, pvalue <= sig_level)

def step5(p0, context, low_enough, diagram_type="one_sided_right"):
    if not low_enough:
        text = "With such a high p-value, I fail to reject the null hypothesis that the proportion of %s is actually %.5f" \
                % (context, p0)
        return (text + "\n\n")

    text = "With such a low p-value, I reject the null hypothesis that the proportion of %s " + \
            "is actually %.5f in favor of the alternative hypothesis that it is %s.\n\n"
    dict_values = {
        'one_sided_right': 'more',
        'one_sided_left': 'left',
        'two_sided': 'different'
    }
    text = text % (context, p0, dict_values[diagram_type])
    return text


