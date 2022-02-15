input_file = "wordle_guesses.txt.txt"
output_file = "wordle_guesses_no_dupes.txt"
# take file input_file and output a new file output_file that has every word with duplicate
# letters removed
if __name__ == '__main__':

    # initialize list that will contains all words without duplicate letters
    valid_words = []

    f = open(input_file, 'r')
    words = f.readlines()


    #iterate through all words
    for word in words:

        # initialize list to hold letters in word
        letters = []

        # initialize boolean valid to true; will become false if a duplicate letter is found
        valid = True

        #iterate through letters in word
        for letter in word:
            if letter not in letters:
                letters.append(letter)
            else:
                valid = False
                break;

        if valid:
            valid_words.append(word)

    f.close()

    f = open(output_file, 'w')
    f.writelines(valid_words)
    f.close()

