#!/bin/bash
mogrify -path static/img -resize "300x120>" -monochrome -quality 50 img/*.jpg
mogrify -path static/img -resize "300x120>" -monochrome img/*.png
pngquant --force --ext .png -- static/img/*.png
optipng -clobber static/img/*.png
