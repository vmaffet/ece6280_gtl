from math import sqrt
from csv import DictReader


def vigenere(key, text): #Vignère encryption and decryption
    ciphertext = ""
    for i in range(len(text)):
        ciphertext += chr((ord(text[i]) - ord('a') + key[i % len(key)]) % 26 + ord('a'))
    return ciphertext


def get_divisors(n): #Finds the divisors of a number
    divisors = set()
    for i in range(1, int(sqrt(n))+1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(int(n/i))
    return divisors


def find_possible_key_length(n, text): #Find the possible key_length for a given substring size
    possible_length = {}
    for i in range(len(text)-n):
        pattern = text[i:i+n]
        a = i
        b = text.find(pattern, i+n)
        while b != -1:
            for k in get_divisors(b-a):
                if k in possible_length:
                    possible_length[k] += 1
                else:
                    possible_length[k] = 1
            a = b
            b += n
            b = text.find(pattern, b)
    return possible_length


def get_probabilities(text): #Probability of a character to appear in text
    prob = {}
    for c in text:
        if c in prob:
            prob[c] += 1
        else:
            prob[c] = 1
    for key in prob.keys():
        prob[key] /= len(text)
    return prob


text_input = open("input.txt", "r").read() #Getting ciphertext
l= 3
key_length= {}
keep_on = True
while keep_on:
    keep_on = False
    for it in find_possible_key_length(l, text_input).items():
        keep_on = True
        if it[0] in key_length: #Adding key length vote for each size
            key_length[it[0]] += it[1]
        else:
            key_length[it[0]] = it[1]
    l += 1
del key_length[1] #Removing divisor 1
key = max(key_length, key=key_length.get) #Key length is the most likely divisor
print("The most probable key length is:", key)

text_probabilities = {}
reader = DictReader(open("probabilities.csv", "r", encoding="utf-8-sig"), dialect="excel")
for row in reader:
    text_probabilities[row['letter']] = row['probability']

print("Alphabet probabilities", sorted(text_probabilities.items(), key=lambda x: x[1], reverse=True))

same_sub_key_seq = ["" for x in range(key)]
for i in range(len(text_input)): #Creating subsets of letters with same encoding
    same_sub_key_seq[i % key] += text_input[i]

key_values = []
for seq in same_sub_key_seq:
    seq_prob = get_probabilities(seq) #Computes the character probability for each subset
    print("", sorted(seq_prob.items(), key=lambda x: x[1], reverse=True))
    key_values.append(max(seq_prob, key=seq_prob.get))

val = [sorted(text_probabilities, key=text_probabilities.get, reverse=True)[0] for x in range(key)]
val[1]= sorted(text_probabilities, key=text_probabilities.get, reverse=True)[7] #Picking the 8th most likely english letter

key_int = []
for i in range(len(key_values)): #Calculating decryption key
    key_int.append(ord(val[i]) - ord(key_values[i]))

print("Testing decoding key:", key_int)

result_text = vigenere(key_int, text_input)
print(result_text)

open("output.txt", "w").write(result_text)
