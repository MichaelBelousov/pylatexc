#/usr/bin/env python3

"""
evaluate pyexec and pyeval environments and macros in LaTeX code
to formatted values.

I was going to use pyparsing for the parsing, but I found it
unsuited for text templating
"""

# TODO: use python's six module so users can determine their python
# version by running this script in their own interpreter

import sys
import os
import re
from textwrap import dedent
import six


BEGIN_PYEXEC = r'\begin{pyexec}'
END_PYEXEC   = r'\end{pyexec}'
PYEVAL = r'\pyeval{'


class ParseException (Exception):
    """an exception that ocurred during parsing at a location"""
    def __init__(self, desc, loc):
        self.desc = desc
        self.loc = loc
    def __repr__(self):
        return f'{self.desc}: discovered at location {loc}'


def main():
    """run the pytex source transformer"""
    doc_scope = {}
    out_text = ''

    src = sys.stdin.read()
    limit = len(src)

    i = 0
    while i < limit:
        if src[i:i+len(BEGIN_PYEXEC)] == BEGIN_PYEXEC:
            nxt = consume_pyexec(i, src, doc_scope)
            out_text += src[i:nxt]
            i = nxt
        elif src[i:i+len(PYEVAL)] == PYEVAL:
            nxt, out = consume_pyeval(i, src, doc_scope)
            out_text += out + src[i:nxt]
            i = nxt
        else:
            i += 1
        # TODO: should be faster to find the next occurrence of
        # either indicator


def skip_quote(cursor: int, text: str) -> int:
    """
    returns the index after a quote in a text, assuming the
    cursor is at the beginning of the quote
    """

    limit = len(text)

    def determine_quote_type() -> str:
        first = text[cursor]
        result = first
        i = cursor + 1
        while text[i] == first and i < limit:
            result += text[i]
            i += 1

    indicator = determine_quote_type()

    def is_escaped(cursor: int) -> bool:
        if len(indicator) > 1:
            return False
        else:
            return text[cursor-1] == '\\'

    i = cursor + len(indicator)
    while i < limit:
        if (text[i:i+len(indicator)] == indicator
        and not is_escaped(i)):
            return i + len(indicator)
        i += 1

    raise ParseException('Unterminated Quote', cursor)


def skip_comment(cursor: int, text: str) -> int:
    """
    returns the index after a comment in a text, by skipping
    to the next line, assumiing that the cursor is at the
    beginning of the comment.
    """
    limit = len(text)
    while i < limit:
        was_newline = text[i] == '\n'
        i += 1
        if was_newline:
            break
    return i;


def consume_pyexec(cursor: int, text: str,
                   exec_scope: dict) -> int:
    i = cursor
    while i < len(text):
        if text[i] in ('"', "'"):
            i = skip_quote(i, src)
        elif text[i] == '#':
            i = skip_quote(i, src)
        elif text[i:i+len(END_PYEXEC)] == END_PYEXEC:
            exec(text[cursor:i], exec_scope)
            return i + len(END_PYEXEC)
        else:
            i += 1
    # should never reach here
    raise ParseException('Unterminated Pyexec Expression',
                         cursor)

def consume_pyeval(cursor: int, text: str,
                   eval_scope: dict) -> (int, str):
    """
    returns first the index after a pyeval expression in a text,
    assuming the cursor is the next location from the opening, and
    then the output of the evaluation
    """
    openers_stack = [i-1]
    i = cursor
    while i < limit:
        if not openers_stack:
            return i, eval(text[cursor:i], scope)
        if text[i] = '{':
            openers_stack.append(i)
        if text[i] = '}':
            openers_stack.pop()
        i += 1

    # should never reach here
    raise ParseException('Unterminated Brace Expression',
                         openers_stack.pop())


if __name__ == '__main__':
    main()
