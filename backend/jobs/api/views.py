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
def home(request):
        user_type = request.session.get('user_type')
        print('user',user_type)
        if user_type == 'admin':
            if request.method == 'POST':
                 data = json.loads(request.body)
                 text = data.get('text')
                 job_collection.insert_one({'user_type': 'admin', 'text': text})
                 return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'failed'})
        return JsonResponse({'status': 'failed', 'reason': 'Unauthorized'})
        
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