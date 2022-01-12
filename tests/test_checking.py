"""
Unittests for the typeChecking decorator

"""

# imports
import unittest

from tcheasy import tcheasy

# create test class
class TestTypeChecking(unittest.TestCase):
    """Tests the functionality of the typeChecking
    
    methods:
    --------
    
    
    """

    #region 'setup & teardown' -------------------
    def setUp(self) -> None:
        """setsUp the test class """        
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    #endregion

    #region 'tests' ------------------------------
    def test_decoration_defintion(self):
        """Checks the raises for wrong deco. definitions
        
        CAUTION:
        'positional' and 'kwargs' are checked by
        the same algorithmn. Therefore we only
        need to check on of them (not both).
        
        """

        #region 'to_check no dict'
        """ should not work """
        
        toCheck = []

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'to_check' needs to be a dict.")

        #endregion

        #region 'no kwargs and args'
        """ should not work """
        
        toCheck = {
            'someOther':[],
            'kwargs':[]
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'to_check' allows only the keys 'positional', 'args' & 'kwargs'.")

        #endregion
        
        #region 'kwargs def no dict'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':bool
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':["a"]
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'kwargs' needs to be a dict.")

        #endregion

        #region 'positional def no dict'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'name':'ac',
                    'type':bool
                },
                {
                    'name':'de',
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{},
            'positional':["a"]
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'positional' needs to be a dict.")

        #endregion

        #region 'kwargs keys no int'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':bool
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                5:{}
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "The passed parameter names in 'kwargs' need to be strings. Not a string: '5'.")

        #endregion

        #region 'kwargs missing type'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':bool
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{}
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "Missing 'type' definition in 'kwargs': 'hola'.")

        #endregion

        #region 'kwargs restriction not a string'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':bool
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':str,
                    'restriction':5
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'restriction' specified in 'kwargs': 'hola' is not a str.")

        #endregion

        #region 'kwargs restriction & tuple type given'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':bool
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':(str, int),
                    'restriction':"value > 5"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "If you want to use a 'restriction', then you are not allowed to pass multiple 'type's. Error occured in 'kwargs': 'hola'.")

        #endregion

        #region 'kwargs default wrong type'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':bool
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':(str, int),
                    'default':None
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "Provided 'default' specified in 'kwargs': 'hola' is no 'str | int'.")

        #endregion

        #region 'kwargs default does not meet restriction'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':bool
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':5,
                    'restriction':"value < 4"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'default' specified in 'kwargs': 'hola' does not meet the 'restriction'.")

        #endregion

        #region 'args no list'
        """ should not work """
        
        toCheck = {
            'args':{
                "hola":{
                    'type':int,
                    'default':2,
                    'restriction':"value < 4"
                }
            },
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':2,
                    'restriction':"value < 4"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'args' needs to be a list.")

        #endregion

        #region 'args elements no dict'
        """ should not work """
        
        toCheck = {
            'args':[
                []
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':5,
                    'restriction':"value < 4"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "Each element of 'args' needs to be a dict.")

        #endregion

        #region 'args missing type'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'default':5
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':2,
                    'restriction':"value < 4"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'type' missing in element '0' of 'args'.")

        #endregion

        #region 'args restriction is no string'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':bool,
                    'restriction':5
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':2,
                    'restriction':"value < 4"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'restriction' in element '0' of 'args' is not a str.")

        #endregion

        #region 'args restriction & multiple types'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':(bool, int),
                    'restriction':"value > 5"
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':2,
                    'restriction':"value < 4"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "If you want to use a 'restriction', then you are not allowed to pass multiple 'type's. Error occured at 'args': '0'.")

        #endregion

        #region 'args default not correct type'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':(bool, int),
                    'default':5.0
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':2,
                    'restriction':"value < 4"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "Provided 'default' in element '0' of 'args' is not a(n) 'bool | int'.")

        #endregion

        #region 'args default does not meet restriction'
        """ should not work """
        
        toCheck = {
            'args':[
                {
                    'type':int,
                    'default':5,
                    'restriction':"value < 4"
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':2,
                    'restriction':"value < 4"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "The 'default' specified in element '0' does not meet the 'restriction'.")

        #endregion

        #region 'args has not provided keyword ('name')'
        """ should not work """
        
        toCheck = {
            'args':[
                {   
                    'name':"ac",
                    'type':int,
                    'default':5,
                    'restriction':"value < 4"
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':2,
                    'restriction':"value < 4"
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "'args' at position '0' has a keyword, which is not one of the following: 'type', 'default', 'restriction'.")

        #endregion

        #region 'kwargs has not provided keyword'
        toCheck = {
            'args':[
                {   
                    'type':int,
                    'default':2,
                    'restriction':"value < 4"
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                    'default':2,
                    'restriction':"value < 4",
                    'notAllowed':""
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "The passed parameter 'hola' in 'kwargs' contains a keyword which is not one of the following: 'type', 'default', 'restriction'.")

        #endregion

        #region 'None not correctly provided --> kwargs'
        toCheck = {
            'args':[
                {   
                    'type':int,
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':None,
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "If you want to specify the 'type' None you have to pass it as type(None). Error in 'kwargs': 'hola'.")

        #endregion

        #region 'None not correctly provided --> args'
        toCheck = {
            'args':[
                {   
                    'type':None,
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                }
            }
        }

        with self.assertRaises(AssertionError) as e:
            @tcheasy(toCheck)
            def mixed(ac=True , *args, **kwargs):
                """Only args given with no default """
                return (ac, args, kwargs)

        err = e.exception
        self.assertEqual(str(err), "If you want to specify the 'type' None you have to pass it as type(None). Error in 'args' at position: '0'.")

        #endregion

        #region 'None correct provided'
        toCheck = {
            'args':[
                {   
                    'type':type(None),
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                "hola":{
                    'type':int,
                }
            }
        }

        @tcheasy(toCheck)
        def mixed(ac=True , *args, **kwargs):
            """Only args given with no default """
            return (ac, args, kwargs)

        #endregion

    def test_without(self):
        """Tests a function without any params """
        
        #region 'run with type_check()'
        """ should work """

        # create test function
        @tcheasy()
        def without():
            """No args or kwargs """
            return "without:DONE"

        # call the function
        self.assertEqual(without(), "without:DONE")

        #endregion
        
        #region 'run with type_check(kwargs)'
        """
        should also run, because type_check should
        skip any checks if no *args, **kwargs are
        available in the decorated function
        
        """

        @tcheasy({'kwargs':{'b':{'type':str}}})
        def without2():
            """No args or kwargs """
            return "without:DONE"

        # call the function
        self.assertEqual(without2(), "without:DONE")

        #endregion

        #region 'run with type_check(kwargs), default given'
        """
        should work because no checks or mods. are made
        because there was not a single parameter
        declared within the decorated function
        (--> whitout 2)
        
        """

        @tcheasy({'kwargs':{'b':{'type':str, 'default':"a"}}})
        def without2():
            """No args or kwargs """
            return "without:DONE"

        self.assertEqual(without2(), "without:DONE")

        #endregion

    def test_positional_defined(self):
        """Tests a function with positional arguments """

        #region 'run with type_check()'
        """ should work """
        @tcheasy()
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(1,b=2), (1,2))

        #endregion

        #region 'run with type_check(*args), but only 'positional' provided'
        """ 
        should work.
        The 'args' do only apply to *args.
        a & b are positionals and also no type hinting is
        available, therefore the checks should just be passed.

        """
        
        toCheck = {
            'args':[
                {
                    'type':int
                }
            ]
        }

        @tcheasy(toCheck)
        def args_defined2(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined2(1,2), (1,2))

        #endregion

        #region 'run with type_check(positional), to less positionals'
        """should not work --> error msg """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int,
                    'default':5
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined2(a, b):
            """Only args given with no default """
            return (a,b)
        
        
        # check
        self.assertEqual(args_defined2(1,2)['error'], "[K.0]: Your passed parameter 'b' was not expected.")

        #endregion

        #region 'run with type_check(positional), but to many pos. defined'
        """ 
        should work
        
        in the last step (during modifications) the 
        positionals and args get combined and sorted
        by appearance in the decorated function.
        In this step, all non declared variables get
        killed (even if the developer made the mistake
        to add an additional variable to 'positional').

        """
        
        toCheck = {
            'positional':{
                "a":{
                    'type':int
                    },
                "b":{
                    'type':int,
                    'default':3
                 },
                "c":{
                    'type':int,
                    'default':2
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(1,15), (1,15))

        #endregion

        #region '[K.1] run with type_check(positional), but missing default'
        """ should work --> error msg """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int
                },
                'b':{
                    'type':int
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(1), {'error':"[K.1]: The parameter 'b' is missing.", 'success':False})

        #endregion

        #region 'run with type_check(positional), added default'
        """ should work --> return added element """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int
                },
                'b':{
                    'type':int,
                    'default':3
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(1), (1,3))

        #endregion

        #region '[K.2] run with type_check(positional), wrong type'
        """ should work --> error msg """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int
                },
                'b':{
                    'type':int
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined("a",2)['error'], "[K.2]: The parameter 'a' needs to be a(n) int.")

        #endregion

        #region '[K.2] run with type_check(positional), wrong type (tuple)'
        """ should work --> error msg """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':(int, float)
                },
                'b':{
                    'type':int
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined("a",2)['error'], "[K.2]: The parameter 'a' needs to be a(n) int | float.")

        #endregion

        #region '[K.3] run with type_check(positional), added restriction'
        """ should work --> error msg """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int,
                    'restriction':"value > 5"
                },
                'b':{
                    'type':int
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(1), {'error':"[K.3]: The parameter 'a' does not meet the restriction 'value > 5'. Value is currently '1'.", 'success':False, })

        #endregion

        #region 'run with type_check(positional), no missings, added default'
        """ should work --> return passed """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int
                },
                'b':{
                    'type':int,
                    'default':3
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(1,10), (1,10))

        #endregion

        #region '[K.3] run with type_check(positional), no missings, restrictions failure'
        """ should work -->  error msg """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int,
                    'restriction':"value == 1"
                },
                'b':{
                    'type':int
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(10,10)['error'], "[K.3]: The parameter 'a' does not meet the restriction 'value == 1'. Value is currently '10'.")

        #endregion
        
        #region 'run with type_check(positional), test union with None'
        """ should work --> return passed """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int
                },
                'b':{
                    'type':(int, float, type(None)),
                    'default':3
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(1,None), (1,None))

        #endregion

        #region 'run with type_check(positional) & type hinting'
        """ 
        should work --> use the decorator 
        
        The 'toCheck' elements should overwrite any type
        hints.

        """

        toCheck = {
            'positional':{
                'a':{
                    'type':int
                },
                'b':{
                    'type':int,
                    'default':3
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined(a:str, b):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(1,10), (1,10))

        #endregion

        #region '[K.0] run with type_check(positional) & type hinting, not enought params in deco.'
        """ 
        should not work.
        The decorator has prio and therefore the
        algorithmn assumes only 1 parameter ('a').

        But the function also wants 'b'.
        --> throws error msg.

        """

        toCheck = {
            'positional':{
                'a':{
                    'type':int
                },
            }
        }

        @tcheasy(toCheck)
        def args_defined(a:str, b:int):
            """Only args given with no default """
            return (a,b)

        # check
        self.assertEqual(args_defined(1,10)['error'], "[K.0]: Your passed parameter 'b' was not expected.")

        #endregion
    
    def test_positional_defined_default(self):
        """Tests a function with pos. defaults 
        
        Due to the successful checks in 'test_args_defined'
        we are only going to test special cases
        
        """

        #region 'run with type_check(*args), missing param & missing deco. default'
        """ should work --> default of function should kick in """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int
                },
                'b':{
                    'type':int
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined_default(a, b=13):
            """Only args given with some defaults """
            return (a,b)

        # check
        self.assertEqual(args_defined_default(1), (1,13))

        #endregion

        #region '[K.3] run with type_check(*args), defaults does not meet restric.'
        """ should work --> error msg """
        
        toCheck = {
            'positional':{
                'a':{
                    'type':int
                },
                'b':{
                    'type':int,
                    'restriction':"value < 3"
                }
            }
        }

        @tcheasy(toCheck)
        def args_defined_default(a, b=13):
            """Only args given with some defaults """
            return (a,b)

        # check
        self.assertEqual(args_defined_default(1)['error'], "[K.3]: The parameter 'b' does not meet the restriction 'value < 3'. Value is currently '13'.")

        #endregion

    def test_args(self):
        """Tests a function with only *args
        
        Due to the successful checks in 'test_args_defined'
        we are only going to test special cases
        
        """

        #region '[A.0] run with type_check(*args), more parameters than in deco.'
        """ should work --> error msg """
        
        toCheck = {
            'args':[
                {
                    'type':int,
                    'default':3
                },
                {
                    'type':int
                }
            ]
        }

        @tcheasy(toCheck)
        def args_variable(*args):
            """Only args given with no default """
            return args

        # check
        self.assertEqual(args_variable(1,2,36)['error'], "[A.0]: The are more arbitrary parameters than expected (found '3', expected '2').")

        #endregion

        #region '[A.1] run with type_check(*args), but missing default'
        """ should work --> error msg """
        
        toCheck = {
            'args':[
                {
                    'type':int,
                    'default':3
                },
                {
                    'type':int
                }
            ]
        }

        @tcheasy(toCheck)
        def args_variable(*args):
            """Only args given with no default """
            return args

        # check
        self.assertEqual(args_variable(), {'error':"[A.1]: The '*args' parameter at position '1' is missing.", 'success':False})

        #endregion

        #region '[A.2] run with type_check(*args), wrong type'
        """ should work --> error msg """
        
        toCheck = {
            'args':[
                {
                    'type':int,
                    'default':3
                },
                {
                    'type':int
                }
            ]
        }

        @tcheasy(toCheck)
        def args_variable(*args):
            """Only args given with no default """
            return args

        # check
        self.assertEqual(args_variable(5, 'notAInt'), {'error':"[A.2]: The '*args' parameter at position '1' needs to be a(n) int.", 'success':False})

        #endregion

        #region '[A.3] run with type_check(*args), restriction not met'
        """ should work --> error msg """
        
        toCheck = {
            'args':[
                {
                    'type':int,
                    'default':3
                },
                {
                    'type':str,
                    'restriction':"value == 'hallo'"
                }
            ]
        }

        @tcheasy(toCheck)
        def args_variable(*args):
            """Only args given with no default """
            return args

        # check
        self.assertEqual(args_variable(5, 'notTheKey'), {'error':"[A.3]: The '*args' parameter at position '1' does not meet the restriction 'value == \'hallo\''. Value is currently 'notTheKey'.", 'success':False})

        #endregion

        #region 'run with type_check(*args), restriction met'
        """ should work --> error msg """
        
        toCheck = {
            'args':[
                {
                    'type':int,
                    'default':3
                },
                {
                    'type':str,
                    'restriction':"value in ['hallo', 'ja', 'nein']"
                }
            ]
        }

        @tcheasy(toCheck)
        def args_variable(*args):
            """Only args given with no default """
            return args

        # check
        self.assertEqual(args_variable(5, "ja"), (5, "ja"))

        #endregion

        #region 'run with type_check(*args), defaults given by deco.'
        """ should work --> return defaults """
        
        toCheck = {
            'args':[
                {
                    'type':int,
                    'default':3
                },
                {
                    'type':int,
                    'default':3
                }
            ]
        }

        @tcheasy(toCheck)
        def args_variable(*args):
            """Only args given with no default """
            return args

        # check
        self.assertEqual(args_variable(), (3,3))

        #endregion

    def test_kwargs_variable(self):
        """Tests a function with only **kwargs 
        
        **kwargs and positionals share the same
        assertions.
        Therefore only special cases are checked.
        
        """

        #region 'run with type_check(**kwargs)'
        """ should work --> return passed + defaults """
        
        toCheck = {
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def kwargs_variable(**kwargs):
            """Only args given with no default """
            return kwargs

        # check
        self.assertEqual(kwargs_variable(a=3), {'a':3, 'b':5, 'c':5})

        #endregion

        #region '[K.0]: run with type_check(**kwargs), not expected param'
        """ should work --> error msg """
        
        toCheck = {
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def kwargs_variable(**kwargs):
            """Only args given with no default """
            return kwargs

        # check
        self.assertEqual(kwargs_variable(a=3, d=5)['error'], "[K.0]: Your passed parameter 'd' was not expected.")

        #endregion

        #region '[K.1]: run with type_check(**kwargs), missing param'
        """ should work --> error msg """
        
        toCheck = {
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def kwargs_variable(**kwargs):
            """Only args given with no default """
            return kwargs

        # check
        self.assertEqual(kwargs_variable(b=5)['error'], "[K.1]: The parameter 'a' is missing.")

        #endregion

        #region '[K.2]: run with type_check(**kwargs), wrong type'
        """ should work --> error msg """
        
        toCheck = {
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def kwargs_variable(**kwargs):
            """Only args given with no default """
            return kwargs

        # check
        self.assertEqual(kwargs_variable(a=5, b="string")['error'], "[K.2]: The parameter 'b' needs to be a(n) int | NoneType.")

        #endregion

        #region '[K.3]: run with type_check(**kwargs), missed restriction'
        """ should work --> error msg """
        
        toCheck = {
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def kwargs_variable(**kwargs):
            """Only args given with no default """
            return kwargs

        # check
        self.assertEqual(kwargs_variable(a=5, c=3)['error'], "[K.3]: The parameter 'c' does not meet the restriction 'value >= 4'. Value is currently '3'.")

        #endregion

    def test_mixed(self):
        """Tests a function with positional, args, kwargs """

        #region 'run with type_check(pos, *args, **kwargs), no positionals'
        """ should work --> return passed + defaults """
        
        toCheck = {
            'args':[
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def mixed(ac=True , *args, **kwargs):
            """Only args given with no default """
            return (ac, args, kwargs)

        # check
        self.assertEqual(mixed(a=5), (True, ("default",), {'a':5, 'b':5, 'c':5}))

        #endregion

        #region '[A.1] run with type_check(pos, *args, **kwargs), no positionals'
        """ should work --> error msg
        
        So the 'toCheck' defines two parameters
        for '*args'. But non is provided.
        (the second has a default!)

        """
        
        toCheck = {
            'args':[
                {
                    'type':bool
                },
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def mixed(ac=True , *args, **kwargs):
            """Only args given with no default """
            return (ac, args, kwargs)

        # check
        self.assertEqual(mixed(a=5)['error'], "[A.1]: The '*args' parameter at position '0' is missing.")

        #endregion

        #region 'run with type_check(pos, *args, **kwargs)'
        """ should work --> return passed + defaults """
        
        toCheck = {
            'positional':{
                'ac':{
                    'type':bool
                }
            },
            'args':[
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def mixed(ac=True , *args, **kwargs):
            """Only args given with no default """
            return (ac, args, kwargs)

        # check
        self.assertEqual(mixed(a=5), (True, ("default",), {'a':5, 'b':5, 'c':5}))

        #endregion

        #region '[K.2] run with type_check(**kwargs), wrong type 'ac''
        """ should work --> error msg """
        
        toCheck = {
            'positional':{
                'ac':{
                    'type':bool,
                }
            },
            'args':[
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def mixed(ac=True , *args, **kwargs):
            """Only args given with no default """
            return (ac, args, kwargs)

        # check
        self.assertEqual(mixed(5, a=5)['error'], "[K.2]: The parameter 'ac' needs to be a(n) bool." )

        #endregion

        #region 'run with type_check(**kwargs), wrong type ac (--> type hint)'
        """ should work --> error msg """
        
        toCheck = {
            'args':[
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def mixed(ac:bool =True , *args, **kwargs):
            """Only args given with no default """
            return (ac, args, kwargs)

        # check
        self.assertEqual(mixed(5, a=5)['error'], "[K.2]: The parameter 'ac' needs to be a(n) bool." )

        #endregion

        #region 'run with type_check(**kwargs), ordering + param name'
        """ 
        Should work because all parameters are first assigned
        to '**kwargs', then the declaration info kicks in and
        sorts 'ac' back to the variables.
        
        """
        
        toCheck = {
            'args':[
                {
                    'type':str,
                    'default':"default"
                }
            ],
            'kwargs':{
                'a':{
                    'type':int,
                },
                'b':{
                    'type':(int, type(None)),
                    'default':5
                },
                'c':{
                    'type':int,
                    'default':5,
                    'restriction':"value >= 4"
                }
            }
        }

        @tcheasy(toCheck)
        def mixed(ac , *args, **kwargs):
            """Only args given with no default """
            return (ac, args, kwargs)

        # check
        self.assertEqual(mixed(a=5, ac=5), (5, ("default", ), {'a':5, 'b':5, 'c':5}) )

        #endregion

    def test_use_hints(self):
        """Uses pythons type hinting as ressource for checks 
        
        CAUTION:
        Type hints only work for positional arguments.
        Also, these are only used if 'positional'
        declarations are not provided.
        
        """

        #region 'run with type hinting'
        """ should work --> return passed + defaults """

        @tcheasy()
        def hinting(ac:str, a:int, b:bool, *args, **kwargs):
            """No default """
            return (ac, a, b, args, kwargs)

        # check
        self.assertEqual(hinting('hallo', 5, True), ('hallo', 5, True, (), {}))

        #endregion

        #region '[K.2] run with type hinting, wrong type'
        """ should work --> return error """

        @tcheasy()
        def hinting(ac:int, a:int, b:bool, *args, **kwargs):
            """No default """
            return (ac, a, b, args, kwargs)

        # check
        self.assertEqual(hinting('hallo', 5, True)['error'], "[K.2]: The parameter 'ac' needs to be a(n) int.")

        #endregion

        #region 'run with type hinting, with defaults, changed order'
        """ should work --> return passed + defaults """

        @tcheasy()
        def hinting(ac, a, b = True):
            """No default """
            return (ac, a, b)

        # check
        self.assertEqual(hinting('hallo', a=5), ('hallo', 5, True))

        #endregion

        #region 'run with type hinting, with defaults, all parameters are passed.'
        """ should work --> return passed """

        @tcheasy()
        def hinting(ac, a, b = True):
            """No default """
            return (ac, a, b)

        # check
        self.assertEqual(hinting('hallo', a=5, b=False), ('hallo', 5, False))

        #endregion

        #region 'mixed: positional by hints, **kwargs by definition'
        """ should work --> return defaults + passed """

        toCheck = {
            'kwargs':{
                'zz':{
                    'type':int,
                    'default':5
                }
            }
        }

        @tcheasy(toCheck)
        def hinting(ac:str, a, b = True, **kwargs):
            """No default """
            return (ac, a, b, kwargs)

        # check
        self.assertEqual(hinting('hallo', a=5, b=False), ('hallo', 5, False, {'zz':5}))

        #endregion

        #region '[K.2] mixed: positional by hints, **kwargs by definition; wrong type'
        """ should work --> return defaults + passed """

        toCheck = {
            'kwargs':{
                'zz':{
                    'type':int,
                    'default':5
                }
            }
        }

        @tcheasy(toCheck)
        def hinting(ac:int, a, b = True, **kwargs):
            """No default """
            return (ac, a, b, kwargs)

        # check
        self.assertEqual(hinting('hallo', a=5, b=False)['error'], "[K.2]: The parameter 'ac' needs to be a(n) int." )

        #endregion

        #region '[A.1] mixed: positional by hints, **kwargs by definition; wrong ordering'
        """ should work --> return error
        
        We changed the ordering.
        This case 'bricks' because the algorithmn assumes
        'nichts' to be the parameter 'a'.
        So overall the '*args' at position 0 is missing.

        """

        toCheck = {
            'args':[
                {
                    'type':int
                }
            ],
            'kwargs':{
                'zz':{
                    'type':int,
                    'default':5
                }
            }
        }

        @tcheasy(toCheck)
        def hinting(ac:str, a, b = True, *args, **kwargs):
            """No default """
            return (ac, a, b, args, kwargs)

        # check
        self.assertEqual(hinting('hallo', "nichts", a=5, b=False)['error'], "[A.1]: The '*args' parameter at position '0' is missing." )

        #endregion

        #region '[A.2] mixed: positional by hints, **kwargs by definition; wrong type'
        """ should work --> return error
        
        We changed the ordering.
        This case 'bricks' because the algorithmn assumes
        'nichts' to be the parameter 'a'.
        So overall the '*args' at position 0 is missing.

        """

        toCheck = {
            'args':[
                {
                    'type':int
                }
            ],
            'kwargs':{
                'zz':{
                    'type':int,
                    'default':5
                }
            }
        }

        @tcheasy(toCheck)
        def hinting(ac:str, a, b = True, *args, **kwargs):
            """No default """
            return (ac, a, b, args, kwargs)

        # check
        self.assertEqual(hinting('hallo', 5, "b", "notAInt", b=False)['error'], "[A.2]: The '*args' parameter at position '0' needs to be a(n) int." )

        #endregion




