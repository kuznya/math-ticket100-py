# 0.22

# *** stat obj ***
import random

# --------------------------------------------------------------
CODE_LEN = 6
stack = [(-1, [])]*CODE_LEN
s_ops = ".*/+-"

max_cnt = 500000


def do(opcode, lvl):
    p, op = divmod(opcode, 5)
    l = stack[lvl - 1][1]
    a, b = l[p], l[p + 1]

    if op == 0:  # concat
        for i in range(1, lvl):
            if stack[i][0] % 5: return None
        if a == 0: return None
        if b > 9: return None
        x = a * 10 + b
    elif op == 1:  # mul
        x = a * b
    elif op == 2:  # div
        if b == 0: return None
        if a % b: return None
        x = a / b
    elif op == 3:  # plus
        x = a + b
    elif op == 4:  # minus
        x = a - b
    else: raise ValueError
    ll = l[:p] + [x] + l[p + 2:]
    stack[lvl] = (opcode, ll)
    return x


def do_expression(l,lvl):
    # print stack[lvl]
    opcode = stack[lvl][0]
    p, op = divmod(opcode, 5)
    a, b = l[p], l[p + 1]

    prior_need = False
    for t in stack[lvl + 1:]:
        if t[0] % 5 in [1, 2]:
            prior_need = True
            break
        if t[0] / 5 == p: break

    s_op = s_ops[op]
    if s_op == '.': s_op = ''
    x = str(a) + s_op + str(b)
    if op in [3, 4] and prior_need: x = '(' + x + ')'

    ll = l[:p] + [x] + l[p + 2:]
    return ll


def op_str(opcode):
    if opcode<0: return '=>'
    place = opcode/5 + 1
    op = s_ops[opcode % 5]
    return "%d%c" % (place,op)


def stack_print():
    for t in stack:
        print(op_str(t[0]), t[1])
    print()


def stack_expression_print():
    # stack_print()
    # return
    l = stack[0][1]
    # print l
    for lvl in range(1, CODE_LEN):
        # print lvl
        l = do_expression(l, lvl)
        # print l
    print(l[0], "\n")


def search(code, target, mode='first'):
    stack[0] = (-1, list(map(int, str(code))))

    cnt = 0
    for i1 in range(25):
        if do(i1, 1) is None: continue
        for i2 in range(20):
            if do(i2, 2) is None: continue
            for i3 in range(15):
                if do(i3, 3) is None: continue
                for i4 in range(10):
                    if do(i4, 4) is None: continue
                    for i5 in range(5):
                        if do(i5, 5) is None: continue
                        cnt += 1
                        # print "%d\r" % (cnt,)
                        if (stack[5][1] == [target]) or (cnt >= max_cnt):
                            print(code, cnt)
                            stack_print()
                            if mode == 'first': stack_expression_print()  # works for first mode only

                            if mode == 'first': return
    # print code, 'not found!', cnt
    print(code, '- end -', cnt, "\n")
    return

# *** Go ***
while True:
    s = input("6 digit number>")
    # print(repr(s))
    if s == 'q': break
    if s == '':
        s = str(random.randint(100000, 999999))
    elif len(s) != 6 or not s.isdigit or int(s) < 100000:
        continue
    code = int(s)
    search(code, 100)
#"""
#search(562199,100)