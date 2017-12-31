p = 467
g = 2


def get_public_key(a):
    return (g**a) % p


def get_k(a, b):
    return (b**a) % p
