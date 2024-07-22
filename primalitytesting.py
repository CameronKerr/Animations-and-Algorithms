#####################
# Primality Testing #
#####################

from random import randint

# Function which runs a Fermat primality test on k up to 'threshold' iterations
def fermat_test(k, threshold):
    i = 0
    # Loop through 'threshold' amount of iterations
    while i < threshold:
        # Generate ranom integer in mod k and raise it to the (k-1)th power
        a = randint(2, k-1)
        x = a**(k-1)
        # Find x mod k
        x = x % k
        # If k is prime x mod k will be 1 so return False if it isn't
        if x != 1:
            return False
        i = i + 1
    # If k satisfies FLT over all iterations we can predict k to be prime
    return True

# Function which runs a Lucas-Lehmer Primality test on 2^p - 1
def lucaslehmer_test(p):
    # Set initial Lucas number and k
    k = 2**p - 1
    s = 4
    i = 1
    # Get (k-2)nd Lucas number to see if it is a multiple of k
    while i < (p-1):
        s = (s*s - 2) % k
        i = i + 1
    # If it is a multiple of k it is a prime
    return s == 0

# Function which finds all Mersenne primes with exponent between 'start' and 'end'
def primality_test(start, end):
    primes = []
    # Loop through all numbers
    for i in range(start, end+1):
        # Do Fermat test to determine if i is prime
        if fermat_test(i, 25):
            if lucaslehmer_test(i):
                primes.append(i)
    return primes       