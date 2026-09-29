from flask import Flask, request

app = Flask(__name__)

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
