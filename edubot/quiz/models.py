"""Models for the quiz app."""
from django.db import models

# Create your models here.
class Quiz(models.Model):
    """Model definition for Quiz."""
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField('Question', related_name='quizzes')
    results = models.ManyToManyField('Result', related_name='quizzes')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

    def get_questions_count(self):
        """Returns the number of questions in a quiz."""
        #pylint: disable=no-member
        return self.questions.count()

    def add_question(self, question):
        """Adds a question to a quiz."""
        #pylint: disable=no-member
        self.questions.add(question)

    def get_questions(self):
        """Returns all questions for a quiz."""
        #pylint: disable=no-member
        return self.questions.all()

    def get_results(self):
        """Returns all results for a quiz."""
        #pylint: disable=no-member
        return self.results.all()

class Question(models.Model):
    """Model definition for Question."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_questions')
    file = models.FileField(upload_to='quiz_files', blank=True, null=True)
    file_type = models.CharField(max_length=200, blank=True, null=True, choices=(
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ))
    question = models.TextField()
    choice_1 = models.CharField(max_length=200)
    choice_2 = models.CharField(max_length=200)
    choice_3 = models.CharField(max_length=200)
    choice_4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.question}"


class Result(models.Model):
    """Model definition for Result."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_results')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.quiz} - {self.score}"
