#!/bin/bash
#`date -Im`\t$1 >> static/twtxt.txt
POSTTIME=`date -Im`
TMPFILE=/tmp/$POSTTIME.twtxt.txt
echo "$POSTTIME\t" >> $TMPFILE
vim $TMPFILE && cat $TMPFILE >> static/twtxt.txt
