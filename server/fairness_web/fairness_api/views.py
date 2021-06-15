from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .services import RecommendationService, DatabaseResetService, InitialCheckup


class Initialization(APIView):
    """Methods related to initial requirement checking"""

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Validates the availability of required resources to continue with the application",
        operation_description="""This is a GET method that does not require any other parameter. Upon invocation, \
        it will check for the availability of the database file that is required for this application. If it is not \
            in the appropriate location, then the method will return a non-zero response. """,
        responses={
            200: openapi.Response("Successful"),
            404: openapi.Response("One or multiple required file(s) were not found"),
        },
        tags=["Initialization"],
    )
    def get(self, request, format=None):

        state = InitialCheckup.check_for_db_availability()
        if state == 0:
            return Response("Successful", status=status.HTTP_200_OK)
        else:
            return Response("One or multiple required file(s) were not found", status=status.HTTP_404_NOT_FOUND)



class ResearchInterest(APIView):
    """Methods related to obtaining research interests available in the system"""

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Returns a list of available Research Interests",
        operation_description="""This is a GET method that does not require any other parameter. Upon invocation, \
            it will returns a list of strings where each string represents a research \
            interest that is available and applicable in the system.""",
        responses={
            200: openapi.Response({"research_interests": []})
        },
        tags=["Listing Research Interests"],
    )
    def get(self, request, format=None):

        research_interest = [
            "Anthropology",
            "Artificial Intelligence",
            "Climate Research",
            "Cultural Studies",
            "Data Science",
            "Digital Education",
            "Digital Humanities",
            "Digital Libraries",
            "Digital Media",
            "Economics",
            "Education",
            "Environment",
            "Ethnology",
            "Gender Studies",
            "History",
            "Humanities",
            "Information Retrieval",
            "Knowledge Graphs",
            "Legal Artificial Intelligence",
            "Machine Learning",
            "Natural Language Processing",
            "Peace & Conflict Studies",
            "Political Sciences",
            "Political Studies",
            "Project Management",
            "Psychology",
            "Recommendaton Systems",
            "Recommender Systems",
            "Religion",
            "Transaltional Science",
            "Translation Sciences",
            "Usability",
            "User Modeling",
            "Virtual Reality",
        ]
        return Response({"research_interests": research_interest}, status=status.HTTP_200_OK)

    # def regenerate_ri(self, request, format=None):
    #     db_svc = DatabaseResetService()
    #     self.research_interest = db_svc.repopulate_research_interest_array()


class User(APIView):
    """View related to Getting list of users"""

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Returns a list of Users",
        operation_description="""This is a GET method that returns a list of Users. It can be used with or without the pagination parameters. \
            Please see method parameters for information regarding keys for pagination parameters.""",
        manual_parameters=[
            openapi.Parameter(name="page_size", in_=openapi.IN_QUERY, required=False, description="Size of each page", type=openapi.TYPE_STRING),
            openapi.Parameter(name="page_number", in_=openapi.IN_QUERY, required=False, description="Number of each page, starting from 0", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response("Successful Response with array of users"),
            400: openapi.Response("Malformed Parameter(s)"),
        },
        tags=["Listing Available Users"],
    )
    def get(self, request, format=None):

        req_page_size = request.GET["page_size"]
        req_page_number = request.GET["page_number"]

        if req_page_size != None and req_page_number != None:
            if req_page_size.isnumeric() != True or req_page_number.isnumeric() != True:
                return Response("Malformed Parameter(s)", status=status.HTTP_400_BAD_REQUEST)
        else:
            req_page_size = 902
            req_page_number = 0

        recommendation_service = RecommendationService()
        output = recommendation_service.get_all_users(req_page_number, req_page_size)
        return Response(output, status=status.HTTP_200_OK)


class Recommendation(APIView):
    """View for obtaining recommendation for a specific user and a specific research interest"""

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Returns calculated Recommendations",
        operation_description="""This is a GET method that returns two lists of Recommendations. One of these list possess uncorrected, raw recommendation. \
        The other one presents a bias corrected version of the raw recommendation. They have a descriptive key that can be found in the responses section. \
        However, this method can be used in conjunction with the pagination parameter. Please see details on the parameters section. Furthermore, please note \
        that the uuid, research interest, and similarity weight paramteres are mandatory here.""",
        manual_parameters=[
            openapi.Parameter(name="uuid", in_=openapi.IN_QUERY, required=True, description="UUID of user", type=openapi.TYPE_STRING),
            openapi.Parameter(name="research_interest", in_=openapi.IN_QUERY, required=True, description="Research Interest from predefined list of Research Interest", type=openapi.TYPE_STRING),
            openapi.Parameter(name="sim_weight", in_=openapi.IN_QUERY, required=True, description="Preference indicative weight for cosine similarity", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response("Successful Response with bias and bias corrected list", output={"with_bias": "", "bias_corrected": "", "length": "", "female_ratio": ""}),
            400: openapi.Response("Malformed Parameter(s)"),
            500: openapi.Response("Internal Server Error"),
        },
        tags=["Generating Recommendation"],
    )
    def get(self, request, format=None):

        req_uuid = request.GET["uuid"]
        req_research_interest = request.GET["research_interest"]
        req_sim_weight = request.GET["sim_weight"]
        # req_page_size = request.GET["page_size"]
        # req_page_number = request.GET["page_number"]

        if req_uuid == None or len(req_uuid) == 0 or req_research_interest == None or len(req_research_interest) == 0:
            return Response("Malformed Parameter(s)", status=status.HTTP_400_BAD_REQUEST)
        
        # pagination parameters are not mandatory here
        # if req_page_size != None and req_page_number != None:
        #     if req_page_size.isnumeric() != True or req_page_number.isnumeric() != True:
        #         return Response("Malformed Parameter(s)", status=status.HTTP_400_BAD_REQUEST)

        recommendation_service = RecommendationService()
        output = recommendation_service.get_recommendation(req_uuid, req_research_interest, req_sim_weight)

        if output == 1:
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(output, status=status.HTTP_200_OK)


class DatabaseReset(APIView):
    """View related to regenerating the database."""

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="URL for regenerating database",
        operation_description="""Sometimes, due to the change in the database, we shall feel the necessity of repopulating the database. This URL is \
        for that purpose. Please note that it will take approximately 40 minutes to complete, so make sure that you know what you are doing, before invoking this URL. \
        The method paramters are mentioned""",
        manual_parameters=[
            openapi.Parameter(name="person_json", in_=openapi.IN_QUERY, required=False, description="name of person json file", type=openapi.TYPE_STRING),
            openapi.Parameter(name="similarity_json", in_=openapi.IN_QUERY, required=False, description="name of similarity json file", type=openapi.TYPE_STRING),
            openapi.Parameter(name="pickle_file_name", in_=openapi.IN_QUERY, required=True, description="name of database pickle file", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response("Successful!"),
            400: openapi.Response("Malformed Parameter(s)"),
            500: openapi.Response("Internal Server Error"),
        },
        tags=["Database Reset"],
    )
    def get(self, request, format=None):

        req_person = request.GET["person_json"]
        req_similarity = request.GET["similarity_json"]
        req_pickle_file_name = request.GET["pickle_file_name"]

        # pickle file name is made to be mandatory
        if req_pickle_file_name == None or len(req_pickle_file_name) == 0:
            return Response("Malformed Request", status=status.HTTP_400_BAD_REQUEST)

        # json file for person information is not mandatory. if it is not provided, then a predefined name is assigned
        if req_person != None: 
            if len(req_person) != 0:
                return Response("Malformed Parameter(s)", status=status.HTTP_400_BAD_REQUEST)
        else:
            req_person = "persons_list.json"


        # json file for similarity information is not mandatory. if it is not provided, then a predefined name is assigned
        if req_similarity != None:
            if len(req_similarity) != 0:
                return Response("Malformed Parameter(s)", status=status.HTTP_400_BAD_REQUEST)
        else:
            req_similarity = "scores_dict.json"


        db_rest_svc = DatabaseResetService()
        return_code = db_rest_svc.recreate_db(req_person, req_similarity, req_pickle_file_name)

        if return_code != 0:
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("Success", status=status.HTTP_200_OK)
