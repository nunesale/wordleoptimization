import time

input_word_list = "wordle_guesses.txt"
total_freq_data = "total_letter_frequency.txt"
position1_data = "position1_letter_frequency.txt"
position2_data = "position2_letter_frequency.txt"
position3_data = "position3_letter_frequency.txt"
position4_data = "position4_letter_frequency.txt"
position5_data = "position5_letter_frequency.txt"
output_file = "hello wordl scores no dupes.txt"

return_top = 100
total_value_dict = {}
pos1_value_dict = {}
pos2_value_dict = {}
pos3_value_dict = {}
pos4_value_dict = {}
pos5_value_dict = {}
word_list = []

# NOTE: I do not reccommend running this for groups of 3, it will take a very very long time

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


# returns true if letter is in position in any of the words in list group, otherwise returns false
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


# find the pairs of words with the most points according to the scoring dictionaries
def top_pairs():
    # initialize the list that will hold the top pairs
    pairs_list = []

    # initialize the variable that will hold the lowest of the top scores
    min_score = 0

    # iterate through the list of words
    for i in range(len(word_list)):
        word1 = word_list[i]
        score1 = 0

        # calculate the score of word 1
        for j in range(len(word1)):
            if word1[j] not in word1[0:j]:
                score1 += total_value_dict[word1[j]]
            score1 += get_positional_value(word1[j], j)

        # iterate through the remaining list of words
        for j in range(i + 1, len(word_list)):

            word2 = word_list[j]
            score2 = 0
            # assign a score to word 2, taking the letters in word 1 into account1
            for k in range(len(word2)):
                if word2[k] not in word1 and word2[k] not in word2[0:k]:
                    score2 += total_value_dict[word2[k]]
                if not check_letter_in_position_in_group([word1], word2[k], k):
                    score2 += get_positional_value(word2[k], k)

            # if the list still has room, add this pair to the list
            if len(pairs_list) < return_top:
                min_score = insert_in_order(pairs_list, word1 + "," + word2, score1 + score2)

            # if the score of this pair is larger than the min score in the list, remove that pair and add this pair in
            # the appropriate spot
            elif score1 + score2 >= min_score:
                pairs_list.pop(-1)
                min_score = insert_in_order(pairs_list, word1 + "," + word2, score1 + score2)

    f = open("wordle_top_" + str(return_top) + "_pairs.txt", 'w')
    f.writelines(pairs_list)
    f.close()


# find the groups of 3 words with the most points according to the scoring dictionaries
# NOTE this was taking so long to run that I abandoned the idea
def top_three():
    # initialize the list that will hold the top groups of 3
    threes_list = []

    # initialize the variable that will hold the lowest of the top scores
    min_score = 0
    # iterate through the list of words
    # iterate through the list of words
    for i in range(len(word_list)):
        word_start_time = time.time()
        word1 = word_list[i]
        score1 = 0

        print("Progress check: " + word1 + " " + str(i) + "/" + str(len(word_list)))

        # calculate the score of word 1
        for j in range(len(word1)):
            if word1[j] not in word1[0:j]:
                score1 += total_value_dict[word1[j]]
            score1 += get_positional_value(word1[j], j)

        # iterate through the remaining list of words
        for j in range(i + 1, len(word_list)):

            word2 = word_list[j]
            score2 = 0
            # assign a score to word 2, taking the letters in word 1 into account1
            for k in range(len(word2)):
                if word2[k] not in word1 and word2[k] not in word2[0:k]:
                    score2 += total_value_dict[word2[k]]
                if not check_letter_in_position_in_group([word1], word2[k], k):
                    score2 += get_positional_value(word2[k], k)

            # iterate through remaining list of words
            for k in range(j + 1, len(word_list)):
                word3 = word_list[k]
                score3 = 0
                # assign a score to word 3, taking the letters in words 1 and 2 into account1
                for l in range(len(word3)):
                    if word3[l] not in word1 and word3[l] not in word2 and word3[l] not in word3[0:l]:
                        score3 += total_value_dict[word3[l]]
                    if not check_letter_in_position_in_group([word1, word2], word3[l], l):
                        score3 += get_positional_value(word3[l], l)

                    # if the list still has room, add this group to the list
                    if len(threes_list) < return_top:
                        min_score = insert_in_order(threes_list, word1 + "," + word2 + "," + word3, score1 + score2 +
                                                    score3)

                    # if the score of this group is larger than the min score in the list, remove that group and add
                    # this group in the appropriate spot
                    elif score1 + score2 + score3 >= min_score:
                        threes_list.pop(-1)
                        min_score = insert_in_order(threes_list, word1 + "," + word2 + "," + word3, score1 + score2 +
                                                    score3)

        print("--- Word done in %s seconds ---" % (time.time() - word_start_time))

    f = open("wordle_top_" + str(return_top) + "_threes.txt", 'w')
    f.writelines(threes_list)
    f.close()


if __name__ == '__main__':

    # fill the word list
    f = open(input_word_list, 'r')
    lines = f.readlines()
    for line in lines:
        word_list.append(line.rstrip())

    f.close()

    # fill the total count dictionary
    f = open(total_freq_data, 'r')
    lines = f.readlines()
    for line in lines:
        line_strip = line.rstrip()
        line_split = line_strip.split(":")
        total_value_dict[line_split[0]] = int(line_split[1])

    f.close()

    # fill the position 1 count dictionary
    f = open(position1_data, 'r')
    lines = f.readlines()
    for line in lines:
        line_strip = line.rstrip()
        line_split = line_strip.split(":")
        pos1_value_dict[line_split[0]] = int(line_split[1])

    f.close()

    # fill the position 2 count dictionary
    f = open(position2_data, 'r')
    lines = f.readlines()
    for line in lines:
        line_strip = line.rstrip()
        line_split = line_strip.split(":")
        pos2_value_dict[line_split[0]] = int(line_split[1])

    f.close()

    # fill the position 3 count dictionary
    f = open(position3_data, 'r')
    lines = f.readlines()
    for line in lines:
        line_strip = line.rstrip()
        line_split = line_strip.split(":")
        pos3_value_dict[line_split[0]] = int(line_split[1])

    f.close()

    # fill the position 4 count dictionary
    f = open(position4_data, 'r')
    lines = f.readlines()
    for line in lines:
        line_strip = line.rstrip()
        line_split = line_strip.split(":")
        pos4_value_dict[line_split[0]] = int(line_split[1])

    f.close()

    # fill the position 5 count dictionary
    f = open(position5_data, 'r')
    lines = f.readlines()
    for line in lines:
        line_strip = line.rstrip()
        line_split = line_strip.split(":")
        pos5_value_dict[line_split[0]] = int(line_split[1])

    f.close()

    answered = False
    answer = 0
    while not answered:
        print("Type 1 for pairs, or 2 for groups of 3")
        answer = int(input())
        if answer == 1 or answer == 2:
            answered = True
    if answer == 1:
        print("Running pairs")
        start_time = time.time()
        top_pairs()
        print("--- %s seconds ---" % (time.time() - start_time))
    if answer == 2:
        print("Running groups of 3")
        start_time = time.time()
        top_three()
        print("--- %s seconds ---" % (time.time() - start_time))
