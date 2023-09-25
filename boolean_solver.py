import collections, typing

class operators:
    class AND:
        def __init__(self, a, b) -> None:
            self.a, self.b = a, b

        def __repr__(self) -> str:
            return f'({self.a} * {self.b})'

        def __str__(self) -> str:
            return repr(self)

        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(operators, _f_name)(self, _m)
            
            return wrapper

    class OR:
        def __init__(self, a, b) -> None:
            self.a, self.b = a, b

        def __repr__(self) -> str:
            return f'({self.a} + {self.b})'

        def __str__(self) -> str:
            return repr(self)

        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(operators, _f_name)(self, _m)
            
            return wrapper

    class NAND:
        def __init__(self, a, b) -> None:
            self.a, self.b = a, b

        def __repr__(self) -> str:
            return f'[({self.a}) * ({self.b})]'

        def __str__(self) -> str:
            return repr(self)

        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(operators, _f_name)(self, _m)
            
            return wrapper

    class NOR:
        def __init__(self, a, b) -> None:
            self.a, self.b = a, b

        def __repr__(self) -> str:
            return f'[({self.a}) + ({self.b})]'

        def __str__(self) -> str:
            return repr(self)
        
        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(operators, _f_name)(self, _m)
            
            return wrapper

    class One:
        def __repr__(self) -> str:
            return '1'

        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(operators, _f_name)(self, _m)
            
            return wrapper

        def __str__(self) -> str:
            return repr(self)

        def not_(self) -> 'Zero':
            return operators.Zero()

    class Zero:
        def __repr__(self) -> str:
            return '0'

        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(operators, _f_name)(self, _m)
            
            return wrapper

        def __str__(self) -> str:
            return repr(self)

        def not_(self) -> 'One':
            return operators.One()

class M:
    def __init__(self, _id:typing.Any) -> None:
        self._id = _id
        self._not = False

    def not_(self) -> 'M':
        self._not = not self._not
        return self

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return ['', 'not '][self._not] + str(self._id)

    def __getattr__(self, _f_name) -> typing.Callable:
        def wrapper(_m:'M') -> 'operator':
            return getattr(operators, _f_name)(self._id, _m)
        
        return wrapper

if __name__ == '__main__':
    print(M(1).AND(M(2)).OR(M(3)).NOR(M(4)))
    

    
    


