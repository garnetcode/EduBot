"""Quiz service."""
from django.core.cache import cache
# pylint: disable = no-name-in-module
# pylint: disable = import-error
# pylint: disable = import-self
from quiz.models import Quiz
from users.models import User


class QuizService:
    """Quiz service."""

    def __init__(self, session):
        """Initialize the service."""
        self.phone_number = session['phone_number']
        self.selected_answer = session['selected_answer']
        #pylint: disable = no-member
        self.quiz = Quiz.objects.get(id=session['quiz_id'])
        self.quiz_session = None

        if not cache.get(self.phone_number):
            #pylint: disable = no-member
            self.quiz = Quiz.objects.get(id=session['quiz_id'])
            self.quiz_session = {
                'quiz_id': self.quiz.id,
            }
            self.save_quiz_session()
        else:
            self.quiz_session = self.get_quiz_session()
        print("#######################", self.quiz_session)

    def get_quiz_session(self):
        """Get quiz session from cache."""
        sess = cache.get(f"{self.phone_number}_quiz_session")
        if sess:
            #pylint: disable = no-member
            self.quiz = Quiz.objects.get(id=sess['quiz_id'])
        else:
            sess = {
                'quiz_id': self.quiz.id,
            }
            self.save_quiz_session()
        return sess

    def save_quiz_session(self):
        """Save quiz session to cache."""
        cache.set(f"{self.phone_number}_quiz_session", self.quiz_session, 60 * 60 * 24)
        return

    def deliver_quiz(self):
        """Deliver quiz to user."""
        questions = self.quiz.get_questions()
        if self.quiz_session.get('count'):
            count = self.quiz_session['count']
            print("#######################, UPDATE COUNT", count)
        else:
            count = 0
        
        if count > 0:
            user = User.objects.get(phone_number=self.phone_number)
            self.quiz.answer_question(user, questions[count-1], self.selected_answer)
        

        if count < len(questions):
            question = questions[count]
            self.quiz_session['count'] = count + 1
            self.save_quiz_session()
            if question.file:

                return {
                    "is_valid": True,
                    "data": [],
                    "requires_controls": True,
                    "is_first_step": False,
                    "is_last_step": False if count < len(questions) - 1 else True,
                    "type": "quiz",
                    "message": {
                        "response_type": "image",
                        "image": "https://bow-space.com/media/files/quizz/4.png",#question.file.url if question.file else None,
                        "text": f"*Question* \n\n{question.question}\n\n*A*. {question.choice_1}\n\n*B*. {question.choice_2}n\n*C*. {question.choice_3}n\n*D*. {question.choice_4}",
                        "answer": question.answer,
                    }
                }
            else:
                return {
                    "is_valid": True,
                    "data": [],
                    "type": "quiz",
                    "requires_controls": True,
                    "is_first_step": False,
                    "is_last_step": False if count < len(questions) - 1 else True,
                    "message": {
                        "response_type": "text",
                        "text": f"*Question* \n\n{question.question}\n\n*A*. {question.choice_1}\n\n*B*. {question.choice_2}\n\n*C*. {question.choice_3}\n\n*D*. {question.choice_4}",
                        "answer": question.answer,
                    }
                }

        else:
            cache.delete(f"{self.phone_number}_quiz_session")
            return {
                "is_valid": True,
                "data": [],
                "requires_controls": False,
                "is_first_step": False,
                "is_last_step": False,
                "message": {
                    "menu": "course_menu",
                    "exclude_back": True,
                    "response_type": "button",
                    "text": "You have completed the quiz. Thank you.",
                }
                
            }
    