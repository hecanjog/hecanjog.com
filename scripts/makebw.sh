#!/bin/bash
mogrify -path static/img -resize "200x200>" -monochrome -quality 50 img/*.jpg
mogrify -path static/img -resize "200x200>" -monochrome img/*.png
pngquant --force --ext .png -- static/img/*.png
optipng -clobber static/img/*.png
