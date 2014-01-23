#!/bin/sh

here=`pwd`
basename=`basename $0`
root=`echo $0 | sed "s/$basename//"`
cd $root
. ./clue.env

python ./src/clue/manage.py runserver



