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

SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
REGULAR_QUOTE = Literal(SINGLE_QUOTE) | Literal(DOUBLE_QUOTE)
TRIPLE_SINGLE_QUOTE = "'''"
TRIPLE_DOUBLE_QUOTE = '"""'
TRIPLE_QUOTE = Literal(TRIPLE_SINGLE_QUOTE) | Literal(TRIPLE_DOUBLE_QUOTE)

UNESCAPED_REGULAR_QUOTE = PrecededBy(CharsNotIn('\\')) + REGULAR_QUOTE
UNESCAPED_TRIPLE_QUOTE = PrecededBy(CharsNotIn('\\')) + TRIPLE_QUOTE

UNESCAPED_QUOTE = ( UNESCAPED_TRIPLE_QUOTE 
                  | UNESCAPED_REGULAR_QUOTE )
NOTQUOTE = CharsNotIn(SINGLE_QUOTE + DOUBLE_QUOTE)

p_pyexec_start = Literal(r'\begin{pyexec}')
p_pyexec_end   = Literal(r'\end{pyexec}')
p_pyeval_start = Literal(r'\pyeval')

p_closed_brace_text = Forward()
p_closed_brace_text << ( ZeroOrMore( Optional(NOTBRACE)
                                    + LBRACE
                                    + p_closed_brace_text
                                    + RBRACE )
                        + Optional(NOTBRACE) )
p_closed_brace_text = Combine(p_closed_brace_text)


# need to add support for single quote and triple quote recognition, as well
# as escaped quote recognition
p_even_quote_amt = ( ZeroOrMore( Optional(NOTQUOTE)
                               + UNESCAPED_QUOTE
                               + Optional(NOTQUOTE)
                               + UNESCAPED_QUOTE )
                   + NOTQUOTE )

# NOTQUOTED(py_exec
# Combine(
p_pyexec = ( p_pyexec_start
           + Combine(Optional( p_even_quote_amt
                             + p_pyexec_end
                             + p_even_quote_amt ))       ('value')
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
