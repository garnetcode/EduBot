"""Quiz service."""
import json
from django.core.cache import cache


class QuizService:
    """Quiz service."""

    def __init__(self):
        """Initialize the service."""
        self.cache = cache

    def get_quiz(self, quiz_id):
        """Get quiz from cache."""
        return json.loads(self.cache.get(quiz_id))

    def get_quizzes(self):
        """Get all quizzes from cache."""
        return [json.loads(quiz) for quiz in self.cache.get_many(self.cache.keys('*'))]

    def save_quiz(self, quiz):
        """Save quiz to cache."""
        self.cache.set(quiz['id'], json.dumps(quiz))

    def delete_quiz(self, quiz_id):
        """Delete quiz from cache."""
        self.cache.delete(quiz_id)

    def delete_quizzes(self):
        """Delete all quizzes from cache."""
        self.cache.clear()