## Armstrong number

n=153
# Convert the number to a string to easily access each digit
rev = sum(int(digit) ** 3 for digit in str(n))
# rev = sum(map(lambda x: int(x) ** 3, str(n)))
print(rev)

if n == rev:
    print("Armstrong number")
else:
    print("Not an Armstrong number")

## Given strings are anagrams

from collections import Counter

str1 = "listen"
str2 = "silent"

# Compare the frequency of characters in both strings
if Counter(str1) == Counter(str2):
    print("Given strings are anagrams")
else:
    print("Not an anagram")
------------------
str1 = "listen"
str2 = "silent"

# Create a frequency dictionary for both strings
def get_char_frequency(string):
    freq_dict = {}
    for char in string:
        freq_dict[char] = freq_dict.get(char, 0) + 1
    return freq_dict

if get_char_frequency(str1) == get_char_frequency(str2):
    print("Given strings are anagrams")
else:
    print("Not an anagram")

## Sieve of Eratosthenes 

n = 20
primes = [True] * (n + 1)  # Create a list to mark prime numbers
primes[0] = primes[1] = False  # 0 and 1 are not prime numbers

# Sieve of Eratosthenes
for i in range(2, int(n**0.5) + 1):
    if primes[i]:
        for j in range(i * i, n + 1, i):
            primes[j] = False

# Collect prime numbers
my_list = [i for i in range(2, n + 1) if primes[i]]
print(my_list)
