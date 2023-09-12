#!/bin/bash

NAME=$1
LATE=0

if [[ $NAME == *"LATE"* ]] ; then 
    LATE=1
    echo "Marked as late..."
fi

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
