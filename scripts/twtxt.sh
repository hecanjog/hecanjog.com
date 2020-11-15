#!/bin/bash
set -e
POSTTIME=`date -Is`
TMPFILE=/tmp/$POSTTIME.twtxt.txt
vim $TMPFILE
if test -f "$TMPFILE"; then
    echo -e "$POSTTIME\t`cat $TMPFILE`" >> static/twtxt.txt
fi

cp static/twtxt.txt static/gemini/twtxt.txt
