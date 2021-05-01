import csv
import json 
import tables as pt
from collections import namedtuple

class User(pt.IsDescription):
    uuid = pt.StringCol(50)
    name = pt.StringCol(50)
    nationality = pt.StringCol(40)
    gender = pt.StringCol(10)
    research_interests = pt.StringCol(itemsize=30, shape=15)


class Publication(pt.IsDescription):
    publication_id = pt.StringCol(50)
    author_id = pt.StringCol(50)  # uuid
    title = pt.StringCol(200)
    abstract = pt.StringCol(500)


class Similarity(pt.IsDescription):
    uuid = pt.StringCol(50)
    hop_distance = pt.Float32Col(shape=920)
    cosine_sim = pt.Float32Col(shape=920)


class Similarity_UserArray(pt.IsDescription):
    id = pt.Int32Col()
    users = pt.StringCol(itemsize=50, shape=920)


class Converter:

    def __init__(self, h5file):
        self.h5file = h5file

    def convert_to_similarity_file(self, sim_file):

        # uarray = self.h5file.create_table(self.h5file.root, 'similarity_userarray', Similarity_UserArray)
        sim = self.h5file.create_table(self.h5file.root, 'similarity', Similarity)
        
        with open(sim_file) as json_file:
            data = json.load(json_file)
            for item in data:
                obj = namedtuple("A", item.keys())(*item.values())

                sim_row['uuid'] = obj.uuid.encode(encoding='UTF-8')
                sim_row['cosine_sim'] = obj.sim_score 
                sim_row['hop_distance'] = obj.hop_dist
                
                sim_row['research_interest'] = row[1]
                sim_row['cosine_sim'] = row[2:len(row)]
                    
                sim_row.append()

            sim.flush()

    def convert_to_user_info(self, json_file):

        user_info_table = self.h5file.create_table(self.h5file.root, 'user_info', User)
        publication_table = self.h5file.create_table(self.h5file.root, 'publication', Publication)
        
        with open(json_file) as json_file:
            data = json.load(json_file)

            for item in data:
                obj = namedtuple("A", item.keys())(*item.values())

                h5_row = user_info_table.row
                
                h5_row['uuid'] = obj.uuid.encode(encoding='UTF-8')
                h5_row['name'] = obj.name.encode(encoding='UTF-8')
                h5_row['nationality'] = obj.nationality.encode(encoding='UTF-8')
                h5_row['gender'] = obj.gender.encode(encoding='UTF-8')

                interest_arr = []

                for i in range(15):
                    interest_arr.append('')

                for j in range(len(obj.research_interest)):
                    if j < 15:
                        interest_arr[j] = obj.research_interest[j].encode(encoding='UTF-8')

                h5_row['research_interests'] = interest_arr

                for paper in obj.papers:
                    p = namedtuple("A", paper.keys())(*paper.values())
                    pub_row = publication_table.row

                    pub_row['publication_id'] = p.uuid.encode(encoding='UTF-8')
                    pub_row['author_id'] = obj.uuid.encode(encoding='UTF-8')
                    pub_row['title'] = p.title.encode(encoding='UTF-8')
                    pub_row['abstract'] = p.abstract.encode(encoding='UTF-8')

                    pub_row.append()

                h5_row.append()

        publication_table.flush()
        user_info_table.flush()

        self.sample_from_user()
        return

    def sample_from_user(self):

        user_tbl = self.h5file.root.user_info
        paper_tbl = self.h5file.root.publication
        search_str = "b12408f0-d239-49cb-8098-c88f76fad069"
        for row in user_tbl.where("uuid == '" + search_str + "'"):
            arr = [a.decode('UTF-8') for a in row['research_interests'] if len(a) != 0]
            print('user name:' + row['name'].decode('UTF-8') + 'research_interests: ' + ', '.join(arr))
            for item in paper_tbl.where("author_id == '" + search_str + "'"):
                print(item['title'])
                

    def sample_from_similarity(self):

        tbl = self.h5file.root.similarity
        for row in tbl.where("uuid == '" + 'xyz2' + "'"):
            print(row['hop_distance'])
            print(row['cosine_sim'])

    def sample_from_sim_user_array(self):

        tbl = self.h5file.root.similarity_userarray
        for row in tbl.where("id == " + str(1)):
            print(row['users'])
