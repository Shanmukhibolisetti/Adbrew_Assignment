from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json, logging, os
from bson.objectid import ObjectId
from pymongo import MongoClient

mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
db = MongoClient(mongo_uri)['test_db']
collection = db['todo_collection']

class TodoListView(APIView):

    def get(self, request):
        # Implement this method - return all todo items from db instance above.
        tasks = list(collection.find())
        for task in tasks:
            task['_id'] = str(task['_id']) 
        return Response(tasks, status=status.HTTP_200_OK)
        
    def post(self, request):
        # Implement this method - accept a todo item in a mongo collection, persist it using db instance above.
        task = request.data.get("task", "")
        if not task:
            return Response({"error": "Task field is required."}, status=status.HTTP_400_BAD_REQUEST)
        collection.insert_one({"task": task})

        return Response({"message": "Task added successfully."}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, todo_id):
        try:
            result = collection.delete_one({"_id": ObjectId(todo_id)})
            if result.deleted_count == 0:
                return Response({"error": "Task not found."}, status=404)

            return Response({"message": "Task deleted successfully."}, status=200)

        except:
            return Response({"error": "Invalid task ID"}, status=400)

