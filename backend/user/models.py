from django.db import models
import json

# Create your models here.
class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=100)
    CreateDate = models.DateTimeField(auto_now_add=True)
    isActive=models.BooleanField(default=False)
    zhibi=models.IntegerField(default=0)
    own_photos=models.TextField(default=json.dumps([0] * 30))

    def set_array_element(self, index, value):
        # 确保索引在有效范围内  
        if 0 <= index < 30:  
            photos_data = json.loads(self.own_photos)  
            photos_data[index] = value  
            self.own_photos = json.dumps(photos_data)  
            self.save()  
    
    def get_array_element(self, index):  
        # 确保索引在有效范围内  
        if 0 <= index < 30:  
            photos_data = json.loads(self.own_photos)  
            return photos_data[index]  
        return -1
    
    #获取当前正在使用的头像编号(默认为0，1是已购买，2是正在使用)
    def get_used_element(self):
        photos_data = json.loads(self.own_photos)
        for i in range(0,30):
            if(photos_data[i]==2): return i
        return -1

class Survey(models.Model):
    SurveyID = models.AutoField(primary_key=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')
    Title = models.CharField(max_length=200)
    Description = models.TextField(max_length=500, blank=True)
    Is_released = models.BooleanField(default=False)
    Is_open = models.BooleanField(default=True)
    Is_deleted=models.BooleanField(default=False)

    PublishDate = models.DateTimeField()
    #0 是普通问卷，1是投票问卷，2是报名问卷，3是考试问卷
    Category = models.IntegerField(default=0)   
    TotalScore = models.IntegerField(null=True, blank=True)
    TimeLimit = models.IntegerField(null=True, blank=True)

class BaseQuestion(models.Model):
    QuestionID = models.AutoField(primary_key=True)
    Survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='%(class)s_questions')
    Text = models.TextField(max_length=500)
    IsRequired = models.BooleanField(default=True)
    Number = models.IntegerField()

    class Meta:
        abstract = True

class BlankQuestion(BaseQuestion):
    Score = models.IntegerField(null=True, blank=True)

class ChoiceQuestion(BaseQuestion):
    HasOtherOption = models.BooleanField(default=False)
    MaxSelectable = models.IntegerField(default=1)
    Score = models.IntegerField(null=True, blank=True)

class ChoiceOption(models.Model):
    OptionID = models.AutoField(primary_key=True)
    Question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name='choice_options')
    Text = models.CharField(max_length=200)
    IsCorrect = models.BooleanField(default=False)
    
class OtherOption(models.Model):
    IsRequired = models.BooleanField(default=True)
    Text = models.TextField(max_length=500)

class RatingQuestion(BaseQuestion):
    MinRating = models.IntegerField(default=1)
    MaxRating = models.IntegerField(default=5)
    
class RatingOption(models.Model):
    OptionID = models.AutoField(primary_key=True)
    Question = models.ForeignKey(RatingQuestion, on_delete=models.CASCADE, related_name='rating_options')
    Text = models.CharField(max_length=200)
    IsCorrect = models.BooleanField(default=False)

class Answer(models.Model):
    AnswerID = models.AutoField(primary_key=True)
    Submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='%(class)s_answers')

    class Meta:
        abstract = True

class BlankAnswer(Answer):
    Question = models.ForeignKey(BlankQuestion, on_delete=models.CASCADE)
    Content = models.TextField(max_length=500)
    GivenScore = models.IntegerField(null=True, blank=True)

class ChoiceAnswer(Answer):
    Question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    ChoiceOptions = models.ForeignKey(ChoiceOption, on_delete=models.CASCADE)

class RatingAnswer(Answer):
    Question = models.ForeignKey(RatingQuestion, on_delete=models.CASCADE)
    RatingOptions = models.ForeignKey(RatingOption, on_delete=models.CASCADE)

class Submission(models.Model):
    SubmissionID = models.AutoField(primary_key=True)
    Survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='submissions')
    Respondent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    SubmissionTime = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=20, choices=[('Unsubmitted', 'Unsubmitted'), ('Submitted', 'Submitted'), ('Graded', 'Graded'),('Deleted','Deleted')])
    Duration = models.DurationField(null=True, blank=True)

class SurveyStatistic(models.Model):
    StatisticID = models.AutoField(primary_key=True)
    Survey = models.OneToOneField(Survey, on_delete=models.CASCADE, related_name='statistics')
    TotalResponses = models.IntegerField(default=0)
    AverageScore = models.FloatField(null=True, blank=True)
    LastResponseDate = models.DateTimeField(null=True, blank=True)

class Template(models.Model):
    TemplateID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Type = models.CharField(max_length=50)
    DefaultQuestionsJSON = models.JSONField()
    Description = models.TextField(max_length=500, blank=True)

class RewardOffering(models.Model):
    RewardID = models.AutoField(primary_key=True)
    Survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='rewards')
    Description = models.TextField()
    TotalZhibi = models.IntegerField()
    AvailableQuota = models.IntegerField()

class UserRewardRecord(models.Model):
    RecordID = models.AutoField(primary_key=True)
    Respondent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reward_records')
    Survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='user_rewards')
    Zhibi = models.IntegerField()
    RedemptionDate = models.DateField()