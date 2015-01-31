import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time, os, solver

mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'

def sh(somefloat):
    return "%.3f" % somefloat

def normalDiagram(mean, sample, diagram_type='one_sided_right'):
    x = np.arange(-3, 3, .01)
    y = np.exp(-(x ** 2) / 2) / np.sqrt(2 * np.pi)
    plt.figure(1, figsize=(2.5, 2))
    plt.plot(x, y, color='0.19')
    frame = plt.gca()
    frame.spines['right'].set_visible(False)
    frame.spines['left'].set_visible(False)
    frame.spines['top'].set_visible(False)
    frame.xaxis.set_ticks_position('bottom')
    frame.axes.get_yaxis().set_ticks([])
    frame.axes.get_xaxis().set_label_text("$\hat{p}$")
    shade_color = '#99bbee'
    
    tail_constant = .28
    left_tail_value = -3 + tail_constant * 6
    left_tail_cutoff = int(len(x) * tail_constant)
    right_tail_value = -3 + (1 - tail_constant) * 6
    right_tail_cutoff = int(len(x) * (1 - tail_constant))

    if diagram_type == 'one_sided_left':
        plt.xticks((left_tail_value, 0), (sh(sample), sh(mean)), fontsize="10")
        plt.fill_between(x[:left_tail_cutoff], y[:left_tail_cutoff], color=shade_color)

    elif diagram_type == 'one_sided_right':
        plt.xticks((0, right_tail_value), (sh(mean), sh(sample)), fontsize="10") 
        plt.fill_between(x[right_tail_cutoff:], y[right_tail_cutoff:], color=shade_color)
    
    elif diagram_type == 'two_sided':
        sample_left = min([sample, 2 * mean - sample])
        sample_right = max([sample, 2 * mean - sample])
        plt.xticks((left_tail_value, 0, right_tail_value),
                (sh(sample_left), sh(mean), sh(sample_right)), fontsize="10")
        plt.fill_between(x[:left_tail_cutoff], y[:left_tail_cutoff], color=shade_color)
        plt.fill_between(x[right_tail_cutoff:], y[right_tail_cutoff:], color=shade_color)

    plt.savefig("diagram.png")
    plt.close()

latexHeader = '''
\\documentclass[10pt]{article}
\\usepackage{lmodern}
\\usepackage[margin=.8in]{geometry}
\\usepackage[T1]{fontenc}
\\usepackage{amsmath}
\\linespread{1.17}
\\usepackage{graphicx}
\\usepackage{multicol}
\\begin{document}
\\begin{multicols}{2}
'''

def init():
    result = ''
    result += latexHeader
    alpha = float(input('significance level: '))
    context = input('p = proportion of: ')
    context_pop = input('population of: ')
    p0 = float(input('p0 is: '))
    ps = float(input('sample p is: '))
    samp_size = int(input('sample size: '))
    h_type = input('hypothesis type (greater, lesser, neq): ')
    d_type = {
        'greater': 'one_sided_right',
        'lesser': 'one_sided_left',
        'neq': 'two_sided'
    }
    symbol_type = {
        'greater': '>',
        'lesser': '<',
        'neq': "\\neq"
    }
    normalDiagram(p0, ps, diagram_type=d_type[h_type])
    result += solver.step1(p0, context, symbol_type[h_type])
    result += solver.step2(p0, samp_size, context_pop)
    result += solver.step3(p0, samp_size)
    text, pvalue, low_enough = solver.step4(p0, ps, samp_size, alpha, diagram_type=d_type[h_type])
    result += "\n\\columnbreak\n"
    result += "\\textbf{Calculations}\n\n"
    result += text
    result += solver.step5(p0, context, low_enough, diagram_type=d_type[h_type])
    result += "\n\\end{multicols}\n\\end{document}"
    output_file = open('product.ltx', 'w')
    output_file.write(result)
    output_file.close()
    os.system('pdflatex product.ltx')
    time.sleep(2)
    os.system('open product.pdf')

if __name__ == '__main__':
    init()
