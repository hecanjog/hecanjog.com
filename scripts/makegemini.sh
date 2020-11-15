#!/bin/bash

rm static/gemini/*.gmi;
for p in static/*.html; do
    dest=${p%%.*}
    dest=${dest##*/}
    pandoc -f html -t plain --lua-filter vendor/gemini-pandoc-lua-filter/gemini.lua $p -o static/gemini/$dest.gmi
done

rm static/gemini/blog/*.gmi;
for p in static/blog/*.html; do
    dest=${p%%.*}
    dest=${dest##*/}
    pandoc -f html -t plain --lua-filter vendor/gemini-pandoc-lua-filter/gemini.lua $p -o static/gemini/blog/$dest.gmi
done

rm static/gemini/listening/*.gmi;
for p in static/listening/*.html; do
    dest=${p%%.*}
    dest=${dest##*/}
    pandoc -f html -t plain --lua-filter vendor/gemini-pandoc-lua-filter/gemini.lua $p -o static/gemini/listening/$dest.gmi
done
