from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
import datetime


# Create your views here.
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sutgJxLaXWo7gKMR:sutgJxLaXWo7gKMR@cluster0.2ytii.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['job-portal']
info_collection = db['info']
job_collection = db['jobs']
company_collection = db['companies']  

@csrf_exempt
def register_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
  
        company_info = {
            'name': data.get('companyName'),
            'description': data.get('companyDescription'),
            'website': data.get('companyWebsite'),
            'address': data.get('companyAddress'),
            'hiring_manager': {
                'name': data.get('hiringManagerName'),
                'email': data.get('email'),
                'phone': data.get('phone')
            },
            'created_at': datetime.datetime.utcnow()
        }
        
        email = data.get('email')
        password = data.get('password')

  
        existing_user = info_collection.find_one({'email': email})
        if existing_user:
            return JsonResponse({'status': 'failed', 'message': 'Email already registered'})

     
        company_result = company_collection.insert_one(company_info)
        company_id = company_result.inserted_id

        
        admin_info = {
            'email': email,
            'password': password,
            'role': 'admin',
            'company_id': str(company_id),  
            'created_at': datetime.datetime.utcnow()
        }
        
        info_collection.insert_one(admin_info)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')
        role = data.get('role', 'user')

        existing_user = info_collection.find_one({'email': email})
        if existing_user:
            return JsonResponse({'status': 'failed', 'message': 'Email already registered'})

        # Insert new user
        info_collection.insert_one({
            'name': name,
            'email': email,
            'mobile': mobile,
            'password': password,
            'role': role
        })
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})

@csrf_exempt
def login_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = info_collection.find_one({
            'email': email, 
            'password': password, 
            'role': 'admin'
        })
        if user:
            company = company_collection.find_one({'_id': ObjectId(user['company_id'])})
            if company:
                company['_id'] = str(company['_id']) 
                return JsonResponse({
                    'status': 'success',
                    'user': {
                        'email': user.get('email'),
                        'role': user.get('role'),
                        'company': company
                    }
                })
        return JsonResponse({'status': 'failed', 'reason': 'Invalid credentials'})

    return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = info_collection.find_one({
            'email': email, 
            'password': password, 
            'role': 'user'
        })
        if user:
            return JsonResponse({
                'status': 'success',
                'user': {
                    'name': user.get('name'),
                    'email': user.get('email'),
                    'role': user.get('role')
                }
            })
        return JsonResponse({'status': 'failed', 'reason': 'Invalid credentials'})

    return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})



@csrf_exempt
def post_job(request):
    """
    API to post a new job to the MongoDB collection.
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            job = {
                "id": job_collection.count_documents({}) + 1,  
                "Job title": body.get("title"),
                "company": body.get("company"),
                "location": body.get("location"),
                "qualification": body.get("qualification"),
                
                "job_description": body.get("job_description"),
                "required_skills_and_qualifications": body.get("required_skills_and_qualifications"),
                "salary_range": body.get("salary_range"),
                }

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
            jobs = list(job_collection.find({}))

            if not jobs:
                return JsonResponse({"status": "success", "message": "No jobs uploaded."}, status=200)

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
            jobs = list(job_collection.find({}))

            if not jobs:
                return JsonResponse({"status": "success", "message": "No jobs uploaded."}, status=200)

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
            text_id = request.GET.get('text_id')  
            text = job_collection.find_one({'_id': ObjectId(text_id)})
            if text:
                text['_id'] = str(text['_id'])  
                return JsonResponse({'status': 'success', 'text': text})
            return JsonResponse({'status': 'failed', 'reason': 'Text not found'})
        return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})

@csrf_exempt
def get_company_details(request, company_id):
    """
    API to get company details by company ID
    """
    if request.method == "GET":
        try:
            company = company_collection.find_one({'_id': ObjectId(company_id)})
            if company:
                company['_id'] = str(company['_id'])
                return JsonResponse({
                    'status': 'success',
                    'company': company
                })
            return JsonResponse({
                'status': 'failed',
                'message': 'Company not found'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    return JsonResponse({
        'status': 'failed',
        'reason': 'Invalid request method'
    })

@csrf_exempt
def update_company_details(request, company_id):
    """
    API to update company details
    """
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            update_data = {
                'name': data.get('companyName'),
                'description': data.get('companyDescription'),
                'website': data.get('companyWebsite'),
                'address': data.get('companyAddress'),
                'hiring_manager': {
                    'name': data.get('hiringManagerName'),
                    'email': data.get('email'),
                    'phone': data.get('phone')
                },
                'updated_at': datetime.datetime.utcnow()
            }
            
            result = company_collection.update_one(
                {'_id': ObjectId(company_id)},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Company details updated successfully'
                })
            return JsonResponse({
                'status': 'failed',
                'message': 'Company not found or no changes made'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    return JsonResponse({
        'status': 'failed',
        'reason': 'Invalid request method'
    })