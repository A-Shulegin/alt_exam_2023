from dataclasses import dataclass, field
from typing import Union
from unification import Var, unifiable, var, vars
from kanren import conde, eq, lall, membero, run
from math import factorial

@unifiable
@dataclass

class House:
    nationality: Union[str, Var] = field(default_factory=var)
    color: Union[str, Var] = field(default_factory=var)
    animal: Union[str, Var] = field(default_factory=var)
    drink: Union[str, Var] = field(default_factory=var)
    cigarettes: Union[str, Var] = field(default_factory=var)
    

def righto(right, left, houses):
    neighbors = tuple(zip(houses[:-1], houses[1:]))
    return membero((left, right), neighbors)

def neighbors(a, b, houses):
    return conde(
        [righto(a, b, houses)],
        [righto(b, a, houses)]
    )

def check_answer(answer):
    flag = True
    if len(answer) > 1:
        flag = False
    else:
        answer = answer[0]
        try:
            for category in ['nationality', 'drink', 'animal', 'cigarettes', 'color']:
                undefine_count = 0
                for i in range(5):
                    if type(getattr(answer[i], category)) != str:
                        undefine_count += 1
                if undefine_count > 1:
                    flag = False
        except:
            flag = False
    return flag

def variants_quantity(result):
    variants_quantity = 0
    for i in range(len(result)):
        empty = [0, 0, 0, 0, 0]
        for j in range(5):
            if type(result[i][j]) == House:
                if type(result[i][j].nationality) != str:
                    empty[0] += 1
                if type(result[i][j].drink) != str:
                    empty[1] += 1
                if type(result[i][j].animal) != str:
                    empty[2] += 1
                if type(result[i][j].cigarettes) != str:
                    empty[3] += 1
                if type(result[i][j].color) != str:
                    empty[4] += 1
            else:
                for k in range(5):
                    empty[k] += 1
        for j in range(5):
            empty[j] = factorial(empty[j])
        variants_quantity += empty[0] * empty[1] * empty[2] * empty[3] * empty[4]
    return(variants_quantity)

houses = vars(5)
goals = conde((
    eq(House(animal="cats"), houses[4]),
    neighbors(House(nationality="Dane"), House(drink="water"), houses),
    righto(House(animal="fish"), House(nationality="Sweden"), houses),
    membero(House(animal="horses", nationality="Sweden"), houses),
    eq(House(drink="milk"), houses[2]),
    membero(House(animal="dogs", cigarettes="Philip Morris"), houses),
    membero(House(drink="tea", nationality="German"), houses),
    righto(House(cigarettes="Pall Mall"), House(color="yellow"), houses),
    eq(House(cigarettes="Rothmans"), houses[2]),
    righto(House(animal="cats"), House(nationality="Norwegian"), houses),
    eq(House(nationality="German"), houses[0]),
    righto(House(cigarettes="Marlboro"), House(drink="tea"), houses),
    righto(House(drink="beer"), House(nationality="Norwegian"), houses),
    righto(House(drink="water"), House(nationality="Englishman"), houses),
    neighbors(House(cigarettes="Dunhill"), House(nationality="Dane"), houses),
    righto(House(cigarettes="Dunhill"), House(color="red"), houses),
    neighbors(House(nationality="German"), House(color="blue"), houses),
    membero(House(color="white", drink="beer"), houses),
))

results = run(0, houses, goals)
print(check_answer(results))
if (check_answer(results)):
    for i in range(5):
        print(results[0][i])