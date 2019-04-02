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
from pyparsing import Optional as Opt

##### Parser #####


LBRACE = '{'
RBRACE = '}'
NOTBRACE = CharsNotIn(LBRACE + RBRACE)

BSLASH = '\\'
NOTBSLASH = CharsNotIn(BSLASH)

SINGLEQUOTE = "'"
DOUBLEQUOTE = '"'
NOTQUOTE = CharsNotIn(SINGLEQUOTE + DOUBLEQUOTE)


p_single_quote_str        = QuotedString("'",   escChar=BSLASH, unquoteResults=False)
p_double_quote_str        = QuotedString('"',   escChar=BSLASH, unquoteResults=False)
p_triple_single_quote_str = QuotedString("'''", escChar=BSLASH, unquoteResults=False)
p_triple_double_quote_str = QuotedString('"""', escChar=BSLASH, unquoteResults=False)

p_string_literal = ( p_triple_single_quote_str
                   | p_triple_double_quote_str
                   | p_single_quote_str
                   | p_double_quote_str )

p_python_ignore = ( p_string_literal
                  | pythonStyleComment)

# a section of text where all recursive braced sections end, indicating
# that a \pyeval{ {1,2,3,{4,5}},{6,7} } expression can be ended
p_closed_brace_text = Forward()
p_closed_brace_text << Combine(
                        ( ZeroOrMore( Opt(NOTBRACE)
                                    + LBRACE
                                    + p_closed_brace_text
                                    + RBRACE )
                        + Opt(NOTBRACE) )
                       .ignore(p_python_ignore))


p_pyexec_begin = r'\begin{pyexec}'
p_pyexec_end   = r'\end{pyexec}'
p_pyeval = r'\pyeval'

# TODO: SkipTo(X|Y) + ((X + ...) | (Y + ...))

p_pyexec_content = (OneOrMore(~p_python_ignore +  
        ~Literal(p_pyexec_begin) + ~Literal(p_pyexec_end) + 
        White(exact=1)|Word(printables,exact=1)) 
        )#.setParseAction(lambda t:t[0].strip())) 


p_pyexec = Combine(nestedExpr(p_pyexec_begin,
                              p_pyexec_end,
                              content=p_pyexec_content,
                              ignoreExpr=p_python_ignore))


p_pyeval = ( p_pyeval + LBRACE
           + p_closed_brace_text   ('val')
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
