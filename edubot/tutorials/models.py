"""Models for the tutorials app."""
import uuid
from django.db import models

class Lesson(models.Model):
    """A lesson is a single unit of instruction."""
    title = models.CharField(max_length=200,default="title", null=False)
    content_type = models.CharField(max_length=200, choices=(
        ('text', 'Text'),
        ('video','Video'),
        ('document', 'Document'),
        ('quiz', 'Quiz'),
        ('audio', 'Audio'),
        ('image', 'Image'),
    ),
    default='text'
    )
    date_published = models.DateTimeField(auto_now_add=True)
    tutorial_class = models.ForeignKey(
        'Tutorial',
        on_delete=models.CASCADE,
        related_name='tutorial_class',
        null=True
    )
    instructions = models.TextField(default="Instruction", null=False)
    file = models.FileField(upload_to='lessons/', null=True, blank=True)

    def __str__(self):
        """Unicode representation of Lesson."""
        return f"{self.title}"

    @classmethod
    def lesson_exists(cls, tutorial, title):
        """Check if the lesson exists."""
        #pylint: disable=no-member
        return cls.objects.filter(tutorial_class=tutorial, title=title).exists()

class Tutorial(models.Model):
    """A tutorial is a collection of lessons."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    published_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    date_published = models.DateTimeField("date published", auto_now_add=True)
    published = models.BooleanField(default=False)
    steps = models.ManyToManyField('Lesson')
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        """Unicode representation of Tutorial."""
        return f"{self.title}"

class CallRequest(models.Model):
    """A call request is a request for a call."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    date_of_call = models.DateTimeField()
    agenda = models.TextField(default="Agenda", null=False)
    status = models.CharField(
        max_length=200,
        choices=(
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('completed', 'Completed'),
        ),
        default='pending'
    )
    call_link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        """Unicode representation of CallRequest."""
        return f"{self.requested_by} - {self.course} - {self.date_of_call} - {self.status}"

    @classmethod
    def call_request_exists(cls, user, course, date_of_call):
        """Check if the call request exists."""
        #pylint: disable=no-member
        return cls.objects.filter(requested_by=user, course=course, date_of_call__date=date_of_call, status='pending').exists()



class Conversation(models.Model):
    """A conversation is a collection of messages."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    has_unread = models.BooleanField(default=False)
    messages = models.ManyToManyField('Message')
    

    def __str__(self):
        """Unicode representation of Conversation."""
        return f"{self.user} - {self.course}"

    
    def get_messages(self):
        """Get all the messages in a conversation."""
        # pylint: disable=no-member
        return self.messages.all()
    
    def post_message(self, sender, content):
        """Post a message to a conversation."""
        # pylint: disable=no-member
        message = Message.objects.create(sender=sender, content=content)
        self.messages.add(message)
        self.has_unread = True
        return message
    

class Message(models.Model):
    """A message is a single message in a conversation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        """Unicode representation of Message."""
        return f"{self.sender} - {self.content}"