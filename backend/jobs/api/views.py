from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId


# Create your views here.
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['job-portal']
info_collection = db['info']
job_collection = db['jobs']

@csrf_exempt
def register_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user_type = 'admin'

        info_collection.insert_one({'username': username, 'password': password, 'user_type': user_type})
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user_type = 'user'

        info_collection.insert_one({'username': username, 'password': password, 'user_type': user_type})
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})

@csrf_exempt
def login_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = info_collection.find_one({'username': username, 'password': password, 'user_type': 'admin'})
        if user:
            request.session['user_type'] = user['user_type']
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failed', 'reason': 'Invalid credentials'})

    return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = info_collection.find_one({'username': username, 'password': password, 'user_type': 'user'})
        if user:
            request.session['user_type'] = user['user_type']
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failed', 'reason': 'Invalid credentials'})

    return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})



@csrf_exempt
def post_job(request):
    """
    API to post a new job to the MongoDB collection.
    """
    if request.method == "POST":
        try:
            # Parse the request body
            body = json.loads(request.body.decode("utf-8"))
            job = {
                "id": job_collection.count_documents({}) + 1,  # Auto-generate ID
                "Job title": body.get("title"),
                "company": body.get("company"),
                "location": body.get("location"),
                "qualification": body.get("qualification"),
                # "applicants": body.get("applicants", 0),  # Defaults to 0 if not provided
                "job_description": body.get("job_description"),
                "required_skills_and_qualifications": body.get("required_skills_and_qualifications"),
                "salary_range": body.get("salary_range"),
                }

            # Insert the job into the collection
            job_collection.insert_one(job)

            return JsonResponse({"status": "success", "message": "Job posted successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
    

@csrf_exempt
def get_jobs(request):
    """
    API to get all jobs from the MongoDB collection.
    """
    if request.method == "GET":
        try:
            # Fetch all jobs from the collection
            jobs = list(job_collection.find({}))

            if not jobs:
                return JsonResponse({"status": "success", "message": "No jobs uploaded."}, status=200)

            # Convert ObjectId to string for each job
            for job in jobs:
                job["_id"] = str(job["_id"])
                job["job_title"] = job.pop("Job title")

            return JsonResponse({"status": "success", "jobs": jobs}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
    
@csrf_exempt
def fetch_jobs(request):
    """
    API to get all jobs from the MongoDB collection.
    """
    if request.method == "GET":
        try:
            # Fetch all jobs from the collection
            jobs = list(job_collection.find({}))

            if not jobs:
                return JsonResponse({"status": "success", "message": "No jobs uploaded."}, status=200)

            # Convert ObjectId to string for each job
            for job in jobs:
                job["_id"] = str(job["_id"])
                job["job_title"] = job.pop("Job title")

            return JsonResponse({"status": "success", "jobs": jobs}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
    

        
@csrf_exempt
def user(request):
    user_type = request.session.get('user_type')
    print('user', user_type)
    if user_type == 'user':
        if request.method == 'GET':
            text_id = request.GET.get('text_id')  # Ensure text_id is passed as a query parameter
            text = job_collection.find_one({'_id': ObjectId(text_id)})
            if text:
                text['_id'] = str(text['_id'])  # Convert ObjectId to string
                return JsonResponse({'status': 'success', 'text': text})
            return JsonResponse({'status': 'failed', 'reason': 'Text not found'})
        return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})