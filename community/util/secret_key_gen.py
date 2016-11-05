# Generates a random secret key and stores it in the PROJECT_ROOT dir
import os


def generate_key(PROJECT_ROOT):
    secret_file = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        secret_key = open(secret_file).read().strip()
    except IOError:
        try:
            import random
            secret_key = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            secret = open(secret_file, 'w')
            secret.write(secret_key)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters \
            to generate your secret key!' % secret_file)
    return secret_key
