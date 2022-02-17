"""
Unittests for the parameter sorting function

"""

# imports
import unittest

from tcheasy.sort_parameters import sort_parameters

# create test class
class TestSortParameters(unittest.TestCase):
    """
    
    methods:
    --------
    setUp
        Setup method
    tearDown
        Teardown method
    test_only_positional
        Tests sorting of positionals
    test_only_args
        Tests sorting for *args
    test_mixed
        Tests sorting of mixed types

    """

    #region 'setup & teardown' -------------------
    def setUp(self) -> None:
        """setsUp the test class """        
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    #endregion

    #region 'tests' ------------------------------
    def test_only_positional(self):
        """
        Checks a function with only positional
        parameters.
        
        """

        #region 'no defaults, no hints'
        """ should return only elements for positional """


        # build function
        def example(a, b, c):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(1,2,3), {
            'positional':{'a':1, 'b':2, 'c':3},
            'args':[],
            'kwargs':{},
            'hinting':{},
            'declared':["a","b","c"],
            'self':{'available':False, 'value':None}
        })
        

        #endregion

        #region 'some defaults (use them during call), no hints'
        """ should return only elements for positional """

        # build function
        def example(a, b, c=10):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(1, b=2), {
            'positional':{'a':1, 'b':2, 'c':10},
            'args':[],
            'kwargs':{},
            'hinting':{},
            'declared':["a","b","c"],
            'self':{'available':False, 'value':None}
        })
        

        #endregion

        #region 'some defaults (do not use them), no hints'
        """ should return only elements for positional """

        # build function
        def example(a, b, c=10):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(1, b=2, c=50), {
            'positional':{'a':1, 'b':2, 'c':50},
            'args':[],
            'kwargs':{},
            'hinting':{},
            'declared':["a","b","c"],
            'self':{'available':False, 'value':None}
        })
        

        #endregion

        #region 'no defaults, some hints'
        """ should return only elements for positional 
        'None' should change to the 'any'.
        """

        # build function
        def example(a, b:str, c:int):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(1, 2, c=3), {
            'positional':{'a':1, 'b':2, 'c':3},
            'args':[],
            'kwargs':{},
            'hinting':{'a':(type(None), int, float, complex, bool, str, list, tuple, dict, set, object), 'b':str, 'c':int},
            'declared':["a","b","c"],
            'self':{'available':False, 'value':None}
        })
        
        #endregion

        #region 'some defaults (use them), some hints'
        """ should return only elements for positional 
        'None' should change to the 'any'.
        """

        # build function
        def example(a, b:str, c:int = 1):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(1, "apple")['positional'], {'a':1, 'b':"apple", 'c':1})
        
        #endregion

        #region 'some defaults (do not use them), some hints'
        """ should return only elements for positional 
        'None' should change to the 'any'.
        """

        # build function
        def example(a, b:str, c:int = 1):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(1, b="apple", c=15)['positional'], {'a':1, 'b':"apple", 'c':15})
        
        #endregion

        #region 'for class method'

        # build class
        class TestClass:

            def test_method(self:int, a, b:int, c:bool = True) -> dict:

                # get locals
                loc = locals()

                # run sorting
                result = sort_parameters(self.test_method, loc, False)

                return result

        
        # create class case
        case = TestClass()

        # run function
        result = case.test_method("123", 123, False)
        self.assertEqual(result['positional'], {'a':"123", 'b':123, 'c':False})
        self.assertEqual(result['self']['available'], True)

        #endregion

    def test_only_args(self):
        """
        Checks a function with only *args.
        
        """

        #region 'without hints'
        # build function
        def example(*args):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(100,200), {
            'positional':{},
            'args':(100, 200),
            'kwargs':{},
            'hinting':{},
            'declared':['args'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'with hints'
        """ should not add elements to hinted. """

        # build function
        def example(*args:int):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(100,200), {
            'positional':{},
            'args':(100, 200),
            'kwargs':{},
            'hinting':{},
            'declared':['args'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'test class method'
        # build class
        class TestClass:

            def __init__(self):

                self.attribute = "attribute"

            def test_method(self, *args) -> dict:

                # get locals
                loc = locals()

                # run sorting
                result = sort_parameters(self.test_method, loc, False)

                return result

        
        # create class case
        case = TestClass()

        # run function
        result = case.test_method("123", 123, False)
        self.assertEqual(result['args'], ("123", 123, False))
        self.assertEqual(result['self']['available'], True)

        #endregion

    def test_only_kwargs(self):
        """Tests a function with only **kwargs """

        #region 'without hints'
        # build function
        def example(**kwargs):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(c=100,pp="something", theta=.1), {
            'positional':{},
            'args':[],
            'kwargs':{'c':100,'pp':"something", 'theta':.1},
            'hinting':{},
            'declared':['kwargs'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'with hints'
        """ should not add elements to hinted. """

        # build function
        def example(**kwargs:int):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result


        # call it
        self.assertEqual(example(a=100,z=200), {
            'positional':{},
            'args':[],
            'kwargs':{'a':100, 'z':200},
            'hinting':{},
            'declared':['kwargs'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'test class method'
        # build class
        class TestClass:

            def test_method(self, **kwargs) -> dict:

                # get locals
                loc = locals()

                # run sorting
                result = sort_parameters(self.test_method, loc, False)

                return result

        
        # create class case
        case = TestClass()

        # run function
        result = case.test_method(z="123", p=123, q=False, y={})
        self.assertEqual(result['kwargs'], {'z':"123", 'p':123, 'q':False, 'y':{}})
        self.assertTrue(result['self']['available'])

        #endregion

    def test_mixed(self):
        """Tests a mixed function declaration """

        #region 'without defaults, without hints'
        # build function
        def example(a, b, c, *args, **kwargs):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result

        # call it
        self.assertEqual(example(100,200,300,400,k="something"), {
            'positional':{'a':100, 'b':200, 'c':300},
            'args':(400,),
            'kwargs':{'k':"something"},
            'hinting':{},
            'declared':['a', 'b', 'c', 'kwargs', 'args'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'some defaults (not using it), without hints'
        # build function
        def example(a, b="something", c="again", *args, **kwargs):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result

        # call it
        self.assertEqual(example(100,200,300,400,k="something"), {
            'positional':{'a':100, 'b':200, 'c':300},
            'args':(400,),
            'kwargs':{'k':"something"},
            'hinting':{},
            'declared':['a', 'b', 'c', 'kwargs', 'args'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'some defaults (using it), without hints, mixed order'
        # build function
        def example(a, b="something", c="again", *args, **kwargs):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result

        # call it
        self.assertEqual(example(100, p=13, c=15, k="something"), {
            'positional':{'a':100, 'b':"something", 'c':15},
            'args':(),
            'kwargs':{'k':"something", 'p':13},
            'hinting':{},
            'declared':['a', 'b', 'c', 'kwargs', 'args'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'some defaults (using it), without hints, normal order'
        # build function
        def example(a, b="something", c="again", *args, **kwargs):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result

        # call it
        self.assertEqual(example(a=100, p=13, k="something"), {
            'positional':{'a':100, 'b':"something", 'c':'again'},
            'args':(),
            'kwargs':{'k':"something", 'p':13},
            'hinting':{},
            'declared':['a', 'b', 'c', 'kwargs', 'args'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'some defaults (not using it), without hints, mixed order'
        # build function
        def example(a, b="something", c="again", *args, **kwargs):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result

        # call it
        self.assertEqual(example(a=100, p=15, c="yes", b="no", k="something"), {
            'positional':{'a':100, 'b':"no", 'c':'yes'},
            'args':(),
            'kwargs':{'k':"something", 'p':15},
            'hinting':{},
            'declared':['a', 'b', 'c', 'kwargs', 'args'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'no defaults, with hints'
        # build function
        def example(a:int, b:None, c:dict, *args:float, **kwargs):

            # get locals
            loc = locals()

            # run sorting
            result = sort_parameters(example, loc, False)

            return result

        # call it
        self.assertEqual(example(100,200,400,500,500,500,Z="none"), {
            'positional':{'a':100, 'b':200, 'c':400},
            'args':(500,500,500,),
            'kwargs':{'Z':"none"},
            'hinting':{'a':int, 'b':None, 'c':dict},
            'declared':['a', 'b', 'c', 'kwargs', 'args'],
            'self':{'available':False, 'value':None}
        })

        #endregion

        #region 'test class method'
        # build class
        class TestClass:

            def test_method(self, a:int, *args:float, **kwargs) -> dict:

                # get locals
                loc = locals()

                # run sorting
                result = sort_parameters(self.test_method, loc, False)

                return result

        
        # create class case
        case = TestClass()

        # run function
        result = case.test_method(5, True, z="123", p=123, q=False, y={})
        self.assertEqual(result['kwargs'], {'z':"123", 'p':123, 'q':False, 'y':{}})
        self.assertEqual(result['args'], (True,))
        self.assertEqual(result['positional'], {'a':5})
        self.assertEqual(result['declared'], ["a", "kwargs", "args"])
        self.assertTrue(result['self']['available'])

        #endregion
