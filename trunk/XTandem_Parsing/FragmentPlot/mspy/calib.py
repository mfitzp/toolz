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

# load libs
import math
import numpy as num
from numpy.linalg import solve as solveLinEq

# load configuration
import config


# SPECTRUM CALIBRATION FUNCTIONS
# ------------------------------

def calibration(data, model='linear'):
    """Calculate calibration constants for given references.
        data: (list) pairs of (measured mass, reference mass)
        model: ('linear' or 'quadratic')
    """
    
    # set fitting model and initial values
    if model=='linear':
        model = _linearModel
        initials = (0.5, 0)
    elif model=='quadratic':
        model = _quadraticModel
        initials = (1, 0, 0)
    
    # calculate calibration constants
    params = _leastSquaresFit(model, initials, data)
    
    return model, params[0], params[1]  # model fce, model parameters, chi-square
# ----


def _linearModel(params, x):
    """Function for linear model."""
    
    a, b = params
    return a*x + b
    


def _quadraticModel(params, x):
    """Function for quadratic model."""
    
    a, b, c = params
    return a*x*x + b*x + c
    



# LEAST SQUARE FITTING WRITTEN BY KONRAD HINSEN
# ---------------------------------------------

def _leastSquaresFit(model, parameters, data, max_iterations=None, stopping_limit = 0.005):
    """General non-linear least-squares fit using the
    Levenberg-Marquardt algorithm and automatic derivatives."""
    
    n_param = len(parameters)
    p = ()
    i = 0
    for param in parameters:
        p = p + (_DerivVar(param, i),)
        i = i + 1
    id = num.identity(n_param)
    l = 0.001
    chi_sq, alpha = _chiSquare(model, p, data)
    niter = 0
    while 1:
        delta = solveLinEq(alpha+l*num.diagonal(alpha)*id,-0.5*num.array(chi_sq[1]))
        next_p = map(lambda a,b: a+b, p, delta)
        next_chi_sq, next_alpha = _chiSquare(model, next_p, data)
        if next_chi_sq > chi_sq:
            l = 10.*l
        else:
            l = 0.1*l
            if chi_sq[0] - next_chi_sq[0] < stopping_limit: break
            p = next_p
            chi_sq = next_chi_sq
            alpha = next_alpha
        niter = niter + 1
        if max_iterations is not None and niter == max_iterations:
            pass
    return map(lambda p: p[0], next_p), next_chi_sq[0]


def _isDerivVar(x):
    """Returns 1 if |x| is a DerivVar object."""
    return hasattr(x,'value') and hasattr(x,'deriv')


def _chiSquare(model, parameters, data):
    """ Count Chi-square. """
    
    n_param = len(parameters)
    chi_sq = 0.
    alpha = num.zeros((n_param, n_param))
    for point in data:
        sigma = 1
        if len(point) == 3:
            sigma = point[2]
        f = model(parameters, point[0])
        chi_sq = chi_sq + ((f-point[1])/sigma)**2
        d = num.array(f[1])/sigma
        alpha = alpha + d[:,num.newaxis]*d
    return chi_sq, alpha


def _mapderiv(func, a, b):
    """ Map a binary function on two first derivative lists. """
    
    nvars = max(len(a), len(b))
    a = a + (nvars-len(a))*[0]
    b = b + (nvars-len(b))*[0]
    return map(func, a, b)


class _DerivVar:
    """This module provides automatic differentiation for functions with any number of variables."""
    
    def __init__(self, value, index=0, order=1):
        if order > 1:
            raise ValueError, 'Only first-order derivatives'
        self.value = value
        if order == 0:
            self.deriv = []
        elif type(index) == type([]):
            self.deriv = index
        else:
            self.deriv = index*[0] + [1]
    
    def __getitem__(self, item):
        if item < 0 or item > 1:
            raise ValueError, 'Index out of range'
        if item == 0:
            return self.value
        else:
            return self.deriv
    
    def __coerce__(self, other):
        if _isDerivVar(other):
            return self, other
        else:
            return self, _DerivVar(other, [])
    
    def __cmp__(self, other):
        return cmp(self.value, other.value)
    
    def __add__(self, other):
        return _DerivVar(self.value + other.value, _mapderiv(lambda a,b: a+b, self.deriv, other.deriv))
    __radd__ = __add__
    
    def __sub__(self, other):
        return _DerivVar(self.value - other.value, _mapderiv(lambda a,b: a-b, self.deriv, other.deriv))
    
    def __mul__(self, other):
        return _DerivVar(self.value*other.value,
            _mapderiv(lambda a,b: a+b,
                map(lambda x,f=other.value:f*x, self.deriv),
                map(lambda x,f=self.value:f*x, other.deriv)))
    
    __rmul__ = __mul__
    
    def __div__(self, other):
        if not other.value:
            raise ZeroDivisionError, 'DerivVar division'
        inv = 1./other.value
        return _DerivVar(self.value*inv,
            _mapderiv(lambda a,b: a-b,
                map(lambda x,f=inv: f*x, self.deriv),
                map(lambda x,f=self.value*inv*inv: f*x,
                    other.deriv)))
    
    def __rdiv__(self, other):
        return other/self
    
    def __pow__(self, other, z=None):
        if z is not None:
            raise TypeError, 'DerivVar does not support ternary pow()'
        val1 = pow(self.value, other.value-1)
        val = val1*self.value
        deriv1 = map(lambda x,f=val1*other.value: f*x, self.deriv)
        if _isDerivVar(other) and len(other.deriv) > 0:
            deriv2 = map(lambda x, f=val*num.log(self.value): f*x,
                             other.deriv)
            return _DerivVar(val,_mapderiv(lambda a,b: a+b, deriv1, deriv2))
        else:
            return _DerivVar(val,deriv1)
    
    def __rpow__(self, other):
        return pow(other, self)
    

