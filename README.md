
# PyLaTeXc

A preprocessor/evaluator of pytex source files
(LaTeX with embedded python) into valid LaTeX.  

Let me know if you think this would be more readily achieved with
a compiler plugin, I opted for the script-fu solution.

## Install

I haven't put it up on PyPI, I would want to set up some unit tests
and tox testing (to test support for different versions of Python) 
before I put it up there.  

You can still however install with pip's handy git targets.

```Sh
pip install git+https://github.com/MichaelBelousov/PyTeXc.git
```

## What is it?

Allows you to use Python in your LaTeX document (whichever supported
version you have installed) by means of an execution environment and
an evaluation macro:

```LaTeX

\begin{pyexec}
    import math  # you can define your calculations in the document!
    x = 100
\end{pyexec}

\begin{document}

The value of $x$ is \pyeval{x}!

\end{document}
```

It's all just textual substitution, where the pyexec environments
disappear and the pyevals are replaced with their formatted equivalents.  

Try something more advanced, like grabbing the collected works of
Shakespeare from MIT's portal and generating a word frequency chart
in your document with pgf plots.

### TODO:

* replace slow string concatentations with buffered writes and splices with views
* hide internal functions and add a higher level interface
* move to independent github repo
* add config of the macros used (e.g. pyeval => pev)

