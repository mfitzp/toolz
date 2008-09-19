#!/usr/bin/env python

from numpy import array

from pca_module import *
import time
import unittest


############## UNIT TESTING ############## 
# Some correct test-values (made 09.05.2007):
# With PCA Module 1.0

# small data set:
X = array([[2, 3, 4, 1],
	   [1, 3, 1, 5],
	   [4, 6, 4, 3],
	   [2, 1, 1, 1],
	   [1, 2, 5, 3],
	   [7, 3, 4, 1]], float)

# mean_center(X) 
X_centered = array([[-0.83333333,  0.,          0.83333333, -1.33333333],
                    [-1.83333333,  0.,        -2.16666667,  2.66666667],
                    [ 1.16666667,  3.,          0.83333333,  0.66666667],
                    [-0.83333333, -2.,         -2.16666667, -1.33333333],
                    [-1.83333333, -1.,          1.83333333,  0.66666667],
                    [4.16666667,  0.,          0.83333333, -1.33333333]])

# standardization(X)                   
X_standardized = array([[0.94573249,  1.96396101,  2.54399491,  0.67082039],
                        [0.47286624,  1.96396101,  0.63599873,  3.35410197],
                        [1.89146497,  3.92792202,  2.54399491,  2.01246118],
                        [0.94573249,  0.65465367,  0.63599873,  0.67082039],
                        [0.47286624,  1.30930734,  3.17999364,  2.01246118],
                        [3.31006371,  1.96396101,  2.54399491,  0.67082039]])




# correct for this X, after calculation (using default parameters): 
# T and P are rotated 180 degrees for NIPALS compared to SVD
Scores_nipals = array([[ 0.40051737, -0.50691688, -0.66225458,  0.61661848],
		       [-2.02073029,  1.12318439,  0.64736695, -0.29402578],
		       [ 1.19358998,  1.70566985,  0.33604821,  0.44214757],
		       [-1.12545468, -1.70021128,  0.56437118,  0.30423703],
		       [-0.34480393,  0.10827787, -1.55227377, -0.44666215],
		       [ 1.89688155, -0.73000396,  0.66674201, -0.62231515]])

Scores_svd = array([[ 0.39124108, -0.51852819, -0.65880069, -0.61661898],
		    [-1.99906634,  1.16627592,  0.63836698,  0.29402557],
		    [ 1.22637448,  1.6839338,   0.32751855, -0.44214676],
		    [-1.1591248,  -1.67453156,  0.57293566, -0.30423691],
		    [-0.34093005,  0.10590213, -1.55329349,  0.44666045],
		    [ 1.88150563, -0.7630521,   0.673273,    0.62231662]])

Loadings_nipals = array([[ 0.6328911,   0.37617472,  0.54163826, -0.40567159],
			 [-0.09435526,  0.69688179,  0.14720258,  0.69554602],
			 [ 0.56210255,  0.22325287, -0.79608775,  0.02105201],
			 [-0.52401018,  0.56833662, -0.22628235, -0.59262392]])

Loadings_svd = array([[ 0.63031124,  0.38949747,  0.54528096, -0.39200527],
		      [-0.10342202,  0.69068596,  0.13190968,  0.70346046],
		      [ 0.56340401,  0.21963272, -0.79628203,  0.01650193],
		      [ 0.52401101, -0.56833625,  0.22628177,  0.59262376]])

# correct for this X, after SVD calculation:          
explained_var = array([0.44388322,  0.32759266,  0.17262798,  0.05589614])

# Correlation Loadings with Scores of PCA (svd):
Correlation_Loadings = array([[ 0.8398842,   0.51900196,  0.72658209, -0.52234359],
                              [-0.11838866,  0.79063804,  0.15099889,  0.80526119],
                              [ 0.4681721,   0.1825083,  -0.66168686,  0.01371262],
                              [ 0.24777719, -0.26873626,  0.10699672,  0.28022054]])


# amount of decimals to check
accurate = 6   # used where there should be high accuracy
not_so_accurate = 2    

class TestPCA(unittest.TestCase):   
    def test_centering(self):
        # if mean center fails, PCA will fail
        X_c = mean_center(X)
        
        self.failUnlessEqual(X_c.shape, X_centered.shape, 'wrong shape')
        
        for i in range(len(X_centered)):
            for j in range(len(X_centered[0])):
                self.failUnlessAlmostEqual(X_c[i,j], X_centered[i,j], accurate,'wrong value in X_c[%i,%i] (svd)' % (i,j))        
     
    def test_standardization(self):
        # if standardization fails, PCA will fail
        X_std = standardization(X)
        
        self.failUnlessEqual(X_std.shape, X_standardized.shape, 'wrong shape')
        
        for i in range(len(X_standardized)):
            for j in range(len(X_standardized[0])):
                self.failUnlessAlmostEqual(X_std[i,j], X_standardized[i,j], accurate, 'wrong value in X_std[%i,%i] (svd)' % (i,j))        
         
    def test_nipals1a(self):
        # using default parameters (should be: standardize=True, PCs=10, threshold=0.0001)
        T, P, e_var = PCA_nipals(X)
        self.failUnlessEqual(T.shape, Scores_nipals.shape, 'wrong shape')
        self.failUnlessEqual(P.shape, Loadings_nipals.shape, 'wrong shape')
        self.failUnlessEqual(e_var.shape, explained_var.shape, 'wrong shape')
        
        for i in range(len(Scores_nipals)):
            for j in range(len(Scores_nipals[0])):
                self.failUnlessAlmostEqual(T[i,j], Scores_nipals[i,j], accurate, 'wrong value in T[%i,%i] (svd)' % (i,j))
        
        for i in range(len(Loadings_nipals)):
            for j in range(len(Loadings_nipals[0])):
                self.failUnlessAlmostEqual(P[i,j], Loadings_nipals[i,j], accurate, 'wrong value in P[%i,%i] (svd)' % (i,j))        
        
        for i in range(len(explained_var)):
            self.failUnlessAlmostEqual(e_var[i], explained_var[i], not_so_accurate, 'wrong value in e_var['+str(i)+'] (svd)')
    
    def test_nipals1b(self):
        # using default parameters (should be: standardize=True, PCs=10, threshold=0.0001)
        T, P, E = PCA_nipals(X, E_matrices=True)
        self.failUnlessEqual(T.shape, Scores_nipals.shape, 'wrong shape')
        self.failUnlessEqual(P.shape, Loadings_nipals.shape, 'wrong shape')
        #self.failUnlessEqual(E.shape, explained_var.shape, 'wrong shape')
        for i in range(len(Scores_nipals)):
            for j in range(len(Scores_nipals[0])):
                #pass
                self.failUnlessAlmostEqual(T[i,j], Scores_nipals[i,j], accurate, 'wrong value in T[%i,%i]' % (i,j))
        
        #print P
        for i in range(len(Loadings_nipals)):
            for j in range(len(Loadings_nipals[0])):
                #pass
                self.failUnlessAlmostEqual(P[i,j], Loadings_nipals[i,j], accurate, 'wrong value in P[%i,%i]' % (i,j))        
        
        #print E
        for i in range(len(explained_var)):
            pass
            #self.failUnlessAlmostEqual(e_var[i], explained_var[i], not_so_accurate, 'wrong value in e_var['+str(i)+']')



    def test_nipals2(self):
        # using default parameters (should be: standardize=True, PCs=10, threshold=0.0001)
        T, P, e_var = PCA_nipals2(X)        
        self.failUnlessEqual(T.shape, Scores_nipals.shape, 'wrong shape')
        self.failUnlessEqual(P.shape, Loadings_nipals.shape, 'wrong shape')
        self.failUnlessEqual(e_var.shape, explained_var.shape, 'wrong shape')
        
        for i in range(len(Scores_nipals)):
            for j in range(len(Scores_nipals[0])):
                self.failUnlessAlmostEqual(T[i,j], Scores_nipals[i,j], accurate, 'wrong value in T[%i,%i] (svd)' % (i,j))
        
        for i in range(len(Loadings_nipals)):
            for j in range(len(Loadings_nipals[0])):
                self.failUnlessAlmostEqual(P[i,j], Loadings_nipals[i,j], accurate, 'wrong value in P[%i,%i] (svd)' % (i,j))        
        
        for i in range(len(explained_var)):
            self.failUnlessAlmostEqual(e_var[i], explained_var[i], not_so_accurate, 'wrong value in e_var['+str(i)+'] (svd)')
   
   
    def test_nipals2b(self):
        # using default parameters (should be: standardize=True, PCs=10, threshold=0.0001)
        T, P, E = PCA_nipals2(X, E_matrices=True)
        self.failUnlessEqual(T.shape, Scores_nipals.shape, 'wrong shape')
        self.failUnlessEqual(P.shape, Loadings_nipals.shape, 'wrong shape')
        #self.failUnlessEqual(E.shape, explained_var.shape, 'wrong shape')
        for i in range(len(Scores_nipals)):
            for j in range(len(Scores_nipals[0])):
                #pass
                self.failUnlessAlmostEqual(T[i,j], Scores_nipals[i,j], accurate, 'wrong value in T[%i,%i]' % (i,j))
        
        #print P
        for i in range(len(Loadings_nipals)):
            for j in range(len(Loadings_nipals[0])):
                #pass
                self.failUnlessAlmostEqual(P[i,j], Loadings_nipals[i,j], accurate, 'wrong value in P[%i,%i]' % (i,j))        
        
        #print E
        for i in range(len(explained_var)):
            pass
            #self.failUnlessAlmostEqual(e_var[i], explained_var[i], not_so_accurate, 'wrong value in e_var['+str(i)+']')
  
  
    def test_nipals_c(self):
        # using default parameters (should be: standardize=True, PCs=10, threshold=0.0001)
        T, P, E = PCA_nipals_c(X, E_matrices=True)
        self.failUnlessEqual(T.shape, Scores_nipals.shape, 'wrong shape')
        self.failUnlessEqual(P.shape, Loadings_nipals.shape, 'wrong shape')
        #self.failUnlessEqual(e_var.shape, explained_var.shape, 'wrong shape')
        
        for i in range(len(Scores_nipals)):
            for j in range(len(Scores_nipals[0])):
                self.failUnlessAlmostEqual(T[i,j], Scores_nipals[i,j], accurate, 'wrong value in T[%i,%i] (svd)' % (i,j))
        
        for i in range(len(Loadings_nipals)):
            for j in range(len(Loadings_nipals[0])):
                self.failUnlessAlmostEqual(P[i,j], Loadings_nipals[i,j], accurate, 'wrong value in P[%i,%i] (svd)' % (i,j))        
        
        for i in range(len(explained_var)):
            pass
            #self.failUnlessAlmostEqual(e_var[i], explained_var[i], not_so_accurate, 'wrong value in e_var['+str(i)+'] (svd)')
  

    def test_nipals_c2(self):
        # using default parameters (should be: standardize=True, PCs=10, threshold=0.0001)
        T, P, e_var = PCA_nipals_c(X)
        self.failUnlessEqual(T.shape, Scores_nipals.shape, 'wrong shape')
        self.failUnlessEqual(P.shape, Loadings_nipals.shape, 'wrong shape')
        self.failUnlessEqual(e_var.shape, explained_var.shape, 'wrong shape')
        
        for i in range(len(Scores_nipals)):
            for j in range(len(Scores_nipals[0])):
                self.failUnlessAlmostEqual(T[i,j], Scores_nipals[i,j], accurate, 'wrong value in T[%i,%i] (svd)' % (i,j))
        
        for i in range(len(Loadings_nipals)):
            for j in range(len(Loadings_nipals[0])):
                self.failUnlessAlmostEqual(P[i,j], Loadings_nipals[i,j], accurate, 'wrong value in P[%i,%i] (svd)' % (i,j))        
        
        for i in range(len(explained_var)):
            self.failUnlessAlmostEqual(e_var[i], explained_var[i], not_so_accurate, 'wrong value in e_var['+str(i)+'] (svd)')
  
  
    def test_svd(self):
        # using default parameters (should be: standardize=True)
        T, P, e_var = PCA_svd(X)       
        self.failUnlessEqual(T.shape, Scores_svd.shape, 'wrong shape')
        self.failUnlessEqual(P.shape, Loadings_svd.shape, 'wrong shape')
        self.failUnlessEqual(e_var.shape, explained_var.shape, 'wrong shape')
        
        for i in range(len(Scores_svd)):
            for j in range(len(Scores_svd[0])):
                self.failUnlessAlmostEqual(T[i,j], Scores_svd[i,j], accurate, 'wrong value in T[%i,%i] (svd)' % (i,j))
        
        for i in range(len(Loadings_svd)):
            for j in range(len(Loadings_svd[0])):
                self.failUnlessAlmostEqual(P[i,j], Loadings_svd[i,j], accurate, 'wrong value in P[%i,%i] (svd)' % (i,j))        
        
        for i in range(len(explained_var)):
            self.failUnlessAlmostEqual(e_var[i], explained_var[i], not_so_accurate, 'wrong value in e_var['+str(i)+'] (svd)')
        
        
    def test_corr_loadings(self):
        T, P, e_var = PCA_svd(X)
        CorrLoad = CorrelationLoadings(X, T)
        
        for i in range(len(Correlation_Loadings)):
            for j in range(len(Correlation_Loadings[0])):
                self.failUnlessAlmostEqual(CorrLoad[i,j], Correlation_Loadings[i,j], accurate, 'wrong value in CorrLoad[%i,%i] (svd)' % (i,j))        
           
        
        
############## SPEED TESTING ############## 

def speed_test():
        # averaged Cheese data set:
	Ost = array([[ 5.72916667,  3.41666667,  3.175     ,  2.075     ,  1.28333333,
		 2.61666667,  6.22083333,  3.55416667,  2.39583333,  4.67916667,
		 4.32916667,  2.95      ,  2.63333333,  1.99166667,  1.25      ,
		 2.87083333,  4.11666667],
	       [ 6.075     ,  2.74166667,  3.63333333,  2.22916667,  1.225     ,
		 3.38333333,  6.17083333,  2.775     ,  2.14166667,  4.26666667,
		 4.11666667,  3.37083333,  2.67083333,  2.04583333,  1.38333333,
		 3.4       ,  4.0875    ],
	       [ 6.11666667,  3.49166667,  3.52083333,  1.89166667,  1.20833333,
		 2.7125    ,  6.1625    ,  3.45833333,  2.25833333,  4.59166667,
		 4.35      ,  3.14583333,  2.76666667,  1.74166667,  1.35416667,
		 3.02916667,  4.18333333],
	       [ 6.0875    ,  3.18333333,  3.84583333,  1.925     ,  1.09166667,
		 3.025     ,  6.19583333,  3.0625    ,  2.20416667,  4.29583333,
		 4.46666667,  3.42083333,  2.57916667,  1.80833333,  1.18333333,
		 2.83333333,  4.37916667],
	       [ 6.64166667,  2.42916667,  4.39583333,  2.18333333,  1.125     ,
		 4.4375    ,  6.54583333,  2.4625    ,  2.10833333,  4.90833333,
		 4.7375    ,  3.94583333,  2.79166667,  2.2125    ,  1.29166667,
		 4.37083333,  3.99166667],
	       [ 5.95833333,  3.7625    ,  3.25833333,  1.90416667,  1.42083333,
		 2.45833333,  6.00833333,  3.86666667,  2.4875    ,  4.10833333,
		 4.09583333,  2.94583333,  2.37083333,  1.81666667,  1.39583333,
		 2.46666667,  4.4375    ],
	       [ 6.4375    ,  2.8375    ,  3.94583333,  2.225     ,  1.575     ,
		 3.49166667,  6.725     ,  2.52083333,  2.20833333,  4.3375    ,
		 4.85833333,  4.05416667,  3.0875    ,  2.35833333,  1.7       ,
		 4.1875    ,  3.8875    ],
	       [ 6.625     ,  2.85833333,  4.25      ,  2.10833333,  1.19583333,
		 3.7875    ,  6.55833333,  2.7       ,  2.21666667,  3.99166667,
		 4.82916667,  3.975     ,  2.85      ,  2.25833333,  1.54583333,
		 4.23333333,  4.01666667],
	       [ 5.99583333,  3.27083333,  3.2625    ,  2.1       ,  1.125     ,
		 2.33333333,  6.23333333,  3.0375    ,  2.37916667,  4.43333333,
		 4.66666667,  3.5625    ,  2.75833333,  2.075     ,  1.45      ,
		 3.125     ,  3.88333333],
	       [ 5.82916667,  3.35416667,  3.21666667,  1.525     ,  1.12916667,
		 1.475     ,  6.10833333,  3.35833333,  2.25833333,  4.2625    ,
		 4.15833333,  3.3375    ,  2.40833333,  1.6       ,  1.25833333,
		 2.35833333,  4.05      ],
	       [ 6.05833333,  3.0375    ,  3.8       ,  1.975     ,  1.15      ,
		 2.95      ,  6.35      ,  2.47916667,  2.22083333,  4.24166667,
		 4.55833333,  3.89583333,  2.8       ,  2.34166667,  1.54166667,
		 3.96666667,  4.12916667],
	       [ 6.33333333,  2.31666667,  4.125     ,  2.52916667,  1.45      ,
		 4.35416667,  6.75      ,  1.92916667,  2.22916667,  4.32916667,
		 4.75      ,  4.15416667,  2.9625    ,  2.64166667,  1.82916667,
		 5.06666667,  4.08333333],
	       [ 5.825     ,  4.82916667,  1.49583333,  1.07083333,  1.        ,
		 1.09583333,  6.1       ,  4.825     ,  2.45833333,  4.65      ,
		 3.99166667,  1.7875    ,  2.22083333,  1.22083333,  1.1375    ,
		 1.24583333,  4.09166667],
	       [ 5.65      ,  4.6625    ,  1.92916667,  1.025     ,  1.        ,
		 1.075     ,  6.025     ,  4.60833333,  2.175     ,  4.97083333,
		 4.12083333,  1.79583333,  2.29166667,  1.        ,  1.025     ,
		 1.025     ,  4.21666667]])        



	X = array([[2, 3, 4, 1],
		   [1, 3, 1, 5],
		   [4, 6, 4, 3],
		   [2, 1, 1, 1],
		   [1, 2, 5, 3],
		   [7, 3, 4, 1]])

	Ost_copy = Ost.copy()
        
        """
	print 
	print "nipals numeric array (5x)"
	c0 = time.clock()
	#T1, P1, explained_var1 = PCA_nipals(Ost, False)
	#T1, P1, explained_var1 = PCA_nipals(Ost, False)
	#T1, P1, explained_var1 = PCA_nipals(Ost, False)
	#T1, P1, explained_var1 = PCA_nipals(Ost, False)
	#T1, P1, explained_var1 = PCA_nipals(Ost, False)
	cpu_time = time.clock() - c0
	print "time: " + str(cpu_time*1000) + " ms\n"
	#print T1
	#print P1
	#print explained_var1

	print 
	print "nipals c (5x)"
	c0 = time.clock()
	#T2, P2, explained_var2 = PCA_nipals_c(Ost, False)
	#T2, P2, explained_var2 = PCA_nipals_c(Ost, False)
	#T2, P2, explained_var2 = PCA_nipals_c(Ost, False)
	#T2, P2, explained_var2 = PCA_nipals_c(Ost, False)
	#T2, P2, explained_var2 = PCA_nipals_c(Ost, False)
	cpu_time = time.clock() - c0
	print "time: " + str(cpu_time*1000) + " ms\n"
	#print T2
	#print P2
	#print explained_var2
        """
        
	print "svd numpy array"
	c0 = time.clock()
	T1, P1, explained_var1 = PCA_svd(Ost, False)
	cpu_time = time.clock() - c0
	print "time: " + str(cpu_time*1000) + " ms\n"

	#print T1
	#print P1
	#print explained_var1

	print 
	print "nipals numpy matrix"
	c0 = time.clock()
	T2, P2, explained_var2 = PCA_nipals(Ost_copy, False)
	cpu_time = time.clock() - c0
	print "time: " + str(cpu_time*1000) + " ms\n"
	#print T2
	#print P2
	#print explained_var2

	print 
	print "nipals numpy array"
	c0 = time.clock()
	T3, P3, explained_var3 = PCA_nipals2(Ost_copy, False)
	cpu_time = time.clock() - c0
	print "time: " + str(cpu_time*1000) + " ms\n"
	#print T3
	#print P3
	#print explained_var3

	print 
	print "nipals c"
	try:
	    c0 = time.clock()
	    T4, P4, explained_var4 = PCA_nipals_c(Ost_copy, False)
	    cpu_time = time.clock() - c0
	    print "time: " + str(cpu_time*1000) + " ms\n"
	except:
	    print "could not run PCA_nipals_c"
	#print T4
	#print P4
	#print explained_var4


"""
Some results (Windows, Ost data set):

svd numpy array
time: 6.35388017192 ms


nipals numpy matrix
time: 24.2377173635 ms


nipals numpy array
time: 69.8650247448 ms
"""

"""
I noticed Cygwin will not give valid numbers for time testing. 
Seems like there is time stepping of about 16ms. I must test
on a Linux machine where I can install scipy and numpy. 
But here is what I got anyway (with Numeric).

Some results (Cygwin, Ost data set):


nipals numeric array (5x)
time: 313.0 ms


nipals c (5x)
time: 16.0 ms  (sometimes 0.0 ms)
"""


if __name__ == '__main__':
    #speed_test()
    unittest.main()