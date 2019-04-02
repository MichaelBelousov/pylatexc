
from . import *
from textwrap import dedent
from itertools import repeat

def spaced_data_to_matrix(data, x, y, row_alter = lambda t: t):
    return [row_alter(data.split()[0+i*x:(1+i)*x]) for i in range(y)]
    # return ' \\\\\n'.join( (' & '.join(map(str, row)) for row in read) )

def make_tabular(data, labels, form=lambda t: t):

    TAB, NL, end = ' '*4, '\n', r' \\'

    data = [[str(form(x)) for x in row] for row in data]

    return dedent(f"""\
    \\begin{{tabular}} {{ {'|l'+'c'.join(('|',)*len(data[0]))} }}
        \\hline
    { TAB+' & '.join(map(str, labels))+end }
        \\hline
    {NL.join((TAB+' & '.join(map(str, d))+end for d in data))}
        \\hline
    \\end{{tabular}}""")

def print_tabular(data, labels, form=lambda t: t):

    TAB, NL, end = ' '*4, '\n', r' \\'

    data = [[str(form(x)) for x in row] for row in data]

    print(f"""\
\\begin{{tabular}} {{ {'|l'+'c'.join(('|',)*len(data[0]))} }}
    \\hline
{ TAB+' & '.join(map(str, labels))+end }
    \\hline
{NL.join((TAB+' & '.join(map(str, d))+end for d in data))}
    \\hline
\\end{{tabular}}
""")

    for i, label in enumerate(labels[1:]):

        i = i+1
        columns = list(zip(*data))
        curcol = columns[i]
        indepcol = columns[0]

        coords = ' '.join(map(
            lambda t: repr(tuple((float(i) for i in t))), 
            zip(indepcol, curcol)))

        print(f"""\
\\begin{{tikzpicture}}
    \\begin{{axis}}[
        xlabel={{ {labels[0]} }},
        ylabel={{ {label} }}]
        \\addplot[color=blue,mark=x]
            coordinates {{ {coords} }}; 
    \\end{{axis}}
\\end{{tikzpicture}}
""")

