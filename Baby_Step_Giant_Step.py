class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def is_prime(num):
    """ Check if a number is a prime number. """
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def inverse(a, p):
    for i in range(1, p):
        if (a * i) % p == 1:
            return i
    return -1

def add(p1, p2, a, p):
    if p1.x == p2.x and p1.y == p2.y:
        m = (3 * (p1.x ** 2) + a) * inverse(2 * p1.y, p) % p
        m = (m + p) % p
        x = (m ** 2 - 2 * p1.x) % p
        y = (m * (p1.x - x) - p1.y) % p
        return Point(x, y)
    else:
        arr = (p2.y - p1.y) % p
        abj = (p2.x - p1.x) % p
        abj = (abj + p) % p
        inverse1 = inverse(abj, p)
        m = (arr * inverse1) % p
        x = (m ** 2 - p1.x - p2.x) % p
        y = (m * (p1.x - x) - p1.y) % p
        return Point(x, y)

def subtract_points(P, Q, p, a):
    if Q.x == 0 and Q.y == 0:
        return P
    else:
        neg_Q = Point(Q.x, (-Q.y + p) % p)
        return add(P, neg_Q, a, p)

def multiply(point, n, a, p):
    if n == 0:
        return Point(0, 0)
    elif n == 1:
        return point
    else:
        result = point
        for i in range(1, n):
            result = add(result, point, a, p)
        return result

def print_points(points):
    for p in points:
        print(f"({p.x}, {p.y})")

def main():
    p = int(input("Enter the value of p (must be a prime number): "))
    while not is_prime(p):
        print("The value entered for p is not a prime number.")
        p = int(input("Please enter a prime number for p: "))

    m = int(input("Enter the value of m: "))
    a = int(input("Enter the value of a of the curve: "))
    b = int(input("Enter the value of b of the curve: "))
    Gx = int(input("Enter the x coordinate of point G: "))
    Gy = int(input("Enter the y coordinate of point G: "))
    G = Point(Gx, Gy)
    Ax = int(input("Enter the x coordinate of point A: "))
    Ay = int(input("Enter the y coordinate of point A: "))
    A = Point(Ax, Ay)

    points = []
    points1 = []
    print("Baby Step:")
    for i in range(m):
        result = multiply(G, i, a, p)
        print(f"{i}G: ({result.x}, {result.y})")
        points.append(result)

    print("Giant Step:")
    for j in range(m):
        result = multiply(G, j * m, a, p)
        print(f"{j * m}G: ({result.x}, {result.y})")
        difference = subtract_points(A, result, p, a)
        print(f"{j}: ({difference.x}, {difference.y})")
        points1.append(difference)

    found = False
    coincidence_i = coincidence_j = 0
    for i in range(m):
        if found:
            break
        for j in range(m):
            if points[i].x == points1[j].x and points[i].y == points1[j].y:
                coincidence_i = i
                coincidence_j = j
                print(f"Coincidence: i={i} j={j}")
                found = True
                break

    alpha = coincidence_i + coincidence_j * m
    alpha = (alpha + p) % p
    print(f"Secret key {alpha}")

if __name__ == "__main__":
    main()


# Ejemplo de uso
# p = 17
# m = 5
# a = 2
# b = 2
# Gx = 5
# Gy = 1
# Ax = 10
# Ay = 6