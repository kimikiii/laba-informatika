import math
import re


def parse_shift(tokens):
    res = parse_add_sub(tokens)
    while tokens and tokens[0] == '<<':
        tokens.pop(0)
        res = int(res) << int(parse_add_sub(tokens))
    return res


def parse_add_sub(tokens):
    res = parse_mul_div(tokens)
    while tokens and tokens[0] in ('+', '-'):
        op = tokens.pop(0)
        right = parse_mul_div(tokens)
        if op == '+':
            res += right
        else:
            res -= right
    return res


def parse_mul_div(tokens):
    res = parse_unary(tokens)
    while tokens and tokens[0] in ('*', '/'):
        op = tokens.pop(0)
        right = parse_unary(tokens)
        if op == '*':
            res *= right
        else:
            res /= right
    return res


def parse_unary(tokens):
    if tokens and tokens[0] == '-':
        tokens.pop(0)
        return -parse_unary(tokens)
    if tokens and tokens[0] == '+':
        tokens.pop(0)
        return parse_unary(tokens)
    return parse_primary(tokens)


def parse_primary(tokens):
    token = tokens.pop(0)

    if token == 'tan':
        tokens.pop(0)
        val = parse_shift(tokens)
        tokens.pop(0)
        return math.tan(val)

    if token == '(':
        val = parse_shift(tokens)
        tokens.pop(0)
        return val

    if '.' in token:
        return float(token)
    return int(token)


def calculate(expression):
    tokens = re.findall(r'\d+(?:\.\d+)?|tan|<<|[+\-*/()]', expression)
    return parse_shift(tokens)


if __name__ == "__main__":
    print("Ввод выражения или 'exit' для выхода")

    while True:
        user_input = input("Выражение: ")

        if user_input.strip().lower() == "exit":
            print("Завершение работы.")
            break

        if not user_input.strip():
            continue

        try:
            print("Ответ:", calculate(user_input))
        except ZeroDivisionError:
            print("Ошибка: деление на ноль!")
        except Exception:
            print("Ошибка в выражении. Проверь правильность ввода.")