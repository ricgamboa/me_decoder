# This module must be replaced with secure communication between the local me_decoder server and the client,
# the client is the system that only knows the original question, the id of the user, and the encrypted answer, and
# request the decryption of the answer

import flask
import json
from flask import request, jsonify

import me_decoder


def main():
    # Server confguration
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/new_answer/', methods=["GET", "POST"])
    def add_new_answer():
        # Receive the answer from the user POST and save
        if request.method == "POST":
            answer = request.get_json()
            me_decoder.save_answer(answer)
            return "answer saved"
        return "Error"

    @app.route('/new_question/', methods=["GET", "POST"])
    def add_new_question():
        # Receive new question and save
        if request.method == "POST":
            new_question = request.get_json()
            question = me_decoder.convert_to_question(new_question)
            question.save_info()
            return "question saved"
        return "Error"

    @app.route('/solve_answer/', methods=["GET"])
    def solve_answer():
        # Decrypt the the answer received from the specified user an question
        question_global_id = request.args.get("question")
        user_global_id = request.args.get("user")
        plain_answer = me_decoder.decode(question_global_id, user_global_id)
        return jsonify(plain_answer)

    app.run(port=8080)


if __name__ == "__main__":
    main()
