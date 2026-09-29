from flask import Flask, request
import random
app = Flask(__name__)

EXERCISES = [
    {"file": "2/000", "answer": "3"},
    {"file": "3/000", "answer": "4"},
]
CALL_EXERCISES = {}
def choose_exercise():
    return random.choice(EXERCISES)

@app.route("/")
def home():
    return "Forest School Phone is running"


@app.route("/exercise1")
def exercise1():
    answer = request.args.get("answer", "")
    call_id = request.args.get("ApiCallId", "")
    
    # Первый вход: проиграть вопрос и получить одну цифру
    if not answer:
        exercise = choose_exercise()
        CALL_EXERCISES[call_id] = exercise
        return f"read=f-/{exercise['file']}=answer,,1,1,7,No,yes,no,,,,,,InsertLettersTypeChangeNo,no"
        # Правильный ответ: 2 + 1 = 3
    exercise = CALL_EXERCISES.get(call_id)
    if not exercise:
        return "go_to_folder=/2"
    if answer == exercise["answer"]:
        return "id_list_message=t-נכון&go_to_folder=/2"
    # Неправильный ответ: попробовать ещё раз
    return f"id_list_message=t-נסה שוב&read=f-/{exercise['file']}=answer,,1,1,7,No,yes,no,,,,,,InsertLettersTypeChangeNo,no"
