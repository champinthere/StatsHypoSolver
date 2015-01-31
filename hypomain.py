import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'

def normalDiagram(mean, sample, diagram_type='one_sided_right'):
    x = np.arange(-3, 3, .01)
    y = np.exp(-(x ** 2) / 2) / np.sqrt(2 * np.pi)
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
        plt.xticks((left_tail_value, 0), (sample, mean), fontsize="13")
        plt.fill_between(x[:left_tail_cutoff], y[:left_tail_cutoff], color=shade_color)

    elif diagram_type == 'one_sided_right':
        plt.xticks((0, right_tail_value), (mean, sample), fontsize="13") 
        plt.fill_between(x[right_tail_cutoff:], y[right_tail_cutoff:], color=shade_color)

    # plt.xticks((0, xvalue), (.746, .831), fontsize="13")
    # cutoff = int(len(x) * .72)
    # plt.fill_between(x[cutoff:], y[cutoff:], color='#99bbee')

    plt.savefig("diagram.png")
    plt.close()

latexHeader = '''
\\documentclass[11pt]{article}
\\usepackage{lmodern}
\\usepackage[T1]{fontenc}
\\usepackage{amsmath}
\\linespread{1.25}
\\usepackage{graphicx}
\\usepackage{multicols}
\\begin{document}
'''

def init():
    result = ''
    result += latexHeader
    alpha = input('significance level: ')
    context = input('p = proportion of: ')
    p0 = float(input('p0 is: '))
    ps = float(input('sample p is: '))
    samp_size = int(input('sample size: '))
    h_type = input('hypothesis type (greater, lesser, neq): ')
    d_type = {
        'greater': 'one_sided_right',
        'less': 'one_sided_left',
        'neq': 'two_sided'
    }
    symbol_type = {
        'greater': '>',
        'less': '<',
        'neq': "\\neq"
    }
    normalDiagram(p0, ps, diagram_type=d_type[h_type])
    result += '\end{document}'
