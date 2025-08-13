import sys

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def ifib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

def serie(n):
    a, b = 0, 1
    while True:
        if a > n:
            break
        else:
            print("{0:2d}".format(a), end = " ")
            a, b = b, a + b

    return a

if __name__ == "__main__":
    import sys
    # print(fib(int(sys.argv[1])))
    serie(int(sys.argv[1]))
