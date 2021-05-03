import json
import os.path
import tables as pt

from graph.recommender_system import *
from h5.repository_access import RepoAccess

from enum import Enum


class Information(Enum):
    DATABASE_PATH = "graph/data"
    DATABASE_NAME = "db.h5"
    FILE_WITH_MAPPED_RESEARCH_INTEREST = "uuid_without_blanks.csv"


class RecommendationService():

    def __init__(self):
        self.read_mode = pt.open_file(Information.DATABASE_PATH.value + '/' + Information.DATABASE_NAME.value, 'r')
        self.access = RepoAccess(self.read_mode)

    def get_all_users(self, page_number, page_size):
        
        start_index = int(page_number) * int(page_size)
        end_index = start_index + int(page_size)

        output = self.access.get_all_users(start_index, end_index)
        self.read_mode.close()
        return output

    def get_recommendation(self, req_uuid, req_research_interest, weight_for_similarity, req_page_size, req_page_number):
        
        obj_array = self.access.get_similarity(req_uuid, req_research_interest)
        self.read_mode.close()

        scored_items = []
        for item in obj_array:
            scored_items.append(ResponseStructure(
                                item.uuid,
                                item.name,
                                item.affiliation,
                                [a for a in item.research_interests if len(a) != 0],
                                item.gender,
                                item.nationality,
                                round(item.hop_distance, 3),
                                round(float(item.cosine_sim), 3),
                                round((float(weight_for_similarity)*item.hop_distance + (1-float(weight_for_similarity)) * item.cosine_sim), 3)
                            ))
        
        with_bias = self.sort_biased_array(scored_items)
        bias_corrected = self.sort_bias_processed_array(scored_items)
        bias_corrected = self.add_reference_to_bias_corrected_data(with_bias, bias_corrected)

        if req_page_size != None and req_page_number != None:
            start_index = int(req_page_size) * int(req_page_number)
            end_index = start_index + int(req_page_size)

            with_bias = with_bias[start_index:end_index]
            bias_corrected = bias_corrected[start_index:end_index]

        output = {
            'with_bias': self.jsonify_recommendation(with_bias, True),
            'bias_corrected': self.jsonify_recommendation(bias_corrected, False)
        }

        return output

    def sort_biased_array(self, arr):
        return sorted(arr, key=lambda x: x.score, reverse=True)

    def sort_bias_processed_array(self, arr):
        return sorted(arr, key=lambda x: x.score, reverse=False)

    def jsonify_recommendation(self, obj_array, bias):
        output_arr = []
        if bias:
            for item in obj_array:
                output_arr.append({
                    'uuid': item.uuid,
                    'name': item.name,
                    'affiliation': item.affiliation,
                    'research_interests': item.research_interests,
                    'gender': item.gender,
                    'nationality': item.nationality,
                    'hop_distance': item.hop_distance,
                    'cosine_sim': item.cosine_sim,
                    'score': item.score
                })
        else:
            for item in obj_array:
                output_arr.append({
                    'uuid': item.uuid,
                    'name': item.name,
                    'affiliation': item.affiliation,
                    'research_interests': item.research_interests,
                    'gender': item.gender,
                    'nationality': item.nationality,
                    'hop_distance': item.hop_distance,
                    'cosine_sim': item.cosine_sim,
                    'score': item.score,
                    'bias_ref': item.bias_ref
                })

        return output_arr

    def add_reference_to_bias_corrected_data(self, with_bias, bias_corrected):

        for item in bias_corrected:
            for t in range(len(with_bias)):
                if with_bias[t].uuid == item.uuid:
                    item.bias_ref = t
                    break

        return bias_corrected


class DatabaseResetService():

    def __init__(self):
        self.write_mode = pt.open_file(
            Information.DATABASE_PATH.value + '/' + Information.DATABASE_NAME.value, 'w')
        self.access = RepoAccess(self.write_mode)

    def recreate_db(self, person_json, similarity_json, pickle_file_name):

        person_json_path = Information.DATABASE_PATH.value + '/' + person_json
        similarity_json_path = Information.DATABASE_PATH.value + '/' + similarity_json
        pickle_file_path = Information.DATABASE_PATH.value + '/' + pickle_file_name
        file_path_with_mapped_research_interest = Information.DATABASE_PATH.value + '/' + Information.FILE_WITH_MAPPED_RESEARCH_INTEREST.value

        # start = time.time()
        # data_service = Data(pickle_file_path, file_path_with_mapped_research_interest)
        # print("returned from data service: " + str(time.time() - start)) # took 2463.6140756607056 seconds / 41.0602346 minutes

        # scores json size is 16.7MB
        # person json size is 1.01MB 
        # hdf db size is 1.86 MB !! without any compression

        # with open(person_json_path, 'w', encoding='utf-8') as f:
        #     json.dump(data_service.persons, f, default=Person.to_json, indent=4)

        # print("person json file completed")

        # with open(similarity_json_path, 'w') as fp:
        #     json.dump(data_service.scores_List, fp, indent=4)

        print("similarity json file completed")

        if os.path.isfile(person_json_path) and os.path.isfile(similarity_json_path):
            start = time.time()
            self.access.reload_database(person_json_path, similarity_json_path)
            print("database has been re-written: " + str(time.time() - start))
            self.write_mode.close()
            return 0
        else:
            return 1


class ResponseStructure():
    def __init__(self, uuid, name, affiliation, research_interests, gender, nationality, hop_distance, cosine_sim, score):

        self.uuid = uuid
        self.name = name
        self.affiliation = affiliation
        self.research_interests = research_interests
        self.gender = gender
        self.nationality = nationality
        self.hop_distance = hop_distance
        self.cosine_sim = cosine_sim
        self.score = score
