from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import RecommendationService


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


class User(APIView):

    def get(self, request, format=None):
        recommendation_service = RecommendationService('h5/output.h5')
        output = recommendation_service.get_all_users()
        return Response(output)


class Recommendation(APIView):

    def get(self, request, format=None):

        req_uuid = request.GET['uuid']
        req_research_interest = request.GET['research_interest']
        req_sim_weight = request.GET['sim_weight']
        req_page_size = request.GET['page_size']
        req_page_number = request.GET['page_number']

        if req_uuid == None or len(req_uuid) == 0 or req_research_interest == None or len(req_research_interest) == 0:
            return Response().status_code(400)
        if req_page_size != None and req_page_number != None: 
            if req_page_size.isnumeric() != True or req_page_number.isnumeric() != True:
                return Response().status_code(400)

        recommendation_service = RecommendationService('h5/output.h5')
        output = recommendation_service.get_recommendation(req_uuid, req_research_interest, req_sim_weight, req_page_size, req_page_number)
        return Response(output)
