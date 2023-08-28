from flask import Flask, render_template, redirect, request, session
from surveys import Survey, Question

app = Flask(__name__)
app.secret_key="secretKey"
responses = []

survey = Survey("What do software engineers think?", "Through a series of questions we shall find out!",
                [
                    Question("Did the software engineer break the code again?"),
                    Question("Is the programmer's favorite dance move the 'Boolean Shuffle'?"),
                    Question("Did the developer try turning it off and on before calling for help?"),
                    Question("Is debugging the process of removing all traces of bugs or just the will to live?")
                ])

@app.route("/survey")
def home():
    session['current_page'] = -1
    survey_title = survey.title 
    survey_instructions = survey.instructions
    return render_template("survey.html", survey_title=survey_title, survey_instructions=survey_instructions)

@app.route("/submit", methods=["POST"])
def submit():
    response = request.form.get("btn")
    if response:
        responses.append(response)
    session['current_page'] = session['current_page'] + 1
    if session['current_page'] >= len(survey.questions):
        session['complete'] = True
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{session['current_page']}")

@app.route("/questions/<int:question_index>")
def question(question_index):
    if question_index >= len(survey.questions):
        return redirect("/thanks")
    current_question = survey.questions[question_index]
    return render_template('question.html', question=current_question.question)

@app.route("/questions/1")
def question1():
    return render_template('question.html', question=survey.questions[1].question)

@app.route("/questions/2")
def question2():
    return render_template('question.html', question=survey.questions[2].question)

@app.route("/questions/3")
def question3():
    return render_template('question.html', question=survey.questions[3].question)

@app.route("/thanks")
def thanks():
    return f"""<h1>Thank you for participating!</h1>
              <h2>Here are the results!</h2>
              <p>{responses}</p> 
        """
        