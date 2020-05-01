# Module to include the option to save question in database
# Must be replaced with a secure connection to database

import sqlite3
import json
from pathlib import Path

from me_components import Question


class QuestionDB(Question):
    # Add method to save the question information in the database
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
                       (self.id, self.num_answer_letters,icons_json,pos_list_json))

        connection.commit()
        cursor.close()
