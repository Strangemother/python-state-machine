from machine import Machine
from node import Node
from conditions import Condition as C
from pprint import pprint


class Car(Machine):

	def turn(self, on=True):
		e = self.get_nodes('Engine')
		if len(e) > 0:
			e = e[0]
			print 'turn on', e
			is_on = e.set('on', on)
			e.set('electrics', on)

	def started(self, nodes):
		print 'Car ready to turn on'
		# self.events.listen('valid', valid)


class Engine(Node):
	on = False
	electrics = False

	def prime(self, engine, condition, *args, **kw):
		print 'Engine ECU State is priming'
		self.state = 'primed'
		print 'Engine set primed'

	def conditions(self):
		return [
			C('ECU', 'state', 'priming', valid=self.prime)
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

	def conditions(self):
		return (
			C('ECU', 'on', True, valid=self.ecu_on),
		)


class ECU(Node):
	on = False

	def engine_primed(self, engine, congd, *args, **kw):
		print 'engine primed'
		if self.state == 'priming':
			print 'Engine set ready'
			self.set('state','ready')

	def electrics_prime(self, engine, cond, *args, **kw):
		print 'Prime electrics_prime'
		self.set('state', 'priming')
		return True


	def turn_on(self, node, cond, *args, **kw):
		print 'ECU Heard turn on', node, cond
		self.set('on', True)
		# turn on dash

	def conditions(self):
		return (
			C('Engine', 'on', True, valid=self.turn_on),
			C('Engine', 'electrics', True, valid=self.electrics_prime),
			C('Engine', 'primed', True, valid=self.engine_primed),
		)


def run():
	car = Car('car')
	parts = [Body(), Dashboard(), Engine(), ECU()]
	car.add(*parts)
	car.turn(on=True)
	return car
	# import pdb; pdb.set_trace()
