# This module must be replaced with communication between the local me_decoder server and the client,
# the client is the system that only knows the original question, the id of the user, and the encrypted answer, and
# request the decryption of the answer

from pathlib import Path
import me_question_db
import json

class ClientCommunicator():

    def __init__(self):
        self.question = me_question_db.QuestionDB(0, 0)
        self.answer = []
        self.senderid = 0

    def wait_for_request(self):
        input("Press enter to send the request...")

    def receive_request_info(self):
        # This method must be replaced to receive information
        # from the client

        # Receive info from client side
        test_client_info_path = Path.cwd().joinpath("project_files", "test_client_info")
        # Convert info and save to object
        with open(test_client_info_path, "rt") as client_info:
            received_info = json.load(client_info)
        self.question.id = received_info["question_info"]["question_id"]
        self.question.num_answer_letters = received_info["question_info"]["number_letters"]
        for ic_li in received_info["question_info"]["icons_lists"]:
            self.question.append_icon_set(ic_li)
        for pos_li in received_info["question_info"]["positions_lists"]:
            self.question.append_position_list(pos_li)
        self.senderid = received_info["answer_info"]["user_id"]
        self.answer = received_info["answer_info"]["answer"]

    def send_answer(self, answer):
        # This method must be replaced to send answer to the client
        letters = ["a", "b", "c", "d"]
        print("Answer decrypted is:")
        for answer_letter in answer:
            int(answer_letter)
            print(" {} ".format(letters[answer_letter]), end='')
