#!/usr/bin/env python3

import argparse
import hashlib
import re
import requests

def check_breach(password):
    hash_val = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = hash_val[:5]
    suffix = hash_val[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)
    return suffix in res.text

def score_password(password):
    score = 0
    if len(password) >= 8: score += 20
    if re.search(r'[A-Z]', password): score += 10
    if re.search(r'[a-z]', password): score += 10
    if re.search(r'[0-9]', password): score += 10
    if re.search(r'[\W_]', password): score += 10
    if password.lower() in ["password", "123456"]: score -= 20
    return score

def main():
    parser = argparse.ArgumentParser(description="AI Password Strength Checker")
    parser.add_argument("password", help="Password to evaluate")
    args = parser.parse_args()
    pw = args.password

    print(f"Password: {pw}")
    print(f"Strength Score: {score_password(pw)}/100")
    if check_breach(pw):
        print("Warning: This password has been breached!")
    else:
        print("Good news: This password is not known to be breached.")

if __name__ == "__main__":
    main()
