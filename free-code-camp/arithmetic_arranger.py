def arithmetic_arranger(problems, calc=False):
    errors = [
        "Error: Too many problems.",
        "Error: Operator must be '+' or '-'.",
        "Error: Numbers cannot be more than four digits.",
        "Error: Numbers must only contain digits.",
    ]
    arranged_problems = ""
    if len(problems) > 5:
        return errors[0]

    answer = [[] for _ in range(3 if not calc else 4)]
    for problem in problems:
        ans = single_problem(problem, calc)
        if isinstance(ans, int):
            return errors[ans]
        for i, line in enumerate(ans):
            answer[i].append(line)

        joined_answer = []
        for line in answer:
            joined_answer.append("    ".join(line))

    return "\n".join(joined_answer)


def make_equal(first, second):
    if len(first) < len(second):
        first = " " * (len(second) - len(first)) + first
    else:
        second = " " * (len(first) - len(second)) + second
    return (first, second)


def calculate_result(first, second, operator):
    d = {"+": lambda x, y: x + y, "-": lambda x, y: x - y}
    return d[operator](first, second)


def single_problem(problem, calc=False):
    first, operator, second = problem.split()
    if operator != "+" and operator != "-":
        return 1
    if not first.isdigit() or not second.isdigit():
        return 3
    n = len(first)
    m = len(second)
    if n > 4 or m > 4:
        return 2
    first, second = make_equal(first, second)
    answer = []
    answer.append("  " + first)
    answer.append(operator + " " + second)
    answer.append("--" + "-" * (max(n, m)))
    if calc:
        output = str(calculate_result(int(first), int(second), operator))
        answer.append(" " * (max(n, m) + 2 - len(output)) + output)

    return answer


print(
    arithmetic_arranger(
        ["32 - 698", "1 - 3801", "45 + 43", "123 + 49", "988 + 40"], True
    )
)
