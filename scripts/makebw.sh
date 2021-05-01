#!/bin/bash
COLORS=6
QUALITY=50
SIZE="220x220>"

mogrify -path static/img -resize $SIZE -dither FloydSteinberg -remap colors.gif -quality $QUALITY img/*.jpg
mogrify -path static/img -resize $SIZE -dither FloydSteinberg -remap colors.gif img/*.png

mogrify -path static/img/originals -dither FloydSteinberg -colors $COLORS -quality $QUALITY img/*.jpg
mogrify -path static/img/originals -dither FloydSteinberg -colors $COLORS img/*.png

pngquant --force --ext .png -- static/img/*.png
pngquant --force --ext .png -- static/img/originals/*.png

optipng -clobber static/img/*.png
optipng -clobber static/img/originals/*.png
