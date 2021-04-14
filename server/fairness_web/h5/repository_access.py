import csv
import tables as pt 


class RepoAccess():

    def __init__(self, h5file):
        self.h5file = h5file

    def get_similarity_for_uuid(self, uuid):
        
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
            
            info = {}
            for row in user_tbl.where("uuid == '" + str(user_array[i].decode('UTF-8')) + "'"):
            
                obj = ReturnedObject(row['uuid'].decode('UTF-8'), 
                                    row['first_name'].decode('UTF-8'), 
                                    row['last_name'].decode('UTF-8'), 
                                    row['affiliation'].decode('UTF-8'), 
                                    row['research_interest'].decode('UTF-8'), 
                                    row['gender'].decode('UTF-8'), 
                                    hop_dis[i], 
                                    cos_sim[i])
                return_array.append(obj)

        
        return return_array
            

class ReturnedObject():

    def __init__(self, uuid, first_name, last_name, affiliation, research_interest, gender, hop_distance, cosine_sim):
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name
        self.affiliation = affiliation
        self.research_interest = research_interest
        self.gender = gender
        self.hop_distance = hop_distance
        self.cosine_sim = cosine_sim
