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
            'Education',
            'History',
            'Digital education', 
            'Digital education, Cultural studies', 
            'Education,Digital education',
            'Education, Cultural studies', 
            'Education, Digital education', 
            'Political sciences',
            'Political sciences, Education', 
            'Cultural studies', 
            'Cultural studies,History,Religion',
            'Cultural studies,Digital libraries',
            'Humanities', 
            'Digital humanities',
            'History,Education', 
            'History, Political sciences', 
            'History, Cultural studies',
            'Eductaion,History', 
            'Information retrieval',
            'Information retrieval,Recommender systems',
            'Knowledge graphs',
            'Recommender systems, Information Retrieval', 
            'Information retrieval, Natural language processing',
            'Digital libraries, Education', 'Data science', 
            'Machine learning',
            'Recommender systems', 
            'Natural language processing',
            'User Modeling', 
            'User Modeling, Natural language processing',
            'Knowledge graphs, Machine learning',
            'User Modeling, Recommender systems',
            'Machine learning, Translation science',
            'User Modeling, Natural language processing, Recommender systems',
            'Recommender systems, Knowledge graphs',
            'Knowledge graphs, Natural language processing', 
            'Usability',
            'Information retrieval, Cultural studies',
            'Natural langauge processing',
            'Machine learning, Knowledge graphs',
            'Cultural studies, Information retrieval',
            'Knowledge graphs, Natural language processing, Information retrieval',
            'Translation science, Information retrieval',
            'Machine learning, Natural language processing',
            'Information retrieval, User Modeling',
            'Natural language processing, Information Retrieval',
            'Natural language processing, Information retrieval',
            'Digital libraries', 
            'Digital humanities, Digital education',
            'Digital education,Digital libraries', 
            'History, Education',
            'Environment, Political sciences', 
            'Environment', 'Religion',
            'Psychology', 
            'Education, Digital Education', 
            'Ethnology',
            'Political sciences,History', 
            'History,Cultural studies',
            'History,Political sciences.', 
            'Gender studies',
            'Religion, Education', 
            'Religion, Political sciences',
            'Religion, Cultural studies',
            'Virtual Reality',
            'Legal artificial intelligence', 'Recommender systems, Education'
            'Legal artificial intelligence, Information retrieval, Natural language processing',
        ]

        return Response({'research_interests': research_interest})


class User(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              "Size of each page", type=openapi.TYPE_STRING),
            openapi.Parameter('page_number', openapi.IN_QUERY,
                              "Number of each page, starting from 0", type=openapi.TYPE_STRING),
        ], responses={
            200: openapi.Response(
                'Successful Response with array of users'
            ),
            400: openapi.Response(
                'Malformed URL Request'
            ),
        },
        tags=[
            'Users'
        ]
    )
    def get(self, request, format=None):

        req_page_size = request.GET['page_size']
        req_page_number = request.GET['page_number']

        if req_page_size != None and req_page_number != None:
            if req_page_size.isnumeric() != True or req_page_number.isnumeric() != True:
                return Response().status_code(400)

        recommendation_service = RecommendationService()
        output = recommendation_service.get_all_users(req_page_number, req_page_size)
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
        output = recommendation_service.get_recommendation(req_uuid, req_research_interest, req_sim_weight, req_page_size, req_page_number)
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
