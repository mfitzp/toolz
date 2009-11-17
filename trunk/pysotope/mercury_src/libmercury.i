%module libmercury

%{
    #define SWIG_FILE_WITH_INIT
    #include "libmercury.h"
%}

%include "numpy.i"
%include "std_vector.i"
namespace std {
	%template(DoubleVector) vector<double>;
	%template(IntVector) vector<double>;
	%template(compVec) vector<unsigned int>;
}

%init 
%{
    import_array();
%}

%include "libmercury.h"
