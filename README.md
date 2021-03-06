# PyLaTeXc

A preprocessor/evaluator of pylatex source files
(LaTeX with embedded python) into valid LaTeX.  

Let me know if you think this would be more readily achieved with
a compiler plugin, I opted for the script-fu solution.

## What is it?

Allows you to use Python in your LaTeX document (whichever supported
version you have installed) by means of an execution environment and
an evaluation macro:

```LaTeX

\begin{pyexec}
    import math  # you can define your calculations in the document!
    x = math.log(100)
\end{pyexec}

\begin{document}

The value of $x$ is \pyeval{x}!

And the value of $y$ is \pyeval{{1,2,3}&{2,1}}

\end{document}
```

It's all just textual substitution, where the pyexec environments
disappear and the pyevals are replaced with their formatted equivalents.  

Try something more advanced, like grabbing the collected works of
Shakespeare from MIT's portal and generating a word frequency chart
in your document with pgf plots.

## Install

I haven't put it up on PyPI, I would want to set up some unit tests
and tox testing (to test support for different versions of Python) 
before I put it up there.  

You can still however install with pip's handy git targets.

```Sh
pip install git+https://github.com/MichaelBelousov/PyTeXc.git
```

## Usage

You can use the optional arguments or default to stdin/stdout,
invoking from python using its module argument is ideal because that
way you can control your python version by the interpreter you are
invoking.

```Sh
python -m pylatexc -i path/to/input.file -o path/to/output.file
python -m pylatexc < path/to/input.file > path/to/output.file
python3 -m pylatexc < path/to/input.file > path/to/output.file
```

### Notes

Checkout [cog](https://nedbatchelder.com/code/cog/), I prefer the syntax in pylatexc's method.
It feels more homey.

I wrote an article about this on my blog:
[https://mikemikeb.com/#/blog](https://mikemikeb.com/#/blog)

### TODO:

* replace slow string concatentations with buffered writes and slices with views
* hide internal functions and add a higher level interface
* add config of the macros used (e.g. pyeval => pev)
