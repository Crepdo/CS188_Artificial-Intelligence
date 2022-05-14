#!/bin/bash

echo "tar xvf submit.tar"

mkdir tmp; 
mv submit.tar ./tmp/;
cd tmp;
tar xvf submit.tar;

mv bustersAgents.py ../
mv inference.py ../
cd ..

echo "start running unittest"

python3 autograder.py > results.txt

echo "process results"

python3 server_grader.py

exit
