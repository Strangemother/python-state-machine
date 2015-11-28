import unittest
from mock import create_autospec
from mock import MagicMock
from scatter.mixins import NameMixin, GetSetMixin, EventMixin, ConditionsMixin
from axel import Event


class TestNameMixin(unittest.TestCase):
    def test___repr__(self):
        name_mixin = NameMixin()
        expected = '<scatter.mixins:NameMixin("NameMixin")>'
        self.assertEqual(expected, name_mixin.__repr__())
        name_mixin = NameMixin()
        name_mixin._name = 'Dave'
        expected = '<scatter.mixins:NameMixin("Dave")>'
        self.assertEqual(expected, name_mixin.__repr__())

    def test___str__(self):

        name_mixin = NameMixin()
        self.assertEqual('Node "NameMixin"', name_mixin.__str__())

        m = NameMixin()
        m._name ='Dave'
        self.assertEqual('Node "Dave"', m.__str__())

    def test_get_name(self):
        name_mixin = NameMixin()
        name_mixin._name ='Dave'
        self.assertEqual('Dave', name_mixin.get_name())
        m = NameMixin()
        m.get_name()
        self.assertEqual('NameMixin', m.get_name())


class TestGetSetMixin(unittest.TestCase):
    def test___getattr__(self):
        gsm = GetSetMixin()
        key = 'foo'
        setattr(gsm, key, 1)
        self.assertEqual(1, gsm.__getattr__(key))

    def test___setattr__(self):
        get_set_mixin = GetSetMixin()
        get_set_mixin.set = MagicMock()
        key = 'foo'
        v = 1
        # get_set_mixin.__dict__[key] = v
        get_set_mixin.__setattr__(key, v)
        get_set_mixin.set.assert_called_with(key,v)

    def test___setattr____dict__(self):
        get_set_mixin = GetSetMixin()
        key = 'foo'
        v = 1
        get_set_mixin.set(key, v)
        self.assertEqual(v, get_set_mixin.__dict__[key])

    def test_get(self):
        get_set_mixin = GetSetMixin()
        k = 'foo'
        expected = 1
        get_set_mixin.__dict__[k] = expected
        self.assertEqual(expected, get_set_mixin.get(k))
        # No error raised.
        self.assertEqual(None, get_set_mixin.get('missing'))


    def test_set(self):
        get_set_mixin = GetSetMixin()
        get_set_mixin.get = MagicMock()

        k = 'foo'
        v = 1
        get_set_mixin.set(k, v)
        get_set_mixin.get.assert_called_with(k)
        self.assertEqual(v, get_set_mixin.__dict__[k])


class TestEventMixin(unittest.TestCase):

    def test__build_event(self):
        '''
        Eventor is generated on self when called.
        '''
        event_mixin = EventMixin()
        event_mixin._build_event()
        eh = event_mixin._event_handlers
        self.assertIsInstance(eh, Event)

    def test__build_event_error(self):
        '''
        An error is raised from dispatch if a handler errors.
        The error type should match the error raised from the handler
        '''
        def e_handler(name, *args, **kw):
            return 0/0

        def f_handler(name, *args, **kw):
            return bad_ref

        name = 'event_name'
        args = [1,2,4]
        # e_handler = MagicMock(return_value=[a])
        event_mixin = EventMixin()
        event_mixin._build_event()

        event_mixin._event_handlers += e_handler

        with self.assertRaises(ZeroDivisionError):
            event_mixin._dispatch(name, *args)

        event_mixin._event_handlers -= e_handler
        event_mixin._event_handlers += f_handler

        with self.assertRaises(NameError):
            event_mixin._dispatch(name, *args)

    def test__dispatch(self):
        '''
        Eventor is generated on self when called.
        '''
        event_mixin = EventMixin()
        event_mixin._build_event()
        name = 'event_name'
        args = [1,2,4]
        event_mixin._event_handlers = MagicMock(return_value=None)
        event_mixin._dispatch(name, *args)
        event_mixin._event_handlers.assert_called_with(name, *args)


class TestConditionsMixin(unittest.TestCase):

    def test_conditions(self):
        '''
        Returns a tuple
        '''
        conditions_mixin = ConditionsMixin()
        self.assertIsInstance(conditions_mixin.conditions(), tuple)

    def test__run_conditions(self):
        '''
        Empty conditions list returns true validity
        '''
        conditions_mixin = ConditionsMixin()
        self.assertTrue(conditions_mixin._run_conditions(1,2,3))

    def test__run_conditions_uses_conditions(self):

        conditions_mixin = ConditionsMixin()
        conditions_mixin.conditions = MagicMock(return_value=())
        conditions_mixin._run_conditions(1,2,3)
        conditions_mixin.conditions.assert_called_with()

    def test__conditions(self):
        '''
        Returns local conditions if they exist
        '''
        conditions_mixin = ConditionsMixin()
        foo = dict()
        conditions_mixin._conditions = foo
        self.assertEqual(conditions_mixin.conditions(), foo)

        conditions_mixin = ConditionsMixin()
        conditions_mixin._conditions = None
        self.assertIsInstance(conditions_mixin.conditions(), tuple)


if __name__ == '__main__':
    unittest.main()
