from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import tables as pt 


# Create your views here.
class HelloApiView(APIView):
    """ Testing REST API """

    def get(self, request, format=None):
        return Response({'message': 'Hello'})


class PyTableTester(APIView):
    """ Testing PyTables """

    def get(self, request, format=None):
        h5file = pt.open_file('test.h5', 'w')
        return Response({'message': str(h5file.root)})


class ResearchInterest(APIView):
    """ Research Interest """

    def get(self, request, format=None):
        research_interest = [
            'History',
            'Religion',
            'Anthropology',
            'Ethnology',
            'Musicology',
            'Education',
            'Digital Education',
            'Digital Libraries',
            'Digital Humanities',
            'Political Sciences',
            'Gender Studies',
            'Cultural Studies',
            'Usability',
            'Project Management',
            'Information Retrieval',
            'Natural Language Processing',
            'Translation Science',
            'Data Science',
            'Legal Artificial Intelligence',
            'Artificial Intelligence',
            'Machine Learning',
            'Recommender Systems',
            'Knowledge Graphs'
        ]
        return Response({'research_interests': research_interest})