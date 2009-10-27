# -------------------------------------------------------------------------
#     Copyright (C) 2008-2010 Martin Strohalm <mmass@biographics.cz>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE in the
#     main directory of the program
# -------------------------------------------------------------------------

# load configuration
import config

# register basic objects
from blocks import *
from objects import *

# register modules
from basics import *
from proteo import *
from peakpicking import *
from pattern import *
from averagine import *
from smoothing import *
from baseline import *
from calib import *

# register parsers
from parser_xy import parseXY
from parser_mzxml import parseMZXML
from parser_mzdata import parseMZDATA
from parser_bruker_flex import parseBRUKERFLEX
