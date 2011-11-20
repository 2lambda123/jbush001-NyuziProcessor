from testcase import *
from types import *
import struct

class FloatingPointTests(TestCase):
	def test_floatingPointAddition():
		testValues = [
			(17.79, 19.32, 37.11), # Exponents are equal
			(0.34, 44.23, 0x423247ad), # Exponent 2 larger (44.57, adjusted for truncated rounding)
			(44.23, 0.034, 0x42310e55), # Exponent 1 larger
			(-1.0, 5.0, 4.0), # First element is negative and has smaller exponent
			(-5.0, 1.0, -4.0), # First element is negative and has larger exponent		
			(5.0, -1.0, 4.0),  # Second element is negative and has smaller exponent
			(1.0, -5.0, -4.0), # Second element is negative and has larger exponent
			(5.0, 0.0, 5.0), # Zero identity (zero is a special case in IEEE754)
			(0.0, 5.0, 5.0),
			(0.0, 0.0, 0.0),
			(7.0, -7.0, 0.0), # Result is zero
			(1000000.0, 0.0000001, 1000000.0), # Second op is lost because of precision
			(0.0000001, 0.00000001, 0x33ec3923), # Very small number 
			(1000000.0, 10000000.0, 11000000.0)	# Very large number
		]

		cases = []
	
		regIndex = 0
		inRegs = {}
		outRegs = {}
		code = ''
		for value1, value2, expectedResult in testValues:
			outRegs['u' + str(regIndex)] = expectedResult
			inRegs['u' + str(regIndex + 1)] = value1
			inRegs['u' + str(regIndex + 2)] = value2
			code += 'f' + str(regIndex) + ' = f' + str(regIndex + 1) + ' + f' + str(regIndex + 2) + '\n'
			regIndex += 3
			
			if regIndex == 30:
				cases +=  [ (inRegs, code, outRegs, None, None, None) ]
				inRegs = {}
				outRegs = {}
				code = ''
				regIndex = 0
	
		if regIndex > 0:
			cases +=  [ (inRegs, code, outRegs, None, None, None) ]
			inRegs = {}
			outRegs = {}
			code = ''

		return cases
	
	def test_floatingPointScalarCompare():
		testValues = [
			(-2.0, '>', -3.0, 1),
			(-3.0, '>', -2.0, 0),
			(17.0, '>', 2.0, 1),
			(2.0, '>', 17.0, 0),
			(5, '>', -17, 1),
			(-17, '>', 5, 0),
			(15, '>', -7, 1),
			(-7, '>', 15, 0),
			(-2.0, '>=', -3.0, 1),
			(-3.0, '>=', -2.0, 0),
			(17.0, '>=', 2.0, 1),
			(2.0, '>=', 17.0, 0),
			(5, '>=', -17, 1),
			(-17, '>=', 5, 0),
			(15, '>=', -7, 1),
			(-7, '>=', 15, 0),
			(-5, '>=', -5, 1),
			(-2.0, '<', -3.0, 0),
			(-3.0, '<', -2.0, 1),
			(17.0, '<', 2.0, 0),
			(2.0, '<', 17.0, 1),
			(5, '<', -17, 0),
			(-17, '<', 5, 1),
			(15, '<', -7, 0),
			(-7, '<', 15, 1),
			(-2.0, '<=', -3.0, 0),
			(-3.0, '<=', -2.0, 1),
			(17.0, '<=', 2.0, 0),
			(2.0, '<=', 17.0, 1),
			(5, '<=', -17, 0),
			(-17, '<=', 5, 1),
			(15, '<=', -7, 0),
			(-7, '<=', 15, 1),
			(-5, '<=', -5, 1),
		]
	
		cases = []
		regIndex = 0
		inRegs = {}
		outRegs = {}
		code = ''
		for value1, operator, value2, expectedResult in testValues:
			outRegs['u' + str(regIndex)] = 0xffff if expectedResult else 0
			inRegs['u' + str(regIndex + 1)] = value1
			inRegs['u' + str(regIndex + 2)] = value2
			code += 'u' + str(regIndex) + ' = f' + str(regIndex + 1) + ' ' + operator + ' f' + str(regIndex + 2) + '\n'
			regIndex += 3
			
			if regIndex == 30:
				cases +=  [ (inRegs, code, outRegs, None, None, None) ]
				inRegs = {}
				outRegs = {}
				code = ''
				regIndex = 0
	
		if regIndex > 0:
			cases +=  [ (inRegs, code, outRegs, None, None, None) ]
			inRegs = {}
			outRegs = {}
			code = ''
			
		return cases
	
	def test_floatingPointVectorCompare():
		vec1 = [ (random.random() - 0.5) * 10 for x in range(16) ]
		vec2 = [ (random.random() - 0.5) * 10 for x in range(16) ]
		
		greaterMask = 0
		lessMask = 0
		greaterEqualMask = 0
		lessEqualMask = 0
		for x in range(16):
			greaterMask |= (0x8000 >> x) if vec1[x] > vec2[x] else 0
			lessMask |= (0x8000 >> x) if vec1[x] < vec2[x] else 0
			greaterEqualMask |= (0x8000 >> x) if vec1[x] >= vec2[x] else 0
			lessEqualMask |= (0x8000 >> x) if vec1[x] <= vec2[x] else 0
	
		return ({ 	'v0' : [ x for x in vec1 ],
					'v1' : [ x for x in vec2 ] },
			'''
				s2 = vf0 > vf1  
				s3 = vf0 < vf1
				s4 = vf0 >= vf1
				s5 = vf0 <= vf1
			''',
			{ 	'u2' : greaterMask, 
				'u3' : lessMask,	 
				'u4' : greaterEqualMask,	
				'u5' : lessEqualMask }, None, None, None)	
				
	def test_floatingPointRAWDependency():
		return ({ 'u1' : 7.0, 'u2' : 11.0, 'u4' : 13.0 }, '''
			f0 = f1 + f2
			f3 = f0 + f4
		''', { 'u0' : 18.0, 'u3' : 31.0 }, None, None, None)

	def test_infAndNanAddition():
		INF = 0x7f800000
		NAN = 0xffffffff
	
		return ({ 'u1' : INF, 'u2' : NAN, 'u3' : 3.14 }, '''
			f4 = f1 - f1		; inf - inf = nan
			f5 = f1 + f3		; inf + anything = inf
			f6 = f1 + f1		; inf + inf = inf
			f7 = f1 - f3		; inf - anything = inf
			f8 = f2 + f3		; nan + anything = nan
			f9 = f2 + f2		; nan + nan = nan
			f10 = f2 - f3		; nan - anything = nan
			f11 = f2 - f2		; nan - nan = nan
		''', { 
			'u4' : NAN,
			'u5' : INF,
			'u6' : INF,
			'u7' : INF,
			'u8' : NAN,
			'u9' : NAN,
			'u10' : NAN,
			'u11' : NAN
		}, None, None, None)
		
	def test_floatingPointMultiplication():
		return ({ 'u1' : 2.0, 
			'u2' : 4.0, 
			'u5' : 27.3943, 
			'u6' : 99.382,
			'u8' : -3.1415,
			'u9' : 2.71828,
			'u11' : -1.2,
			'u12' : -2.3,
			'u14' : 4.0,
			'u15'  : 0.001,
			'u17'	: 0.0,
			'u18'	: 19.4
			}, '''
			f3 = f1 * f2
			f4 = f5 * f6
			f7 = f8 * f9
			f10 = f11 * f12
			f13 = f14 * f15
			f16 = f17 * f18		; zero identity
			f19 = f18 * f17		; zero identity (zero in second position)
		''', { 'u3' : 8.0, 
			'u4' : 2722.5003226,
			'u7' : -8.53947662,
			'u10' : 2.76,
			'u13' : 0.004,
			'u16' : 0.0,
			'u19' : 0.0
		}, None, None, None)
		
	def test_itof():
		return ({ 'u1' : 12, 
				'u2' : 1.0, 
				'u5' : -123, 
				'u7' : 23, 
				'u8' : 4.0 },
			'''
				f3 = sitof(u1, f2)	
				f4 = sitof(u5, f2)
				f6 = sitof(u7, f8)
			''',
			{ 'u3' : 12.0,
			 	'u4' : -123.0,
			 	'u6' : 92.0
			}, None, None, None)

	def test_ftoi():
		return ({ 'u1' : 12.0, 
				'u2' : 1.0, 
				'u5' : -123.0, 
				'u7' : 23.0, 
				'u8' : 4.0 },
			'''
				u3 = sftoi(f1, f2)	
				u4 = sftoi(f5, f2)
				u6 = sftoi(f7, f8)
			''',
			{ 'u3' : 12,
			 	'u4' : -123,
			 	'u6' : 92
			}, None, None, None)
			
	def test_reciprocal():
		return ({ 'u1' : 12345.0 }, '''
			f0 = reciprocal(f1)
		''', { 'u0' : 0x38a9c000 }, None, None, None)
	
	
			
			
			
