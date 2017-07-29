import sys
import crypt
import itertools as it


def main():
    # Ensure proper usage.
    if len(sys.argv) != 2:
        print("Usage: ./crack hash")
        exit(1)
    crack_password(sys.argv[1])


def crack_password(user_hash):
    # Get salt for hash function.
    salt = user_hash[:2]
    alphabet = []
    # Add lower and uppercase letters to alphabet list
    for letter in it.chain(range(65, 91), range(97, 123)):
        alphabet.append(chr(letter))
    # Check all possible permutations of letters for each below assumption
    for i in range(1, 4):
        for possible_password in it.product(alphabet, repeat=i):
            # Generate hash of permutation and compare with input
            if crypt.crypt("".join(possible_password), salt) == user_hash:
                # Print out cracked password if there's a match
                print("".join(possible_password))
                exit(0)

if __name__ == "__main__":
    main()