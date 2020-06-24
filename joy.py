

class Stack:

    def __init__(self, items=[]):
        self.items = items

    def pop(self):
        return self.items.pop(0)

    def peek(self):
        return self.items[0]

    def push(self, new_item):
        self.items.insert(0, new_item)
        return self

    def pushstack(self, other):
        self.items = other.items + self.items
        return Stack(other.items + self.items)

    def copy(self):
        return Stack(self.items[:])

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return '[%s]' % ' '.join([str(x) for x in self.items[::-1]])


# ~~~
def small(stack):
    a = stack.pop()
    stack.push(a)
    stack.push(a < 2)


def i(stack):
    a = stack.pop()
    evaluate(stack, a)


def null(stack):
    a = stack.pop()
    stack.push(a)
    stack.push(a == 0)


def dup(stack):
    a = stack.pop()
    stack.push(a)
    stack.push(a)


def add(stack):
    a = stack.pop()
    b = stack.pop()
    stack.push(a + b)


def pred(stack):
    a = stack.pop()
    stack.push(a - 1)


def drop(stack):
    a = stack.pop()


def succ(stack):
    a = stack.pop()
    stack.push(a + 1)


def eq(stack):
    a = stack.pop()
    b = stack.pop()
    stack.push(a == b)


def subtract(stack):
    a = stack.pop()
    b = stack.pop()
    stack.push(b - a)


def mul(stack):
    a = stack.pop()
    b = stack.pop()
    stack.push(a * b)


def app2(stack):
    q = stack.pop()
    x1 = Stack([stack.pop()])
    x2 = Stack([stack.pop()])
    evaluate(x1, q.copy())
    evaluate(x2, q.copy())
    stack.pushstack(x1)
    stack.pushstack(x2)



def linrec(stack):
    after = stack.pop()
    before = stack.pop()
    base = stack.pop()
    pred = stack.pop()

    rec = Stack(['linrec', after.copy(), before, base, pred])

    evaluate(stack, pred.copy())

    if stack.pop():
        evaluate(stack, base.copy())
    else:
        evaluate(stack, before.copy())
        evaluate(stack, rec.copy())
        evaluate(stack, after.copy())


def genrec(stack):
    after = stack.pop()
    before = stack.pop()
    base = stack.pop()
    pred = stack.pop()
    # print('stack:', stack)
    rec = Stack(['genrec', after, before, base, pred])
    evaluate(stack, pred.copy())
    # print('p:', stack.peek())
    if stack.pop():
        evaluate(stack, base.copy())
    else:
        # print('>?', stack)
        evaluate(stack, before.copy())
        stack.push(rec.copy())
        evaluate(stack, after.copy())



# Parsing
def split_text(text):
    tokens = []
    curr_token = ''
    for char in text:
        if char == ' ':
            tokens.append(curr_token)
            curr_token = ''
        elif char == '[':
            tokens.append(curr_token)
            tokens.append('[')
            curr_token = ''
        elif char == ']':
            tokens.append(curr_token)
            tokens.append(']')
            curr_token = ''
        else:
            curr_token += char
    tokens.append(curr_token)
    return [x for x in tokens if x.strip() != '']


def parse_stack(text):
    splits = [int(x) if x.isnumeric() else x for x in split_text(text)]
    tokens = Stack(splits)
    def parse_helper(tokens):
        stack = Stack([])
        while len(tokens) > 0:
            t = tokens.pop()
            if t == ']':
                return stack
            elif t == '[':
                stack.push(parse_helper(tokens))
            else:
                stack.push(t)
        return stack

    return parse_helper(tokens)


def evaluate(left_reg, right_reg):
    right_reg.items = right_reg.items[::-1]
    combinators = {
        'dup': dup,
        '+': add,
        '*': mul,
        'eq': eq,
        'sub': subtract,
        'linrec': linrec,
        'genrec': genrec,
        'pred': pred,
        'succ': succ,
        'app2': app2,
        'i': i,
        'small': small,
        'null': null,
        'drop': drop
    }

    while len(right_reg) > 0:
        comb = right_reg.pop()
        if isinstance(comb, int):
            left_reg.push(comb)
        elif isinstance(comb, Stack):
            left_reg.push(comb)
        else:
            combinators[comb](left_reg)

    return left_reg
        


fib = parse_stack('17 [small] [] [pred dup pred] [app2 +] genrec')
flat_list = parse_stack('0 [dup 10 eq] [drop] [succ] [1] linrec')
inc_list = parse_stack('0 [dup 10 eq] [] [dup succ] [] linrec')
dec_list = parse_stack('10 [dup 0 eq] [] [dup pred] [] linrec')
x = fib
print('>>>', x)
s2 = evaluate(Stack([]), x)
print('result:', s2)

