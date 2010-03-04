#include "Python.h"
#include "arrayobject.h"
#include <stdlib.h>


static PyObject *calculations_scaleAndShift(PyObject *self, PyObject *args)	{
	PyArrayObject *inarr, *outarr;
	double scaleX, scaleY, shiftX, shiftY, actualX, actualY;
	unsigned char *adr;
	double *inAdr, *outAdr;
	int i, dim1, dim2;
	npy_intp outarr_dims[2];

	if(!PyArg_ParseTuple(args, "Odddd", &inarr, &scaleX, &scaleY, &shiftX, &shiftY))	{
		return NULL;
	}
	if((inarr->nd!=2))	{
		PyErr_Format(PyExc_ValueError, "Invalid input array.");
		return NULL;
	}

///////////////////////////////////////////////////////////////////////debug
//	printf("Input: %d, %d, %d, %d\n", inarr->dimensions[0], inarr->dimensions[1], inarr->strides[0], inarr->strides[1]);
//	printf("Scale and shift: %f, %f, %f, %f\n", scaleX, scaleY, shiftX, shiftY);

	adr=(unsigned char *) inarr->data;
	inAdr=(double *) adr;
	dim1=inarr->dimensions[0];
	dim2=inarr->dimensions[1];

	outarr_dims[0]=(npy_intp) dim1; outarr_dims[1]=2;
	outarr=(PyArrayObject *) PyArray_SimpleNew(2, outarr_dims, PyArray_DOUBLE);
	if(outarr==NULL)	{
		PyErr_Format(PyExc_ValueError, "Creation of an array failed (insufficient memory?)");
		return NULL;
	}
	outAdr=outarr->data;

	for(i=0; i<inarr->dimensions[0]; i++)	{
///////////////////////////////////////////////////////////////////////debug
//		printf("Pair no. %d: %f, %f\n", i, doubleAdr[2*i], doubleAdr[2*i+1]);
		actualX=inAdr[2*i];
		actualY=inAdr[2*i+1];
		actualX=round(actualX*scaleX+shiftX);
		actualY=round(actualY*scaleY+shiftY);
		outAdr[2*i]=actualX;
		outAdr[2*i+1]=actualY;
	}
	return PyArray_Return(outarr);
}

static PyObject *calculations_filterPoints(PyObject *self, PyObject *args)	{
	PyArrayObject *inarr, *outarr;
	double filterSize, lastX, lastY, maxY, minY, currentX, currentY;

	int dim1, dim2;
	int i;
	npy_intp outarr_dims[2];
	int counter;
	unsigned char *adr;
	double *inAdr, *outAdr, *buffer;

	if(!PyArg_ParseTuple(args, "Od", &inarr, &filterSize))	{
		return NULL;
	}
	if(inarr->nd!=2) {// || inarr->descr->type_num!=PyArray_DOUBLE)	{
		PyErr_Format(PyExc_ValueError, "Invalid input array");
		return NULL;
	}

	dim1=inarr->dimensions[0];
	dim2=inarr->dimensions[1];

	if((buffer=(double*)malloc(2*dim1*dim2*sizeof(double)))==NULL)  {
		PyErr_Format(PyExc_ValueError, "Insufficient memory");
		return NULL;
	}

//////////////////////////////////////////////////debug
//printf("dim1=%d, dim2=%d, strides1=%d, strides2=%d \n", dim1, dim2, strides1, strides2);

	adr=(unsigned char *) inarr->data;
	inAdr=(double *) adr;
	buffer[0]=inAdr[0]; //
	buffer[1]=inAdr[1]; // copy first pair to outAdr
	lastX=inAdr[0];
	lastY=minY=maxY=inAdr[1];
	counter=1;
//////////////////////////////////////////////////debug
//printf("Entering loop. %f - %f %f\n", lastX, minY, maxY);
	for(i=1; i<dim1; i++)	{
		currentX=inAdr[2*i];
		currentY=inAdr[2*i+1];
//////////////////////////////////////////////////debug
//printf("Pair no. %d: %f,%f\n", i, currentX, currentY);
		if((currentX-lastX)>=filterSize)  {
			buffer[counter*2]=lastX;
			buffer[counter*2+1]=minY;
			buffer[(counter+1)*2]=lastX;
			buffer[(counter+1)*2+1]=minY;
			if(currentY>lastY)  {
				buffer[(counter+1)*2+1]=maxY;
			} else {
				buffer[counter*2+1]=maxY;
			}
//////////////////////////////////////////////////debug
//printf("\tfilterSize exceeded (%f, %f): storing values %f, %f, %f\n", currentX, lastX, minY, lastX, maxY);
			lastX=currentX;
			lastY=maxY=minY=currentY;
			counter+=2;
		} else  {
			minY=(currentY<minY)?currentY:minY;
			maxY=(currentY>maxY)?currentY:maxY;
//////////////////////////////////////////////////debug
//printf("\tminY=%f, maxY=%f\n", minY, maxY);
		}
	}
	buffer[counter*2]=currentX;
	buffer[counter*2+1]=currentY;
	counter++;
//////////////////////////////////////////////////debug
//printf("Finished on %d\n", counter);

	outarr_dims[0]=(npy_intp) counter; outarr_dims[1]=2;
	outarr=(PyArrayObject *) PyArray_SimpleNew(2, outarr_dims, PyArray_DOUBLE);
	if(outarr==NULL)	{
		PyErr_Format(PyExc_ValueError, "Creation of an array failed (insufficient memory?)");
		return NULL;
	}
	outAdr=outarr->data;

	for(i=0; i<counter; i++)  {
	  outAdr[i*2]=buffer[i*2];
	  outAdr[i*2+1]=buffer[i*2+1];
	}
	free(buffer);

	return PyArray_Return(outarr);
}

static PyMethodDef calculations_methods[]={
	{"filterPoints", calculations_filterPoints, METH_VARARGS, "filterPoints(PyObject, double)\n"},
	{"scaleAndShift", calculations_scaleAndShift, METH_VARARGS, "scaleAndShift(PyObject, double, double, double, double)\n"},
	{NULL, NULL, 0, NULL}};

PyMODINIT_FUNC initcalculations()	{
	Py_InitModule3("calculations", calculations_methods, "Fast calculations for mspy.plot.\n");
	import_array();
}