from swiplserver import PrologMQI, PrologThread, create_posix_path
import re


def get_param(old):
    return '"' + old + '"' if "_" not in old else old.upper()


def get_result(res, no, yes):
    resp = ""
    if not res or type(res) != bool and len(res) == 0:
        resp = no
    else:
        if type(res) == bool:
            resp = yes
        else:
            ans = {}
            for el in res:
                for key in el:
                    if key not in ans:
                        ans[key] = [el[key]]
                    else:
                        ans[key].append(el[key])
            res = []
            for key in ans:
                res.append(f"{key}:")
                res.append("\n".join(ans[key]))
            resp = "\n".join(res)
    resp += "\n" + "-"*30
    return resp


class CheckCanAttackI:
    def __init__(self, card1, card2):
        self.card1 = get_param(card1)
        self.card2 = get_param(card2)

    def execute(self, prolog_thread):
        res = prolog_thread.query(f'canAttack({self.card1}, {self.card2}).')
        print(get_result(res, "Cant attack", "Can attack"))


class CheckCanAttackMe:
    def __init__(self, card1, card2):
        self.card2 = get_param(card1)
        self.card1 = get_param(card2)

    def execute(self, prolog_thread):
        res = prolog_thread.query(f'canAttack({self.card1}, {self.card2}).')
        print(get_result(res, "Cant attack", "Can attack"))


class CheckCanDistractEnemy:
    def __init__(self, card1, card2):
        self.card2 = get_param(card1)
        self.card1 = get_param(card2)

    def execute(self, prolog_thread):
        res = prolog_thread.query(f'canDefense({self.card1}, {self.card2}).')
        print(get_result(res, "Cant distract", "Can distract"))


class GetAllCheaperAllEquals:
    def __init__(self, card1, card2):
        self.card2 = get_param(card1)
        self.card1 = get_param(card2)

    def execute(self, prolog_thread):
        res = prolog_thread.query(f'cheaperOrEq({self.card1}, {self.card2}).')
        print(get_result(res, "Nothing found", "Cheaper or equals"))


class GetAllWhoCanCounterAttackI:
    def __init__(self, card1, card2):
        self.card2 = get_param(card1)
        self.card1 = get_param(card2)

    def execute(self, prolog_thread):
        res = prolog_thread.query(f'canCounterattack({self.card1}, {self.card2}).')
        print(get_result(res, "Nothing found", "Can counterattack"))


class GetAllWhoCanCounterAttackMe:
    def __init__(self, card1, card2):
        self.card1 = get_param(card1)
        self.card2 = get_param(card2)

    def execute(self, prolog_thread):
        res = prolog_thread.query(f'canCounterattack({self.card1}, {self.card2}).')
        print(get_result(res, "Nothing found", "Can counterattack"))


class GetAllProfitableToDistract:
    def __init__(self, card1, card2):
        self.card2 = get_param(card1)
        self.card1 = get_param(card2)

    def execute(self, prolog_thread):
        res = prolog_thread.query(f'profitableToDistract({self.card1}, {self.card2}).')
        print(get_result(res, "Nothing found", "Can counterattack"))



PROLOG_PATH = "lab1_1.pl"


examples = [
    f'I want to play as Prince, who can I attack?',
    f'I want to play as Minions, who can attack me?',
    f'What card can I use to distract the Giant?',
    f'Which cards are cheaper or equals than Baby Dragon?',
    f'How can I counterattack the Sparky?',
    f'Who can the Balloon counterattack?',
    f'Which card is beneficial for me to distract the Archers?'
]

patterns = {
    r'I want to play as (.+), who can I attack\?': CheckCanAttackI,
    r'I want to play as (.+), who can attack me\?': CheckCanAttackMe,
    r'What card can I use to distract the (.+)\?': CheckCanDistractEnemy,
    r'Which cards are cheaper or equals than (.+)\?': GetAllCheaperAllEquals,
    r'How can I counterattack the (.+)\?': GetAllWhoCanCounterAttackI,
    r'Who can the (.+) counterattack\?': GetAllWhoCanCounterAttackMe,
    r'Which card is beneficial for me to distract the (.+)\?': GetAllProfitableToDistract
}

with PrologMQI() as mqi:
    with mqi.create_thread() as prolog_thread:
        path = create_posix_path(PROLOG_PATH)
        prolog_thread.query(f'consult("{path}")')
        print("Ваши вопросы")
        print("Примеры вопросов:\n-", "\n- ".join(examples))
        print("Для завершения напишите - exit")
        while True:
            ent = input('?- ')
            if ent == 'exit':
                break
            for pattern in patterns:
                match = re.match(pattern, ent)
                if match is None:
                    continue
                answerClass = patterns[pattern](*match.groups(), "Anyone_of_this")
                answerClass.execute(prolog_thread)
                break
            else:
                print("Неправильно задан вопрос, попробуйте еще раз.")
