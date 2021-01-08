from django.db import models

# Create your models here.

class CompanyModelDtls(models.Model):
    symbol = models.CharField(max_length=100)
    company_name = models.CharField(max_length=250)
    country = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100,null= True)
    model_summary = models.TextField(null=True)
    is_trained = models.BooleanField(default= False)
    trained_on = models.DateTimeField(null=True)
    file_path = models.CharField(max_length=100, null= True)
    model_loss = models.CharField(max_length=100, null= True)
    model_optimizer = models.CharField(max_length=100, null= True)
    epoch = models.IntegerField(null= True)
    batch_size = models.IntegerField(null= True)
    days = models.IntegerField(null= True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class CompanyModelDtlsHstry(models.Model):
    company = models.ForeignKey(CompanyModelDtls, on_delete=models.CASCADE)
    model_loss = models.CharField(max_length=100, null= True)
    model_optimizer = models.CharField(max_length=100, null= True)
    epoch = models.IntegerField(null= True)
    batch_size = models.IntegerField(null= True)
    days = models.IntegerField(null= True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model_optimizer