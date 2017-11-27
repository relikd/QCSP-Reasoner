#!/usr/bin/env python3
# coding: utf8

class Algebra(object):
	def __init__(self, name, *symbols):
		super(Algebra, self).__init__()
		self.name = name
		self.baseRelations = set()
	
	def addBaseRelations(self, *symbols):
		for symbol in symbols:
			self.baseRelations.add(symbol)
	
	def universe(self):
		return Relation(self, self.baseRelations, "U")

	def Rel(self, *symbols):
		return Relation(self, set(symbols), ''.join(symbols))
	
	def __str__(self):
		return "%s := {%s}" % (self.name, ','.join(self.baseRelations))


class Relation(object):
	def __init__(self, algebra, symbols, name = ""):
		super(Relation, self).__init__()
		self.name = name
		self.algebra = algebra
		self.symbols = symbols

	def intersection(self, other):
		if self.algebra != other.algebra: return "ERROR"
		name = "(%s ∩ %s)" % (self.name, other.name)
		sym = self.symbols.intersection(other.symbols)
		return Relation(self.algebra, sym, name)

	def union(self, other):
		if self.algebra != other.algebra: return "ERROR"
		name = "(%s ∪ %s)" % (self.name, other.name)
		sym = self.symbols.union(other.symbols)
		return Relation(self.algebra, sym, name)

	def complement(self):
		name = "%sᶜ" % (self.name) # converse "%s⁻¹" % (self.name)
		# remove double complement
		# while name[-6:] == "ᶜᶜ": name = name[:-6]
		sym = self.symbols.symmetric_difference(self.algebra.baseRelations)
		return Relation(self.algebra, sym, name)
	
	def __str__(self):
		return "%s  =  {%s}" % (self.name, ','.join(self.symbols))


alg = Algebra("Boolean Set Algebra")
alg.addBaseRelations("<",">","=") 
smaller = alg.Rel("<")
larger  = alg.Rel(">")
equal   = alg.Rel("=")
seq     = alg.Rel("<","=")
leq     = alg.Rel(">","=")

print alg
print 
print leq
print alg.universe().intersection(smaller)
print alg.universe().complement().intersection(smaller)
print leq.union(smaller).intersection(equal).complement()
print 

