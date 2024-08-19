from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST
PYTHON_QUESTION_LIST = [
    {
        'question_text': 'What is the output of 2 + 2 in Python?',
        'acceptable_answers': ['4', 'four'],
        'correct_answer': '4'
    },
    {
        'question_text': 'Which keyword is used to define a function in Python?',
        'acceptable_answers': ['def'],
        'correct_answer': 'def'
    },
    {
        'question_text': 'What data structure does a Python list resemble?',
        'acceptable_answers': ['array', 'dynamic array'],
        'correct_answer': 'array'
    },
    {
        'question_text': 'How do you start a comment in Python?',
        'acceptable_answers': ['#', 'hash'],
        'correct_answer': '#'
    },
    {
        'question_text': 'What is the correct file extension for Python files?',
        'acceptable_answers': ['.py'],
        'correct_answer': '.py'
    }
]
def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
      '''
    if current_question_id is None:
        return False, "No current question to answer."

    # Get the current question from the list using the ID
    current_question = PYTHON_QUESTION_LIST[current_question_id]

    # Normalize and validate the answer
    normalized_answer = answer.strip().lower()
    if normalized_answer not in current_question['acceptable_answers']:
        return False, f"Invalid answer: {answer}"

    # Store the answer in the session
    if "user_answers" not in session:
        session["user_answers"] = []
    
    session["user_answers"].append(normalized_answer)
   

   
    return True, ""


def get_next_question(current_question_id):
    
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    # Check if there is a next question
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]
        return next_question['question_text'], next_question_id
    else:
        return None, None  # No more questions

    
def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    user_answers = session.get("user_answers", [])
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    # Calculate the number of correct answers
    for i, user_answer in enumerate(user_answers):
        correct_answer = PYTHON_QUESTION_LIST[i]['correct_answer']
        if user_answer == correct_answer.lower():
            correct_answers += 1

    score = (correct_answers / total_questions) * 100
    return f'You completed the quiz! You scored {correct_answers} out of {total_questions}. Your score is {score:.2f}%.'
    

   
