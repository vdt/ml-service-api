from django.db import models

Organization
Data about the organization that is using this
Location info
Size
Billing details
Premium service subscriptions (if any)
User
Foreign key to organization
Data about a user in the organization
Currently teacher or student

EssaySet
Data about a set of essays
Maximum allowed score
Number of additional targets (rubric score points, etc)
Number of additional numeric predictors (if any)
Prompt
Premium additional feedback models to use (ie thesis, coherence, etc)
Foreign key to organization

Essay
Foreign key to EssaySet
Foreign key to a User
Text of the essay
Additional numeric predictors (if any)
Train – boolean indicating whether this is a training essay or a test essay

EssayGrade
Foreign key to Essay
Contains the grade assigned to the essay
The type of grader
Any feedback the grader had
Scores on additional targets specified (if any)
Scores on premium feedback models (if any)
Foreign key to a user (if teacher graded)

class UserRoles():
    student = "student"
    teacher = "teacher"
    administrator = "administrator"

class EssayTypes():
    test = "test"
    train = "train"

class GraderTypes():
    machine = "ML"
    instructor = "IN"
    peer = "PE"

class Organization(models.Model):
    #TODO: Add in address info, etc later on
    organization_size = models.IntegerField(default=0)
    organization_name = models.TextField()
    #TODO: Add in billing details, etc later, along with rules on when to ask
    premium_service_subscriptions = models.TextField()

class UserProfile(models.Model):
    #TODO: Add in a callback where if user identifies as "administrator", then they can create an organization
    user = models.ForeignKey(User, unique=True, blank=True,null=True)
    organization = models.ForeignKey(Organization)
    #Add in userinfo here.  Location, etc
    name = models.TextField()
    role = models.CharField(max_length=20)

class Course(models.Model):
    #A user can have many courses, and a course can have many users
    users = models.ManyToManyField(UserProfile)
    course_name = models.TextField()

class Problem(models.Model):
    course = models.ForeignKey(Course)
    #Max scores for one or many targets
    max_target_scores = model.TextField()
    number_of_additional_predictors = models.IntegerField()
    prompt = models.TextField()
    #If org has subscriptions to premium feedback models
    premium_feedback_models = models.TextField()

class Essay(models.Model):
    #Each essay is written for a specific problem
    problem = models.ForeignKey(Problem)
    #Each essay is written by a specified user
    user = models.ForeignKey(UserProfile)
    #Each user writes text (their essay)
    essay_text = models.TextField()
    #Schools may wish to send additional predictors (student grade level, etc)
    additional_predictors = models.TextField()
    #The type of essay
    essay_type = models.CharField(max_length=20)

class EssayGrade(models.Model):
    #Each essaygrade is for a specific essay
    essay = models.ForeignKey(Essay)
    #How the essay was scored for numerous targets
    target_scores = models.TextField()
    #What type of grader graded it
    grader_type = models.CharField(max_length=20)
    #Feedback from the grader
    feedback = models.TextField()
    #Annotated text from the grader
    annotated_text = models.TextField()
    #Scores on premium feedback model, if any
    premium_feedback_scores = models.TextField()
    #whether or not the grader succeeded
    success = models.BooleanField()
    #For peer grading and staff grading, we will use this
    user = models.ForeignKey(UserProfile,blank=True,null=True)







