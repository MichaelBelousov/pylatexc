#/usr/bin/env python3

"""
evaluate pyexec and pyeval environments and macros in LaTeX code
to formatted values.

I was going to use pyparsing for the parsing, but I found it
unsuited for text templating, I probably should have gone with
jinja2 to be completely honest
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


class ParseException(Exception):
    """an exception that ocurred during parsing at a location"""
    def __init__(self, src, desc, loc):
        # minimum of 0
        zclamp = lambda t: max(0, t)
        # maximum of src size
        mclamp = lambda t: min(t, len(src))
        nl_chr = '\n'
        nl_lit = r'\n'
        super().__init__(dedent(f"""
            {desc}: discovered at location {loc}
            { src[zclamp(loc-10):mclamp(loc+10)]
                .replace(nl_chr, nl_lit) }
            { (loc-zclamp(loc-9))*' '+'^'+' '*(mclamp(loc+10)-loc) }
            """))

def main():
    """run the pytex source transformer"""

    doc_scope = {}
    out_text = ''

    src = sys.stdin.read()
    limit = len(src)

    last = 0
    i = 0
    while i < limit:
        if src[i:i+len(BEGIN_PYEXEC)] == BEGIN_PYEXEC:
            out_text += src[last:i]
            nxt = consume_pyexec(i, src, doc_scope)
            i = last = nxt
        elif src[i:i+len(PYEVAL)] == PYEVAL:
            out_text += src[last:i]
            nxt, out = consume_pyeval(i, src, doc_scope)
            out_text += str(out)
            i = last = nxt
        else:
            i += 1
        # TODO: should be faster to find the next occurrence of
        # either indicator via find? (at least just clearer)
    out_text += src[last:i]
    sys.stdout.write(out_text)


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
        return result

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

    raise ParseException(text, 'Unterminated Quote', cursor)


def skip_comment(cursor: int, text: str) -> int:
    """
    returns the index after a comment in a text, by skipping
    to the next line, assuming that the cursor is at the
    beginning of the comment.
    """
    limit = len(text)
    i = cursor
    while i < limit:
        was_newline = text[i] == '\n'
        i += 1
        if was_newline:
            break
    return i;


def consume_pyexec(cursor: int, text: str,
                   exec_scope: dict) -> int:
    i = cursor
    limit = len(text)
    while i < limit:
        if text[i] in ('"', "'"):
            i = skip_quote(i, text)
        elif text[i] == '#':
            i = skip_comment(i, text)
        elif text[i:i+len(END_PYEXEC)] == END_PYEXEC:
            exec(dedent(text[cursor+len(BEGIN_PYEXEC):i]),
                 exec_scope)
            return i + len(END_PYEXEC)
        else:
            i += 1
    # should never reach here
    raise ParseException(text, 'Unterminated Pyexec Expression',
                         cursor)

def consume_pyeval(cursor: int, text: str,
                   eval_scope: dict) -> (int, str):
    """
    returns first the index after a pyeval expression in a text,
    assuming the cursor is the next location from the opening, and
    then the output of the evaluation
    """
    limit = len(text)
    i = cursor + len(PYEVAL)
    openers_stack = [i-1]
    while i < limit:
        if not openers_stack:
            return i, eval(text[cursor+len(PYEVAL):i-1].strip(),
                           eval_scope)
        if text[i] == '{':
            openers_stack.append(i)
        if text[i] == '}':
            openers_stack.pop()
        i += 1

    # should never reach here
    raise ParseException(text, 'Unterminated Brace Expression',
                         openers_stack.pop())


if __name__ == '__main__':
    main()
