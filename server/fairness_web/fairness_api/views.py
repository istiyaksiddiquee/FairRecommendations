from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import tables as pt 

from h5.repository_access import RepoAccess

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

        output_arr = []
        read_mode = pt.open_file('h5/output.h5', 'r')
        access = RepoAccess(read_mode)
        obj_array = access.get_similarity_for_uuid('xyz1')
        for item in obj_array:
            output_arr.append ({
                'uuid': item.uuid, 
                'first_name': item.first_name,
                'last_name': item.last_name, 
                'affiliation': item.affiliation,
                'research_interest': item.research_interest,
                'gender': item.gender, 
                'hop_distance': item.hop_distance,
                'cosine_sim': item.cosine_sim
            })

        return Response(output_arr)
