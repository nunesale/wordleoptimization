input_guesses = "wordle_guesses.txt"
input_answers = "wordle_answers.txt"

total_value_dict = {}
pos1_value_dict = {}
pos2_value_dict = {}
pos3_value_dict = {}
pos4_value_dict = {}
pos5_value_dict = {}
word_list = []
answer_list = []

alphabet = "abcdefghijklmnopqrstuvwxyz"


# a class to hold data concerning the feedback given on the previous guesses
class LetterData:
    def __init__(self, letter, position, colour):
        self.letter = letter
        self.position = position
        self.colour = colour


# takes a string in the form of word1,word2,...,score, and returns the score as an int
def get_score(entry):
    entry_split = entry.split(",")
    return int(entry_split[-1].rstrip())


# returns true if letter is in any of the words in list group, otherwise returns false
# group is an element of group_list
def check_letter_in_group(group, letter):
    for k in range(len(group)):
        if letter in group[k]:
            return True
    return False


# returns true if letter is in position in any of the words in list group, otherwise returns false
# group is an element of group_list
def check_letter_in_position_in_group(group, letter, position):
    for k in range(len(group)):
        if letter == group[k][position]:
            return True
    return False


# returns the value of letter in position
def get_positional_value(letter, position):
    if position == 0:
        return pos1_value_dict[letter]
    elif position == 1:
        return pos2_value_dict[letter]
    elif position == 2:
        return pos3_value_dict[letter]
    elif position == 3:
        return pos4_value_dict[letter]
    elif position == 4:
        return pos5_value_dict[letter]
    return 0


# returns true if word is a possible answer given the input_letter_data
def verify_word(word, input_letter_data):
    valid = True
    for datum in input_letter_data:
        if datum.colour == "b" and datum.letter in word:
            valid = False
            break
        elif datum.colour == "y" and (datum.letter not in word or datum.letter == word[datum.position]):
            valid = False
            break
        elif datum.colour == "g" and datum.letter != word[datum.position]:
            valid = False
            break
    return valid


# User inputs what they have guessed and what feedback they received. Program outputs the best next guess, assuming
# hard mode limitations.
if __name__ == '__main__':

    # fill the word list
    f = open(input_guesses, 'r')
    lines = f.readlines()

    for line in lines:
        word_list.append(line.rstrip())

    f.close()

    # fill the answer list
    f = open(input_answers, 'r')
    lines = f.readlines()
    for line in lines:
        answer_list.append(line.rstrip())

    f.close()

    # initialize the letter count dictionaries
    for letter in alphabet:
        total_value_dict[letter] = 0
        pos1_value_dict[letter] = 0
        pos2_value_dict[letter] = 0
        pos3_value_dict[letter] = 0
        pos4_value_dict[letter] = 0
        pos5_value_dict[letter] = 0

    answered = False
    answer = ""

    input_words_list = []

    # holds 3 element tuples of data: letter, position and colour (b, y, g)
    input_letter_data = []

    input_count = -1

    # get how many input words there are
    while not answered:
        print("how many words do you have?")
        input_count = int(input())
        if 0 < input_count < 6:
            answered = True

    # get all input words and their return data, and store it
    while input_count > 0:
        answered = False
        while not answered:
            print("Enter input word:")
            answer = input()

            answered = True
            for letter in answer:
                if not letter.isalpha():
                    answered = 0

        answered = False
        input_words_list.append(answer)

        while not answered:
            print("Enter feedback data as a series of letters representing what was returned for this word: b = "
                  "black/grey letter, y = yellow letter, g = green letter")

            answer = input()

            if len(answer) == len(input_words_list[-1]):
                answered = True

                for letter in answer:
                    if letter not in "byg":
                        answered = False

        for i in range(len(input_words_list[-1])):
            input_letter_data.append(LetterData(input_words_list[-1][i], i, answer[i]))

        input_count -= 1

    best_score = 0
    best_words = []
    valid_answers = []

    # filter answer list for valid answers
    for i in range(len(answer_list)):
        guess = answer_list[i]
        print("Evaluating: " + answer_list[i] + " " + str(i) + "/" + str(len(answer_list)))

        if verify_word(guess, input_letter_data):
            valid_answers.append(guess)

    # iterate through all valid answers and create dictionaries that hold total letter counts and positional letter
    # counts
    for answer in valid_answers:

        # iterate through all letters
        for i in range(len(answer)):

            # increment the counter for the letter
            total_value_dict[answer[i]] += 1

            # increment the counter for the position this letter is in
            if i == 0:
                pos1_value_dict[answer[i]] += 1
            elif i == 1:
                pos2_value_dict[answer[i]] += 1
            elif i == 2:
                pos3_value_dict[answer[i]] += 1
            elif i == 3:
                pos4_value_dict[answer[i]] += 1
            elif i == 4:
                pos5_value_dict[answer[i]] += 1

    # iterate through the guess list
    valid_answer_scores = []
    for i in range(len(word_list)):

        guess = word_list[i]
        print("Evaluating: " + guess + " " + str(i) + "/" + str(len(word_list)))

        # Verify that this is a valid guess in hard mode, that also optimizes the information given
        if verify_word(guess, input_letter_data):

            score = 0
            # iterate through all letters in word to get the score
            for j in range(len(guess)):

                # check if this letter is in any of the words in the group
                if not check_letter_in_group(input_words_list, guess[j]):
                    score += get_positional_value(guess[j], j)
                    if guess[j] not in guess[0:j]:
                        score += total_value_dict[guess[j]]

                        # check if this letter is in the same position in any of the words in group
                elif not check_letter_in_position_in_group(input_words_list, guess[j], j):
                    score += get_positional_value(guess[j], j)

            # if this guess is a valid answer, store it's score
            if guess in valid_answers:
                valid_answer_scores.append(guess + "," + str(score))

            # delete previous best guess and store new best guess if score is higher
            if score > best_score:
                best_words = [guess]
                best_score = score

            # add this guess to the list if it's score is equal
            elif score == best_score:
                best_words.append(guess)

    # if no guesses found, return a message
    if len(best_words) == 0:
        print("NO WORDS FOUND")

    else:

        # if no answers found, return a message
        if len(valid_answers) == 0:
            print("NO VALID ANSWERS")

        else:

            # print answers in descending score order
            valid_answer_scores.sort(key=get_score, reverse=True)
            for word in valid_answer_scores:
                print(word)
            print("There are " + str(len(valid_answer_scores)) + " valid answers:")

        # print best guess(es)
        print("Score: " + str(best_score))
        for word in best_words:
            print(word)
