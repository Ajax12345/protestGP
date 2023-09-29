import collections, typing, copy
import itertools

class operators:
    OPS = [
        'AND', 'OR', 'NAND', 'NOR'
    ]
    class AND:
        def __init__(self, *args) -> None:
            self.container = [*args]

        def toList(self, level = 0) -> list:
            if not level:
                return [[i.toList(level + 1) for i in self.container]]
            
            return [i.toList(level + 1) for i in self.container]

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
            if isinstance(_m, operators.OR):
                return _m.OR(self)

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

        def toList(self, level = 0) -> list:
            return [[K] if not isinstance(K:=i.toList(level + 1), list) else K for i in self.container]

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

        def toList(self, level = 0) -> list:
            if not level:
                return [1]
            
            return 1

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

        def toList(self, level = 0) -> list:
            if not level:
                return [0]
            
            return 0

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

        def toList(self, level = 0) -> list:
            if not level:
                return [self.toTuple()]
            
            return self.toTuple()

        def toTuple(self) -> tuple:
            return (self._not, self._id)

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
RULE_TRUNC = {
    'AND':[
        (M(1).AND(Zero()), Zero()),
        (M(1).AND(One()), M(1)),
        (M(1).AND(M(1).NOT()), Zero()),
    ],
    'OR':[
        (M(1).OR(One()), One()),
        (M(1).OR(Zero()), M(1)),
        #(M(1).OR(M(1)), M(1)),
        #(M(1).OR(M(1).NOT()), One()),
        (M(1).OR(M(1).AND(M(2))), M(1)),
        #(M(2).OR(M(1).AND(M(2).NOT()), M(1).OR(M(2)))
        #(M(1).AND(M(2)).OR(M(1).AND(M(2).NOT())), M(1)),
    ]
}

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

def reduce_expression_trunc(new_expr) -> 'operator':
    print('new expr here', new_expr)
    def not_t(t):
        return (not t[0], t[1])

    if not isinstance(new_expr, list):
        new_expr = new_expr.toList()

    new_expr = [{*i} for i in new_expr]
    for and_expr in new_expr:
        if len(and_expr) < 2:
            continue

        for rule, result in RULE_TRUNC['AND']:
            [[a, b]] = rule.toList()
            for c_a in and_expr:
                if isinstance(c_a, tuple):
                    bindings = {a:c_a, not_t(a):int(not c_a) if isinstance(c_a, int) else not_t(c_a)}
                    if (c_b:=bindings.get(b, b)) in and_expr:
                        #print(bindings, and_expr, c_a, c_b)
                        and_expr.remove(c_a)
                        and_expr.remove(c_b)
                        and_expr.add(bindings.get(result.toList(1), result.toList(1)))
                        return reduce_expression_trunc(new_expr)
    
    for rule, result in RULE_TRUNC['OR']:
        #print('rule', rule.toList())
        print('rule, result', rule, result)
        [[a], b] = sorted(rule.toList(), key=len)
        for i, c_a in enumerate(new_expr):
            bindings = {a:c_a}
            for j, c_b in enumerate(new_expr):
                if i != j:
                    if len(b) == 1 and isinstance(b[0], int):
                        if len(c_b) == 1 and isinstance(c_b_val:=[*c_b][0], int) and b[0] == c_b_val:
                            new_expr = [s for I, s in enumerate(new_expr) if I not in [j, i]] + [bindings.get(k, [k]) for k in result.toList()]
                            return reduce_expression_trunc(new_expr)
                        
                        continue

                    if not (c_a - c_b):
                        new_expr = [s for I, s in enumerate(new_expr) if I not in [j, i]] + [bindings.get(k, [k]) for k in result.toList()]
                        return reduce_expression_trunc(new_expr)

    return new_expr


def reduce_expression(new_expr) -> 'operator':
    if not isinstance(new_expr, list):
        new_expr = new_expr.toList()

    for rule, result in RULES:
        rule = rule.toList()
        if len(rule) <= len(new_expr):
            rule = sorted(rule, key=len)
            for groups in itertools.permutations([*enumerate(new_expr)], len(rule)):
                if len(rule) == 1:
                    ((group_ind, group),) = groups
                    queue = [(rule[0], group, {})]
                    while queue:
                        subrules, group, bindings = queue.pop(0)
                        if not subrules:
                            if isinstance(result, (entities.Zero, entities.One)):
                                new_expr[group_ind] = group+result.toList()

                            else:
                                #print('in here result', result.toList(), result.toList(1), bindings)
                                new_expr[group_ind] = group+[bindings[i] for i in result.toList()]
                            
                            return reduce_expression(new_expr, False)
                        
                        subrule, *subrules = subrules
                        for i, a in enumerate(group):
                            new_bindings = copy.deepcopy(bindings)
                            if isinstance(subrule, int):
                                if a == subrule:
                                    queue.append((subrules, group[:i]+group[i+1:], new_bindings))

                                continue
                            
                            if subrule in new_bindings:
                                if new_bindings[subrule] == a:
                                    queue.append((subrules, group[:i]+group[i+1:], new_bindings))

                                continue
                            
                            new_bindings[subrule] = a
                            new_bindings[(int(not subrule[0]), subrule[1])] = (int(not a[0]), a[1]) if isinstance(a, tuple) else int(not a)
                            queue.append((subrules, group[:i]+group[i+1:], new_bindings))
                        
                    continue

                queue = [([*zip(rule, groups)], {}, [])]
                while queue:
                    rule_groups, bindings, used_groups = queue.pop(0)
                    if not rule_groups:
                        if isinstance(result, (entities.Zero, entities.One)):
                            return reduce_expression([a for i, a in enumerate(new_expr) if i not in used_groups]+[result.toList()], False)

                        if isinstance(result, operators.OR):
                            return reduce_expression([a for i, a in enumerate(new_expr) if i not in used_groups] + [[k for j in i for k in bindings[j]] for i in result.toList()], False)
                        
                        return reduce_expression([a for i, a in enumerate(new_expr) if i not in used_groups] + [bindings[i] for i in result.toList()], False)
                    
                    (subrule, (group_ind, group)), *rule_groups = rule_groups
                    for chunk_group in (chunk_groups(group, len(subrule)) if len(subrule) > 1 else [[group]]):
                        new_bindings = copy.deepcopy(bindings)
                        failed = False
                        for rule_name, chosen_subgroup in zip(subrule, chunk_group):
                            if isinstance(rule_name, int):
                                if len(chosen_subgroup) != 1 or rule_name != chosen_subgroup[0]:
                                    failed = True
                                    break
                                
                                if rule_name == chosen_subgroup[0]:
                                    continue

                            s_c = sorted(chosen_subgroup)
                            if rule_name in new_bindings and new_bindings[rule_name] != s_c:
                                failed = True
                                break
                            
                            r_n = (int(not rule_name[0]), rule_name[1])
                            if r_n in new_bindings and (len(chosen_subgroup) != 1 or new_bindings[r_n] != [(int(not chosen_subgroup[0][0]), chosen_subgroup[0][1])]):
                                failed = True
                                break
                            
                            if rule_name not in new_bindings:
                                new_bindings[rule_name] = s_c

                            if len(s_c) == 1:
                                new_bindings[r_n] = [(int(not chosen_subgroup[0][0]), chosen_subgroup[0][1])] if isinstance(s_c[0], tuple) else int(not s_c[0])

                        if failed:
                            continue

                        queue.append((rule_groups, new_bindings, used_groups + [group_ind]))
                    
    return new_expr

def ListToObj(inp:typing.List[list]) -> typing.Any:
    or_container = []
    for i in inp:
        and_cont = []
        for j in i:
            if isinstance(j, tuple):
                and_cont.append(entities.M(j[1], j[0]))
            else:
                and_cont.append(entities.One() if j else entities.Zero())
        
        or_container.append(operators.AND(*and_cont))

    return operators.OR(*or_container)
                
if __name__ == '__main__':
    M = entities.M
    One = entities.One
    Zero = entities.Zero
    
    
    tests = [
        M(1).OR(Zero()),
        M(1).NOT().AND(Zero()),
        M(1).OR(M(1).NOT()),
        M(1).OR(M(1)),
        M(1).OR(M(1).AND(M(2))),
        M(1).OR(M(1).NOT().AND(M(2))),
        (M(1).NOT().OR(M(2))).AND(M(1)),
        M(1).AND(M(2)).OR(M(1).NOT().AND(M(2))),
        (M(1).NOT().OR(M(2).NOT())).AND(M(1).NOT().OR(M(2))),
        M(1).OR(M(1).AND(M(1).NOT())),
        M(1).AND(M(2)).OR(M(1).AND(M(2).NOT())),
        M(1).NOT().OR(M(2).AND(M(1).NOT())),
        M(1).NOT().NOR(M(1).NOT()),
        M(1).NOR(M(1).NOT()),
        M(1).OR(M(1).AND(M(2).NOT()).AND(M(3)).AND(M(4))),
        M(1).NOT().AND((M(1).AND(M(2)).AND(M(3)).AND(M(4))).NOT()),
        (M(1).OR(M(2).NOT()).OR(M(3).NOT())).AND(M(1).OR(M(2).NOT()).OR(M(3))).AND(M(1).OR(M(2)).OR(M(3).NOT())),
        ((M(1).AND(M(2).NOT())).AND(M(3).OR(M(2).AND(M(4)))).OR(M(1).NOT().AND(M(2).NOT()))).AND(M(3)),
        (M(1).AND(M(2))).OR(M(1).AND(M(2).OR(M(3)))).OR(M(2).AND(M(2).OR(M(3)))),
        (M(1).OR(M(2))).AND(M(1).OR(M(3))).AND(M(2).OR(M(4))).AND(M(3).OR(M(5))).AND(M(4).OR(M(6))).AND(M(5).OR(M(6)))
    ]
    for i, a in enumerate(tests, 1):
        pass
    #print(reduce_expression_trunc(M(1).AND(M(1)).AND(M(2)).AND(One())))
    #print(reduce_expression_trunc(M(1).OR(M(1).AND(M(2)))))
    #print(One().toList())


