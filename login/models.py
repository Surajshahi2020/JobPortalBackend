from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100)
    image = models.FileField(null=True)
    mobile = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=15, null=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user}"


class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    slug = models.SlugField(max_length=100)
    gender = models.CharField(max_length=15, null=True)
    company = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=15, null=True)
    is_blocked = models.BooleanField(default=False)
    status = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return f"{self.user.username}"


class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    salary = models.FloatField(max_length=20)
    image = models.FileField(null=True)
    description = models.CharField(max_length=500)
    experience = models.CharField(max_length=50)
    location = models.CharField(max_length=20)
    skills = models.CharField(max_length=200)
    creationdate = models.DateField()
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.title}"


class Apply(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    resume = models.FileField(null=True)
    slug = models.SlugField(max_length=100)
    apply_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.id}--{self.slug}"


class Payment(models.Model):
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    apply_date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=5)
    pidx = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.id}"
