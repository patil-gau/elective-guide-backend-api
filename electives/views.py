from re import A
from students.models import Students
from typing import Generic
from .models import ElectiveFaculty, ElectiveSemester,Electives, RecommanderQuestions
from rest_framework import generics
from .serializers import ElectiveListSerializer,FacultyAllocatedElective,ElectiveInfoSerializer,ElectiveSelectedSerializer,ElectiveChoosenPrioritySerializer, RecommanderQuestionsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Electives,ElectiveStudent,ElectiveDetails,ElectiveSelected,ElectiveChoosenPriority
from rest_framework.response import Response
from rest_framework import status
import cloudinary.uploader as uploader
from rest_framework.parsers import MultiPartParser, JSONParser ,FormParser,FileUploadParser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import sklearn
from sklearn.linear_model import LinearRegression
from elective_recommander.settings import STATIC_URL,BASE_DIR



class ElectivesListView(generics.ListAPIView):
    queryset = Electives.objects.all()
    serializer_class = ElectiveListSerializer
    # permission_classes = [IsAuthenticated]

class ElectivesEnrolled(APIView):
    def post(self, request):
        student_id = request.data['user_id']
        
        try:
            elective_student = ElectiveStudent.objects.get(student_id=student_id)
            elective_id = elective_student.elective_id
            serializer = ElectiveListSerializer(elective_id)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            error = "something went wrong"
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
class UploadElectiveInfo(APIView):
    #   permission_classes = [IsAuthenticated]

      parser_classes = (
        MultiPartParser,
        JSONParser,
        FormParser,
        FileUploadParser
      )
      def post(self, request):
          serializer = ElectiveInfoSerializer(data=request.data)
          if serializer.is_valid():
              serializer.save()
              return Response("success",status=status.HTTP_200_OK)
          else:
               print("invalid serializer")
               return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
                      

class FacultyAssignedToElective(APIView):
    def post(self, request):
        try:
           queryset=ElectiveFaculty.objects.filter(faculty_id=request.data['faculty_id'])
           print(queryset)
           serializer = FacultyAllocatedElective(queryset,many=True)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
        

class ElectiveDetailsRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ElectiveDetails.objects.all()
    serializer_class = ElectiveInfoSerializer


class ElectiveSelectedListCreateAPIView(generics.ListCreateAPIView):
    queryset = ElectiveSelected.objects.all()
    serializer_class = ElectiveSelectedSerializer


class ElectiveReport(generics.RetrieveAPIView):
    queryset = ElectiveDetails.objects.all()
    serializer_class = ElectiveInfoSerializer

class ElectiveDetailedReport(APIView):
    def post(self, request):
        print(request.data)
        elective_id = request.data['elective_id']
        cgpa = float(request.data['cgpa'])
        result = {}
        dataset = BASE_DIR + STATIC_URL + 'JR_dataset.csv'
        df = pd.read_csv(dataset)
        print(df)
        try:
            #get elective detail info
            electiveDetail=ElectiveDetails.objects.get(elective_id=elective_id)
            serializer = ElectiveInfoSerializer(electiveDetail)
            result = serializer.data

            #get faculty name of that elective
            elective_faculty = ElectiveFaculty.objects.get(elective_id=elective_id)
            result['faculty_name'] = elective_faculty.faculty_id.faculty_name
            print(result)
            #predict the marks
            #get elective name
            elective_name = result['elective_name']
            print(elective_name)

            data = df.loc[:,[elective_name,'cgpa']]
            Upper_OutlierLimit1 = data[elective_name].quantile(0.95)
            Lower_OutlierLimit1 = data[elective_name].quantile(0.05)
            data = data[(data[elective_name]<=Upper_OutlierLimit1)&(data[elective_name]>=Lower_OutlierLimit1)]
            Upper_OutlierLimit2 = data['cgpa']
            Lower_OutlierLimit2 = data['cgpa'].quantile(0.05)
            data = data[(data['cgpa']<=Upper_OutlierLimit2)&(data['cgpa']>=Lower_OutlierLimit2)]
            data = data.dropna()
            x = data['cgpa']
            y = data[elective_name]
            x, y = np.array(x).reshape(-1, 1), np.array(y)
            model = LinearRegression()
            model.fit(x, y)
            model = LinearRegression().fit(x, y)
            y_pred = model.predict(np.array(cgpa).reshape(-1,1))
            predicted_score = y_pred[0]

            result['predicted_score'] = predicted_score
            
            
            return Response(result)

        except Exception as e:
            print(e) 
            return Response(e) 


class ElectivesForParticularSemester(APIView):
    def get(self,request,pk):
        result = []
        elective_object = {}
        student=Students.objects.get(student_id=pk)
        semester_id = student.semester_id
        print(semester_id.semester_id)
        elective_semester=ElectiveSemester.objects.filter(semester_id=semester_id.semester_id)
        for elective in elective_semester:
            elective_object['elective_name'] = elective.elective_id.elective_name
            elective_object['elective_id'] = elective.elective_id.elective_id
            result.append(elective_object)
            elective_object = {}
        print(result)    
        return Response(result)              

class ElectivePriorityView(APIView):
    def post(self, request):
        for data in request.data:
            serializer = ElectiveChoosenPrioritySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
        return Response("success") 
       
class AllQuestionsView(APIView):
    def get(self,request,pk):
        student=Students.objects.get(student_id=pk)
        semester_id = student.semester_id
        print(semester_id.semester_id)
        questions=RecommanderQuestions.objects.filter(semester_id=semester_id.semester_id)
        serializer = RecommanderQuestionsSerializer(questions,many=True)
        return Response(serializer.data) 

class RecommandElective(APIView):
    def post(self, request):
        data = request.data
        for questionObj in data:
            answer = questionObj['answer']
            if(answer=="yes"):
                return Response({'status':1,"message":questionObj['elective']},status=status.HTTP_200_OK)

        return Response({'status':0,"message":"try answering  properly"},status=status.HTTP_200_OK)       
            


        

