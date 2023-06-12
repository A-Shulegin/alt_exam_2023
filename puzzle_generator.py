import time 
from random import randint
from random import shuffle
from dataclasses import dataclass, field
from typing import Union
from unification import Var, unifiable, var, vars
from kanren import conde, eq, lall, membero, run
from math import factorial
import os

@unifiable
@dataclass
class House:
    nationality: Union[str, Var] = field(default_factory=var)
    drink: Union[str, Var] = field(default_factory=var)
    animal: Union[str, Var] = field(default_factory=var)
    cigarettes: Union[str, Var] = field(default_factory=var)
    color: Union[str, Var] = field(default_factory=var)

rules = {
    1: 'eq',
    2: 'membero',
    3: 'neighbors',
    4: 'righto'
}
categories = {
    1: 'nationality',
    2: 'drink',
    3: 'animal',
    4: 'cigarettes',
    5: 'color'
}

categories_value = {
    'nationality': {
        1: 'Englishman',
        2: 'Norwegian',
        3: 'Sweden',
        4: 'Dane',
        5: 'German'
    },
    'drink': {
        1: 'beer',
        2: 'tea',
        3: 'water',
        4: 'milk', 
        5: 'coffe',
    },
    'animal': {
        1: 'birds',
        2: 'horses',
        3: 'fish',
        4: 'dogs', 
        5: 'cats',
    },
    'cigarettes': {
        1: 'Rothmans',
        2: 'Dunhill',
        3: 'Pall Mall',
        4: 'Philip Morris', 
        5: 'Marlboro',
    },
    'color': {
        1: 'white',
        2: 'yellow',
        3: 'green',
        4: 'red', 
        5: 'blue',
    },
}

def new_rule(right_answer):
    global rule_code_list
    global translated_list_of_rules
    current_rule = rules[randint(1, 4)]
    match current_rule:
        case 'eq':
            rule = new_eq_rule(right_answer)
        case 'membero':
            categories_number = [1, 2, 3, 4, 5]
            shuffle(categories_number)
            category_1 = categories[categories_number[0]]
            category_2 = categories[categories_number[1]]
            category_1_value = categories_value[category_1][randint(1, 5)]
            house_index = [getattr(right_answer[i], category_1) for i in range(5)].index(category_1_value)
            category_2_value = getattr(right_answer[house_index], category_2)
            rule = f'membero(House({category_1}="{category_1_value}", {category_2}="{category_2_value}"), houses)'
            rule_code = sorted([category_1_value, category_2_value])
            if rule_code in rule_code_list[1]:
                rule = ''
            else:
                rule_code_list[1].append(rule_code)
                rule_code = ['membero', category_1, category_1_value, category_2, category_2_value]
                translated_list_of_rules.append(rule_code)
        case 'neighbors':
            categories_number = [1, 2, 3, 4, 5]
            shuffle(categories_number)
            category_1 = categories[categories_number[0]]
            category_2 = categories[categories_number[1]]
            category_1_value = categories_value[category_1][randint(1, 5)]
            house_1_index = [getattr(right_answer[i], category_1) for i in range(5)].index(category_1_value)
            if house_1_index == 0:
                house_2_index = 1
            elif house_1_index == 4:
                house_2_index = 3
            else:
                house_diff = [-1, 1]
                shuffle(house_diff)
                house_2_index = house_1_index + house_diff[0]
            category_2_value = getattr(right_answer[house_2_index], category_2)
            rule = f'neighbors(House({category_1}="{category_1_value}"), House({category_2}="{category_2_value}"), houses)'
            rule_code = sorted([category_1_value, category_2_value])
            if rule_code in rule_code_list[2]:
                rule = ''
            else:
                rule_code_list[2].append(rule_code)
                rule_code = ['neighbors', category_1, category_1_value, category_2, category_2_value]
                translated_list_of_rules.append(rule_code)
        case 'righto':
            categories_number = [1, 2, 3, 4, 5]
            shuffle(categories_number)
            category_1 = categories[categories_number[0]]
            category_2 = categories[categories_number[1]]
            house_1_index = randint(1, 4)
            house_2_index = house_1_index - 1
            category_1_value = getattr(right_answer[house_1_index], category_1)
            category_2_value = getattr(right_answer[house_2_index], category_2)
            rule = f'righto(House({category_1}="{category_1_value}"), House({category_2}="{category_2_value}"), houses)'
            rule_code = [category_1_value, category_2_value]
            if rule_code in rule_code_list[3]:
                rule = ''
            else:
                rule_code_list[3].append(rule_code)
                rule_code = ['righto', category_1, category_1_value, category_2, category_2_value]
                translated_list_of_rules.append(rule_code)
    return rule

def new_eq_rule(right_answer):
    global rule_code_list
    global translated_list_of_rules
    category = categories[randint(1, 5)]
    category_value = categories_value[category][randint(1, 5)]
    house_number = [getattr(right_answer[i], category) for i in range(5)].index(category_value)
    rule = f'eq(House({category}="{category_value}"), houses[{house_number}])'
    rule_code = [category_value, house_number]
    if rule_code in rule_code_list[0]:
        rule = ''
    else:
        rule_code_list[0].append(rule_code)
        rule_code = ['eq', category, category_value, house_number]
        translated_list_of_rules.append(rule_code)
    return(rule)

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

def translate(rule_code):
    translate = {
        'white': 'белого цвета',
        'red': 'красного цвета',
        'blue': 'синего цвета',
        'green': 'зеленого цвета',
        'yellow': 'желтого цвета',
        'birds': 'содержат птиц',
        'horses': 'содержат лошадей',
        'fish': 'содержат рыбок',
        'cats': 'содержат кошек',
        'dogs': 'содержат собак',
        'Rothmans': 'курят Rothmans',
        'Dunhill': 'курят Dunhill',
        'Pall Mall': 'курят Pall Mall',
        'Philip Morris': 'курят Philip Morris', 
        'Marlboro': 'курят Marlboro',
        'beer': 'пьют пиво',
        'tea': 'пьют чай',
        'water': 'пьют воду',
        'milk': 'пьют молоко', 
        'coffe': 'пьют кофе',
        'Englishman': 'живет англичанин',
        'Norwegian': 'живет норвежец',
        'Sweden': 'живет швед',
        'Dane': 'живет датчанин',
        'German': 'живет немец'
    }
    match rule_code[0]:
        case 'eq':
            if rule_code[1] == 'color':
                result_rule = f'Дом №{rule_code[3]+1} {translate[rule_code[2]]}.'
            else:
                result_rule = f'В доме №{rule_code[3]+1} {translate[rule_code[2]]}.'
        case 'righto':
            if rule_code[1] == 'color':
                result_rule = f'Слева от дома {translate[rule_code[2]]} находится '
            else:
                result_rule = f'Слева от дома, в котором {translate[rule_code[2]]}, находится '
            if rule_code[3] == 'color':
                result_rule += f'дом {translate[rule_code[4]]}.'
            else:
                result_rule += f'дом, в котором {translate[rule_code[4]]}.'
        case 'membero':
            if rule_code[3] == 'color':
                temp = rule_code[4]
                rule_code[4] = rule_code[2]
                rule_code[2] = temp
                rule_code[3] = rule_code[1]
                rule_code[1] = 'color'
            if rule_code[1] == 'color':
                result_rule = f'В доме {translate[rule_code[2]]} {translate[rule_code[4]]}.'
            else:
                result_rule = f'В доме, в котором {translate[rule_code[2]]}, {translate[rule_code[4]]}.'
        case 'neighbors':
            if rule_code[1] == 'color':
                result_rule = f'Дом {translate[rule_code[2]]} и '
            else:
                result_rule = f'Дом, в котором {translate[rule_code[2]]}, и '
            if rule_code[3] == 'color':
                result_rule += f'дом {translate[rule_code[4]]} находятся по соседству.'
            else:
                result_rule += f'дом, в котором {translate[rule_code[4]]}, находятся по соседству.'
    return result_rule

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

print('Введите название файла: ')
task_name = input()
right_answer = [[], [], [], [], []]
numbers = [1, 2, 3, 4, 5]
for key in categories_value:
    shuffle(numbers)
    for j in range(5):
        right_answer[j].append(categories_value[key][numbers[j]])
for i in range(5):
    right_answer[i] = House(
        right_answer[i][0],
        right_answer[i][1],
        right_answer[i][2],
        right_answer[i][3],
        right_answer[i][4]
    )

flag = True
count = 0
rule_code_list = [[], [], [], []]
list_of_rules = []
translated_list_of_rules = []
old_quantity = 0
max_time = 1
while flag:
    start = time.time()
    rule = ''
    while rule == '':
        rule = new_rule(right_answer)
    list_of_rules.append(rule)
    goals = ''
    for i in range(len(list_of_rules)):
        goals += '   ' + str(list_of_rules[i]) + ','
        if i != len(list_of_rules) - 1:
            goals += '\n'
    result = ''
    code = f""" 
from dataclasses import dataclass, field
from typing import Union
from unification import Var, unifiable, var, vars
from kanren import conde, eq, lall, membero, run
@unifiable
@dataclass
class House:
    nationality: Union[str, Var] = field(default_factory=var)
    drink: Union[str, Var] = field(default_factory=var)
    animal: Union[str, Var] = field(default_factory=var)
    cigarettes: Union[str, Var] = field(default_factory=var)
    color: Union[str, Var] = field(default_factory=var)

def righto(right, left, houses):
    near = tuple(zip(houses[:-1], houses[1:]))
    return membero((left, right), near)
    
def neighbors(a, b, houses):
    return conde([righto(a, b, houses)], [righto(b, a, houses)])

houses = vars(5)
goals = lall(
{goals}
)

global result
result = run(0, houses, goals)
"""
    exec(code)
    end = time.time() - start
    if check_answer(result):
        flag = False
    count += 1
    new_quantity = variants_quantity(result)
    if (((old_quantity / new_quantity) >= 2 or len(list_of_rules) == 1) and end < max_time):
        old_quantity = new_quantity
        max_time += end + 0.5
        print('Добавлено условий:', count, 'Прошло времени:', end, 'Количество вариантов:', variants_quantity(result))
    else:
        list_of_rules.pop()
        translated_list_of_rules.pop()
        count -= 1
        print('Условие не было добавлено')

        

task_file = open(f"{task_name}.txt", "w+")
for i in range(5):
    task_file.write(f'Дом №{i+1}: ')
    for category in categories.values():
        task_file.write(f'{getattr(right_answer[i], category)} ')
    task_file.write('\n')
for i in range(len(translated_list_of_rules)):
    translated_list_of_rules[i] = f'{i+1}. {translate(translated_list_of_rules[i])}\n'
    task_file.write(translated_list_of_rules[i])
for i in range(len(list_of_rules)):
    list_of_rules[i] = f'{list_of_rules[i]},\n'
    task_file.write(list_of_rules[i])
    