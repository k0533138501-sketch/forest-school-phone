from flask import Flask, request
import random
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
SUBTRACTION_ANSWERS = {
    "0": "3",
    "1": "3",
    "2": "4",
    "3": "4",
    "4": "5",
    "5": "5",
    "6": "6",
    "7": "6",
    "8": "7",
    "9": "8",
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
    
    
def run_exercises(correct_answers, audio_folder, answer, next_folder=None):
    call_id = request.args.get("ApiCallId", "") + audio_folder
    saved = CALL_EXERCISES.get(call_id)

    if saved is None:
        exercise = random.randint(0, len(correct_answers) - 1)
        saved = {
            "exercise": exercise,
            "correct_answer": correct_answers[str(exercise)],
            "total": 0,
            "first_try_correct": 0,
            "had_error": False
        }
        CALL_EXERCISES[call_id] = saved

    exercise = saved["exercise"]
    correct_answer = saved["correct_answer"]

    if not answer:
        return f"read=f-{audio_folder}/{exercise:03d}=answer,,1,1,7,No,yes,no,,,,,,InsertLettersTypeChangeNo,no"

    if answer == correct_answer:
        saved["total"] += 1
        if not saved["had_error"]:
            saved["first_try_correct"] += 1
        if saved["total"] >= 10:
            result = saved["first_try_correct"]
            CALL_EXERCISES.pop(call_id, None)
            if next_folder:
                return f"id_list_message=t-ענית על עשר שאלות.t-ענית נכון בפעם הראשונה על.n-{result}.t-שאלות&go_to_folder={next_folder}"
            return f"id_list_message=t-ענית על עשר שאלות.t-ענית נכון בפעם הראשונה על.n-{result}.t-שאלות&"
        exercise = random.randint(0, len(correct_answers) - 1)
        saved["exercise"] = exercise
        saved["correct_answer"] = correct_answers[str(exercise)]
        saved["had_error"] = False
        return f"id_list_message=t-נכון&go_to_folder={audio_folder}"
    saved["had_error"] = True
    return f"id_list_message=t-נסה שוב&go_to_folder={audio_folder}"
    
@app.route("/level1_test")
def level1_test():
    answer = request.args.get("answer", "")
    return run_exercises(CORRECT_ANSWERS, "/4", answer, next_folder="/6")
@app.route("/level2_test")
def level2_test():
    answer = request.args.get("answer", "")
    #return run_exercises(SUBTRACTION_ANSWERS, "/6", answer)
    return run_exercises(CORRECT_ANSWERS, "/4", answer)
