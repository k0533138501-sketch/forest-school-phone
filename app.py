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
MIXED_ANSWERS = {
    "0": "6",
    "1": "5",
    "2": "7",
    "3": "6",
    "4": "8",
    "5": "6",
    "6": "9",
    "7": "7",
    "8": "9",
    "9": "5",
}
MULTIPLICATION_2_ANSWERS = {
    "0": "2",
    "1": "4",
    "2": "6",
    "3": "8",
    "4": "10",
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
        return "id_list_message=t-נכון&go_to_folder=/7"

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
    
    
def run_exercises(correct_answers, audio_folder, answer):
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
            if audio_folder == "/4":
                return f"id_list_message=t-ענית על עשר שאלות.t-ענית נכון בפעם הראשונה על.n-{result}.t-שאלות&go_to_folder=/7"
            if audio_folder == "/6":
                return f"id_list_message=t-ענית על עשר שאלות.t-ענית נכון בפעם הראשונה על.n-{result}.t-שאלות&go_to_folder=/8"
            return f"id_list_message=f-/9/010.t-ענית על עשר שאלות.t-ענית נכון בפעם הראשונה על.n-{result}.t-שאלות&go_to_folder=/10"
                
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
    return run_exercises(CORRECT_ANSWERS, "/4", answer)
@app.route("/level2_test")
def level2_test():
    answer = request.args.get("answer", "")
    return run_exercises(SUBTRACTION_ANSWERS, "/6", answer)
@app.route("/mixed_test")
def mixed_test():
    answer = request.args.get("answer", "")
    return run_exercises(MIXED_ANSWERS, "/9", answer)
@app.route("/fable_transition")
def fable_transition():
    return "id_list_message=f-/8/000&go_to_folder=/9" 
@app.route("/second_fable")
def second_fable():
    return "id_list_message=f-/10/000&go_to_folder=/11"
@app.route("/multiplication_test")
def multiplication_test():
    answer = request.args.get("answer", "")
    call_id = request.args.get("ApiCallId", "") + "/11"

    saved = CALL_EXERCISES.get(call_id)

    if saved is None:
        saved = {
            "stage": 0,
            "index": 0,
            "order": list(range(5)),
            "had_error": False,
            "first_try_correct": 0
        }
        CALL_EXERCISES[call_id] = saved

    exercise = saved["order"][saved["index"]]
    correct = MULTIPLICATION_2_ANSWERS[str(exercise)]

    if not answer:
        return (
            f"read=f-/11/{exercise:03d}=answer,,2,1,7,"
            "No,yes,no,,,,,,InsertLettersTypeChangeNo,no"
        )

    if answer != correct:
        saved["had_error"] = True
        return "id_list_message=t-נסה שוב&go_to_folder=/11"

    if not saved["had_error"]:
        saved["first_try_correct"] += 1

    saved["had_error"] = False
    saved["index"] += 1

    if saved["index"] == 5:
        saved["stage"] += 1
        saved["index"] = 0

        if saved["stage"] == 1:
            return (
                "id_list_message=t-נכון.t-מצוין. "
                "עכשיו נחזור על אותם התרגילים עוד פעם"
                "&go_to_folder=/11"
            )

        if saved["stage"] == 2:
            saved["order"] = random.sample(range(5), 5)
            return (
                "id_list_message=t-נכון.t-ועכשיו ננסה בלי סדר"
                "&go_to_folder=/11"
            )

        result = saved["first_try_correct"]
        CALL_EXERCISES.pop(call_id, None)
        return (
            "id_list_message=f-/9/010."
            "t-כל הכבוד. סיימת חמישה עשר תרגילים."
            f"t-ענית נכון בפעם הראשונה על.n-{result}.t-תרגילים"
        )

    return "id_list_message=t-נכון&go_to_folder=/11"
@app.route("/transition")
def transition():
    return "id_list_message=f-/7/000&go_to_folder=/6" 
@app.route("/story1")
def story1():
    return "id_list_message=f-/1/000&go_to_folder=/4"
