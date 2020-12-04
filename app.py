from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSE_STORAGE_KEY = 'responses'

@app.route('/')
def show_start():
    """ Shows survey home page for user to select 'start' """

    return render_template('survey_start.html', survey=survey)


@app.route('/begin', methods=["POST"])
def start_survey():
    """ Redirects to first question page  """

    session[RESPONSE_STORAGE_KEY] = []

    # session["start_key"] = True

    return redirect('/questions/0')


@app.route('/questions/<int:question_num>')
def show_question(question_num):
    """ Display question page to user """

    responses = session.get(RESPONSE_STORAGE_KEY)

    if responses is None:
        flash("Please start survey!")
        return redirect('/')

    if len(responses) == len(survey.questions):
        flash("You're done!")
        return redirect('/thankyou')

    if question_num != len(responses):
        flash("Invalid question!")
        return redirect(f"/questions/{len(responses)}")

    curr_question = survey.questions[question_num]

    return render_template('question.html', question=curr_question)


@app.route('/answer', methods=["POST"])
def grab_answer():
    """ Grabs answer from form for question and adds to response list
        Redirects to next question """

    curr_answer = request.form["answer"]
    responses = session[RESPONSE_STORAGE_KEY]
    responses.append(curr_answer)
    session['reponses'] = responses

    if len(responses) == len(survey.questions):
        return redirect('/thankyou')

    return redirect(f"/questions/{len(responses)}")


@app.route('/thankyou')
def show_thankyou():
    """ Display completion page with thank you """

    session.pop(RESPONSE_STORAGE_KEY)

    return render_template('completion.html')
