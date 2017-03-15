# -*- coding:utf8 -*-
import numbers

class intB(object):
	"""This onject restrain int values down to 16 bits only"""
	MAX_VALUE = 1
	MIN_VALUE = 0
	
	def __init__(self, bits, *args, **kargs):
		if bits < 1: raise ValueError('bit number should be > 1')
		self.MAX_VALUE = 1 << (bits - 1)
		self.bits = bits
		self.set(int(*args))
	
	def index(self):
		return self.value
	
	def __repr__(self):
		return 'int%d(%d)' % (self.bits, self.value)
	
	def __call__(self):
		return self.value
	
	def set(self, value):
		self.value = value % self.MAX_VALUE
		return self.value
	
	# ~self
	def __invert__(self):
		return intB(self.bits, self.MAX_VALUE - self.value)
	
	# self[a:b]
	def __getitem__(self, item):
		print(item)
	
	# self + value
	def __add__(self, value): return intB(self.bits, self() + value)
	def __radd__(self, value): return self.__add__(value)
	
	# self - value
	def __sub__(self, value): return self.__add__(-value)
	def __rsub__(self, value): return self.__sub__(value)
	
	# self * value
	def __mul__(self, value): return intB(self.bits, self() * value)
	def __rmul__(self, value): return self.__mul__(value)
	
	# self / value
	def __div__(self, value): return intB(self.bits, self() // value)
	def __rdiv__(self, value): return self.__div__(value)
	
	# self << value
	def __lshift__(self, value): return intB(self.bits, self() << value)
	
	# self >> value
	def __rshift__(self, value): return intB(self.bits, self() >> value)