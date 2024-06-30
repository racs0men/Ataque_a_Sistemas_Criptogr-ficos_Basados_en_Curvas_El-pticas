from hashlib import sha256
from random import randint
from tinyec import registry
import pandas as pd
import time

curves = ['brainpoolP256r1', 'brainpoolP384r1', 'brainpoolP512r1', 'secp256r1', 'secp384r1', 'secp521r1']

def diffie_hellman_key_exchange(curve):
    G = curve.g
    n = curve.field.n

    private_key_sender = randint(1, n-1)
    public_key_sender = private_key_sender * G

    private_key_receiver = randint(1, n-1)
    public_key_receiver = private_key_receiver * G

    shared_key_sender = private_key_sender * public_key_receiver
    shared_key_receiver = private_key_receiver * public_key_sender
    return (private_key_sender, public_key_sender, private_key_receiver, public_key_receiver, shared_key_sender, shared_key_receiver)

def test_diffie_hellman_on_curves(num_trials):
    results = []
    total_execution_time = 0
    for curve_name in curves:
        curve = registry.get_curve(curve_name)
        start_time = time.time()
        for _ in range(num_trials):
            private_key_sender, public_key_sender, private_key_receiver, public_key_receiver, shared_key_sender, shared_key_receiver = diffie_hellman_key_exchange(curve)
            assert shared_key_sender == shared_key_receiver, "Shared keys do not match!"
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        results.append({'Curve': curve_name, 'Execution Time (s)': execution_time})
    df = pd.DataFrame(results)
    df.index += 1
    total_row = pd.DataFrame([{'Curve': 'Total', 'Execution Time (s)': total_execution_time}])
    df = pd.concat([df, total_row], ignore_index=True)
    return df

num_trials = int(input("Enter the number of times to run the Diffie-Hellman exchange for each curve: "))

dh_results_df = test_diffie_hellman_on_curves(num_trials)
print(dh_results_df)