find_top = 13000
max_repeat_letters = 5
total_value_dict = {}
pos1_value_dict = {}
pos2_value_dict = {}
pos3_value_dict = {}
pos4_value_dict = {}
pos5_value_dict = {}
input_file = "wordle_best_" + str(find_top) + "_additions_recursive.txt"
output_file = "wordle_best_" + str(find_top) + "_additions_recursive.txt"
input_guesses = "wordle_guesses.txt"
total_freq_data = "total_letter_frequency.txt"
position1_data = "position1_letter_frequency.txt"
position2_data = "position2_letter_frequency.txt"
position3_data = "position3_letter_frequency.txt"
position4_data = "position4_letter_frequency.txt"
position5_data = "position5_letter_frequency.txt"


# takes a string in the form of word1,word2,...,score, and returns the score as an int
def get_score(entry):
    entry_split = entry.split(",")
    return int(entry_split[-1].rstrip())


# insert a string in the form of text,score into list in the appropriate spot
# return the new lowest score in the list
def insert_in_order(list, text, score):
    # construct the string to insert
    inserted_text = text + "," + str(score) + "\n"

    # iterate through list
    for index in range(len(list)):
        if get_score(list[index]) < score:
            list.insert(index, inserted_text)
            return get_score(list[-1])

    # If we get here it means the provided score is lower than every score in the list, so we should append
    list.append(inserted_text)
    return score


# returns true if letter is in any of the words in list group, otherwise returns false
# group is an element of group_list
def check_letter_in_group(group, letter):
    for k in range(len(group) - 1):
        if letter in group[k]:
            return True
    return False


# returns true if letter is in position in any of the words in list group, otherwise returns false
# group is an element of group_list
def check_letter_in_position_in_group(group, letter, position):
    for k in range(len(group) - 1):
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


# takes two lists of words and checks if they contain the same words
def check_if_duplicate(line_split1, line_split2):
    for word in line_split1:
        if word not in line_split2:
            return False
    return True


# takes a string and returns the number of unique alphabetical letters in it
# assumes input strings are in all upper or all lower case
def count_letters(line):
    count = 0
    for letter_index in range(len(line)):
        if line[letter_index].isalpha() and line[letter_index] not in line[:letter_index]:
            count = count + 1
    return count


# given a list of groups of words and their scores, finds the find_top best words to add to each set to maximize it's
# score
if __name__ == '__main__':

    answered = False
    answer = 0

    while not answered:
        print("Press 1 for regular (easier to read) output, or press 2 for recursive output (In a format that allows "
              "this code to be ran on it again)")
        answer = int(input())
        if answer == 1 or answer == 2:
            answered = True

    word_list = []
    group_list = []

    # stores the exact string from the file for later use
    original_group_list = []

    # stores the number of unique letters in the word combination at the respective index in group_list
    letter_count = []

    # fill the group list using the groups and scores from the file, as well as the unique letters list
    f = open(input_file, 'r')
    lines = f.readlines()

    # use the first line to get how many letters are in each line
    input_letters = 0
    for letter in lines[0]:
        if letter.isalpha():
            input_letters += 1

    print("Counting unique letters....")
    for i in range(len(lines)):
        print("Counting " + str(i) + "/" + str(len(lines)))
        original_group_list.append(lines[i])
        line_strip = lines[i].rstrip()
        letter_count.append(count_letters(line_strip))
        line_split = line_strip.split(',')
        group_list.append(line_split)

    f.close()

    # fill the word list
    f = open(input_guesses, 'r')
    lines = f.readlines()

    word_letters = 0
    # use the first word to get how many letters are in each word
    for letter in lines[0]:
        if letter.isalpha():
            word_letters += 1

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

    additions_list = []
    # iterate through every group
    for i in range(len(group_list)):

        print("Evaluating group: " + original_group_list[i] + " " + str(i) + "/" + str(len(group_list)))
        # initialize the current score of the group as the minimum score
        group_score = int(group_list[i][-1])
        min_score = int(group_list[i][-1])
        top_additions = []

        # iterate through all words to find the best additions
        for word in word_list:

            score = group_score
            new_unique_letters = 0

            # iterate through all letters in word to get the score
            for j in range(len(word)):

                # if too many duplicate letters are found stop examining this word
                if (input_letters + j) - (letter_count[i] + new_unique_letters) > max_repeat_letters:
                    break

                # check if this letter is in any of the words in the group
                if not check_letter_in_group(group_list[i], word[j]):
                    score += get_positional_value(word[j], j)
                    if word[j] not in word[0:j]:
                        score += total_value_dict[word[j]]
                        new_unique_letters += 1

                # check if this letter is in the same position in any of the words in group
                elif not check_letter_in_position_in_group(group_list[i], word[j], j):
                    score += get_positional_value(word[j], j)

            # do not add this word if it would cause the combination to repeat too many letters
            if (input_letters + word_letters) - (letter_count[i] + new_unique_letters) <= max_repeat_letters:

                # if the list still has room add this word to the list
                if len(top_additions) < find_top:
                    min_score = insert_in_order(top_additions, word, score)

                # if score is greater than min score, remove the lowest scoring word and
                # add this word to top_additions in the appropriate spot
                elif score >= min_score:
                    top_additions.pop(-1)
                    min_score = insert_in_order(top_additions, word, score)

        # add the list of the best additions to additions_list, at the same index as the group
        additions_list.insert(i, top_additions)

    # write the file output

    if answer == 1:
        f = open("wordle_best_" + str(find_top) + "_additions.txt", 'w')
        # iterate and write all the input groups
        for i in range(len(original_group_list)):
            f.write(original_group_list[i])

            # iterate and write the list of top additions
            for addition in additions_list[i]:
                f.write("    " + addition)
        f.close()

    # write the file output in the same format as an input file
    # this also sorts the output by score
    elif answer == 2:
        print("Creating output...")
        output_lines = []
        for i in range(len(group_list)):
            start_line = ""
            for j in range(len(group_list[i]) - 1):
                start_line = start_line + group_list[i][j] + ","
            for addition in additions_list[i]:
                output_lines.append(start_line + addition)
        print("Sorting...")
        output_lines.sort(key=get_score, reverse=True)

        output_lines = output_lines[:1000000]
        # eliminate combinations that have the same words as other combinations
        print("Eliminating duplicates...")
        i = 0
        while i < len(output_lines):

            print("Checking " + str(i) + "/" + str(len(output_lines)))

            line_split = output_lines[i].rstrip().split(',')

            j = i + 1
            while j < len(output_lines):

                line2_split = output_lines[j].rstrip().split(',')
                # if scores are not the same don't check any further into the list
                if line2_split[-1] != line_split[-1]:
                    break
                # if duplicate found remove it
                elif check_if_duplicate(line_split[:-1], line2_split[:-1]):
                    output_lines.pop(j)
                    j = j - 1

                j = j + 1

            i = i + 1

        print("Writing...")
        f = open(output_file, 'w')
        f.writelines(output_lines)
        f.close()
