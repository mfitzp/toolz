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

# register essential objects
import blocks
import objects


# COMMON MASS RELATED FUNCTIONS
# -----------------------------

def delta(measuredMass, countedMass, units='ppm'):
    """Calculate error between measuredMass and countedMass in specified units.
        measuredMass: (float)
        countedMass: (float)
        units: ('Da' or 'ppm')
    """
    
    if units == 'ppm':
        return (measuredMass - countedMass)/countedMass*1000000
    elif units == 'Da':
        return (measuredMass - countedMass)
    elif units == '%':
        return (measuredMass - countedMass)/countedMass*100
    else:
        raise ValueError, 'Unknown units for delta mass! -->' + units
# ----


def mz(mass, charge, currentCharge=0, agentFormula='H', agentCharge=1, massType='Mo'):
    """Calculate m/z value for given mass and charge.
        mass: (tuple of (Mo,Av) or float)
        charge: (int) desired charge of ion
        currentCharge: (int) if mass is charged already
        agentFormula: (str) charging agent formula
        agentCharge: (int) charging agent charge
        massType: ('Mo' or 'Av') used mass type if mass value is float
    """
    
    # set mass type
    if massType == 'Mo':
        massType = 0
    else:
        massType = 1
    
    # get agent mass
    agentFormula = objects.formula(agentFormula)
    agentMass = agentFormula.getMass()
    agentMass = (agentMass[0]-agentCharge*0.000549, agentMass[1]-agentCharge*0.000549)
    
    # recalculate zero charge
    agentCount = currentCharge/agentCharge
    if currentCharge != 0:
        if type(mass) in (tuple, list):
            massMo = mass[0]*abs(currentCharge) - agentMass[0]*agentCount
            massAv = mass[1]*abs(currentCharge) - agentMass[1]*agentCount
            mass = (massMo, massAv)
        else:
            mass = mass*abs(currentCharge) - agentMass[massType]*agentCount
    if charge == 0:
        return mass
    
    # calculate final charge
    agentCount = charge/agentCharge
    if type(mass) in (tuple, list):
        massMo = (mass[0] + agentMass[0]*agentCount)/abs(charge)
        massAv = (mass[1] + agentMass[1]*agentCount)/abs(charge)
        return (massMo, massAv)
    else:
        return (mass + agentMass[massType]*agentCount)/abs(charge)
# ----

