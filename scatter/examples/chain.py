from machine import Machine
from node import Node
from conditions import Condition as Cnd
from pprint import pprint

class A(Node):
	on = False


class B(Node):
	on = False

	def chain_react(self, node, cond, val_cond):
		self.set('on', True)

	_conditions = (
			Cnd('A', 'on', True, 'chain_react'),
		)


class C(Node):
	on = False

	def chain_react(self, node, cond, val_cond):
		print 'chain_react', node
		print 'chain_react', cond
		print 'chain_react', val_cond
		self.set('on', True)

	_conditions = (
			Cnd('B', 'on', True, 'chain_react'),
		)


class D(Node):
	on = False

	_conditions = (
			Cnd('C', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


class E(Node):
	on = False

	_conditions = (
			Cnd('D', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


class F(Node):
	on = False

	_conditions = (
			Cnd('E', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


class G(Node):
	on = False

	_conditions = (
			Cnd('F', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


class H(Node):
	on = False

	_conditions = (
			Cnd('G', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


class I(Node):
	on = False

	_conditions = (
			Cnd('H', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


class J(Node):
	on = False

	_conditions = (
			Cnd('I', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


class K(Node):
	on = False

	_conditions = (
			Cnd('J', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


class L(Node):
	on = False

	_conditions = (
			Cnd('K', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


class M(Node):
	on = False

	_conditions = (
			Cnd('L', 'on', True, 'chain_react'),
		)

	def chain_react(self, *args, **kw):
		self.set('on', True)


def run():
	m = Machine('Chain')
	nodes = [A(), B(), C(), D(), E(), F(), G(), H(), I(), J(), K(), L(), M()]
	m.add(*nodes)
	# import pdb; pdb.set_trace()
	a=m.get_nodes('A')[0]
	a.set('on', True)

