# author: Sirinian Aram Emmanouil

import shutil
import sys
from random import shuffle
import pandas as pd
# from string import ascii_lowercase

PAGE_ONE_FILE_PATH = "./page1.csv"
PAGE_TWO_FILE_PATH = "./page2.csv"
PAGE_THREE_FILE_PATH = "./page3.csv"
PAGE_FOUR_FILE_PATH = "./page4.csv"
PAGE_FIVE_FILE_PATH = "./page5.csv"

PAGE_ONE_CODE_NUMBER = 1
PAGE_TWO_CODE_NUMBER = 2
PAGE_THREE_CODE_NUMBER = 3
PAGE_FOUR_CODE_NUMBER = 4
PAGE_FIVE_CODE_NUMBER = 5


def printProgressBar(
        iteration, total, prefix='', suffix='', decimals=1, length=100,
        fill='█', autosize=False):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        autosize    - Optional  : automatically resize the length of the progress bar to the terminal window (Bool)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    if autosize:
        cols, _ = shutil.get_terminal_size(fallback = (length, 1))
        length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def read_dataframe_from_csv_file(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print("File " + file_path + " cannot be found.")
        sys.exit()


def print_all_available_options():
    print(str(PAGE_ONE_CODE_NUMBER) + ") \t" + "PAGE 1")
    print(str(PAGE_TWO_CODE_NUMBER) + ") \t" + "PAGE 2")
    print(str(PAGE_THREE_CODE_NUMBER) + ") \t" + "PAGE 3")
    print(str(PAGE_FOUR_CODE_NUMBER) + ") \t" + "PAGE 4")
    print(str(PAGE_FIVE_CODE_NUMBER) + ") \t" + "PAGE 5")


def load_chosen_pages(model_code):
    chosen_dataframe = pd.DataFrame()

    if (model_code == PAGE_ONE_CODE_NUMBER):
        file_path = PAGE_ONE_FILE_PATH
        chosen_dataframe = read_dataframe_from_csv_file(file_path)

    if (model_code == PAGE_TWO_CODE_NUMBER):
        file_path = PAGE_TWO_FILE_PATH
        chosen_dataframe = read_dataframe_from_csv_file(file_path)

    if (model_code == PAGE_THREE_CODE_NUMBER):
        file_path = PAGE_THREE_FILE_PATH
        chosen_dataframe = read_dataframe_from_csv_file(file_path)

    if (model_code == PAGE_FOUR_CODE_NUMBER):
        file_path = PAGE_FOUR_FILE_PATH
        chosen_dataframe = read_dataframe_from_csv_file(file_path)

    if (model_code == PAGE_FIVE_CODE_NUMBER):
        file_path = PAGE_FIVE_FILE_PATH
        chosen_dataframe = read_dataframe_from_csv_file(file_path)

    return chosen_dataframe


"""
def ask_user_a_yes_or_no_question(question):
    while True:
        answer = (input(question + "[y/n]: ")).lower()

        if (answer == "y" or answer == "yes" or answer == "yeah"):
            return True
        elif (answer == "n" or answer == "no" or answer == "nah"):
            return False
        else:
            continue
"""


def ask_user_for_page_code_numbers():
    while True:
        print_all_available_options()
        try:
            page_codes = [int(x.strip()) for x in input("Your page preference:").split(",")]
        except ValueError:
            print("Please enter an valid integer or integers")
            continue

        for page_code in page_codes:
            if (page_code != PAGE_ONE_CODE_NUMBER) and \
                    (page_code != PAGE_TWO_CODE_NUMBER) and \
                    (page_code != PAGE_THREE_CODE_NUMBER) and \
                    (page_code != PAGE_FOUR_CODE_NUMBER) and \
                    (page_code != PAGE_FIVE_CODE_NUMBER):
                print("Please enter an valid integer or integers")
                continue

        return page_codes


def answer_question(question, answers):
    while True:
        print(question)
        for i in range(len(answers)):
            print(str(i+1) + "): " + answers[i])
        answer = input("Your answer " + "[1 - " + str(len(answers)) + "]" + ": ")
        answer_text = ""

        try:
            sting_int = int(answer)
            if (sting_int >= 1 and sting_int <= len(answers)):
                answer_text = answers[sting_int - 1]
                return answer_text
            else:
                print("Please enter an valid integer")
        except ValueError:
            print("Please enter an valid integer")


def answer_questions(chosen_dataframe):
    for index, row in chosen_dataframe.iterrows():
        row['Correct answer'] = row[row['Correct answer']]

    chosen_dataframe = chosen_dataframe.sample(frac=1)
    all_answers = []
    all_questions = chosen_dataframe["Question"].tolist()
    all_correct_answers = chosen_dataframe["Correct answer"].tolist()
    all_user_answers = []

    for index, row in chosen_dataframe.drop(columns=['Question', 'Correct answer']).iterrows():
        answers = row.tolist()
        shuffle(answers)
        all_answers.append(answers)

    i = 1
    for question, answers in zip(all_questions, all_answers):
        printProgressBar(i, len(all_questions))
        print("")
        all_user_answers.append(answer_question(question, answers))
        i += 1

    raw_data = {'Question': all_questions,
                'Correct answer': all_correct_answers,
                'User\'s answer': all_user_answers
                }

    dataframe = pd.DataFrame(
        raw_data,
        columns = ['Question', 'Correct answer', 'User\'s answer'])

    return dataframe


def print_right_answers(dataframe_with_all_user_answers):
    flag = True
    total_number_of_right_answers = 0
    for index, row in dataframe_with_all_user_answers.iterrows():
        if (row['Correct answer'] != row['User\'s answer']):
            if (flag):
                print("It looks like you made some mistakes, study the right answers and better luck next time!")
                print("")
                print("")
                flag = False
            print(row['Question'])
            print(row['Correct answer'])
            print("")
        else:
            total_number_of_right_answers += 1
    print(
            "Right answered questions: " + str(total_number_of_right_answers) +
            "/" + str(len(dataframe_with_all_user_answers)))


page_codes = ask_user_for_page_code_numbers()
temp_list_of_dataframes = list()
dataframe = pd.DataFrame()

for page_code in page_codes:
    temp_list_of_dataframes.append(load_chosen_pages(page_code))

dataframe = temp_list_of_dataframes.pop()
while (len(temp_list_of_dataframes) >= 1):
    temp_dataframe = temp_list_of_dataframes.pop()
    dataframe = pd.concat([dataframe, temp_dataframe], ignore_index=True)

dataframe_with_all_user_answers = answer_questions(dataframe)
print_right_answers(dataframe_with_all_user_answers)
