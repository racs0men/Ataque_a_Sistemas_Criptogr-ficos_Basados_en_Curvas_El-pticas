from hashlib import sha256
from random import randint
from tinyec import registry
import secrets
import pandas as pd
import time

curves = ['brainpoolP256r1', 'brainpoolP384r1', 'brainpoolP512r1', 'secp256r1', 'secp384r1', 'secp521r1']

# Algorithm 4: Elliptic Curve Diffie-Hellman Key Exchange
def ecdh_key_exchange(curve):
    G = curve.g
    n = curve.field.n

    k_sender = randint(1, n-1)
    A = k_sender * G

    k_receiver = randint(1, n-1)
    B = k_receiver * G

    key_sender = k_sender * B
    key_receiver = k_receiver * A
    return (key_sender, key_receiver)

# Algorithm 5: Malicious Key Generation
def malicious_key_generation(curve):
    G = curve.g
    n = curve.field.n
    byte_size = (n.bit_length() + 7) // 8
    k1 = randint(1, n-1)
    M1 = k1 * G

    k_attacker = secrets.randbelow(n)
    Y = k_attacker * G
    W = 5
    a = 2
    b = 3
    t = 0

    z = (k1 - W * t) * G + (-a * k1 - b) * Y
    zx = z.x % n
    k2 = int.from_bytes(sha256(zx.to_bytes(byte_size, 'big')).digest(), 'big')
    M2 = k2 * G

    k_receiver = randint(1, n-1)
    B = k_receiver * G

    key_malicious_receiver = k_receiver * M2
    key_malicious_sender = k2 * B

    return (key_malicious_receiver, key_malicious_sender, k1, M1, M2, k_attacker, a, b, W, k2)

# Algorithm 6: Key Recovery
def private_key_recovery(curve, M1, M2, k_attacker, a, b, W):
    G = curve.g
    n = curve.field.n
    byte_size = (n.bit_length() + 7) // 8
    r_malicious = a * M1 + b * G

    z1 = M1 - k_attacker * r_malicious
    zx1 = z1.x % n

    if M2 == int.from_bytes(sha256(zx1.to_bytes(byte_size, 'big')).digest(), 'big') * G:
        k2 = int.from_bytes(sha256(zx1.to_bytes(byte_size, 'big')).digest(), 'big')
        return k2

    z2 = z1 - W * G
    zx2 = z2.x % n

    if M2 == int.from_bytes(sha256(zx2.to_bytes(byte_size, 'big')).digest(), 'big') * G:
        k2 = int.from_bytes(sha256(zx2.to_bytes(byte_size, 'big')).digest(), 'big')
        return k2
    return None

def verify_attack(curve):
    key_malicious_receiver, key_malicious_sender, k1, M1, M2, k_attacker, a, b, W, original_k2 = malicious_key_generation(curve)
    k2_recovered = private_key_recovery(curve, M1, M2, k_attacker, a, b, W)
    if k2_recovered is not None and k2_recovered == original_k2:
        return True
    return False

# Function to test the attack on multiple curves and return results
def test_attack_on_curves(num_trials):
    results = []
    total_start_time = time.time()
    for curve_name in curves:
        curve = registry.get_curve(curve_name)
        successes = 0
        start_time = time.time()
        for _ in range(num_trials):
            if verify_attack(curve):
                successes += 1
        end_time = time.time()
        success_rate = (successes / num_trials) * 100
        execution_time = end_time - start_time
        results.append({'Curve': curve_name, 'Success Rate': f'{success_rate:.2f}%', 'Execution Time (s)': execution_time})
    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    results.append({'Curve': 'Total', 'Success Rate': 'N/A', 'Execution Time (s)': total_execution_time})
    df = pd.DataFrame(results)
    df.index += 1
    return df

num_trials = int(input("Enter the number of times to run the attack for each curve: "))

results_df = test_attack_on_curves(num_trials)
print(results_df)