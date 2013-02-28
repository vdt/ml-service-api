from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from tastypie.models import create_api_key
import json
from django.db.models.signals import pre_delete

class UserRoles():
    student = "student"
    teacher = "teacher"
    administrator = "administrator"
    grader = "grader"

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
    organization_name = models.TextField(default="")
    #TODO: Add in billing details, etc later, along with rules on when to ask
    premium_service_subscriptions = models.TextField(default=json.dumps([]))

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    #TODO: Add in a callback where if user identifies as "administrator", then they can create an organization
    user = models.ForeignKey(User, unique=True, blank=True,null=True)
    #TODO: Potentially support users being in multiple orgs, but will be complicated
    organization = models.ManyToManyField(Organization, blank=True,null=True)
    #Add in userinfo here.  Location, etc
    name = models.TextField(blank=True,null=True)
    #User role in their organization
    role = models.CharField(max_length=20,blank=True,null=True)

    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

class Course(models.Model):
    #A user can have many courses, and a course can have many users
    users = models.ManyToManyField(User)
    organization = models.ManyToManyField(Organization)
    #Each course has a name!
    course_name = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Problem(models.Model):
    #A course has many problems, and a problem can be used in many courses
    courses = models.ManyToManyField(Course)
    #Max scores for one or many targets
    max_target_scores = models.TextField(default=json.dumps([1]))
    #If additional numeric predictors are being sent, the count of them
    number_of_additional_predictors = models.IntegerField(default=0)
    #Prompt of the problem
    prompt = models.TextField(default="")
    #If org has subscriptions to premium feedback models
    premium_feedback_models = models.TextField(default=json.dumps([]))
    name = models.TextField(default="")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Essay(models.Model):
    #Each essay is written for a specific problem
    problem = models.ForeignKey(Problem)
    #Each essay is written by a specified user
    user = models.ForeignKey(User, null=True)
    #Each user writes text (their essay)
    essay_text = models.TextField()
    #Schools may wish to send additional predictors (student grade level, etc)
    additional_predictors = models.TextField(default=json.dumps([]))
    #The type of essay (train or test)  see EssayTypes class
    essay_type = models.CharField(max_length=20)
    has_been_ml_graded = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_instructor_scored(self):
        return self.essaygrade_set.filter(grader_type=GraderTypes.instructor).order_by("-modified")[:1]

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
    annotated_text = models.TextField(default="")
    #Scores on premium feedback model, if any
    premium_feedback_scores = models.TextField(default=json.dumps([]))
    #whether or not the grader succeeded
    success = models.BooleanField()
    #For peer grading and staff grading, we will use this
    user = models.ForeignKey(User,blank=True,null=True)
    #Confidence value from the grader
    confidence = models.DecimalField(max_digits=10,decimal_places=9, default=1)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Group(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    class Meta:
        abstract = True

class StudentGroup(Group):
    pass

class TeacherGroup(Group):
    pass

class AdministratorGroup(Group):
    pass

class GraderGroup(Group):
    pass

USER_ROLE_MAPPINGS = {
    UserRoles.student : StudentGroup,
    UserRoles.teacher : TeacherGroup,
    UserRoles.administrator : AdministratorGroup,
    UserRoles.grader : GraderTypes,
    }

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

def pre_delete_problem(sender, instance, **kwargs):
    essays = Essay.objects.filter(problem=instance)
    essays.delete()

def pre_delete_essay(sender, instance, **kwargs):
    essay_grades = EssayGrade.objects.filter(essay=instance)
    essay_grades.delete()

def pre_delete_essaygrade(sender,instance, **kwargs):
    """
    Ensures that an ML model will be retrained if an old ML scored grade is removed for some reason
    """
    essay = instance.essay
    ml_graded_count = essay.essaygrade_set.filter(grader_type=GraderTypes.machine).count()
    if ml_graded_count<=1:
        essay.has_been_ml_graded=False
        essay.save()

def pre_delete_user(sender,instance,**kwargs):
    user_profile = user.profile
    essays = user.essay_set.all()
    essay_grades = user.essaygrade_set.all()
    user_profile.delete()
    essays.update(user=None)
    essay_grades.update(user=None)

def create_permission_group(sender,instance, **kwargs):
    try:
        role_group = USER_ROLE_MAPPINGS[instance.role]
    except:
        role_group = StudentGroup

    role_group = role_group(
        userprofile = instance,
    )
    role_group.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(create_api_key, sender=User)
post_save.connect(create_permission_group,sender=UserProfile)

pre_delete.connect(pre_delete_problem,sender=Problem)
pre_delete.connect(pre_delete_essay,sender=Essay)
pre_delete.connect(pre_delete_essaygrade,sender=EssayGrade)
pre_delete.connect(pre_delete_user, sender=User)

User.profile = property(lambda u: u.get_profile())










