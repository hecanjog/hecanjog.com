#!/bin/bash
mogrify -path static/img -resize "200x200>" -monochrome -quality 50 img/*.jpg
mogrify -path static/img -resize "200x200>" -monochrome img/*.png

mogrify -path static/img/originals -monochrome -quality 50 img/*.jpg
mogrify -path static/img/originals -monochrome img/*.png

pngquant --force --ext .png -- static/img/*.png
pngquant --force --ext .png -- static/img/originals/*.png

optipng -clobber static/img/*.png
optipng -clobber static/img/originals/*.png
