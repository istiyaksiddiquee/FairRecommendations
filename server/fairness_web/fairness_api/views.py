from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import RecommendationService

# Create your views here.
class HelloApiView(APIView):
    """ Testing REST API """

    def get(self, request, format=None):
        return Response({'message': 'Hello'})

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

class DemoForH5(APIView):

    def get(self, request, format=None):

        req_uuid = request.GET['uuid']
        req_research_interest = request.GET['research_interest']
        req_sim_weight = request.GET['sim_weight']

        if req_uuid == None or len(req_uuid) == 0 or req_research_interest == None or len(req_research_interest) == 0:
            return Response().status_code(400)

        recommendation_service = RecommendationService('h5/output.h5')
        output = recommendation_service.get_recommendation(req_uuid, req_research_interest, req_sim_weight)
        return Response(output)
