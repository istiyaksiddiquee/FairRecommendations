from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .services import RecommendationService
from .services import DatabaseResetService


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
        recommendation_service = RecommendationService()
        output = recommendation_service.get_all_users()
        return Response(output)


class Recommendation(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uuid', openapi.IN_QUERY,
                              "UUID of user", type=openapi.TYPE_STRING),
            openapi.Parameter('research_interest', openapi.IN_QUERY,
                              "Research Interest from predefined list of Research Interest", type=openapi.TYPE_STRING),
            openapi.Parameter('sim_weight', openapi.IN_QUERY,
                              "Preference indicative weight for cosine similarity", type=openapi.TYPE_STRING),
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              "Size of each page", type=openapi.TYPE_STRING),
            openapi.Parameter('page_number', openapi.IN_QUERY,
                              "Number of each page, starting from 0", type=openapi.TYPE_STRING),
        ], responses={
            200: openapi.Response(
                'Successful Response with bias and bias corrected list',
                output={'with_bias': '', 'bias_corrected': ''}
            ),
            400: openapi.Response(
                'Malformed URL Request'
            ),
        },
        tags=[
            'Recommendation'
        ]
    )
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

        recommendation_service = RecommendationService()
        output = recommendation_service.get_recommendation(
            req_uuid, req_research_interest, req_sim_weight, req_page_size, req_page_number)
        return Response(output)


class DatabaseReset(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('person_json', openapi.IN_QUERY,
                              "name of person json file", type=openapi.TYPE_STRING),
            openapi.Parameter('similarity_json', openapi.IN_QUERY,
                              "name of similarity json file", type=openapi.TYPE_STRING),
            openapi.Parameter('pickle_file_name', openapi.IN_QUERY,
                              "name of database pickle file", type=openapi.TYPE_STRING),
        ], responses={
            200: openapi.Response(
                'Successful!'
            ),
            400: openapi.Response(
                'Malformed Request'
            ),
        },
        tags=[
            'Database'
        ]
    )
    def get(self, request, format=None):
        req_person = request.GET['person_json']
        req_similarity = request.GET['similarity_json']
        req_pickle_file_name = request.GET['pickle_file_name']

        if (req_person == None
        or len(req_person) == 0
        or req_similarity == None
        or len(req_similarity) == 0
        or req_pickle_file_name == None 
        or len(req_pickle_file_name) == 0):
            return Response("Malformed Request", status=status.HTTP_400_BAD_REQUEST)

        # call to neo4j code to recreate these json files
        # with the corresponding name
        # neosvc = Neo4jSVC()
        # req_person, req_similarity = neosvc.populate_json(req_person, req_similarity)

        db_rest_svc = DatabaseResetService()
        return_code = db_rest_svc.recreate_db(req_person, req_similarity, req_pickle_file_name)

        if return_code != 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        return Response("Success")
