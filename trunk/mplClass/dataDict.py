import os
import sys
import traceback

import numpy as N

class dataSet(dict):
	def __init__(self):
		'''
		Traditionally setup with x and y data
		though a single dataSet could potentially contain 
		more than one dimension.
		
		Work in Progress
			markerStyle
			lineStyle
		'''
		self.keyList = ['xData',
						'yData',
						'zData',
						'numDims',
						'lineStyle',
						'markerStyle',
						'filePath',
						'notes'
						]
				
		for k in self.keyList:
			'''
			Be aware: the note key will be overwritten as a string later...
			This is also true for the numDims key
			'''
			self[k] = []
		
		#this is assumed but will be checked if a 3rd dimension is added
		self['numDims'] = 2 
		self.ready = False
	
	###########################################
	def checkStatus(self, checkDims = False):
		'''
		Determines whether all conditions are met to plot the data
		checkDims flag is for a 3D instance
		'''
		self.ready = True
		
		keyList = ['xData', 'yData', 'zData']
		lenX = len(self['xData'])
		lenY = len(self['yData'])
		lenZ = len(self['zData'])
		
		if lenX != lenY:
			self.ready = False
			return self.ready
		
		if checkDims:
			if lenX != lenZ:
				self.ready = False
				return self.ready
		
		for i in xrange(lenX):
			'''
			iterate through each dataset
			'''
			lenXArray = len(self['xData'][i])
			lenYArray = len(self['yData'][i])
			if lenXArray != lenYarray:
				self.ready = False
				return self.ready
			
			if checkDims:
				lenZArray = len(self['zData'][i])
				if lenXArray != lenZarray:
					self.ready = False
					return self.ready
			
		
		return self.ready
	
	###########################################
	def setXData(self, xArray, filePath = None):
		'''
		Accepts a numpy array
		'''
		if isinstance(xArray, N.ndarray):
			self['xData'].append(xArray)
		
		self.checkStatus()
	
	###########################################
	def setYData(self, yArray, filePath = None):
		'''
		Accepts a numpy array
		filePath is more for record keeping and not necessary
		'''
		if isinstance(yArray, N.ndarray):
			self['yData'].append(yArray)		
		
		self.checkStatus()
	
	###########################################
	def setZData(self, zArray):
		'''
		Accepts a numpy array
		'''
		if isinstance(zArray, N.ndarray):
			self['zData'].append(zArray)		
		
		self.checkStatus(checkDims = True)		
	
	###########################################
	def setNotes(self, noteStr):
		if isinstance(noteStr, str):
			self['notes'] = noteStr
	

if __name__ == "__main__":
	a = dataSet()
	print a.keys()
