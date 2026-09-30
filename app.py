from flask import Flask, request

app = Flask(__name__)
CALL_EXERCISES = {}
CORRECT_ANSWERS = {
    "0": "3",
    "1": "4",
    "2": "2",
    "3": "4",
    "4": "5",
    "5": "5",
    "6": "5",
    "7": "5",
    "8": "6",
    "9": "6",
}
@app.route("/")
def home():
    return "Forest School Phone is running"

@app.route("/exercise1")
def exercise1():
    answer = request.args.get("answer", "")

    # Первый вход: проиграть вопрос и получить одну цифру
    if not answer:
        return "read=f-/2/000=answer,,1,1,7,No,yes,no,,,,,,InsertLettersTypeChangeNo,no"

    # Правильный ответ: 2 + 1 = 3
    if answer == "3":
        return "id_list_message=t-נכון&go_to_folder=/3"

    # Неправильный ответ: попробовать ещё раз
    return "id_list_message=t-נסה שוב&go_to_folder=/2"
    
@app.route("/test_params")
def test_params():
    return str(dict(request.args))
@app.route("/check_test")
def check_test():
    exercise = request.args.get("exercise", "")
    answer = request.args.get("answer", "")

    correct_answers = {
        "0": "3",
        "1": "4",
        "2": "2",
        "3": "4",
        "4": "5",
        "5": "5",
        "6": "5",
        "7": "5",
        "8": "6",
        "9": "6",
    }

    if exercise in correct_answers and answer == correct_answers[exercise]:
        return "CORRECT"

    return "WRONG"
@app.route("/random_test")
def random_test():
    import random

    exercise = random.randint(0, 9)
    return str(exercise)
@app.route("/combined_test")
def combined_test():
    print("YEMOT ARGS:", dict(request.args), flush=True)
    import random
    call_id = request.args.get("ApiCallId", "")
    answer = request.args.get("answer", "")
    if not answer:
        exercise = random.randint(0, 9)
        CALL_EXERCISES[call_id] = exercise
    else:
        exercise = CALL_EXERCISES.get(call_id)
        if exercise is not None and answer == CORRECT_ANSWERS[str(exercise)]:
            return "id_list_message=t-נכון&go_to_folder=/4"
        return "id_list_message=t-נסה שוב&go_to_folder=/5"
    filename = f"{exercise:03d}"

    return f"read=f-/4/{filename}=answer,,1,1,7,No,yes,no,,,,,,InsertLettersTypeChangeNo,no"
@app.route("/combined_check")
def combined_check():
    return str(dict(request.args))
@app.route("/retry_test")
def retry_test():
    call_id = request.args.get("ApiCallId", "")
    answer = request.args.get("answer", "")
    exercise = CALL_EXERCISES.get(call_id)
    if answer:
        if exercise is not None and answer == CORRECT_ANSWERS[str(exercise)]:
            return "id_list_message=t-נכון&go_to_folder=/4"
        return "id_list_message=t-נסה שוב&go_to_folder=/5"
    filename = f"{exercise:03d}"
    return f"read=f-/4/{filename}=answer,,1,1,7,No,yes,no,,,,,,InsertLettersTypeChangeNo,no"
    
    

