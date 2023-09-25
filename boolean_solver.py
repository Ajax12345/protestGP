import collections, typing, copy

class operators:
    OPS = [
        'AND', 'OR', 'NAND', 'NOR'
    ]
    class AND:
        def __init__(self, *args) -> None:
            self.container = [*args]

        def AND(self, _m) -> typing.Any:
            if _m.__class__.__name__ not in operators.OPS:
                return operators.AND(*self.container, _m)

            if isinstance(_m, self.__class__):
                return operators.AND(*self.container, *_m.container)

            return _m.AND(self)

        def OR(self, _m) -> typing.Any:
            return operators.OR(self, _m)

        def __repr__(self) -> str:
            return '('+' * '.join(map(str, self.container))+')'
        
        def __str__(self) -> str:
            return repr(self)

    class OR:
        def __init__(self, *args) -> None:
            self.container = [*args]

        def AND(self, _m) -> typing.Any:
            result = []
            for i in self.container:
                if isinstance(t:=i.AND(_m), self.__class__):
                    result.extend(t.container)
                else:
                    result.append(t)
            
            return operators.OR(*result)
        
        def OR(self, _m) -> typing.Any:
            return operators.OR(*self.container, _m)

        def __repr__(self) -> str:
            return '('+' + '.join(map(str, self.container))+')'
        
        def __str__(self) -> str:
            return repr(self)

class entities:
    class One:
        def __repr__(self) -> str:
            return '<1>'

        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(entities, _f_name)(self, _m)
            
            return wrapper

        def AND(self, _m) -> typing.Any:
            if isinstance(_m, self.__class__):
                return operators.AND(self, _m)

            return _m.AND(self)

        def OR(self, _m) -> typing.Any:
            if isinstance(_m, self.__class__):
                return operators.OR(self, _m)

            return _m.OR(self)

        def __str__(self) -> str:
            return repr(self)

        def NOT(self) -> 'Zero':
            return entities.Zero()

    class Zero:
        def __repr__(self) -> str:
            return '<0>'

        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(entities, _f_name)(self, _m)
            
            return wrapper

        def AND(self, _m) -> typing.Any:
            if isinstance(_m, self.__class__):
                return operators.AND(self, _m)

            return _m.AND(self)

        def OR(self, _m) -> typing.Any:
            if isinstance(_m, self.__class__):
                return operators.OR(self, _m)

            return _m.OR(self)

        def __str__(self) -> str:
            return repr(self)

        def NOT(self) -> 'One':
            return entities.One()

    class M:
        def __init__(self, _id:typing.Any) -> None:
            self._id = _id
            self._not = False

        def AND(self, _m) -> typing.Any:
            if isinstance(_m, self.__class__):
                return operators.AND(self, _m)

            return _m.AND(self)

        def OR(self, _m) -> typing.Any:
            if isinstance(_m, self.__class__):
                return operators.OR(self, _m)

            return _m.OR(self)

        def NOT(self) -> 'M':
            self._not = not self._not
            return self

        def __str__(self) -> str:
            return repr(self)

        def __repr__(self) -> str:
            return ['', 'not '][self._not] + str(self._id)

if __name__ == '__main__':
    M = entities.M
    a = M(1).OR(M(2)).OR(M(3)).OR(M(4))
    b = M(5).OR(M(6)).OR(M(7)).OR(M(8))
    print(a, b)
    print(a.AND(b))    

    
    


