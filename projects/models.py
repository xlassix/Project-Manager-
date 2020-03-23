from django.db import models
from .manager import ProjectManager
# Create your models here.
class ProjectModel(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField('name', max_length=30,unique=True,null=False)
    description= models.CharField('description', max_length=400,null=False)
    completed = models.BooleanField("completed",default=False,)
    created = models.DateTimeField('created', auto_now_add=True)

    objects= ProjectManager()
    class Meta:
        db_table = u'Project'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ('created',)

class ActionModel(models.Model):
    project_id = models.ForeignKey(
        'ProjectModel',
        on_delete=models.CASCADE,
        null=False,
        related_name='Project',
    )
    description= models.CharField('description', max_length=400)
    note = models.CharField('description', max_length=400)
    created = models.DateTimeField('created', auto_now_add=True)

    class Meta:
        verbose_name = 'action'
        verbose_name_plural = 'actions'
        ordering = ('created',)



from rest_framework import serializers
class ActionSerializer(serializers.ModelSerializer):
    def update(self,b):
        pass
    def create(self, validated_data,project_id):
        ActionModel.objects.create(**validated_data)
        validated_data["project_id"]=project_id
        return validated_data
    class Meta:
        model = ActionModel
        fields = ['project_id',"description",'note']
        

class ProjectSerializer(serializers.ModelSerializer):
    def update(self,b):
        pass
    def create(self, validated_data):
        ProjectModel.objects.create(**validated_data)
        return validated_data
    class Meta:
        model = ProjectModel
        fields = ['name','description',"id","completed"]
