from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def start_survey():
    """ Shows survey home page for user to select 'start' """

    return render_template('survey_start.html', title=survey.title,
                           instructions=survey.instructions)


@app.route('/begin', methods=["POST"])
def direct_to_question():
    """ Redirects to first question page  """

    return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<question_num>')
def show_question(question_num):
    """ Display question page to user """

    curr_question = survey.questions[len(responses)].question
    curr_choices = survey.questions[len(responses)].choices
    return render_template('question.html', question=curr_question,
                           choices=curr_choices)


@app.route('/answer', methods=["POST"])
def grab_answer():
    """ Grabs answer from form for question and adds to response list
        Redirects to next question """

    curr_answer = request.form["answer"]
    responses.append(curr_answer)

    if len(responses) == len(survey.questions):
        responses[:] = []
        return redirect('/thankyou')

    return redirect(f"/questions/{len(responses)}")


@app.route('/thankyou')
def show_thankyou():
    """ Display completion page with thank you """

    return render_template('completion.html')