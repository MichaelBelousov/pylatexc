#/usr/bin/env python3

"""
evaluate pyexec and pyeval environments and macros in LaTeX code
to formatted values.
"""

# FIXME: replace with proper grammar via pyparsing
# this current 'solution' is extremely naive

import sys
import os
import re
from textwrap import dedent
from pyparsing import *

##### Parser #####

LBRACE = '{'
RBRACE = '}'
NOTBRACE = CharsNotIn(LBRACE + RBRACE)
BSLASH = '\\'

p_single_quote_str = QuotedString("'", escChar=BSLASH, unquoteResults=False)
p_double_quote_str = QuotedString('"', escChar=BSLASH, unquoteResults=False)
p_triple_single_quote_str = QuotedString("'''", escChar=BSLASH, unquoteResults=False)
p_triple_double_quote_str = QuotedString('"""', escChar=BSLASH, unquoteResults=False)

# XXX: this one might not be necessary...
# a section of text where all recursive braced sections end, indicating
# valid python code
p_closed_brace_text = Forward()
p_closed_brace_text << ( ZeroOrMore( Optional(NOTBRACE)
                                    + LBRACE
                                    + p_closed_brace_text
                                    + RBRACE )
                        + Optional(NOTBRACE) )
p_closed_brace_text = Combine(p_closed_brace_text)


SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
# a section of text where all quoted literals end, indicating
# valid python code
p_closed_quote_text = Combine(
                        ZeroOrMore( Optional(CharsNotIn(SINGLE_QUOTE + DOUBLE_QUOTE))
                                  + ( p_triple_single_quote_str
                                    | p_triple_double_quote_str
                                    | p_single_quote_str
                                    | p_double_quote_str ) )
                        + Optional(CharsNotIn('\'"')) )


p_pyexec_start = Literal(r'\begin{pyexec}')
p_pyexec_end   = Literal(r'\end{pyexec}')
p_pyeval_start = Literal(r'\pyeval')

# Combine(
p_pyexec = ( p_pyexec_start
           + Combine(Optional( p_closed_quote_text
                             + p_pyexec_end
                             + p_closed_quote_text ))       ('value')
           + p_pyexec_end )


p_pyeval = ( p_pyeval_start
           + LBRACE
           + Combine(p_closed_brace_text)                ('value')
           + RBRACE )


def main():

    src = sys.stdin.read()
    scope = {}

    # naive pyexec
    def pyexec(match):
        code = dedent(match[1])
        exec(code, scope)
        return ''

    src = re.sub(r'\\begin\{pyexec\}((.|\n)*?)\\end\{pyexec\}',
                 pyexec, src, flags=re.MULTILINE)

    # naive escaped pyeval
    def pyeval(match):
        code = match[1].replace(r'\}','}')
        return str(eval(code, scope))

    src = re.sub(r'\\pyeval\{(.*?)(?<!\\)\}',
                 pyeval, src, flags=re.MULTILINE)

    print(src)

if __name__ == '__main__':
    main()
