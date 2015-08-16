python
from core import TestNode, Condition
n = TestNode()
n.watch(n, n.get_attrs())
n.bar 
n.bar = 4 
n.bar 

n.valid()
c = Condition(n, 'color', 'blue')
c.valid()
# false
n.color = 'blue'
c.valid()
# true

from core.compares.simple import Negative
Negative().match(1,2)
