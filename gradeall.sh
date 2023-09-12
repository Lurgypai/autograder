#!/bin/bash

rm testdir/grade.py
cp grade.py testdir

rm -r outputs/
mkdir outputs

rm grades.csv
touch grades.csv
echo "Name, valid grade, invalid grade, leaks?, make success, late" >> grades.csv

for FILE in submissions/*; do
    NAME=${FILE##*/}

    echo "Cleaning test dir..."
    if [[ -e testdir-working ]]; then
        rm -rf testdir-working
    fi
    cp -r testdir testdir-working
    echo "Copying to test dir..."
    cp $FILE testdir-working/
    cd testdir-working
    ../makeandtest.sh $NAME
    cd ..
    rm -rf testdir-working
done
