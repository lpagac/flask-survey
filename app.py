from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def show_start():
    """ Shows survey home page for user to select 'start' """

    return render_template('survey_start.html', title=survey.title,
                           instructions=survey.instructions)


@app.route('/begin', methods=["POST"])
def start_survey():
    """ Redirects to first question page  """

    responses.clear()
    
    return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:question_num>')
def show_question(question_num):
    """ Display question page to user """

    curr_question = survey.questions[question_num].question
    curr_choices = survey.questions[question_num].choices
    return render_template('question.html', question=curr_question,
                           choices=curr_choices)


@app.route('/answer', methods=["POST"])
def grab_answer():
    """ Grabs answer from form for question and adds to response list
        Redirects to next question """

    curr_answer = request.form["answer"]
    responses.append(curr_answer)

    if len(responses) == len(survey.questions):
        return redirect('/thankyou')

    return redirect(f"/questions/{len(responses)}")


@app.route('/thankyou')
def show_thankyou():
    """ Display completion page with thank you """

    return render_template('completion.html')