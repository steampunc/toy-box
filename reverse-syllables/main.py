import pronouncing as prc

def reverse_phone(word):
    reversed_phones = []
    for phone in word:
        reversed_phones.append(phone[::-1])
    return reversed_phones

translating_sentence = raw_input("Please enter sentence you would like to reverse: ").split()[::-1]

final_sentence = []
for word in translating_sentence:
    word_possiblities = prc.phones_for_word(word.lower())
    print("Word possiblities: " + str(word_possiblities))
    reversed_word = word_possiblities[0].encode('utf-8').split()[::-1]

    print("Reversed word: " + str(reversed_word))
    reversed_pronunciation = reverse_phone(reversed_word)
    final_sentence.append(" ".join(reversed_pronunciation))
print(final_sentence)

