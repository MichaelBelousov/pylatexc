# PyLaTeXc

A source transformer of pylatex source files (LaTeX with embedded python)
into valid LaTeX.

```LaTeX
\begin{document}

\begin{pyexec}
    import math  # you can define your calculations in the document!
    x = 100
\end{pyexec}

The value of $x$ is \pyeval{x}!

\end{document}
```

Try something more advanced, like grabbing the collected works of
Shakespeare from MIT's portal and generating a word frequency chart
in your document.

### TODO:

* replace slow string concatentations with buffered writes and splices with views
* hide internal functions and add a higher level interface
* move to independent github repo
* add config of the macros used (e.g. pyeval => pev)
