import copy
import random


# Extended Euclidean algorithm
def extended_gcd(aa, bb):
    num1, num2 = abs(aa), abs(bb)
    x, last_x, y, last_y = 0, 1, 1, 0
    while num2:
        num1, (quotient, num2) = num2, divmod(num1, num2)
        x, last_x = last_x - quotient * x, x
        y, last_y = last_y - quotient * y, y
    return num1, last_x * (-1 if aa < 0 else 1), last_y * (-1 if bb < 0 else 1)


# calculate `modular inverse`
def modInv(inv, m):
    g, x, y = extended_gcd(inv, m)
    if g != 1:
        raise ValueError
    return x % m


# double function
def ecc_double(x1, y1, p, a_x):
    s = ((3 * (x1 ** 2) + a_x) * modInv(2 * y1, p)) % p
    x3 = (s ** 2 - x1 - x1) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


# add function
def ecc_add(x1, y1, x2, y2, p, a_x):
    s = 0
    if (x1 == x2):
        s = ((3 * (x1 ** 2) + a_x) * modInv(2 * y1, p)) % p
    else:
        s = ((y2 - y1) * modInv(x2 - x1, p)) % p
        x3 = (s ** 2 - x1 - x2) % p
        y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


#  double and add function
def double_and_add(multi, P, p, a_x):
    (x3, y3) = (0, 0)
    (x1, y1) = copy.copy(P)
    (x_tmp, y_tmp) = copy.copy(P)
    init = 0
    for i in str(bin(multi)[2:]):
        if (i == '1') and (init == 0):
            init = 1
        elif (i == '1') and (init == 1):
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a_x)
            (x3, y3) = ecc_add(x1, y1, x3, y3, p, a_x)
            (x_tmp, y_tmp) = (x3, y3)
        else:
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a_x)
            (x_tmp, y_tmp) = (x3, y3)
    return (x3, y3)


# the curve:E:y^2= x^3+ a x + b
p = 1152921504606847009
a_x = 3
b_x = 4
# the primitive point (3, 10)
P = (30434951196465692, 644563080783699011)
Q = (831823133036407885, 733441546854960077)
n = 621919357

L = 16  # For creating a partition

R_x = [0]  # Will store x coordinate of point R
R_y = [0]  # Will store y coordinate of point R

# For testing purpose
# Whether the ecc_add, ecc_double, double_and_add, modInv functions are working correct or not
##############################################################################################
# 57 = b_x(111001)
# print "57P = ", double_and_add(57, P, p, a)
# x3,y3 = double_and_add(104,P,p,a_x)
# x4, y4 = double_and_add(489, Q, p, a_x)
# print(ecc_add(x3,y3,x4,y4,p,a_x))
###############################################################################################

# Partition algorithm start
H = [x for x in range(1, L + 1)]  # Creating a list H in it contains values from 1 to L
H.insert(0, 0)  # Appending 0 at 0 position

# Alternative for above two lines
# H = [x for x in range(0,L+1)]
# Partition algorith ends


# PollardRho starts
# Initializing list a and b with initial value 0 at 0 position
a = [0]
b = [0]
for j in range(1, L + 1):
    a.append(random.randint(0, n - 1))
    # Generating L random values from 0 to n-1 range including both and appending to list a
    b.append(random.randint(0, n - 1))
    # Generating L random values from 0 to n-1 range including both and appending to list b
    temp1_x, temp1_y = double_and_add(a[j], P, p, a_x)  # Calculating a[j]*P
    # temp1 = [temp1_x, temp1_y]
    temp2_x, temp2_y = double_and_add(b[j], Q, p, a_x)  # Calculating b[j]*Q
    # temp2 = [temp2_x, temp2_y]
    temp3_x, temp3_y = ecc_add(temp1_x, temp1_y, temp2_x, temp2_y, p, a_x)  # Calculating a[j]*P + b[j]*Q
    R_x.append(temp3_x)  # Assigning x and y values for easier calculation
    R_y.append(temp3_y)

# print(R_x)
# print(R_y)
c1 = random.randint(0, n - 1)
d1 = random.randint(0, n - 1)
X1 = [0, 0]
X2 = [0, 0]
var1_x, var1_y = double_and_add(c1, P, p, a_x)
# var1 = [var1_x,var1_y]
var2_x, var2_y = double_and_add(d1, Q, p, a_x)
# var2 = [var2_x,var2_y]
var3_x, var3_y = ecc_add(var1_x, var1_y, var2_x, var2_y, p, a_x)
X1[0] = copy.copy(var3_x)
X1[1] = copy.copy(var3_y)
# correct till now

X2[0] = copy.copy(X1[0])
X2[1] = copy.copy(X1[1])
c2 = copy.copy(c1)
d2 = copy.copy(d1)

# Checking what X1 and X2 values were initially just for understanding purpose
# print(X1)
# print(X2)


flag = True
# Assigning a Flag here because initially the function will do fast walk and slow walk from same point
# so X1 == X2 becomes equal, we can't enter the while loop.
# To grant entry inside loop we used a flag variable here.

while (flag == True or X1[0] != X2[0] or X1[1] != X2[1]):
    flag = False
    j = (X1[0] % 16) + 1
    X1[0], X1[1] = ecc_add(X1[0], X1[1], R_x[j], R_y[j], p, a_x)
    # X1 wil store x and y coordinates of a slow walk as X1[0], X1[1]

    c1 = (c1 + a[j]) % n
    d1 = (d1 + b[j]) % n

    for i in range(1, 2 + 1):
        j = (X2[0] % L) + 1
        X2[0], X2[1] = ecc_add(X2[0], X2[1], R_x[j], R_y[j], p, a_x)
        # X2 will store x and y coordinates of a fast walk as X2[0], X2[1]

        c2 = (c2 + a[j]) % n
        d2 = (d2 + b[j]) % n
    print("X1 =", X1)
    print("X2 =", X2)
    # Printing the X1 and X2 coordinates to check at what point fast walk meets with slow walk points

if d1 == d2:
    print("Failure")
    # exit(0)
else:
    print()
    print(f"c1 = {c1}, c2 ={c2}, d1 = {d1}, d2 = {d2}")
    ans = ((c1 - c2) * modInv(d2 - d1, n)) % n  #
    print()
    print(f"The value of d for Q = dP is {ans}")
    # exit(0)
# PollardRho ends

# Testing
# Checking whether Q= dP really
# print(f"Q={Q},dP={double_and_add(ans, P, p, a_x)}")

# print(X1)
# print(X2)
