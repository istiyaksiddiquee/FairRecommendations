import math
import json
import copy
import time
import os
import chardet
import pandas as pd

import tables as pt

from enum import Enum
from collections import Counter

from graph.recommender_system import Data, Person
from h5.repository_access import RepoAccess


class Information(Enum):
    """
    Stores a set of enums that we are going to use throughout this file.
    """

    DATABASE_PATH = os.getenv("DATA_PATH")
    DATABASE_NAME = os.getenv("DB_FILE_NAME")
    FILE_WITH_MAPPED_RESEARCH_INTEREST = os.getenv("MAPPING_FILE_NAME")


class InitialCheckup:
    """
    Class for checking the availability of some required files
    """

    @staticmethod
    def check_for_db_availability():
        """
        Checking for database availability
        """

        if os.path.isfile(Information.DATABASE_PATH.value + os.sep + Information.DATABASE_NAME.value):
            return 0
        else:
            print("FATAL ERROR: db not found.")
            return 1

    @staticmethod
    def check_for_file_availability(file_path):
        """
        Common method for checking for the availability of other files
        """

        if os.path.isfile(file_path):
            return 0
        else:
            print(f"FATAL ERROR: required file {file_path} was not found.")
            return 1


class RecommendationService:
    """
    Recommendation Service provides helpful methods for getting the users, recommendation, etc.
    """

    def __init__(self):

        # Opening the file in the constructor will work as singleton pattern in our case.
        self.read_mode = pt.open_file(Information.DATABASE_PATH.value + os.sep + Information.DATABASE_NAME.value, "r")
        self.access = RepoAccess(self.read_mode)

    def get_all_users(self, page_number, page_size):
        """
        Method to get all the users based on pagination
        """

        start_index = int(page_number) * int(page_size)
        end_index = start_index + int(page_size)

        output = self.access.get_all_users(start_index, end_index)
        self.read_mode.close()
        return output

    def get_recommendation(self, req_uuid, req_research_interest, weight_for_similarity, req_page_size, req_page_number):
        """
        Method to get the recommendation based on uuid, research interest, weight for similairy and pagination params
        """

        try:
            obj_array = self.access.get_similarity(req_uuid, req_research_interest)
        except IndexError:
            self.read_mode.close()
            return 1

        self.read_mode.close()

        scored_items = []

        for item in obj_array:
            if req_research_interest.encode(encoding="ascii") in item.research_interests:

                paper_list = []
                research_interest_list = [a for a in item.research_interests if len(a) != 0]

                # Removing papers that do not have the same label as the requested research interest
                for paper in item.publication_list:
                    if "ri_label" in paper:
                        ri_label_list = paper["ri_label"]
                        if req_research_interest.title().strip() in ri_label_list:
                            paper_list.append(paper)

                scored_items.append(
                    ResponseStructure(
                        item.uuid,
                        item.name,
                        item.affiliation,
                        research_interest_list,
                        item.gender,
                        item.nationality,
                        paper_list,
                        round(item.hop_distance, 3),
                        round(float(item.cosine_sim), 3),
                        round(
                            (float(weight_for_similarity) * item.hop_distance + (1 - float(weight_for_similarity)) * item.cosine_sim),
                            3,
                        ),
                    )
                )

        if len(scored_items) != 0:
            counted_genders = Counter(item.gender for item in scored_items)

            female_count = None
            for gender, k in counted_genders.items():
                if gender.lower() == "female":
                    female_count = k

            # this bias will be imposed throughout the pages
            female_ratio = float(female_count / len(scored_items))

            with_bias = self.sort_biased_array(scored_items)

            # bias_corrected = self.sort_bias_processed_array(scored_items)
            bias_corrected = self.bias_correction(copy.deepcopy(with_bias), female_ratio, page_size=req_page_size)
            bias_corrected = self.add_reference_to_bias_corrected_data(with_bias, bias_corrected)

            # implementing pagination
            if req_page_size != None and req_page_number != None:
                start_index = int(req_page_size) * int(req_page_number)
                end_index = start_index + int(req_page_size)

                with_bias = with_bias[start_index:end_index]
                bias_corrected = bias_corrected[start_index:end_index]

            output = {
                "with_bias": self.jsonify_recommendation(with_bias, True),
                "bias_corrected": self.jsonify_recommendation(bias_corrected, False),
                "length": len(scored_items),
                "female_ratio": round(female_ratio, 3),
            }

            return output
        return []

    def bias_correction(self, arr, expected_ratio, page_size):
        """
        Algorithm for correcting the bias throughout pages. This ensures that the ratio of female researchers
        reaches a minimum value on each displayed pages so that there is better exposure for the works of female
        researchers.
        """

        chunks = math.ceil(len(arr) / int(page_size))
        expected_female_count = expected_ratio * int(page_size)

        for k in range(chunks):
            m = k * int(page_size)
            n = m + int(page_size)
            female_count = 0

            if m < len(arr):
                if n > len(arr):
                    n = len(arr)

                for i in range(m, n):
                    if arr[i].gender.lower() == "female":
                        female_count += 1

                if expected_female_count > female_count:
                    females_to_import = expected_female_count - female_count
                    # print(f"picking up {females_to_import} number of female")

                    item_array = []
                    position_array = []

                    for i in range(n, len(arr)):
                        if arr[i].gender.lower() == "female":
                            females_to_import -= 1
                            position_array.append(i)
                            item_array.append(copy.deepcopy(arr[i]))
                            if females_to_import < 1:
                                break

                    if len(position_array) != 0:
                        start_index = n - len(position_array)
                        for i in range(len(position_array)):
                            j = position_array[i] - 1
                            while j >= start_index:
                                arr[j + 1] = copy.deepcopy(arr[j])
                                j -= 1
                            arr[start_index] = copy.deepcopy(item_array[i])
                            start_index += 1
        return arr

    def sort_biased_array(self, arr):
        """
        Sorting helps us maintain the order throughout pages
        """

        return sorted(arr, key=lambda x: x.score, reverse=True)

    def sort_bias_processed_array(self, arr):
        """
        Sorting the biased processed array
        """

        return sorted(arr, key=lambda x: x.score, reverse=False)

    def jsonify_recommendation(self, obj_array, bias):
        """
        Helper method to jsonify the response object.
        """

        output_arr = []
        if bias:
            for item in obj_array:
                output_arr.append(
                    {
                        "uuid": item.uuid,
                        "name": item.name,
                        "affiliation": item.affiliation,
                        "research_interests": item.research_interests,
                        "gender": item.gender,
                        "nationality": item.nationality,
                        "publication_list": item.publication_list,
                        "hop_distance": item.hop_distance,
                        "cosine_sim": item.cosine_sim,
                        "score": item.score,
                    }
                )
        else:
            for item in obj_array:
                output_arr.append(
                    {
                        "uuid": item.uuid,
                        "name": item.name,
                        "affiliation": item.affiliation,
                        "research_interests": item.research_interests,
                        "gender": item.gender,
                        "nationality": item.nationality,
                        "publication_list": item.publication_list,
                        "hop_distance": item.hop_distance,
                        "cosine_sim": item.cosine_sim,
                        "score": item.score,
                        "bias_ref": item.bias_ref,
                    }
                )

        return output_arr

    def add_reference_to_bias_corrected_data(self, with_bias, bias_corrected):
        """
        We would like to see the impact of the bias correction algorithm on individual person. So
        we decided to add reference of the raw rank in the bias processed ranking. This is then
        showed visually in the UI.
        """

        for item in bias_corrected:
            for t in range(len(with_bias)):
                if with_bias[t].uuid == item.uuid:
                    item.bias_ref = t
                    break

        return bias_corrected


class DatabaseResetService:
    """
    Database service provides an interface to regenerate data from the pickle that was given by GEI. This
    helps us in automatize the process of data extraction.
    """

    def __init__(self):
        self.write_mode = pt.open_file(Information.DATABASE_PATH.value + os.sep + Information.DATABASE_NAME.value, "w")
        self.access = RepoAccess(self.write_mode)

    def repopulate_research_interest_array(self):
        """
        There are multiple research interests in the system. This method provides a way to regenerate the research interests
        if we need. Currently this method is not being used by any upstream method.
        """

        file_path_with_mapped_research_interest = Information.DATABASE_PATH.value + os.sep + Information.FILE_WITH_MAPPED_RESEARCH_INTEREST.value

        if InitialCheckup.check_for_file_availability(file_path_with_mapped_research_interest) == 0:

            outer_list = []
            with open(file_path_with_mapped_research_interest, "rb") as f:
                encoding = chardet.detect(f.read(10000))["encoding"]

            f = pd.read_csv(file_path_with_mapped_research_interest, sep=",", encoding=encoding)

            for item in f.ResearchInt.to_list():
                if type(item) != float:
                    i_list = item.replace("]", "").replace("[", "").replace("'", "").split(",")
                    for i in i_list:
                        outer_list.append(i.strip().title())

            return set(outer_list)

    def recreate_db(self, person_json, similarity_json, pickle_file_name):
        """
        Main method for recreating the database. We recreate the database to its entirity, from the networkx picke file
        to hdf5 database.
        """

        person_json_path = Information.DATABASE_PATH.value + os.sep + person_json
        similarity_json_path = Information.DATABASE_PATH.value + os.sep + similarity_json
        pickle_file_path = Information.DATABASE_PATH.value + os.sep + pickle_file_name
        file_path_with_mapped_research_interest = Information.DATABASE_PATH.value + os.sep + Information.FILE_WITH_MAPPED_RESEARCH_INTEREST.value

        if InitialCheckup.check_for_file_availability(pickle_file_path) == 0 and InitialCheckup.check_for_file_availability(file_path_with_mapped_research_interest) == 0:

            # took 2463.6140756607056 seconds / 41.0602346 minutes
            # scores json size is 16.7MB
            # person json size is 1.01MB
            # hdf db size is 1.86 MB !! without any compression

            """start = time.time()
            data_service = Data(pickle_file_path, file_path_with_mapped_research_interest)
            print("returned from data service: " + str(time.time() - start))

            with open(person_json_path, "w", encoding="utf-8") as f:
                json.dump(data_service.persons, f, default=Person.to_json, indent=4)

            print("person json file completed")

            with open(similarity_json_path, "w") as fp:
                json.dump(data_service.scores_List, fp, indent=4)

            print("similarity json file completed")"""

            if InitialCheckup.check_for_file_availability(person_json_path) == 0 and InitialCheckup.check_for_file_availability(similarity_json_path) == 0:

                start = time.time()
                self.access.reload_database(person_json_path, similarity_json_path, file_path_with_mapped_research_interest)
                print("database has been re-written: " + str(time.time() - start))
                self.write_mode.close()
                return 0
            else:
                return 1
        else:
            print("Could not perform DB Regeneration. Some file(s) were missing.")
            return 1


class ResponseStructure:
    """
    Structure for response sent to server
    """

    def __init__(
        self,
        uuid,
        name,
        affiliation,
        research_interests,
        gender,
        nationality,
        publication_list,
        hop_distance,
        cosine_sim,
        score,
    ):

        self.uuid = uuid
        self.name = name
        self.affiliation = affiliation
        self.research_interests = research_interests
        self.gender = gender
        self.nationality = nationality
        self.publication_list = publication_list
        self.hop_distance = hop_distance
        self.cosine_sim = cosine_sim
        self.score = score
