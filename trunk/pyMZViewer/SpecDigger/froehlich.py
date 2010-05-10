import os, sys, traceback

import numpy as N
import matplotlib.pyplot as P
from mzXMLReader import mzXMLDoc

'''

neutral losses          Glycosidic ions (M+H)+
162.0528                163.06007
324.1056                325.11287
486.1584                487.16567
648.2112                366.13947
810.264
1013.3434
972.3168
1175.3962
1134.3696
1337.449
1296.4224
1499.5018
1458.4752
1661.5546

'''

'''
These lists are used to define which m/z
values are going to be examined.

The names lists are used for the headers of
the resulting csv/summary file.
'''

LOSSLIST = [162.0528,
            324.1056,
            486.1584,
            648.2112,
            810.264,
            1013.3434,
            972.3168,
            1175.3962,
            1134.3696,
            1337.449,
            1296.4224,
            1499.5018,
            1458.4752,
            1661.5546
            ]

LOSSNAMES = []
for loss in LOSSLIST:
    LOSSNAMES.append("[M-%s]+"%loss)

GLYCOLIST = [163.06007,
             325.11287,
             366.13947,
             487.16567
             ]
GLYCONAMES = []
for glyco in GLYCOLIST:
    GLYCONAMES.append('[M+%s]+'%glyo)


