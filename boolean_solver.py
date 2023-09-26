import collections, typing, copy
import itertools

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

        def toString(self) -> str:
            return '('+' * '.join(sorted([i.toString() for i in self.container]))+')'
        
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

        def toString(self) -> str:
            return '('+' + '.join(sorted([i.toString() for i in self.container]))+')'
        
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
            return '<1>'

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

        def toString(self) -> str:
            return str(self)

    class Zero:
        def __repr__(self) -> str:
            return '<0>'

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

        def toString(self) -> str:
            return str(self)

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

        def toString(self) -> str:
            return str(self)

        def __str__(self) -> str:
            return repr(self)

        def __repr__(self) -> str:
            return ['', 'not '][self._not] + str(self._id)

M = entities.M
One = entities.One
Zero = entities.Zero

RULES = [
    #(M(1).AND(Zero()), Zero()),
    #(M(1).AND(One()), M(1)),
    #(M(1).AND(M(1)), M(1)),
    #(M(1).AND(M(1).NOT()), Zero()),

    #(M(1).OR(One()), One()),
    #(M(1).OR(Zero()), M(1)),
    #(M(1).OR(M(1)), M(1)),
    #(M(1).OR(M(1).NOT()), One()),

    (M(1).OR(M(1).AND(M(2))), M(1)),
    #(M(1).AND(M(2)).OR(M(1).AND(M(2).NOT())), M(1)),
    #(M(1).AND(M(2).NOT()).OR(M(2)), M(1).OR(M(2)))
]

def chunk_groups(l, groups, g = []):
    if not l and not groups:
        yield g
        return
    
    if l:
        for i, a in enumerate(l):
            if groups:
                yield from chunk_groups(l[:i]+l[i+1:], groups-1, g+[[a]])
            if g:
                yield from chunk_groups(l[:i]+l[i+1:], groups, g[:-1]+[g[-1]+[a]])

def reduce_expression(expr) -> 'operator':
    reduced = False
    for rule, result in RULES:
        if not isinstance(rule, expr.__class__):
            if hasattr(expr, 'container'):
                for i in expr.container:
                    if i.__class__.__name__ in operators.OPS and reduce_expression(i):
                        reduced = True
            continue
        
        if len(rule.container) <= len(expr.container):
            for groups in itertools.permutations(expr.container, len(rule.container)):
                
                queue = collections.deque([(sorted([*zip(rule.container, groups)], key=lambda x:len(getattr(x, 'container', [0]))), {})])
                print(queue)
                while queue:
                    pairings, bindings = queue.popleft()
                    if not pairings:
                        print('halting in here')
                        print(pairings, bindings, rule, result)
                        return True

                    a, b = pairings.pop(0)
                    bindings = {a:b for a, b in bindings.items()}
                    if not hasattr(a, 'container'):
                        a1, a2 = a.toString(), a.NOT().toString()
                        if a1 in bindings and bindings[a1].toString() != b.toString():
                            continue
                        
                        if a2 in bindings and bindings[a2].toString() != b.NOT().toString():
                            continue
                        
                        bindings[a1] = b
                        bindings[a2] = b.NOT()
                    
                        queue.append((pairings, bindings))
                        continue

                    to_produce, to_match = [], []
                    if hasattr(b, 'container'):
                        to_match = [*b.container]
                    
                    else:
                        to_match = [b]

                    if a.__class__.__name__ in ['One', 'Zero']:
                        if len(to_match) == 1 and a.toString() == to_match[0].toString():
                            queue.append(([*pairings], bindings))

                        continue

                    for j in a.container:
                        j1, j2 = j.toString(), j.NOT().toString()
                        if j1 in bindings:
                            to_match = [i for i in to_match if i not in bindings[j1].container]
                        
                        elif j2 in bindings:
                            to_match = [i for i in to_match if i not in bindings[j2].container]

                        else:
                            to_produce.append(j)

                    if len(to_produce) <= len(to_match):
                        for chunk in chunk_groups(to_match, len(to_produce)):
                            bindings = {a:b for a, b in bindings.items()}
                            for a, b in zip(to_produce, chunk):
                                a1, a2 = a.toString(), a.NOT().toString()
                                n_sub = operators.AND(*b)
                                bindings[a1] = n_sub
                                bindings[a2] = n_sub.NOT()
                        
                            queue.append(([*pairings], bindings))


                
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
    '''
    a = M(1).OR(M(2)).OR(M(3))
    a1 = M(3).OR(M(2)).OR(M(1))
    print(a.toString(), a1.toString())
    '''
    a = M(1).OR(M(1).AND(M(2)))
    _ = reduce_expression(a)


    
    
    
    


