import csv
import tables as pt

from .converter import Converter

class RepoAccess():
    """
    This class acts as a Data Access Layer that simplies the boilerplate codes 
    and offers an abstraction to the upper level classes. We use this class 
    to gain access to the HDF5 database and to get required objects out of it.
    """

    def __init__(self, h5file):
        self.h5file = h5file

    def get_all_users(self, start_index, end_index):
        """
        Method to obtain all users from the table. It contains start and end 
        index to facilitate pagination. 
        """

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
                    'name': x['name'].decode('UTF-8')
                })
        return all_user

    def get_similarity(self, uuid, research_interest):
        """
        Method to obtain a set of users along with their similarity scores based 
        on the UUID and research interest provided on the upstream method e.g. UI.
        """

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
        publication_tbl = self.h5file.root.publication
        
        for i in range(len(user_array)):
            user_uuid = user_array[i]
            if len(user_uuid) != 0:
                for row in user_tbl.where("uuid == '" + str(user_uuid.decode('UTF-8')) + "'"):

                    publication_list = []

                    for pubrow in publication_tbl.where("author_id == '" + str(user_uuid.decode('UTF-8')) + "'"):
                        
                        ri_label = []
                        if len(pubrow['ri_label']) != 0:
                            ri_label = [item.decode('UTF-8') for item in pubrow['ri_label'] if len(item) != 0]

                        publication_list.append({
                            'publication_id': pubrow['publication_id'].decode('UTF-8'),
                            'title': pubrow['title'].decode('UTF-8'),
                            'ri_label': ri_label
                        })

                    obj = ResponseObject(row['uuid'].decode('UTF-8'),
                                        row['name'].decode('UTF-8'),
                                        '',
                                        row['research_interests'],
                                        row['nationality'].decode('UTF-8'),
                                        row['gender'].decode('UTF-8'),
                                        [item for item in publication_list if len(item) != 0],
                                        hop_dis[i],
                                        cos_sim[i])
                    return_array.append(obj)

        return return_array

    def reload_database(self, user_file, sim_file, file_with_mapped_research_interest):
        """
        Method to facilitate database regeneration. 
        """
        converter = Converter(self.h5file)
        converter.convert_to_user_info(user_file, file_with_mapped_research_interest)
        converter.convert_to_similarity_file(sim_file)
        return


class ResponseObject():
    """
    Object structure for Respose to calling method. 
    """
    def __init__(self, uuid, name, affiliation, research_interests, nationality, gender, publication_list, hop_distance, cosine_sim):
        self.uuid = uuid
        self.name = name
        self.affiliation = affiliation
        self.research_interests = research_interests
        self.gender = gender
        self.nationality = nationality
        self.publication_list = publication_list
        self.hop_distance = hop_distance
        self.cosine_sim = cosine_sim
