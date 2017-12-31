print ''
print "############## 3.1 #######################"
# https://www.elektronik-kompendium.de/sites/net/1909031.htm

p = 467
g = 2

def get_a(a):
    return (g**a) % p
def get_b(b):
    return (g**b) % p

def get_k1(a, b):
    return (b**a) % p

def get_k2(a, b):
    return (a**b) % p ## haha

print "## 3.1.1"
a = 83
b = 833

A = get_a(a)
B = get_b(b)

K1 = get_k1(a, B)
K2 = get_k2(A, b)
print "A = " + str(A)
print "B = " + str(B)
print "K1 = " + str(K1)
print "K2 = " + str(K2)

print ''
print "## 3.1.2"
a = 400
b = 134

A = get_a(a)
B = get_b(b)
K1 = get_k1(a, B)
K2 = get_k2(A, b)
print "A = " + str(A)
print "B = " + str(B)
print "K1 = " + str(K1)
print "K2 = " + str(K2)

print ''
print "## 3.1.3"
a = 228
b = 57

A = get_a(a)
B = get_b(b)
K1 = get_k1(a, B)
K2 = get_k2(A, b)
print "A = " + str(A)
print "B = " + str(B)
print "K1 = " + str(K1)
print "K2 = " + str(K2)

print ''
print "############## 3.2 ###############################"
# message = 9
m = 9

# rsa parameter
p = 5
q = 11
e = 3

n = p * q
phi_von_n = (p-1) * (q-1)
print "phi(n) = " + str(phi_von_n)


def get_d(phi_von_n, e):
    for num in range(1, phi_von_n):
        d = (num * phi_von_n + 1) / float(e)
        # d is an integer
        if d % 1 == 0:
            return int(d)

d = get_d(phi_von_n, e)
print "d = " + str(d)

e_von_m = m**e % n
print "encrypted message E(m) = " + str(e_von_m)

d_von_x = e_von_m**d % n
print "decrypted message d(x) = " + str(d_von_x)

print ''
print "############## 3.3 ###############################"

p = 41
q = 17

e1 = 32
e2 = 39

phi_von_n = (p-1) * (q-1)
print "phi(n) = " + str(phi_von_n)


def get_ggt(a, b):
    if(b == 0):
        return a
    else:
        return get_ggt(b, a % b)

ggt = get_ggt(phi_von_n, e1)
print "ggT for phi(n) and e1 = " + str(ggt)

ggt2 = get_ggt(phi_von_n, e2)
print "ggT for phi(n) and e2 = " + str(ggt2)

print "e2 ist teilerfremd mit/zu phi(n) und somit als oeffentlicher RSA-Exponent geeignet :tada:"

d = get_d(phi_von_n, e2)
test = (e2*d) % phi_von_n

print "Der private Exponent ist " + str(d) + "\nVorausgesetzt e * d % phi(n) = 1."
print "Ergebnis der Probe: " + str(test)
