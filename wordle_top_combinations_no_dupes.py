import time

return_top = 100

input_file = "wordle_guesses_no_dupes.txt"
output_file_pairs = "wordle_top_" + str(return_top) + "_pairs_no_dupes.txt"
output_file_fours = "wordle_top_" + str(return_top) + "_fours_no_dupes.txt"


# takes a string in the form of word1,word2,...,score, and returns the score as an int
def get_score(entry):
    entry_split = entry.split(",")
    return int(entry_split[-1].rstrip())


# insert a string in the form of text,score into pairs_list in the appropriate spot
# return the new lowest score in the list
def insert_in_order(group_list, text, score):
    # construct the string to insert
    inserted_text = text + "," + str(score) + "\n"

    # iterate through list
    for index in range(len(group_list)):
        if get_score(group_list[index]) < score:
            group_list.insert(index, inserted_text)
            return get_score(group_list[-1])

    # If we get here it means the provided score is lower than every score in the list, so we should append
    group_list.append(inserted_text)
    return score


# takes a file with name wordle_scores.txt that has words and scores in the form word:score per line, and finds
# the 100 highest scoring combinations of 2 words that do not repeat letters between words.
def top_pairs():
    # initialize the dict that will contain words and their scores
    score_dict = {}
    word_list = []

    # fill the score dictionary using data from the file
    f = open(input_file, 'r')
    lines = f.readlines()
    for line in lines:
        line_strip = line.rstrip()
        line_split = line_strip.split(",")
        score_dict[line_split[0]] = int(line_split[1])
        word_list.append(line_split[0])

    f.close()

    # initialize the list that will hold the top pairs
    pairs_list = []

    # initialize the variable that will hold the lowest of the top scores
    min_score = 0
    # iterate through the list of words
    for i in range(len(word_list)):
        word1 = word_list[i]
        score1 = score_dict[word1]

        # iterate through the remaining list of words
        for j in range(i + 1, len(word_list)):

            word2 = word_list[j]
            valid = True
            # check to see if this word shares letters with word 1, and set valid to false if it does
            for letter in word2:
                if letter in word1:
                    valid = False

            if valid:
                score2 = score_dict[word2]

                # if the list still has room, add this pair to the list
                if len(pairs_list) < return_top:
                    min_score = insert_in_order(pairs_list, word1 + "," + word2, score1 + score2)

                # if the score of this pair is larger than the min score in the list, remove that pair and add this pair in
                # the appropriate spot
                elif score1 + score2 >= min_score:
                    pairs_list.pop(-1)
                    min_score = insert_in_order(pairs_list, word1 + "," + word2, score1 + score2)

    f = open(output_file_pairs, 'w')
    f.writelines(pairs_list)
    f.close()


# takes a file with name wordle_scores.txt that has words and scores in the form word:score per line, and finds
# the 100 highest scoring combinations of 4 words that do not repeat letters between words.
def top_four():
    # initialize the dict that will contain words and their scores
    score_dict = {}
    word_list = []

    # fill the score dictionary using data from the file
    f = open(input_file, 'r')
    lines = f.readlines()
    for line in lines:
        line_strip = line.rstrip()
        line_split = line_strip.split(",")
        score_dict[line_split[0]] = int(line_split[1])
        word_list.append(line_split[0])

    f.close()

    # initialize the list that will hold the top groups of 4
    fours_list = []

    # initialize the variable that will hold the lowest of the top scores
    min_score = 0
    # iterate through the list of words
    for i in range(len(word_list)):

        word_start_time = time.time()
        word1 = word_list[i]
        score1 = score_dict[word1]

        print("Progress check: " + word1 + " " + str(i) + "/" + str(len(word_list)))

        # iterate through the remaining list of words for a second word
        for j in range(i + 1, len(word_list)):

            word2 = word_list[j]
            valid2 = True

            # check to see if this word shares letters with word 1, and set valid2 to false if it does
            for letter in word2:
                if letter in word1:
                    valid2 = False

            if valid2:
                score2 = score_dict[word2]

                # iterate through the remaining list of words for a third word
                for k in range(j + 1, len(word_list)):

                    word3 = word_list[k]
                    valid3 = True

                    # check to see if this word shares letters with words 1 and 2, and set valid3 to false if it does
                    for letter in word3:
                        if letter in word1 or letter in word2:
                            valid3 = False

                    if valid3:
                        score3 = score_dict[word3]

                        # iterate through the remaining list of words for a fourth word
                        for l in range(k + 1, len(word_list)):

                            word4 = word_list[l]
                            valid4 = True

                            # check to see if this word shares letters with words 1, 2 and 3 and set valid4 to false if
                            # it does
                            for letter in word4:
                                if letter in word1 or letter in word2 or letter in word3:
                                    valid4 = False

                            if valid4:
                                score4 = score_dict[word4]

                                # if the list still has room, add this pair to the list
                                if len(fours_list) < return_top:
                                    min_score = insert_in_order(fours_list,
                                                                word1 + "," + word2 + "," + word3 + "," + word4,
                                                                score1 + score2 + score3 + score4)
                                # if the score of this group is larger than the min score in the list, remove
                                # that group and add this group in the appropriate spot
                                elif score1 + score2 + score3 + score4 >= min_score:
                                    fours_list.pop(-1)
                                    min_score = insert_in_order(fours_list,
                                                                word1 + "," + word2 + "," + word3 + "," + word4,
                                                                score1 + score2 + score3 + score4)
        print("--- Word done in %s seconds ---" % (time.time() - word_start_time))

    f = open(output_file_fours, 'w')
    f.writelines(fours_list)
    f.close()


if __name__ == '__main__':
    answered = False
    answer = 0
    while not answered:
        print("Type 1 for pairs, or 2 for groups of 4")
        answer = int(input())
        if answer == 1 or answer == 2:
            answered = True
    if answer == 1:
        print("Running pairs")
        start_time = time.time()
        top_pairs()
        print("--- %s seconds ---" % (time.time() - start_time))
    if answer == 2:
        print("Running groups of 4")
        start_time = time.time()
        top_four()
        print("--- %s seconds ---" % (time.time() - start_time))
