from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .services import RecommendationService
from .services import DatabaseResetService


class ResearchInterest(APIView):
    """ Methods related to obtaining research interests available in the system """

    @swagger_auto_schema(
        operation_summary="Returns a list of available Research Interests",
        operation_description="""This is a GET method that does not require any other parameter. Upon invocation, \
        it will returns a list of strings where each string represents a research \
            interest that is available and applicable in the system.""",
        manual_parameters=[
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, required=False,
                              description="Size of each page", type=openapi.TYPE_STRING),
            openapi.Parameter(name='page_number', in_=openapi.IN_QUERY, required=False,
                              description="Number of each page, starting from 0", type=openapi.TYPE_STRING),
        ], responses={
            200: openapi.Response(
                'Successful Response with array of users'
            ),
            400: openapi.Response(
                'Malformed URL Request'
            ),
        },
        tags=[
            'Listing Research Interests'
        ]
    )
    def get(self, request, format=None):
        
        research_interest = [
            'Anthropology',
            'Artificial Intelligence',
            'Climate Research',
            'Cultural Studies',
            'Data Science',
            'Digital Education',
            'Digital Humanities',
            'Digital Libraries',
			'Economics'
            'Education',
			'Environment',
            'Ethnology',
            'Gender Studies',
            'History',
            'Information retrieval', # TODO: change this to Retrieval with capital R
            'Knowledge Graphs',
            'Legal Artificial Intelligence',
            'Machine Learning',
            'Musicology',
            'Natural Language Processing',
			'Peace & Conflict Studies', 
            'Political Sciences',
            'Project Management',
            'Recommender Systems',
            'Religion',
            'Translation Science',
            'Usability'
        ]

        return Response({'research_interests': research_interest})


class User(APIView):

    @swagger_auto_schema(
        operation_summary="Returns a list of Users",
        operation_description="""This is a GET method that returns a list of Users. It can be used with or without the pagination parameters. \
            Please see method parameters for information regarding keys for pagination parameters.""",
        manual_parameters=[
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, required=False,
                              description="Size of each page", type=openapi.TYPE_STRING),
            openapi.Parameter(name='page_number', in_=openapi.IN_QUERY, required=False,
                              description="Number of each page, starting from 0", type=openapi.TYPE_STRING),
        ], responses={
            200: openapi.Response(
                'Successful Response with array of users'
            ),
            400: openapi.Response(
                'Malformed URL Request'
            ),
        },
        tags=[
            'Listing Available Users'
        ]
    )
    def get(self, request, format=None):

        req_page_size = request.GET['page_size']
        req_page_number = request.GET['page_number']

        if req_page_size != None and req_page_number != None:
            if req_page_size.isnumeric() != True or req_page_number.isnumeric() != True:
                return Response().status_code(400)
        else:
            req_page_size = 902
            req_page_number = 0

        recommendation_service = RecommendationService()
        output = recommendation_service.get_all_users(req_page_number, req_page_size)
        return Response(output)


class Recommendation(APIView):

    @swagger_auto_schema(
        operation_summary="Returns calculated Recommendations",
        operation_description="""This is a GET method that returns two lists of Recommendations. One of these list possess uncorrected, raw recommendation. \
        The other one presents a bias corrected version of the raw recommendation. They have a descriptive key that can be found in the responses section. \
        However, this method can be used in conjunction with the pagination parameter. Please see details on the parameters section. Furthermore, please note \
        that the uuid, research interest, and similarity weight paramteres are mandatory here.""",
        manual_parameters=[
            openapi.Parameter(name='uuid', in_=openapi.IN_QUERY, required=True,
                              description="UUID of user", type=openapi.TYPE_STRING),
            openapi.Parameter(name='research_interest', in_=openapi.IN_QUERY, required=True,
                              description="Research Interest from predefined list of Research Interest", type=openapi.TYPE_STRING),
            openapi.Parameter(name='sim_weight', in_=openapi.IN_QUERY, required=True,
                              description="Preference indicative weight for cosine similarity", type=openapi.TYPE_STRING),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, required=False,
                              description="Size of each page", type=openapi.TYPE_STRING),
            openapi.Parameter(name='page_number', in_=openapi.IN_QUERY, required=False,
                              description="Number of each page, starting from 0", type=openapi.TYPE_STRING),
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
            'Generating Recommendation'
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

        if output == 1:
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(output, status=status.HTTP_200_OK)


class DatabaseReset(APIView):

    @swagger_auto_schema(
        operation_summary="URL for regenerating database",
        operation_description="""Sometimes, due to the change in the database, we shall feel the necessity of repopulating the database. This URL is \
        for that purpose. Please note that it will take approximately 40 minutes to complete, so make sure that you know what you are doing, before invoking this URL. \
        The method paramters are mentioned""",
        manual_parameters=[
            openapi.Parameter(name='person_json', in_=openapi.IN_QUERY, required=False,
                              description="name of person json file", type=openapi.TYPE_STRING),
            openapi.Parameter(name='similarity_json', in_=openapi.IN_QUERY, required=False, 
                              description="name of similarity json file", type=openapi.TYPE_STRING),
            openapi.Parameter(name='pickle_file_name', in_=openapi.IN_QUERY, required=True,
                              description="name of database pickle file", type=openapi.TYPE_STRING),
        ], responses={
            200: openapi.Response(
                'Successful!'
            ),
            400: openapi.Response(
                'Malformed Request'
            ),
        },
        tags=[
            'Database Reset'
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
