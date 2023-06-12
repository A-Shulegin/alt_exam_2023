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
    eq(House(nationality="Норвежец"), houses[0]),
    membero(House(nationality="Англичанин", color="Красный"), houses),
    righto(House(color="Белый"), House(color="Зеленый"), houses),
    membero(House(nationality="Датчанин", drink="Чай"), houses),
    neighbors(House(cigarettes="Rothmans"), House(animal="Кошки"), houses),
    membero(House(color="Желтый", cigarettes="Dunhill"), houses),
    membero(House(nationality="Немец", cigarettes="Marlboro"), houses),
    eq(House(drink="Молоко"), houses[2]),
    neighbors(House(cigarettes="Rothmans"), House(drink="Вода"), houses),
    membero(House(cigarettes="Pall Mall", animal="Птицы"), houses),
    membero(House(nationality="Швед", animal="Собаки"), houses),
    neighbors(House(nationality="Норвежец"), House(color="Синий"), houses),
    membero(House(animal="Лошади", color="Синий"), houses),
    membero(House(cigarettes="Philip Morris", drink="Пиво"), houses),
    membero(House(color="Зеленый", drink="Кофе"), houses)
))

results = run(0, houses, goals)
for i in range(5):
    print(results[0][i])