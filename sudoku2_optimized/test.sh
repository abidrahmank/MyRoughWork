#! /bin/bash
gcc pmain.c
rm z2.tmp 2>/dev/null
for i in 0 1 3 4 6
do
    ./a.out "s$i.txt" > zz.tmp
    diff -y --suppress-common-lines "sort$i.txt" zz.tmp  | tee -a z2.tmp
done
sed 's/[ \t]//g' z2.tmp | sed 's/time://g' | sed 's/|/ /g' | head -4 > z3.tmp
python -c "import numpy as np; x = np.loadtxt('z3.tmp'); y=np.sum(x,0); print 'Speed Up : {0}'.format(y[0]/y[1])"
rm zz.tmp z2.tmp z3.tmp 2>/dev/null 
