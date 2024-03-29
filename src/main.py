#!/usr/bin/python3

from ppips import IntVar, IntProblem, Maximize, Minimize

if __name__ == "__main__":
    x = IntVar("x", range(14))
    y = IntVar("y", range(1,15))
    z = IntVar("z", range(15))

    """
    asdf = x+y-(x/y)*x + 3
    print(asdf)
    print(asdf({x:2, y:4, z:2}))
    """


    # """
    problem = IntProblem("Example", [x, y, z])

    # funcion objetivo
    problem @= Minimize(3*x-2*z+y)

    # restricciones
    problem += x**2 + y - z < 8
    problem += x + y + 1 > 2
    # problem += x + z > 1
    problem += z == 1

    """
    print("Search space:", problem.compute_search_space())
    problem.node_consistency()
    print("Search space:", problem.compute_search_space())

    print("Search space:", problem.compute_search_space())
    problem.arc_consistency()
    print("Search space:", problem.compute_search_space())
    """

    # """
    print(problem)
    solutions = problem.solve("all")
    print("solutions: ", len(solutions))
    for value in solutions:
        print([(k.get_expr(),v) for k, v in value.items()], problem.evaluate(value)[1])

    # print(problem.evaluate(solutions[0])[1])
    # print(problem.evaluate({x:1, y:2, z:1}))
    # """

    """
    print()

    constr = x+y+z > 2
    print(constr)
    z.instance_value(1)
    print(constr({x:2}))
    """

    """
    values = {"x":1, y:3}

    asdf = x < 2*y
    print(asdf)
    print(values)
    print(asdf(values))
    """
