input_word_list = "wordle_guesses.txt"
total_freq_data = "total_letter_frequency.txt"
position1_data = "position1_letter_frequency.txt"
position2_data = "position2_letter_frequency.txt"
position3_data = "position3_letter_frequency.txt"
position4_data = "position4_letter_frequency.txt"
position5_data = "position5_letter_frequency.txt"
output_file = "hello wordl scores no dupes.txt"


# takes a string in the form of word,score, and returns the score as an int
def get_score(entry):
    entry_split = entry.split(",")
    return int(entry_split[1].rstrip())


# takes a list of valid wordle guesses as file wordle_guesses_trimmed.txt and outputs a file wordle_guesses_scored.txt
# which contains each valid guess alongside an assigned score, with a comma seperator
# the score is determined by the frequency of each letter in all possible answers + the frequency of each letter in
# its position in all possible answers
# this information is obtained from the files total_freq_data, position1_data, position2_data, position3_data,
# position4_data, position5_data, which are all in the format "letter:frequency", with one letter per line.
if __name__ == '__main__':

    #establish the dictionaries that will associate letters and positions with values
    total_value_dict = {}
    pos1_value_dict = {}
    pos2_value_dict = {}
    pos3_value_dict = {}
    pos4_value_dict = {}
    pos5_value_dict = {}

    #fill the total count dictionary
    f = open(total_freq_data, 'r')
    lines = f.readlines()
    for line in lines:
        line_strip = line.rstrip()
        line_split = line_strip.split(":")
        total_value_dict[line_split[0]] = int(line_split[1])

    f.close()

    #fill the position 1 count dictionary
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

    f = open(input_word_list, 'r')
    words = f.readlines()

    word_scores = []
    #iterate through every guess

    for word in words:

        # remove the newline character
        word_strip = word.rstrip()

        # initalize the variable that will hold this word's score
        total = 0

        for i in range(len(word_strip)):
            # add the total frequency of the letter to the score
            if word_strip[i] not in word_strip[0:i]:
                total += total_value_dict[word_strip[i]]

            # add the positional frequency of the letter to the score
            if i == 0:
                total += pos1_value_dict[word_strip[i]]
            elif i == 1:
                total += pos2_value_dict[word_strip[i]]
            elif i == 2:
                total += pos3_value_dict[word_strip[i]]
            elif i == 3:
                total += pos4_value_dict[word_strip[i]]
            elif i == 4:
                total += pos5_value_dict[word_strip[i]]

        word_scores.append(word_strip + "," + str(total) + "\n")
    f.close()

    word_scores.sort(key=get_score, reverse=True)

    f = open(output_file, 'w')
    f.writelines(word_scores)
    f.close()
