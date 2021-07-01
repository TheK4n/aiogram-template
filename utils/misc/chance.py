import random


def chance(value: float) -> bool:  # возвращает тру или фалс с шансом <chance>
    return random.random() < value
