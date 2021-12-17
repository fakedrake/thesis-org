#!/usr/bin/env nix-shell
#! nix-shell -i bash
set -e


TEXINPUTS=.:./lib/: \
         latexmk -quiet -interaction=nonstopmode -output-directory=build/ -shell-escape -bibtex -pdf -synctex=1 thesis.tex \
    || ( cat ./build/thesis.log && false )

mv ./build/thesis.pdf thesis.pdf
mv ./build/thesis.synctex.gz ./
