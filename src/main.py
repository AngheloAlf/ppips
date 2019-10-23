#!/usr/bin/python3

from ppips import IntVar, IntProblem, Maximize, Minimize

if __name__ == "__main__":
    x = IntVar("x", range(3))
    y = IntVar("y", range(1,4))
    z = IntVar("z", range(2))

    problem = IntProblem("Example", [x, y, z])

    # funcion objetivo
    problem @= Minimize(3*x-2*z)

    # restricciones
    problem += x + y - z < 3
    problem += x+y > 1
    problem += z == 1

    print(problem)
    solutions = problem.solve("optimal")
    # print(solutions)
    for value in solutions:
        print([(k.get_expr(),v) for k, v in value.items()], problem.evaluate(value))

    # print(problem.evaluate(solutions[0])[1])
    # print(problem.evaluate({x:1, y:2, z:1}))


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
