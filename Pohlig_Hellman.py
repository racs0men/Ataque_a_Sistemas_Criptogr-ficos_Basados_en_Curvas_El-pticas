from sympy import mod_inverse, primefactors

class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def add(self, P, Q):
        if P == (None, None):
            return Q
        if Q == (None, None):
            return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 != y2 or y1 == 0):
            return (None, None)
        if x1 == x2:
            l = (3 * x1 * x1 + self.a) * mod_inverse(2 * y1, self.p) % self.p
        else:
            l = (y2 - y1) * mod_inverse(x2 - x1, self.p) % self.p
        x3 = (l * l - x1 - x2) % self.p
        y3 = (l * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def multiply(self, k, P):
        R = (None, None)
        S = P
        while k:
            if k & 1:
                R = self.add(R, S)
            S = self.add(S, S)
            k >>= 1
        return R

def discrete_logarithm(curve, P, A, q):
    R = (None, None)
    for i in range(q):
        if R == A:
            return i
        R = curve.add(R, P)
    raise ValueError("Logarithm does not exist")

def pohlig_hellman_ec(curve, P, A, n):
    factors = primefactors(n)
    congruences = []
    moduli = []

    for q in factors:
        e = n // q
        Ae = curve.multiply(e, A)
        Pe = curve.multiply(e, P)
        log = discrete_logarithm(curve, Pe, Ae, q)
        congruences.append(log)
        moduli.append(q)

    def solve_congruences(ai, ni):
        x = 0
        N = 1
        for ni in moduli:
            N *= ni
        for ai, ni in zip(congruences, moduli):
            Ni = N // ni
            mi = mod_inverse(Ni, ni)
            x = (x + ai * mi * Ni) % N
        return x

    x = solve_congruences(congruences, moduli)

    return x

def main():
    p = int(input("Enter the value of p: "))
    a = int(input("Enter the value of a: "))
    b = int(input("Enter the value of b: "))
    Gx = int(input("Enter the x coordinate of G: "))
    Gy = int(input("Enter the y coordinate of G: "))
    Ax = int(input("Enter the x coordinate of A: "))
    Ay = int(input("Enter the y coordinate of A: "))

    curve = EllipticCurve(a, b, p)
    G = (Gx, Gy)
    A = (Ax, Ay)
    n = p

    x = pohlig_hellman_ec(curve, G, A, n)
    print(f"The private key is x = {x}")

    A_calculated = curve.multiply(x, G)
    is_correct = A_calculated == A
    print(f"Is the private key correct? {is_correct}")

if __name__ == "__main__":
    main()

# Ejemplo de uso
# p = 89
# a = 0
# b = 7
# Gx = 1
# Gy = 39
# Ax = 4
# Ay = 58