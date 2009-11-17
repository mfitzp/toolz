//============================================================================
// Name        : libmercury_bhc.cpp
// Author      :
// Version     :
// Copyright   : Lesser GNU Public License (LGPL) version 2 or any later version.
// Description : 
/*
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
 
 * Modified by Brian H. Clowers to allow interface to SWIG and calls from Python, 2009
 */
//============================================================================

#include "libmercury.h"
//bhc added
#include <iostream>


void convolve(std::vector<double>& result_mz, std::vector<double>& result_ab, const std::vector<double>& mz1, const std::vector<double>& ab1, const std::vector<double>& mz2, const std::vector<double>& ab2)
{
    size_t n1 = mz1.size();
    size_t n2 = mz2.size();
    if ((n1+n2) == 0)
        return;

    result_mz.clear();
    result_ab.clear();
    // the following two lines speed up calculations by a factor of 3 (!)
    result_mz.resize(n1+n2);
    result_ab.resize(n1+n2);
    // for each isotope peak in the compound...
    double totalAbundance, massExpectation, ithMass, ithAbundance;
    for (size_t k = 0; k < n1 + n2 - 1; k++) {
        totalAbundance = 0;
        massExpectation = 0;
        size_t start = k < (n2 - 1) ? 0 : k - n2 + 1; // start=max(0, k-n2+1)
        size_t end = k < (n1 - 1) ? k : n1 - 1;       // end=min(n1 - 1, k)
        // ... calculate the mass expectation value and the abundance
        for (size_t i = start; i <= end; i++) {
            ithAbundance = ab1[i] * ab2[k - i];
            if (ithAbundance > 0) {
                totalAbundance += ithAbundance;
                ithMass = mz1[i] + mz2[k - i];
                massExpectation += ithAbundance * ithMass;
            }
        }
        // do NOT throw away isotopes with zero probability, this would
        // screw up the isotope count k !!
        result_mz[k] = totalAbundance > 0 ? massExpectation / totalAbundance : 0;
        result_ab[k] = totalAbundance;
    }
}

void prune(std::vector<double>& mz, std::vector<double>& ab, const double limit)
{
    size_t i;
    for (i = 0; i < ab.size(); i++) {
        if(ab[i] > limit)
            break;
    }
    mz.erase(mz.begin(), mz.begin()+i);
    ab.erase(ab.begin(), ab.begin()+i);

    // prune the end
    for (i = ab.size()-1; i >= 0; i--) {
        if(ab[i] > limit)
            break;
    }
    mz.resize(i+1);
    ab.resize(i+1);
    //mz.erase(mz.begin()+i+1, mz.end());
    //ab.erase(ab.begin()+i+1, ab.end());
}

int mercury(std::vector<double>& msa_mz, std::vector<double>& msa_abundance, const std::vector<unsigned int>& composition, const unsigned int MAX_ELEMENTS, const unsigned int MAX_ISOTOPES, const std::vector<unsigned int>& nIsotopes, std::vector< std::vector<double> >& elemMasses, std::vector< std::vector<double> >& elemAbundances, const int charge, const double limit)
{
	/*
	This is by no means an ideal solution.  In an effort to pass the coorect paramters to the funcion
	the multidimensional std::vector is converted to a double.  While I'm sure someone more versed in C++
	could figure this out, I'm at a loss so this will have to work for now.
	*/
    const double electronMass = 0.00054858;

    double elemMassesD[MAX_ELEMENTS][MAX_ISOTOPES];
    double elemAbundancesD[MAX_ELEMENTS][MAX_ISOTOPES];


    for (unsigned int i=0; i < MAX_ELEMENTS; i++)
    {
  	  for (unsigned int j=0; j < MAX_ISOTOPES; j++)
  	  {
  		  elemMassesD[i][j]=elemMasses[i][j];
  		  elemAbundancesD[i][j]=elemAbundances[i][j];
  	  }
    }

    if (composition.size() != MAX_ELEMENTS)
    {
        return(-1);
    }

    unsigned int n;
    std::vector<double> tmp_mz, tmp_abundance, esa_mz, esa_abundance;
    bool msa_initialized = false;
    // walk through the elements
    for (unsigned int e = 0; e < MAX_ELEMENTS; e++)
    {
        // if the element is present in the composition,
        // then calculate ESA and update MSA
        n = composition[e];
        if (n)
        {
            // initialize ESA
            esa_mz.assign(elemMassesD[e], elemMassesD[e] + nIsotopes[e]);
            esa_abundance.assign(elemAbundancesD[e], elemAbundancesD[e] + nIsotopes[e]);
        //    esa_mz.resize(n*nIsotopes[e]);
        //    esa_abundance.resize(n*nIsotopes[e]);
            //while (n > 0) {
            while (1)
            {
                // check if we need to do the MSA update
                if (n & 1)
                {
                    // MSA update
                    if (msa_initialized)
                    {
                        // normal update
                        convolve(tmp_mz, tmp_abundance, msa_mz, msa_abundance, esa_mz, esa_abundance);
                        msa_mz = tmp_mz;
                        msa_abundance = tmp_abundance;
                    }
                    else
                    {
        	        	std::cout << "n == 1" <<std::endl;
                        // for the first assignment MSA=ESA
                        msa_mz = esa_mz;
                        msa_abundance = esa_abundance;
                        msa_initialized = true;
                    }
                    prune(msa_mz, msa_abundance, limit);
                }
                // the ESA update is always carried out (with the exception of
                // the last time, i.e. when n==1)
                if (n==1)
                {
                    break;
                }
                convolve(tmp_mz, tmp_abundance, esa_mz, esa_abundance, esa_mz, esa_abundance);
                esa_mz = tmp_mz;
                esa_abundance = tmp_abundance;
                prune(esa_mz, esa_abundance, limit);
                n = n >> 1;
            }
        }
    }
    // take charge into account (placing the if around two loops is faster
    // than vice versa
    if (charge > 0)
    {
        for (std::vector<double>::iterator i = msa_mz.begin(); i != msa_mz.end(); i++)
        {
            *i = *i / abs(charge) - electronMass;
        }
    }
    if (charge < 0)
    {
        for (std::vector<double>::iterator i = msa_mz.begin(); i != msa_mz.end(); i++)
        {
            *i = *i / abs(charge) + electronMass;
        }
    }
    return(0);
}

//bhc added
//Apparently there is some difficulty in passing a multidimensional array as an argument with C++, this can be done with structs but the
//original program did not use this convention and I don't have a the time or the knowledge to make this more efficient.
 // int main()
 // {
     // const unsigned int MAX_ELEMENTS = 5;
     // const unsigned int MAX_ISOTOPES = 5;
// //     const unsigned int nIsotopes[MAX_ELEMENTS] = { 2, 2, 2, 3, 5 };

      // std::vector<unsigned int> tempIsos;
      // tempIsos.push_back(2);
      // tempIsos.push_back(2);
      // tempIsos.push_back(2);
      // tempIsos.push_back(3);
      // tempIsos.push_back(5);

      // std::vector<double> tempElem1;
      // tempElem1.push_back(1.0078246);
      // tempElem1.push_back(2.0141021);
      // tempElem1.push_back(0);
      // tempElem1.push_back(0);
      // tempElem1.push_back(0);

      // std::vector<double> tempElem2;
      // tempElem2.push_back(12.0000000);
      // tempElem2.push_back(13.0033554);
      // tempElem2.push_back(0);
      // tempElem2.push_back(0);
      // tempElem2.push_back(0);

      // std::vector<double> tempElem3;
      // tempElem3.push_back(14.0030732);
      // tempElem3.push_back(15.0001088);
      // tempElem3.push_back(0);
      // tempElem3.push_back(0);
      // tempElem3.push_back(0);

      // std::vector<double> tempElem4;
      // tempElem4.push_back(15.9949141);
      // tempElem4.push_back(16.9991322);
      // tempElem4.push_back(17.9991616);
      // tempElem4.push_back(0);
      // tempElem4.push_back(0);

      // std::vector<double> tempElem5;
      // tempElem5.push_back(31.972070);
      // tempElem5.push_back(32.971456);
      // tempElem5.push_back(33.967866);
      // tempElem5.push_back(34);
      // tempElem5.push_back(35.967080);

      // std::vector< std::vector<double> > tempElemMasses;
      // tempElemMasses.push_back(tempElem1);
      // tempElemMasses.push_back(tempElem2);
      // tempElemMasses.push_back(tempElem3);
      // tempElemMasses.push_back(tempElem4);
      // tempElemMasses.push_back(tempElem5);

      // std::vector< std::vector<double> > elemMasses(tempElemMasses);

// //      double tempTest[5][5];
// //      for (unsigned int i=0; i < 5; i++)
// //      {
// //    	  for (unsigned int j=0; j < 5; j++)
// //    	  {
// //    		  tempTest[i][j]=elemMasses[i][j];
// //    	  }
// //      }
// //      double elemMasses2[MAX_ELEMENTS][MAX_ISOTOPES] = {
// //        {1.0078246,    2.0141021,    0,        0,    0}, // H
// //        {12.0000000,     13.0033554,     0,         0,    0}, // C
// //        {14.0030732,     15.0001088,     0,         0,    0}, // N
// //        {15.9949141,     16.9991322,     17.9991616,     0,    0}, // O
// //        {31.972070,     32.971456,     33.967866,     34,    35.967080} // S
// //     };

// //      for (unsigned int i = 0; i < MAX_ELEMENTS; i++)
// //       {
// //         std::cout << *elemMasses2[i] << " " << nIsotopes[i];
// //         std::cout << "\n";
// //       }
// //      std::cout << "\n";
// //     const double elemAbundances[MAX_ELEMENTS][MAX_ISOTOPES] = {
// //        {0.99985,    0.00015,    0,        0,    0}, // H
// //        {0.988930,    0.011070,     0,         0,    0}, // C
// //        {0.996337,    0.003663,     0,         0,    0}, // N
// //        {0.997590,    0.000374,    0.002036,     0,    0}, // O
// //        {0.9502,    0.0075,        0.0421,     0,    0.0002} // S
// //     };

      // std::vector<double> tempAbund1;
      // tempAbund1.push_back(0.99985);
      // tempAbund1.push_back(0.00015);
      // tempAbund1.push_back(0);
      // tempAbund1.push_back(0);
      // tempAbund1.push_back(0);

      // std::vector<double> tempAbund2;
      // tempAbund2.push_back(0.988930);
      // tempAbund2.push_back(0.011070);
      // tempAbund2.push_back(0);
      // tempAbund2.push_back(0);
      // tempAbund2.push_back(0);

      // std::vector<double> tempAbund3;
      // tempAbund3.push_back(0.996337);
      // tempAbund3.push_back(0.003663);
      // tempAbund3.push_back(0);
      // tempAbund3.push_back(0);
      // tempAbund3.push_back(0);

      // std::vector<double> tempAbund4;
      // tempAbund4.push_back(0.997590);
      // tempAbund4.push_back(0.000374);
      // tempAbund4.push_back(0.002036);
      // tempAbund4.push_back(0);
      // tempAbund4.push_back(0);

      // std::vector<double> tempAbund5;
      // tempAbund5.push_back(0.9502);
      // tempAbund5.push_back(0.0075);
      // tempAbund5.push_back(0.0421);
      // tempAbund5.push_back(0);
      // tempAbund5.push_back(0.0002);

      // std::vector< std::vector<double> > tempElemAbundances;
// //      elemMasses.size(MAX_ELEMENTS)
      // tempElemAbundances.push_back(tempAbund1);
      // tempElemAbundances.push_back(tempAbund2);
      // tempElemAbundances.push_back(tempAbund3);
      // tempElemAbundances.push_back(tempAbund4);
      // tempElemAbundances.push_back(tempAbund5);


     // std::vector< std::vector<double> > elemAbundances(tempElemAbundances);


     // std::vector<double> mzVec, intVec;
     // std::vector<unsigned int> tempComp;
// //     tempComp.push_back(50);
// //     tempComp.push_back(23);
// //     tempComp.push_back(22);
// //     tempComp.push_back(12);
// //     tempComp.push_back(2);
// //     int tempVal;
// //     // H C N O S (Elements)
// //     std::cout << "Enter Integer Numbers Only!!!!!!!!!\n\n";
// //     std::cout << "Enter the Number of Hydrogen atoms: ";
// //     std::cin >> tempVal;
// //     tempComp.push_back(tempVal);
// //     std::cout << "\n";
// //     std::cout << "Enter the Number of Carbon atoms: ";
// //     std::cin >> tempVal;
// //     tempComp.push_back(tempVal);
// //     std::cout << "\n";
// //     std::cout << "Enter the Number of Oxygen atoms: ";
// //     std::cin >> tempVal;
// //     tempComp.push_back(tempVal);
// //     std::cout << "\n";
// //     std::cout << "Enter the Number of Nitrogen atoms: ";
// //     std::cin >> tempVal;
// //     tempComp.push_back(tempVal);
// //     std::cout << "\n";
// //     std::cout << "Enter the Number of Sulfur atoms: ";
// //     std::cin >> tempVal;
// //     tempComp.push_back(tempVal);
// //     std::cout << "\n";
// //     /*
// //     H378C254N65O75S6
     // tempComp.push_back(37800);
     // tempComp.push_back(25400);
     // tempComp.push_back(65000);
     // tempComp.push_back(75000);
     // tempComp.push_back(6000);
// //     */
     // const std::vector<unsigned int> elemComp(tempComp);

     // int molCharge = 1;
// //     std::cout << "Ion Charge: ";
// //     std::cin >> molCharge;


     // const double pruneLimit = 10e-5;
     // //int mercury(std::vector<double>& msa_mz, std::vector<double>& msa_abundance,
     // //const std::vector<unsigned int>& composition, const int charge, const double limit);
     // //int retVal;
     // mercury(mzVec, intVec, elemComp, MAX_ELEMENTS, MAX_ISOTOPES, tempIsos, elemMasses, elemAbundances, molCharge, pruneLimit);

// //     ///*
// //     std::cout.precision(10);
// ////        for (unsigned int t = 0; t < esa_mz.size(); t++)
// //     {
// //         std::cout << esa_mz[t]<< std::endl;
// //         std::cout << esa_abundance[t]<< std::endl;
// //     }


     // for(int i = 0; i<mzVec.size(); i++)
     // {
         // std::cout << mzVec[i];
         // std::cout << ", ";
         // std::cout << intVec[i];
         // std::cout << std::endl;
     // }
     // //*/
     // std::cout << "Mercury Finished!\n";
// //     int tempVal2;
     // // H C N O S (Elements)
// //     std::cout << "Enter Integer Numbers Only!!!!!!!!!\n\n";
// //     std::cout << "Enter the Number of Hydrogen atoms: ";
// //     std::cin >> tempVal2;

// //     std::vector<double> v1;
// //     v1.assign(3.234, 24);
// //     for(int i = 0; i<v1.size(); i++)
// //     {
// //         std::cout << v1[i];
// //         std::cout << std::endl;
// //     }
     // return 0;
 // }