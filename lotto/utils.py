import random

def generate_lotto_numbers():
    return ",".join(map(str, sorted(random.sample(range(1, 46), 6))))
