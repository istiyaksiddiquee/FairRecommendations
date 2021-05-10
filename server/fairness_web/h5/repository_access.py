import csv
import tables as pt

from .converter import Converter

class RepoAccess():

    def __init__(self, h5file):
        self.h5file = h5file

    def get_all_users(self, start_index, end_index):

        counter = 0
        all_user = []
        user_array_tbl = self.h5file.root.user_info

        for x in user_array_tbl.iterrows():

            if counter < start_index:
                counter += 1
                continue
            elif counter == end_index:
                break
            elif counter >= start_index and counter < end_index:
                counter += 1
                all_user.append({
                    'uuid': x['uuid'].decode('UTF-8'),
                    'name': x['name'].decode('UTF-8'),
                    'gender': x['gender'].decode('UTF-8'),
                    'nationality': x['nationality'].decode('UTF-8'),
                    'research_interests': [a for a in x['research_interests'] if len(a) != 0]
                })
        return all_user

    def get_similarity(self, uuid, research_interest):

        cos_sim = []
        hop_dis = []
        user_array = []
        return_array = []

        user_array_tbl = self.h5file.root.similarity_userarray

        for row in user_array_tbl.where("id == " + str(1)):
            user_array = row['users']

        sim_tbl = self.h5file.root.similarity
        for row in sim_tbl.where("uuid == '" + uuid + "'"):
            cos_sim = row['cosine_sim']
            hop_dis = row['hop_distance']
        

        user_tbl = self.h5file.root.user_info
        
        for i in range(len(user_array)):
            if len(user_array[i]) != 0:
                for row in user_tbl.where("uuid == '" + str(user_array[i].decode('UTF-8')) + "'"):

                    obj = ResponseObject(row['uuid'].decode('UTF-8'),
                                        row['name'].decode('UTF-8'),
                                        '',
                                        row['research_interests'],
                                        row['nationality'].decode('UTF-8'),
                                        row['gender'].decode('UTF-8'),
                                        hop_dis[i],
                                        cos_sim[i])
                    return_array.append(obj)

        return return_array

    def reload_database(self, user_file, sim_file):
        converter = Converter(self.h5file)
        converter.convert_to_user_info(user_file)
        converter.convert_to_similarity_file(sim_file)
        return


class ResponseObject():

    def __init__(self, uuid, name, affiliation, research_interests, nationality, gender, hop_distance, cosine_sim):
        self.uuid = uuid
        self.name = name
        self.affiliation = affiliation
        self.research_interests = research_interests
        self.gender = gender
        self.nationality = nationality
        self.hop_distance = hop_distance
        self.cosine_sim = cosine_sim
