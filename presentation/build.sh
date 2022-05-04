#!/usr/bin/env nix-shell
#! nix-shell -i bash ..
set -e


TEXINPUTS=.:./lib/: \
         latexmk -quiet -interaction=nonstopmode -output-directory=build/ -shell-escape -bibtex -pdf -synctex=1 presentation.tex \
    || ( cat ./build/presentation.log && false )


mv ./build/presentation.pdf presentation.pdf
mv ./build/presentation.synctex.gz ./
