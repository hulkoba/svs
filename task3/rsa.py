
###############################################
###########  3.2  #############################
###############################################
# message = 9
m = 9

# rsa parameter
p = 5
q = 11
e = 3

n = p * q
phi_von_n = (p-1) * (q-1)


def get_d():
    for num in range(1, phi_von_n):
        d = (num * phi_von_n + 1) / float(e)
        # d is an integer
        if d % 1 == 0:
            return int(d)

d = get_d()
print "d = " + str(d)

e_von_m = m**e % n
print "encrypted message E(m) = " + str(e_von_m)

d_von_x = e_von_m**d % n
print "decrypted message d(x) = " + str(d_von_x)

