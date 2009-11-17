/*
 * $Id$
 *
 * libmercury++
 *
 * A C++ library for the calculation of accurate masses
 * and abundances of isotopic peaks
 *
 * Copyright (c) 2006
 *     Marc Kirchner <marc.kirchner@iwr.uni-heidelberg.de>
 *
 * Based on the emass implementation of Perttu Haimi
 * (see Copyright notice below).
 *
 * This code may be distributed under the terms of the
 * Lesser GNU Public License (LGPL) version 2 or any later version.
 */

/*
 *
 * Based on an algorithm developed by Alan L. Rockwood.
 *
 * Published in
 * Rockwood, A.L. and Haimi, P.: "Efficent calculation of
 * Accurate Masses of Isotopic Peaks",
 * Journal of The American Society for Mass Spectrometry
 * JASMS 03-2263, 2006
 *
 * Copyright (c) 2005 Perttu Haimi and Alan L. Rockwood
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms,
 * with or without modification, are permitted provided
 * that the following conditions are met:
 *
 *    * Redistributions of source code must retain the
 *      above copyright notice, this list of conditions
 *      and the following disclaimer.
 *    * Redistributions in binary form must reproduce
 *      the above copyright notice, this list of conditions
 *      and the following disclaimer in the documentation
 *      and/or other materials provided with the distribution.
 *    * Neither the author nor the names of any contributors
 *      may be used to endorse or promote products derived
 *      from this software without specific prior written
 *      permission.
 */

/*
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
#include <cstdlib>
#include <vector>
#include <cmath>

/*
    mercury:    calculates the expected isotpic distribution
            for a given composition
    parameters:
    msa_mz        returned mass list
    msa_abundance    returned abundance list
    composition    a vector of length MAX_ELEMENTS giving the
            the number for occurences of each element
    charge        the charge state for which the isotopic pattern
            is to be calculated
    limit        a pruning limit, (Rockwood et al. 2006) suggest
            a value between 10e-25 and 10e-30
*/
int mercury(std::vector<double>& msa_mz, std::vector<double>& msa_abundance, const std::vector<unsigned int>& composition, const unsigned int MAX_ELEMENTS, const unsigned int MAX_ISOTOPES, const std::vector<unsigned int>& nIsotopes, std::vector< std::vector<double> >& elemMasses, std::vector< std::vector<double> >& elemAbundances, const int charge, const double limit);

