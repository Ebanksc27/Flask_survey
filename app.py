from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

# Initialize response list 
responses = []

@app.route('/')
def show_survey_start():
    from surveys import satisfaction_survey
    return render_template('start.html', survey=satisfaction_survey)

# Route to handle questions 
@app.route('/questions/<int:question_id>')
def show_question(question_id):
    from surveys import satisfaction_survey

    # Redirect to correct page if out-of-order question is accessed
    if question_id != len(responses):
        # Show flash message about what's going wrong
        flash("You're trying to access an invalid question.")
        return redirect(f"/questions/{len(responses)}")

    # Redirect to thank you page if all questions have been answered
    if question_id == len(satisfaction_survey.questions):
        return redirect("/thanks")

    # Normal case: retrieve and display the question
    question = satisfaction_survey.questions[question_id]
    return render_template('question.html', question_num=question_id, question=question)


@app.route('/answer', methods=['POST'])
def handle_answer():
    from surveys import satisfaction_survey

    # Get the answer from the form data
    answer = request.form['choice']

    # Append the answer to the responses list
    responses.append(answer)

    # Check if we've finished the survey
    if len(responses) == len(satisfaction_survey.questions):
        # The user has answered all questions - say thanks and end the survey
        return render_template('thanks.html')
    else:
        # Redirect to the next question
        next_question = len(responses)
        return redirect(f'/questions/{next_question}')

