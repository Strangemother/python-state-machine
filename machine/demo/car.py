from core import Machine, Node
from core.conditions import Condition as C
from pprint import pprint

class Car(Machine):

	def turn(self, on=True):
		e = self.nodes.get('Engine')
		is_on = e.set('on', on)
		e.set('electrics', on)

	def started(self, nodes):
		print 'Car ready to turn on'
		# self.events.listen('valid', valid)


class Engine(Node):
	on = False
	electrics = False

	def prime(self, engine, condition, *args, **kw):
		pass #self.state = 'primed'

	def get_conditions(self):
		return [
			C('ECU', 'state', 'priming', callback=self.prime)
		]

class Body(Node):
	color = 'red'


class Dashboard(Node):
	radio = True
	on = False

	def ecu_on(self, node, cond, *args, **kw):
		print 'Dashboard heard ECU on'
		print node, cond
		# import pdb; pdb.set_trace()

	def get_conditions(self):
		return (
			C('ECU', 'on', True, callback=self.ecu_on),
		)


class ECU(Node):
	on = False

	def engine_primed(self, engine, congd, *args, **kw):
		if self.state == 'priming':
			self.set('state','ready')

	def electrics_prime(self, engine, cond, *args, **kw):
		print 'Prime electrics_prime'
		# self.set('state', 'priming')
		return True


	def turn_on(self, node, cond, *args, **kw):
		print 'ECU Heard turn on', node, cond
		self.set('on', True)
		# turn on dash

	def get_conditions(self):
		return (
			C('Engine', 'on', True, callback=self.turn_on),
			C('Engine', 'electrics', True, callback=self.electrics_prime),
			C('Engine', 'primed', True, callback=self.engine_primed),
		)


def run():
	car = Car('car')
	parts = [Body(), Engine(), ECU()]
	car.start(parts)
	car.turn(on=True)

	# import pdb; pdb.set_trace()
