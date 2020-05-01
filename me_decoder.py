# Main program used to request the decryption of the answer
# This module must run in a secure environment since it uses private user information

from pathlib import Path
import json
import sqlite3

import me_components


class QuestionDB(me_components.Question):
    # Add method to save the question information in the database
    # Must be replaced with a secure connection to database
    def save_info(self):
        icons_json = json.dumps([icons.collection for icons in self.icons_set])
        pos_list_json = json.dumps([pos_list.list for pos_list in self.pos_list_set])

        # Open database
        config_file_path = Path.cwd().joinpath("config_file")
        with open(config_file_path, "r") as config:
            config_info = json.load(config)
        database_path = Path(config_info["DECODER_DATABASE_PATH"])
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Verify tables exists or create
        cursor.executescript("CREATE TABLE IF NOT EXISTS question("
                                 "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"
                                 "global_question_id INTEGER UNIQUE,"
                                 "num_letters INTEGER,"
                                 "icons TEXT,"
                                 "positions TEXT);")
        # Save values to database
        cursor.execute("INSERT OR IGNORE INTO question (global_question_id,num_letters,icons,positions) VALUES (?, ?, ?, ?)",
                       (self.id, self.num_answer_letters, icons_json, pos_list_json))

        connection.commit()
        cursor.close()


def translate(encryp_answer, alph_index_list, alphabet, letters):
    # translate the answer with the known alphabets
    plain_answer = []
    count = 0
    for symbol in encryp_answer:
        alph_index = alph_index_list[count]
        letter_index = alphabet[alph_index].index(symbol)
        plain_answer.append(letters[letter_index])
        count += 1
    return plain_answer


def get_user(required_id):
    # Find user in database and convert to User class
    # This method must be replaced with secure communication with database. Manages very secret information

    sender_id = 0
    sender_name = ''
    sender_icons = []
    sender_cell = 0
    user_found = False

    config_file_path = Path.cwd().joinpath("config_file")
    with open(config_file_path, "r") as config:
        config_info = json.load(config)
    database_path = Path(config_info["USERS_DATABASE_PATH"])
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE global_user_id=?", (required_id,))
    user_tuple = cursor.fetchone()
    connection.commit()
    cursor.close()
    if user_tuple is None:
        print("User not found")

    user = me_components.Sender(0, '')
    user.id = user_tuple[1]
    user.name = user_tuple[2]
    user.icons = json.loads(user_tuple[3])
    user.cell = user_tuple[4]
    return user


def find_alphabet(question, user, alphabet_size):
    # Find the icon used for each letter
    # and the index of the alphabets used for each letter

    icons_used = []
    alph_used = []
    for num_letter in range(question.num_answer_letters):
        icons_used.append(user.find_icon(question.pos_list_set[num_letter].list))
        alph_used.append(
            question.icons_set[num_letter].find_group(icons_used[num_letter], alphabet_size))
    return alph_used


def save_answer(answer):
    # Save answer to database

    config_file_path = Path.cwd().joinpath("config_file")
    with open(config_file_path, "r") as config:
        config_info = json.load(config)
    database_path = Path(config_info["DECODER_DATABASE_PATH"])
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS answer("
                     "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"
                     "user_id INTEGER NOT NULL,"
                     "answer_coded TEXT,"
                     "question_id INTEGER NOT NULL,"
                      "UNIQUE (user_id, question_id))")
    cursor.execute("INSERT OR REPLACE INTO answer (user_id,answer_coded,question_id) VALUES (?,?,?)",
                   (answer["user_id"], json.dumps(answer["answer"]), answer["question_id"]))
    connection.commit()
    cursor.close()


def find_answer(question_id, user_id):
    # Find answer in database and convert to list

    config_file_path = Path.cwd().joinpath("config_file")
    with open(config_file_path, "r") as config:
        config_info = json.load(config)
    database_path = Path(config_info["DECODER_DATABASE_PATH"])
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT answer_coded FROM answer WHERE question_id=? AND user_id=?", (question_id, user_id))
    answer_str = cursor.fetchone()
    connection.commit()
    cursor.close()
    answer = json.loads(answer_str[0])
    return answer


def convert_to_question(question_dic):
    # Convert dictionary to question

    question = QuestionDB(0, 0)
    question.id = question_dic["question_id"]
    question.num_answer_letters = question_dic["number_letters"]
    for ic_li in question_dic["icons_lists"]:
        question.append_icon_set(ic_li)
    for pos_li in question_dic["positions_lists"]:
        question.append_position_list(pos_li)
    return question


def find_question(question_id):
    # Find question in database and convert to class QuestionDB

    config_file_path = Path.cwd().joinpath("config_file")
    with open(config_file_path, "r") as config:
        config_info = json.load(config)
    database_path = Path(config_info["DECODER_DATABASE_PATH"])
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM question WHERE global_question_id=?", (question_id, ))
    question_tuple = cursor.fetchone()
    connection.commit()
    cursor.close()
    question_dic = {"question_id": question_tuple[1], "number_letters": question_tuple[2],
                "icons_lists": json.loads(question_tuple[3]), "positions_lists": json.loads(question_tuple[4])}
    question = convert_to_question(question_dic)
    return question


def decode(question_id, user_id):
    # Receive the information from the server and return the answer decoced

    config_info_path = Path.cwd().joinpath("config_file")
    with open(config_info_path) as config:
        config_info = json.load(config)
        alphabet_size = config_info["ALPHABET_SIZE"]

    # Get the private user information
    user = get_user(user_id)

    # Read the public alphabet
    alphabet_path = Path.cwd().joinpath("public_alphabet")
    with open(alphabet_path) as alphabet:
        public_alphabet = json.load(alphabet)

    # Find the alphabet to use
    question = find_question(question_id)
    alph_use = find_alphabet(question, user, alphabet_size)

    # Decrypt the answer an send the answer decrypted
    answer = find_answer(question_id, user_id)
    plain_answer = translate(answer, alph_use, public_alphabet["alphabets"], public_alphabet["letters"])

    return plain_answer
