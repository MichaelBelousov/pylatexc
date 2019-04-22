#/usr/bin/env python
"""
evaluate pyexec and pyeval environments and macros in LaTeX code
to formatted values
"""

import sys
import os
from textwrap import dedent
import six
import argparse

BEGIN_PYEXEC = r'\begin{pyexec}'
END_PYEXEC   = r'\end{pyexec}'
PYEVAL = r'\pyeval{'

# TODO: make a "fatal" error?

class PyTeXCSyntaxError(SyntaxError):
    """
    A PyTexC syntax error that ocurred during parsing
    at a location in the source text.
    """
    def __init__(self, src, desc, loc):
        # minimum of 0
        zclamp = lambda t: max(0, t)
        # maximum of src size
        mclamp = lambda t: min(t, len(src))
        msg = ('{err_desc}: discovered at line {lineno}, '
               'col {colno}.\n'
               '{line_visual}').format(err_desc=desc,
                                       **self.make_err_info(src, loc))
        super(SyntaxError, self).__init__(msg)
        sys.stderr.write(msg)
        # TODO: make a more appropriate separation for a program halting
        # error?
        sys.exit(1)

    @staticmethod
    def make_err_info(src, err_loc):
        """find information about a source syntax error"""
        lineno = src[:err_loc].count('\n')
        line = src.split('\n')[lineno]
        last_newline_loc = src.rfind('\n', 0, err_loc-1)
        colno = err_loc - last_newline_loc + 1
        return { 'line_visual': "{0}\n{1}^".format(line, colno*' '),
                 'lineno': lineno,
                 'colno': colno
               }

def main(infile, outfile):
    """run the PyTeXC source transformer"""

    doc_scope = {}
    out_text = ''

    src = infile.read()
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
        # maybe not if the loop is JITed
    out_text += src[last:i]
    outfile.write(out_text)


def skip_quote(cursor, text):
    """
    returns the index after a quote in a text, assuming the
    cursor is at the beginning of the quote
    """

    limit = len(text)

    def determine_quote_type():
        first = text[cursor]
        result = first
        i = cursor + 1
        while text[i] == first and i < limit:
            result += text[i]
            i += 1
        return result

    indicator = determine_quote_type()

    def is_escaped(cursor):
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

    raise PyTeXCSyntaxError(text, 'Unterminated Quote', cursor)


def skip_comment(cursor, text):
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


def consume_pyexec(cursor, text, exec_scope):
    i = cursor
    limit = len(text)
    while i < limit:
        if text[i] in ('"', "'"):
            i = skip_quote(i, text)
        elif text[i] == '#':
            i = skip_comment(i, text)
        elif text[i:i+len(END_PYEXEC)] == END_PYEXEC:
            six.exec_(dedent(text[cursor+len(BEGIN_PYEXEC):i]),
                      exec_scope)
            return i + len(END_PYEXEC)
        else:
            i += 1
    # should never reach here
    raise PyTeXCSyntaxError(text, 'Unterminated Pyexec Expression',
                            cursor)

def consume_pyeval(cursor, text, eval_scope):
    """
    returns in a tuple first the index after a pyeval expression in
    a text, assuming the cursor is the next location from the opening,
    and then the output of the evaluation
    """
    limit = len(text)
    i = cursor + len(PYEVAL)
    openers_stack = [i-1]
    while i < limit:
        if not openers_stack:
            return i, eval(text[cursor+len(PYEVAL):i-1].strip(),
                           eval_scope)
        if text[i] in ('"', "'"):
            i = skip_quote(i, text)
        else:
            if text[i] == '{':
                openers_stack.append(i)
            elif text[i] == '}':
                openers_stack.pop()
            i += 1

    # should never reach here
    raise PyTeXCSyntaxError(text, 'Unterminated Brace Expression',
                            openers_stack.pop())


if __name__ == '__main__':
    # TODO: validate arguments to these macros
    parser = argparse.ArgumentParser(
            description='pylatexc, a pylatex file evaluator')
    parser.add_argument(
	'-i', '--input-file', default=sys.stdin,
        type=argparse.FileType('r'),
	help='the input file to read from, defaults to stdin')
    parser.add_argument(
	'-o', '--output-file', default=sys.stdout,
	type=argparse.FileType('w'),
	help='the output file to write to, defaults to stdout')
    args = parser.parse_args()
    main(args.input_file, args.output_file)
