from django.db import models
from django.contrib.auth.models import User
from django.utils.text import wrap
from django.utils.timezone import now

# Helper functions to set be able to set User object as a foreignkey, could be removed when exiting debug state
def user_sentinel():
    return User.objects.get_or_create(username="Default user", password="Default_password")[0]

def user_pk_sentinel():
    return user_sentinel().pk

def reference_sentinel():
    return Reference.objects.get_or_create(description="Example description of reference", url="www.example.com")[0]

# Create your models here.
class Assessment(models.Model):
    name = models.CharField(max_length=40)# Name of the assessment
    organisation = models.CharField(max_length=50)# Name of the organisation performing the assessment
    complete_status = models.BooleanField(default=False)# Complete when all questions have been answered 
    date_last_saved = models.DateField(auto_now=True)# Automatically saves new value when this object is saved
    ultimately_responsible = models.CharField(max_length=50, default="")# The person who is responsible in the end for the assessment
    # User that created the assessment, TODO: rename field to author
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=user_pk_sentinel)
    # Many-to-many field to create user groups
    # With this field we track each user that can edit the assessment
    user_group = models.ManyToManyField(User, related_name="related_assessment")


# IMPORTANT NOTE: questions in the context of this project are both phase introductions
# and the questions themselves. They are seperated by the question_number attributes 
# a question_number = 0 means a phase introductions and otherwise it's a question.
# This is done for convenience in the view rendering both questions and phases.
class Question(models.Model):
    # Create subclass that acts as an enum
    class Jobs():
        _jobs = {
            "DA": "Data scientist",
            "BE": "Bestuur",
            "OG": "Opdracht gever",
            "PL": "Project leider",
            "DE": "Domein expert",
            "PB": "Panel van burgers",
            "VB": "Vertegenwoordiger belangengroep",
            "CISO": "CISO of CIO",
            "CA": "Communicatie adviseur",
            "DB": "Databeheerder of bronhouder",
            "FG": "Functionaris Gegevensbescherming",
            "HR": "HR-Medewerker",
            "JR": "Jurist",
            "OA": "Ontwikkelaar algoritme",
            "OP": "Overige leden projectteam",
            "SE": "Strategisch adviseur ethiek",
        }  

        def __init__(self, job_type, priority) -> None:
            # Priority 1 is highest and 2 or other is lower 
            self.priority = priority
            try:
                self.description = self._jobs[job_type]
            except KeyError:
                raise KeyError("Job type: " + job_type + ", loaded from fixture not recognized!")

    question_title = models.CharField(max_length=140, default="Question title")
    question_text = models.TextField()# Actual question as found in IAMA
    question_context = models.TextField(default="")# Context to question_text
    question_instruction = models.TextField(default="")# Instructions on how to answer the question
    question_phase = models.IntegerField() # Phase number of the question
    question_number = models.DecimalField(max_digits=2, decimal_places=1) # Question number in the phase
    question_warning = models.CharField(max_length=140, default=None, null=True)# Warning that tells when an answer results in question
    question_reference_text = models.CharField(max_length=400, default=None, null=True)# Text that indicates how to utulize the refernces
    job_list = models.JSONField(default=list)# All jobs associated with the question

    # Return the json object as a list of Jobs objects for easier conversion 
    def jobs_as_py_list(self):
        return [self.Jobs(job["type"], job["priority"]) for job in self.job_list]
    
class Answer(models.Model):
    class Status(models.TextChoices):
        RV = "RV", "reviewed"
        AW = "AW", "answered"
        UA = "UA", "unanswered"
    
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.UA)# Whether it's correctly filled in or not
    answer_content = models.TextField(default="") # Content of the answer

    # Attributes to identify the corresponding answer
    assessment_id = models.ForeignKey(Assessment, on_delete=models.CASCADE, default=0)# Related assessment
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, default=0) # Related question
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=user_pk_sentinel)# User that answers

    # For tracking answer history
    created = models.DateTimeField(auto_now_add=True, blank=True)


# Could also have a relation to Assessment, but would be redundant info since the answer is already related
# Don't know what is best practice here, so could be revisited later.
class Collaborator(models.Model):
    name = models.CharField(max_length=60)
    discipline = models.CharField(max_length=40, default="Geen baanbeschrijving")
    organisation = models.CharField(max_length=60)

    # Many to many field as answer can have multiply collaborators and vice versa
    answers = models.ManyToManyField(Answer)

class Reference(models.Model):
    title = models.CharField(max_length=64, default="Example title")
    description = models.TextField()
    url = models.URLField(max_length=128)
    questions = models.ManyToManyField(Question)

class LawCluster(models.Model):
    description = models.TextField()
    cluster_name = models.CharField(max_length=100, default="Default cluster")
    subclusters = models.JSONField(null=True)


