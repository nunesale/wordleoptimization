input_file = "wordle_answers.txt"

# takes a (letter, number) tuple and returns the number
def get_number(entry):
    return entry[1]


# outputs the frequency of each letters in the words contained in the file wordle_answers.txt, as well as the
# frequency of each letter in each position
# assumes each word is 5 letters, and each word is on its own line

if __name__ == '__main__':

    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # create dictionaries to hold letter counts
    alphabet_dict = {}
    index_0 = {}
    index_1 = {}
    index_2 = {}
    index_3 = {}
    index_4 = {}

    for letter in alphabet:
        alphabet_dict[letter] = 0
        index_0[letter] = 0
        index_1[letter] = 0
        index_2[letter] = 0
        index_3[letter] = 0
        index_4[letter] = 0

    f = open(input_file, 'r')

    words = f.readlines()
    # iterate through all words
    for word in words:

        # strip the newline character
        word_strip = word.rstrip()

        # iterate through all letters
        for i in range(len(word_strip)):

            # increment the counter for the letter
            alphabet_dict[word_strip[i]] += 1

            # increment the counter for the position this letter is in
            if i == 0:
                index_0[word_strip[i]] += 1
            elif i == 1:
                index_1[word_strip[i]] += 1
            elif i == 2:
                index_2[word_strip[i]] += 1
            elif i == 3:
                index_3[word_strip[i]] += 1
            elif i == 4:
                index_4[word_strip[i]] += 1

    f.close()
    # convert the total count dictionary to a list of (letter, count) tuples
    alphabet_list = list(alphabet_dict.items())

    # sort the list of tuples by count, descending
    alphabet_list.sort(key=get_number, reverse=True)

    # do the same as above for each index dict
    index_0 = list(index_0.items())
    index_1 = list(index_1.items())
    index_2 = list(index_2.items())
    index_3 = list(index_3.items())
    index_4 = list(index_4.items())

    index_0.sort(key=get_number, reverse=True)
    index_1.sort(key=get_number, reverse=True)
    index_2.sort(key=get_number, reverse=True)
    index_3.sort(key=get_number, reverse=True)
    index_4.sort(key=get_number, reverse=True)

    print("Overall:")
    # print letter count for each word
    for pair in alphabet_list:
        print(pair[0] + ": " + str(pair[1]))

    print("\n")
    # print letter count for the first position
    print("Position 1:")
    for pair in index_0:
        print(pair[0] + ": " + str(pair[1]))

    print("\n")
    # print letter count for the second position
    print("Position 2:")
    for pair in index_1:
        print(pair[0] + ": " + str(pair[1]))

    print("\n")
    # print letter count for the third position
    print("Position 3:")
    for pair in index_2:
        print(pair[0] + ": " + str(pair[1]))

    print("\n")
    # print letter count for the fourth position
    print("Position 4:")
    for pair in index_3:
        print(pair[0] + ": " + str(pair[1]))

    print("\n")
    # print letter count for the fifth position
    print("Position 5:")
    for pair in index_4:
        print(pair[0] + ": " + str(pair[1]))

