from flask import Flask, render_template, redirect, request, session, flash
from surveys import Survey, Question

app = Flask(__name__)
app.secret_key = "secretKey"
responses = []
survey = Survey(
    "What do software engineers think?",
    "Through a series of questions we shall find out!",
    [
        Question("Did the software engineer break the code again?"),
        Question("Is the programmer's favorite dance move the 'Boolean Shuffle'?"),
        Question(
            "Did the developer try turning it off and on before calling for help?"
        ),
        Question(
            "Is debugging the process of removing all traces of bugs or just the will to live?"
        ),
    ],
)
question_completion = {i: False for i in range(len(survey.questions))}


@app.route("/survey")
def home():
    session["current_page"] = -1
    session["responses"] = []
    survey_title = survey.title
    survey_instructions = survey.instructions
    return render_template(
        "survey.html",
        survey_title=survey_title,
        survey_instructions=survey_instructions,
    )


@app.route("/submit", methods=["POST"])
def submit():
    response = request.form.get("btn")
    if response:
        responses = session["responses"]
        responses.append(response)
        session["responses"] = responses
        # Mark the current question as completed
        question_completion[session["current_page"]] = True

    session["current_page"] = session["current_page"] + 1
    if session["current_page"] >= len(survey.questions):
        session["complete"] = True
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{session['current_page']}")


@app.route("/questions/<int:question_index>")
def question(question_index):
    if question_index >= len(survey.questions):
        session["complete"] = True
        return redirect("/thanks")

    if question_index > session["current_page"]:
        flash(
            "You're on the wrong question page. Redirecting to the earliest unanswered question."
        )
        earliest_unanswered = next(
            (i for i, answered in question_completion.items() if not answered), 0
        )
        return redirect(f"/questions/{earliest_unanswered}")

    current_question = survey.questions[question_index]
    return render_template("question.html", question=current_question.question)


@app.route("/thanks")
def thanks():
    results = session["responses"]
    return render_template("thanks.html", results=results)
