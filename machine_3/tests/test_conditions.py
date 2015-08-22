import unittest
from mock import Mock
from ..conditions import Condition
from ..machine.managers import ConditionsManager


class ConditionsTest(unittest.TestCase):

    def test_condition_names(self):
        '''
        A condition can be found by an alias
        '''
        cds = ConditionsManager()
        c= Condition('foo', 'bar',3)
        cds.append_with_names( ('wibble', 'tos',), c)
        self.assertIn('wibble', cds._names)
