import toolz
from kanren import Relation, conde, facts, run, eq, appendo
from cons import cons
from unification import var

father = Relation()
mother = Relation()
facts(
    father,
    ("Семенов Д.Д.", "Филлипова В.Д."),
    ("Филиппов А.А.", "Филиппов Д.А."),
    ("Филиппов Д.А.", "Шувалова И.Д."),
    ("Филиппов Д.А.", "Федорова А.Д."),
    ("Федоров Г.Д.", "Федоров М.Г."),
    ("Федоров Г.Д. Федорова Я.Г."),
    ("Шувалов И.Н.", "Шувалов В.И."),
    ("Шувалов В.И", "Шувалов В.В."),
    ("Шувалов В.И", "Шувалова Е.В."),
    ("Федоров М.Г.", "Кудрявцева А.М."),
    ("Федоров М.Г", "Федоров В.М."),
    ("Федоров М.Г.", "Федоров А.М."),
    ("Кудрявцев Г.В.", "Кудрявцев Г.Г."),
    ("Кудрявцев Г.Г.", "Кудрявцев К.Г."),
    ("Федоров А.М.", "Федоров Я.А."),
)
facts(
    mother,
    ("Семенова М.Д.", "Филлипова В.Д."),
    ("Филиппова М.И.", "Филиппов Д.А."),
    ("Филиппова В.Д.", "Шувалова И.Д."),
    ("Филиппова В.Д.", "Федорова А.Д."),
    ("Федорова М.М.", "Федоров М.Г."),
    ("Федорова М.М.", "Федорова Я.Г."),
    ("Шувалова И.Д.", "Шувалов В.И."),
    ("Шувалова А.А.", "Шувалов В.В."),
    ("Шувалова А.А.", "Шувалов E.В."),
    ("Федорова А.Д.", "Кудрявцева А.М."),
    ("Федорова А.Д.", "Федоров В.М."),
    ("Федорова А.Д.", "Федоров А.М."),
    ("Кудрявцева А.М.", "Кудрявцев Г.Г."),
    ("Кудрявцева А.М.", "Кудрявцев К.Г."),
    ("Федорова К.М.", "Федоров Я.A."),
)


def parent(a, b):
    return conde(
        [father(a, b)],
        [mother(a, b)]
    )

def sibling(a, b):
    p = var()
    return conde((parent(p, a), parent(p, b)))

def nephew(a, b):
    q = var()
    return conde((parent(q, a), sibling(q, b)))

def spouse(a, b):
    c = var()
    return conde((parent(a, c), parent(b, c)))

def childs_spouse(a, b):
    c = var()
    return conde((parent(b, c), spouse(a, c)))

def childs_spouses_nephew(a, b):
    c = var()
    return conde((childs_spouse(c, b), nephew(a, c)))


q = var()
name = "Федоров Г.Д."
result_parent = run(0, q, childs_spouses_nephew(q, name), results_filter=toolz.unique)
print(result_parent)

