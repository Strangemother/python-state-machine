import unittest
from ..usage.runner import Runner

class BasicTests(unittest.TestCase):

    def setUp(self):
       self.r = Runner()
        
    def test_can_run(self):
        '''
        Can Runner.run be called on the Class, calling 
        an internal method.
        '''
        # the run method can be called to
        # run to method on the Runner class
        # using the provided variable
        is_ran = self.r.run('ran')
        self.assertTrue(self.r._ran)
        self.assertTrue(is_ran)
        self.assertIs(str, type(self.r.run('hello')) )


def main():
    unittest.main()


if __name__ == '__main__':
    main()