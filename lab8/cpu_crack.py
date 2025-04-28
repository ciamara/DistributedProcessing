import sys
import hashlib
import itertools
import asyncio
import time

# all possible characters in password
CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'

# checks if length of hash and characters are valid(hex)
def is_valid_sha256(s):
    return len(s) == 64 and all(c in "0123456789abcdef" for c in s)

# asynchronous worker to try different passwords
# start_chars -> subset of characters, one per worker to divide workload
# target_hash -> SHA256 hash of target password
# password_length -> self explanatory
# found_flag -> shared flag to indicate if someone foudn the password
async def worker(start_chars, target_hash, password_length, found_flag):

    for prefix in start_chars:
        if found_flag.done():
            return  # someone found the password

        # all possible combinations of characters appended to prefix
        # generates a hash and compares the generated hash to our target hash
        for combo in itertools.product(CHARSET, repeat=password_length - 1):
            candidate = prefix + ''.join(combo)
            hashed = hashlib.sha256(candidate.encode()).hexdigest()

            # set found flag if hashes match
            if hashed == target_hash:
                found_flag.set_result(candidate)
                return

            # small async pause for better task switching (optional)
            # await asyncio.sleep(0)

async def main():

    # invalid use of program
    if len(sys.argv) != 3:
        print("Invalid usage (python3 cpu_crack.py <SHA256_HASH> <PASSWORD_LENGTH>.)")
        sys.exit(1)

    # sha hash
    # and checking validity
    sha256_hash = sys.argv[1]
    try:
        password_length = int(sys.argv[2])
    except ValueError:
        print("Error: <PASSWORD_LENGTH> must be an integer.")
        sys.exit(1)

    if not is_valid_sha256(sha256_hash):
        print("Error: <SHA256_HASH> must be a valid 64-character hexadecimal string.")
        sys.exit(1)

    if password_length < 1:
        print("Password length must be at least 1.")
        sys.exit(1)

    # print starting parameters
    print()
    print(f"Target hash: {sha256_hash}")
    print(f"Password length: {password_length}")
    print()

    # start time measuring
    start = time.time()

    # CHARSET is divided into 8 groups, each handled by a different worker
    # done by iterating through all the characters in CHARSET and distributing it evenly among all workers
    groups = [[] for _ in range(8)]

    for i, c in enumerate(CHARSET):
        groups[i % 8].append(c)

    # found_flag -> asyncio.Future object to communicate password discovery between workers
    found_flag = asyncio.get_event_loop().create_future()

    # creating tasks for each worker group, calling worker() asynchronously
    tasks = [
        worker(group, sha256_hash, password_length, found_flag)
        for group in groups
    ]

    # wait for all tasks to finish
    await asyncio.gather(*tasks)

    # handling finish, password either found or not
    if found_flag.done():
        print(f"Password found: {found_flag.result()}")
    else:
        print("Password not found.")

    end = time.time()
    print()
    print(f"Time of cracking: {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
