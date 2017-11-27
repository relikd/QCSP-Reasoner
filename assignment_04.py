#!/usr/bin/env python
# coding: utf8

def powerset(seq):
    if len(seq) <= 0: yield []
    else:
    	for item in powerset(seq[1:]):
    		yield item
    		yield [seq[0]]+item


class Algebra(object):
	def __init__(self, name, *symbols):
		super(Algebra, self).__init__()
		self.name = name
		self.baseRelations = set()
		self.labels = dict()
		self.labels[frozenset([])] = "Empty Set"

	def addBaseRelations(self, *symbols):
		prevSet = frozenset(self.baseRelations)
		for symbol in symbols:
			self.baseRelations.add(symbol)
		# Update Labels
		try:
			if self.labels[prevSet] == "Universe":
				del self.labels[prevSet] # delete previous universe
		except KeyError as e:
			pass
		finally:
			self.labels[frozenset(self.baseRelations)] = "Universe"
	
	def setRelationLabel(self, label, *symbols):
		self.labels[frozenset(symbols)] = label
	
	def universe(self):
		return Relation(self, self.baseRelations, "U")

	def Rel(self, *symbols):
		return Relation(self, set(symbols), ''.join(symbols))
	
	def print_JEPD_set(self):
		print("JEPD Set for '%s':" % self.name)
		for x in powerset(list(self.baseRelations)):
			theSet = frozenset(x)
			txt = "  {%s}" % (','.join(x))
			try: txt += " \t\t(%s)" % (self.labels[theSet])
			except KeyError as e: pass
			print(txt)

	def parseStringToRelation(self, string):
		if string[0] == "{" and string[-1] == "}":
			sym = set(string[1:-1].split(','))
			name = ''.join(sym)
			print("Parsing: '%s' into '%s'" % (string, name))
			try:
				print("Assigned Label: '%s'" % self.labels[frozenset(sym)])
			except KeyError as e: pass
			return Relation(self, sym, name)

	def __str__(self):
		return "%s := {%s}" % (self.name, ','.join(self.baseRelations))


class Relation(object):
	def __init__(self, algebra, symbols, name = ""):
		super(Relation, self).__init__()
		self.name = name
		self.algebra = algebra
		self.symbols = symbols

	def intersection(self, other):
		if self.algebra != other.algebra:
			print("Can't intersect %s and %s because of Algebra Set mismatch" % (self.name, other.name))
			return "ERROR"
		name = "(%s ∩ %s)" % (self.name, other.name)
		sym = self.symbols.intersection(other.symbols)
		return Relation(self.algebra, sym, name)

	def union(self, other):
		if self.algebra != other.algebra: 
			print("Can't union %s and %s because of Algebra Set mismatch" % (self.name, other.name))
			return "ERROR"
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
		return "%s  ≣  {%s}" % (self.name, ','.join(self.symbols))


alg = Algebra("Boolean Set Algebra")
alg.addBaseRelations("<",">","=")
# alg.addBaseRelations("!")
smaller = alg.Rel("<")
larger  = alg.Rel(">")
equal   = alg.Rel("=")
seq     = alg.Rel("<","=")
leq     = alg.Rel(">","=")

alg.setRelationLabel("SMALLER","<")
alg.setRelationLabel("GREATER",">")
alg.setRelationLabel("EQUAL","=")
alg.setRelationLabel("GREQ",">","=")

print(alg)
print("")
print(leq)
print(alg.universe().intersection(smaller))
print(alg.universe().complement().intersection(smaller))
print(leq.union(smaller).intersection(equal).complement())
print("")
alg.print_JEPD_set()
print("")
greq = alg.parseStringToRelation("{>,=}")
print(greq.intersection(equal))
print("")

