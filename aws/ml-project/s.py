# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Hello world")

num = int(input('enter a number : '))

def isprime(intd):

    if intd <=1:
        return False
    elif intd == 2:
        return True
    else:
        for i in range(2, intd+1):
            if intd % i == 0:
                return False
        return True


def next_prime(num):
    next_num = num + 1
    while True:
        if isprime(next_num):
            return next_num
        next_num += 1

print(next_prime(num))
# next prime






