#/usr/bin/env python3

"""
evaluate pyexec and pyeval environments and macros in LaTeX code
to formatted values.

I was going to use pyparsing for the parsing, but I found it
unsuited for full text grabbing.
"""

import sys
import os
sys.path.insert(0, '../../')  # this is blasphemous
# from pyparsing import *  # I'm sorry PEP for I have sinned
import re
from textwrap import dedent

BEGIN_PYEXEC = r'\begin{pyexec}'
END_PYEXEC   = r'\end{pyexec}'
PYEVAL = r'\pyeval{'

out_text = ''

def main():
    exec_scope = {}

    src = sys.stdin.read()
    limit = len(src)
    start_loc = 0
    i = 0
    while i < limit:
        if src[i:i+len(BEGIN_PYEXEC)] == BEGIN_PYEXEC:
            nxt = consume_pyexec(i, src)
            out_text += src[i:nxt]
            i = nxt
        elif src[i:i+len(PYEVAL)] == PYEVAL:
            nxt, out = consume_pyeval(i, src)
            out_text += out + src[i:nxt]
            i = nxt
        i += 1
        # TODO: might be faster to find the next occurrence of
        # either


def skip_quote(cursor: int, text: str, indicator: str) -> int:
    """
    returns the index after a quote in a text, assuming the
    cursor is at the beginning of the quote, and the quote
    is indicated by an indicator string (i.e. ',",\"\"\",''')
    """
    pass

def skip_comment(cursor: int, text: str,
                 indicators: str = '#') -> int:
    """
    returns the index after a comment in a text, assuming the
    cursor is at the beginning of the comment, and the comment
    is indicated by an indicator string, '#'
    """
    pass

def consume_pyexec(cursor: int, text: str) -> int:
    i = cursor
    while i < len(text):
        if text[i] in ('"', "'"):
            i = skip_quote(i, src)
    return i

def consume_pyeval(cursor: int, text: str) -> (int, str):
    """
    returns first the index after a pyeval expression in a text,
    assuming the cursor is the next location from the opening, and
    then the output of the evaluation
    """
    pass

if __name__ == '__main__':
    main()
