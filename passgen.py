import itertools
import string
import os

# Extended leetspeak substitutions
LEET_MAP = {
    'a': ['a', '@', '4', '^', 'A'],
    'b': ['b', '8', 'B'],
    'c': ['c', '(', '<', '{', 'C'],
    'd': ['d', 'D'],
    'e': ['e', '3', 'E', '€'],
    'f': ['f', 'F'],
    'g': ['g', '9', '6', 'G'],
    'h': ['h', '#', 'H'],
    'i': ['i', '1', '!', '|', 'I'],
    'j': ['j', 'J'],
    'k': ['k', 'K'],
    'l': ['l', '1', '|', 'L', '£'],
    'm': ['m', 'M', '|\/|'],
    'n': ['n', 'N'],
    'o': ['o', '0', 'O', '()', '*'],
    'p': ['p', 'P'],
    'q': ['q', 'Q'],
    'r': ['r', 'R'],
    's': ['s', '$', '5', 'S'],
    't': ['t', '7', '+', 'T'],
    'u': ['u', 'v', 'U', '|_|'],
    'v': ['v', 'V', 'u'],
    'w': ['w', 'W'],
    'x': ['x', '%', 'X'],
    'y': ['y', 'Y'],
    'z': ['z', '2', 'Z']
}

PREFIXES = ['', '!', '@', '#', '$', '%', '&', '*', 'my', 'the', 'real', 'its', 'admin', 'user', 'pro', 'ultra', 'super', 'mr', 'mrs', 'dr']
SUFFIXES = ['', '!', '@', '#', '$', '%', '&', '*', '123', '1234', '12345', '007', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '69', '420', '666', '777', '321']

INSERT_CHARS = list(string.digits + "!@#$%^&*._-")

KEYBOARD_PATTERNS = ["qwerty", "asdf", "zxcv", "1q2w3e", "123qwe", "!@#$", "password", "letmein"]

MAX_OUTPUT = 100_000_000  # 100 million

def leet_variants(word):
    pools = [LEET_MAP.get(c.lower(), [c]) for c in word]
    for combo in itertools.product(*pools):
        yield ''.join(combo)

def case_variants(word):
    pools = []
    for char in word:
        if char.isalpha():
            pools.append([char.lower(), char.upper()])
        else:
            pools.append([char])
    for combo in itertools.product(*pools):
        yield ''.join(combo)

def insertions(word):
    for i in range(len(word) + 1):
        for ch in INSERT_CHARS:
            yield word[:i] + ch + word[i:]

def deletions(word):
    for i in range(len(word)):
        yield word[:i] + word[i+1:]

def separator_injection(word):
    separators = ['.', '_', '-', '!', '@']
    for sep in separators:
        yield sep.join(list(word))

def transform_full(seed):
    """Full chain of transformations for a seed."""
    seen = set()
    for variant in leet_variants(seed):
        for cased in case_variants(variant):
            if cased not in seen:
                seen.add(cased)
                yield cased
                yield cased[::-1]
                yield from insertions(cased)
                yield from deletions(cased)
                yield cased + cased
                yield from separator_injection(cased)

def generate_passwords(seeds):
    count = 0
    # Single word + patterns
    for seed in seeds:
        for variant in transform_full(seed):
            for pre in PREFIXES:
                for suf in SUFFIXES:
                    yield f"{pre}{variant}{suf}"
                    count += 1
                    if count >= MAX_OUTPUT:
                        return
            # Add keyboard walks
            for pat in KEYBOARD_PATTERNS:
                yield variant + pat
                yield pat + variant
                count += 2
                if count >= MAX_OUTPUT:
                    return

    # Multi-word combos (2–3 words)
    all_variants = []
    for s in seeds:
        all_variants.extend(set(transform_full(s)))
    for r in range(2, 4):
        for combo in itertools.permutations(all_variants, r):
            base = ''.join(combo)
            for pre in PREFIXES:
                for suf in SUFFIXES:
                    yield f"{pre}{base}{suf}"
                    count += 1
                    if count >= MAX_OUTPUT:
                        return

def main():
    print("=== 100M Hybrid Password Generator ===")
    seed_input = input("Enter your seed words (comma-separated): ")
    seeds = [w.strip() for w in seed_input.split(",") if w.strip()]

    filename = "ultimate_passwords.txt"
    open(filename, 'w').close()  # clear file

    print(f"[+] Generating up to {MAX_OUTPUT:,} passwords... This WILL take a long time!")
    with open(filename, 'w') as f:
        for idx, pwd in enumerate(generate_passwords(seeds), 1):
            f.write(pwd + "\n")
           # if idx % 100000 == 0:
               # print(f"Generated {idx:,} passwords so far...")
    print("Generating... please wait.")
    print(f"[+] Done! Passwords saved to {filename}")

if __name__ == "__main__":
    main()

