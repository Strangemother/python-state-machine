from core.conditions import Condition as Cnd
from core.nodes import Node
from core.machine import Machine

class A(Node):
	on = False


class B(Node):
	on = False

	def chain_react(self, node, cond, val_cond):
		self.set('on', True, val_cond)

	def get_conditions(self):
		return (
			Cnd('A', 'on', True, self.chain_react),
		)


class C(Node):
	on = False

	def chain_react(self, node, cond, val_cond):
		print 'chain_react', node
		print 'chain_react', cond
		print 'chain_react', val_cond
		self.set('on', True, val_cond)

	def get_conditions(self):
		return (
			Cnd('B', 'on', True, self.chain_react),
		)


class D(Node):
	on = False

	def chain_react(self, *args, **kw):
		self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('C', 'on', True, self.chain_react),
		)


class E(Node):
	on = False

	def chain_react(self, *args, **kw):
		self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('D', 'on', True, self.chain_react),
		)


class F(Node):
	on = False

	def chain_react(self, *args, **kw):
		self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('E', 'on', True, self.chain_react),
		)


class G(Node):
	on = False

	def chain_react(self, *args, **kw):
		self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('F', 'on', True, self.chain_react),
		)


class H(Node):
	on = False

	def chain_react(self, *args, **kw):
		self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('G', 'on', True, self.chain_react),
		)


class I(Node):
	on = False

	def chain_react(self, *args, **kw):
		self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('H', 'on', True, self.chain_react),
		)


class J(Node):
	on = False

	def chain_react(self, *args, **kw):
		self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('I', 'on', True, self.chain_react),
		)


class K(Node):
	on = False

	def chain_react(self, *args, **kw):
		self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('J', 'on', True, self.chain_react),
		)


class L(Node):
	on = False

	def chain_react(self, *args, **kw):
		self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('K', 'on', True, self.chain_react),
		)


class M(Node):
	on = False

	def chain_react(self, *args, **kw):
		pass # self.set('on', True)

	def get_conditions(self):
		return (
			Cnd('L', 'on', True, self.chain_react),
		)


def run():
	m = Machine('Chain')
	nodes = [A(), B(), C(), D(), E(), F(), G(), H(), I(), J(), K(), L(), M()]
	m.start(nodes)
	import pdb; pdb.set_trace()
	a=m.nodes.get('A')
	a.set('on', True)

