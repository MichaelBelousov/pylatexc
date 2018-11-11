#/usr/bin/env python3

"""
evaluate pyexec and pyeval environments and macros in LaTeX code
to formatted values.
"""

# FIXME: replace with proper grammar via pyparsing
# this current 'solution' is extremely naive

import sys
from pyparsing import *  # I'm sorry PEP for I have sinned
import re
from textwrap import dedent

scope = {}

src = sys.stdin.read()

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
