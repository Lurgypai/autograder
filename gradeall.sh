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
    LATE=0
    if [[ $NAME == *"LATE"* ]] ; then 
        LATE=1
        echo "Marked as late..."
    fi

    echo "Cleaning test dir..."
    rm -rf testdir-working
    cp -r testdir testdir-working
    echo "Copying to test dir..."
    cp $FILE testdir-working/
    cd testdir-working
    echo "Unzipping..."
    unzip -n $NAME 
    echo "Moving up a directory..."
    mv */* .

    echo "ATTEMPTING TO MAKE..."
    make &> "${NAME}-output.txt"
    echo "" >> "${NAME}-output.txt"

    if [[ -e pairsofwords ]] ; then
        echo "Make sucess, grading..."
        ./grade.py -V >> ${NAME}-output.txt
        AUTO_GRADES_LINE=`grep FINAL ${NAME}-output.txt`
        AUTO_GRADES=${AUTO_GRADES_LINE##*-}

        echo "${NAME}, ${AUTO_GRADES}, 1, ${LATE}" >> ../grades.csv
    else
        echo "Make failed for ${NAME}"
        echo "${NAME}, 0, 0, 0, 0, ${LATE}" >> ../grades.csv
    fi
    mv ${NAME}-output.txt ../outputs

    # exit the test dir
    cd ..
done
