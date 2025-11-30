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
        try:
            tasks = list(collection.find())
            for task in tasks:
                task['_id'] = str(task['_id']) 
            return Response(tasks, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"Error fetching tasks: {e}")
            return Response({"error": "Failed to fetch tasks."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        # Implement this method - accept a todo item in a mongo collection, persist it using db instance above.
        try:
            task = request.data.get("task", "")
            if not task:
                return Response({"error": "Task field is required."}, status=status.HTTP_400_BAD_REQUEST)
            collection.insert_one({"task": task})

            return Response({"message": "Task added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(f"Error adding task: {e}")
            return Response({"error": "Failed to add task."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, todo_id):
        try:
            result = collection.delete_one({"_id": ObjectId(todo_id)})
            if result.deleted_count == 0:
                return Response({"error": "Task not found."}, status=404)

            return Response({"message": "Task deleted successfully."}, status=200)

        except Exception as e:
            logging.error(f"Error deleting task: {e}")
            return Response({"error": "Failed to delete task."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

