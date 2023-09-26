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

        def NAND(self, _m) -> typing.Any:
            a, b = self.NOT(), _m.NOT()
            return a.OR(b)

        def NOR(self, _m) -> typing.Any:
            a, b = self.NOT(), _m.NOT()
            return a.AND(b)

        def OR(self, _m) -> typing.Any:
            return operators.OR(self, _m)

        def NOT(self) -> typing.Any:
            return operators.OR(*[i.NOT() for i in self.container])

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
            results = [*self.container]
            if isinstance(_m, self.__class__):
                results.extend(_m.container)
            
            else:
                results.append(_m)

            return operators.OR(*results)

        def NAND(self, _m) -> typing.Any:
            a, b = self.NOT(), _m.NOT()
            return a.OR(b)

        def NOR(self, _m) -> typing.Any:
            a, b = self.NOT(), _m.NOT()
            return a.AND(b)

        def NOT(self) -> typing.Any:
            result = None
            for i in self.container:
                v = i.NOT()
                if result is None:
                    result = v
                else:
                    result = result.AND(v)
                
            return result

        def __repr__(self) -> str:
            return '('+' + '.join(map(str, self.container))+')'
        
        def __str__(self) -> str:
            return repr(self)

class entities:
    ENTITIES = [
        'M',
        'One',
        'Zero'
    ]
    class One:
        def __repr__(self) -> str:
            return '1'

        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(entities, _f_name)(self, _m)
            
            return wrapper

        def AND(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.AND(self, _m)

            return _m.AND(self)

        def NAND(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.OR(self.NOT(), _m.NOT())
            
            a = _m.NOT()
            return a.OR(_m.NOT())

        def NOR(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.AND(self.NOT(), _m.NOT())

            a = _m.NOT()
            return a.AND(_m.NOT())

        def OR(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.OR(self, _m)

            return _m.OR(self)

        def __str__(self) -> str:
            return repr(self)

        def NOT(self) -> 'Zero':
            return entities.Zero()

    class Zero:
        def __repr__(self) -> str:
            return '0'

        def __getattr__(self, _f_name) -> typing.Callable:
            def wrapper(_m:'M') -> 'operator':
                return getattr(entities, _f_name)(self, _m)
            
            return wrapper

        def AND(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.AND(self, _m)

            return _m.AND(self)

        def NAND(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.OR(self.NOT(), _m.NOT())
            
            a = _m.NOT()
            return a.OR(_m.NOT())

        def NOR(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.AND(self.NOT(), _m.NOT())

            a = _m.NOT()
            return a.AND(_m.NOT())

        def OR(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.OR(self, _m)

            return _m.OR(self)

        def __str__(self) -> str:
            return repr(self)

        def NOT(self) -> 'One':
            return entities.One()

    class M:
        def __init__(self, _id:typing.Any, _not = False) -> None:
            self._id = _id
            self._not = _not

        def AND(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.AND(self, _m)

            return _m.AND(self)

        def NAND(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.OR(self.NOT(), _m.NOT())
            
            return _m.NAND(self)

        def NOR(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.AND(self.NOT(), _m.NOT())
            
            return _m.NOR(self)

        def OR(self, _m) -> typing.Any:
            if _m.__class__.__name__ in entities.ENTITIES:
                return operators.OR(self, _m)

            return _m.OR(self)

        def NOT(self) -> 'M':
            return entities.M(self._id, not self._not)

        def __str__(self) -> str:
            return repr(self)

        def __repr__(self) -> str:
            return ['', 'not '][self._not] + str(self._id)

M = entities.M
One = entities.One
Zero = entities.Zero

RULES = [
    (M(1).AND(Zero()), Zero()),
    (M(1).AND(One()), M(1)),
    (M(1).AND(M(1)), M(1)),
    (M(1).AND(M(1).NOT()), Zero()),

    (M(1).OR(One()), One()),
    (M(1).OR(Zero()), M(1)),
    (M(1).OR(M(1)), M(1)),
    (M(1).OR(M(1).NOT()), One()),

    (M(1).OR(M(1).AND(M(2))), M(1)),
    (M(1).AND(M(2)).OR(M(1).AND(M(2).NOT())), M(1)),
    (M(1).AND(M(2).NOT()).OR(M(2)), M(1).OR(M(2)))

]

if __name__ == '__main__':
    M = entities.M
    One = entities.One
    Zero = entities.Zero
    '''
    print(One().AND(Zero()))
    '''
    '''
    b = M(5).AND(M(6)).AND(M(7)).OR(M(4).AND(M(9)))
    c = M(10).AND(M(11))
    print(b, ', ', c)
    print(b.NOT(), ', ', c.NOT())
    print(b.NOR(c))
    '''
    a = M(1).OR(M(2)).OR(M(3))
    b = M(4).OR(M(5)).OR(M(6))
    print(a, b, a.NOR(b))


    
    
    
    


