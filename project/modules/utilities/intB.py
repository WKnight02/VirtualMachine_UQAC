# -*- coding:utf8 -*-
import numbers

class intB(object):
	"""This onject restrain int values down to 16 bits only"""

	def __init__(self, bits, *args, **kargs):
		if bits < 1: raise ValueError('bit number should be > 1')
		self.MAX_VALUE = 1 << (bits - 1)
		self.MIN_VALUE = 0
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
		if isinstance(item, tuple):
			raise NotImplementedError('Only one slicing allowed')
		elif isinstance(item, slice):
			if item.step is not None:
				raise NotImplementedError('Slicing format = [a:b]')
			start = 0 if item.start is None \
				else max(item.start, -self.bits)
			stop = self.bits - 1 if item.stop is None \
				else min(item.stop, self.bits - 1)

			print(start, stop)

			bits = stop - start + 1
			offset = bits % self.bits
			mask = (1 << offset) - 1
			return intB(bits, self() >> start & mask)
		elif item < self.bits and item < :
			return intB(2, self() >> (item % self.bits) & 1)

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
