#!/usr/bin/env python

# \usepackage{minted}
# \begin{minted}{trace-lexer.py:TraceLexer -x}
#   ...
# \end{minted}

import re

from pygments.lexer import RegexLexer, bygroups, combined, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String
from pygments.token import Number, Punctuation, Whitespace


class TraceLexer(RegexLexer):
    """
    A Pygments lexer for annotating simple traces:

    # this query
    Query ... {
      a,b,c := Materialize[...]
      GC {
         Delete[...]
      }
      c := Materialize[...]
    }

    Query .. {
      ...
    }

    ...
    """

    name = 'FluiDB-trace'
    aliases = ['fdb-trace']
    filenames = ['*.fdb']

    tokens = {
        'root': [
            (r"(Inventory)(\s+)({)(\s*)",
             bygroups(Keyword,Text,Operator,Text), 'inventory'),
            (r"(Query)(\s+)(.*)(\s+)({)(\s*)",
             bygroups(Keyword,Text,Keyword.Namespace,Text,Operator,Text), 'query'),
            include('comment'),
            (r'\n',Text),
            (r'...',Comment)
        ],
        'query': [
            (r'(Materialize)(\s*)(\[)(.*)(\])',
             bygroups(Name.Function, Text, Operator, Text, Operator)),
            (r"(GC)(\s*)({)(\s*)", bygroups(Keyword,Text,Operator,Text),'gc'),
            (r',',Operator),
            (r':=',Operator),
            (r'}',Operator,'#pop'),
            (r'\w+',Name),
            (r'\s+',Text),
            include('comment')
        ],
        'gc': [
            (r'(Delete)(\s*)(\[)(.*)(\])',
             bygroups(Name.Function, Text, Operator, Text, Operator)),
            (r'}',Operator,'#pop'),
            (r'\n',Text),
            (r'\s+',Text),
            include('comment')
        ],
        'inventory': [
            (r':=',Operator),
            (r',',Operator),
            (r'}',Operator,'#pop'),
            (r'\n',Text),
            (r'\s+',Text),
            (r'[^,\s]+',Name),
            include('comment')
        ],
        'comment': [
            (r'#.*$',Comment.Single)
        ]
    }
