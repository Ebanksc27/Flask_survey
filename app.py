from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

# Initialize response list 
responses = []

@app.route('/', methods=['GET', 'POST'])
def show_survey_start():
    from surveys import satisfaction_survey
    # if form submitted, clear responses from session 
    if request.method == 'POST':
        session['responses'] = []
        return redirect('/questions/0')
    return render_template('start.html', survey=satisfaction_survey)

# Route to handle questions 
@app.route('/questions/<int:question_id>') 
def show_question(question_id):
    from surveys import satisfaction_survey
    responses = session.get('responses')

    if responses is None:
        # trying to access question too soon, redirecting to start page
        return redirect('/')
    
    if len(responses) == len(satisfaction_survey.questions):
        # All questions have been answered, redirect to thank you page
        return redirect('/thanks')

    if len(responses) != question_id:
        # Trying to access questions out of order.
        flash("Invalid question id attempted.")
        return redirect(f'/questions/{len(responses)}')
    
    question = satisfaction_survey.questions[question_id]
    return render_template('question.html', question_num=question_id, question=question)


@app.route('/answer', methods=['POST'])
def handle_answer():
    # Get the answer from the form data
    answer = request.form['choice']
    # Append the answer to the responses list
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    # Redirect to the next question
    next_question = len(responses)
    from surveys import satisfaction_survey
    if next_question == len(satisfaction_survey.questions):
        return redirect('/thanks')
    else:
        return redirect(f'/questions/{next_question}')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

