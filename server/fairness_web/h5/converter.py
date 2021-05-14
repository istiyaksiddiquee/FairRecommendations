import csv
import json
from collections import namedtuple

import chardet
import numpy as np
import pandas as pd
import tables as pt


class User(pt.IsDescription):
    """
    Skeleton for User Table inside HDF5
    """

    uuid = pt.StringCol(50)
    name = pt.StringCol(50)
    nationality = pt.StringCol(40)
    gender = pt.StringCol(10)
    research_interests = pt.StringCol(itemsize=30, shape=15)


class Publication(pt.IsDescription):
    """
    Skeleton for Publication Table inside HDF5
    """

    publication_id = pt.StringCol(50)
    author_id = pt.StringCol(50)  # uuid
    title = pt.StringCol(200)
    abstract = pt.StringCol(500)
    ri_label = pt.StringCol(itemsize=50, shape=10)


class Similarity(pt.IsDescription):
    """
    Skeleton for Similarity Table inside HDF5
    """

    uuid = pt.StringCol(50)
    hop_distance = pt.Float32Col(shape=920)
    cosine_sim = pt.Float32Col(shape=920)


class Similarity_UserArray(pt.IsDescription):
    """
    Skeleton for storing user array in HDF5
    """

    id = pt.Int32Col()
    users = pt.StringCol(itemsize=50, shape=920)


class Converter:
    """
    Converter class takes care of the JSONs produced by Recommender System Class
    and converts them into H5 file that is used as a data storage
    """

    def __init__(self, h5file):
        self.h5file = h5file
        self.label_dict = None

    def convert_to_similarity_file(self, sim_file):
        """
        This method transforms the json containing similarity and hop distances into a compatible
        representation to store inside the above mentioned tables
        """

        uarray = self.h5file.create_table(self.h5file.root, "similarity_userarray", Similarity_UserArray)
        sim_table = self.h5file.create_table(self.h5file.root, "similarity", Similarity)

        counter = 0
        user_array = ["" for _ in range(920)]

        with open(sim_file) as json_file:
            data = json.load(json_file)
            for item in data:

                obj = namedtuple("A", item.keys())(*item.values())
                sim_row = sim_table.row

                user_array[counter] = obj.uuid.encode(encoding="UTF-8")
                counter += 1

                similarity_scores = np.zeros(920)
                hop_distances = np.zeros(920)

                for j in range(len(obj.sim_score)):
                    similarity_scores[j] = obj.sim_score[j]

                for j in range(len(obj.hop_dist)):
                    similarity_scores[j] = obj.hop_dist[j]

                sim_row["uuid"] = obj.uuid.encode(encoding="UTF-8")
                sim_row["cosine_sim"] = similarity_scores
                sim_row["hop_distance"] = hop_distances

                sim_row.append()

        user_table_row = uarray.row
        user_table_row["id"] = 1
        user_table_row["users"] = user_array
        user_table_row.append()

        uarray.flush()
        sim_table.flush()

    def convert_to_user_info(self, json_file, file_mapped_research_interest):
        """
        This method takes the user json file and generates data representaion of it, which is
        suitable to store in the h5 file. We store those data in user_info and publication table.
        """

        self.label_dict = self.generate_publication_label_dict(file_mapped_research_interest)
        user_info_table = self.h5file.create_table(self.h5file.root, "user_info", User)
        publication_table = self.h5file.create_table(self.h5file.root, "publication", Publication)

        with open(json_file) as json_file:
            data = json.load(json_file)

            for item in data:
                obj = namedtuple("A", item.keys())(*item.values())

                h5_row = user_info_table.row

                h5_row["uuid"] = obj.uuid.encode(encoding="UTF-8")
                h5_row["name"] = obj.name.encode(encoding="UTF-8")
                h5_row["nationality"] = obj.nationality.encode(encoding="UTF-8")
                h5_row["gender"] = obj.gender.encode(encoding="UTF-8")

                interest_arr = []

                for i in range(15):
                    interest_arr.append("")

                # parsing research interest into suitable array representation
                for j in range(len(obj.research_interest)):
                    if j < 15:
                        interest_arr[j] = obj.research_interest[j].title().strip().encode(encoding="UTF-8")

                h5_row["research_interests"] = interest_arr

                for paper in obj.papers:
                    p = namedtuple("A", paper.keys())(*paper.values())
                    pub_row = publication_table.row

                    publication_id = p.uuid.encode(encoding="UTF-8")
                    pub_row["publication_id"] = publication_id
                    pub_row["author_id"] = obj.uuid.encode(encoding="UTF-8")
                    pub_row["title"] = p.title.encode(encoding="UTF-8")
                    pub_row["abstract"] = p.abstract.encode(encoding="UTF-8")

                    label_list = self.parse_label_list_from_dict(self.label_dict, publication_id.decode(encoding="UTF-8"))

                    label_arr = []

                    for i in range(10):
                        label_arr.append("")

                    # parsing publications
                    for j in range(len(label_list)):
                        if j < 10:
                            label_arr[j] = label_list[j].title().strip().encode(encoding="UTF-8")

                    pub_row["ri_label"] = label_arr

                    pub_row.append()

                h5_row.append()

        publication_table.flush()
        user_info_table.flush()

        self.sample_from_user()
        return

    def sample_from_user(self):
        """
        Simple test method to validate the successful completion of the transformation of user json
        """

        user_tbl = self.h5file.root.user_info
        paper_tbl = self.h5file.root.publication
        search_str = "b12408f0-d239-49cb-8098-c88f76fad069"
        for row in user_tbl.where("uuid == '" + search_str + "'"):
            arr = [a.decode("UTF-8") for a in row["research_interests"] if len(a) != 0]
            print("user name:" + row["name"].decode("UTF-8") + "research_interests: " + ", ".join(arr))
            for item in paper_tbl.where("author_id == '" + search_str + "'"):
                print(item["title"])

    def sample_from_similarity(self):
        """
        Simple test method to validate the successful completion of the transformation of similairy json
        """

        tbl = self.h5file.root.similarity
        for row in tbl.where("uuid == '" + "xyz2" + "'"):
            print(row["hop_distance"])
            print(row["cosine_sim"])

    def sample_from_sim_user_array(self):
        """
        Simple test method to validate the successful completion of the transformation of similairy json
        """

        tbl = self.h5file.root.similarity_userarray
        for row in tbl.where("id == " + str(1)):
            print(row["users"])

    def generate_publication_label_dict(self, input_file):
        """
        Helper method to generate label dict from the publication information
        """

        with open(input_file, "rb") as f:
            encoding = chardet.detect(f.read(10000))["encoding"]

        f = pd.read_csv(input_file, sep=",", encoding=encoding)
        dictionary = f.set_index("Paper_id")["ResearchInt"].to_dict()

        return dictionary

    def parse_label_list_from_dict(self, dictionary, publication_id):
        """
        Helper method to parse labels for a particular publication from the dict that was produced
        in the above mentioned method.
        """

        if publication_id in dictionary:
            label_list = dictionary[publication_id]
            if type(label_list) == str:
                str_list = label_list.replace("]", "").replace("[", "").replace("'", "").split(",")
                return [item.strip() for item in str_list]
        return []
