#!/usr/bin/env nix-shell
#! nix-shell -i bash
set -e


TEXINPUTS=.:./lib/: \
         latexmk -quiet -interaction=nonstopmode -output-directory=build/ -shell-escape -pdf thesis.tex \
    || ( cat ./build/thesis.log && false )
