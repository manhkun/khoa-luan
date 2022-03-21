from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import JobSerializer
from .models import Job
from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET'])
def getAllJobs(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    serializer = JobSerializer(job, many=False)
    
    return Response(serializer.data)

@api_view(['POST'])
def newJob(request):
    data = request.data
    job = Job.objects.create(**data)
    serializer = JobSerializer(job, many=False)
    
    return Response(serializer.data)

@api_view(['PUT'])
def updateJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    
    job.title = request.data['title']
    job.description = request.data['description']
    job.email = request.data['email']
    job.address = request.data['address']
    job.jobType = request.data['jobType']
    job.education = request.data['education']
    job.industry = request.data['industry']
    job.experience = request.data['experience']
    job.point = request.data['point']
    job.position = request.data['position']
    job.company = request.data['company']
    job.save()
    
    serializer = JobSerializer(job, many=False)
    
    return Response(serializer.data)
