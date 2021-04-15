import csv
import tables as pt 


class User(pt.IsDescription):
    uuid = pt.StringCol(30)
    first_name = pt.StringCol(20)
    last_name = pt.StringCol(20)
    affiliation = pt.StringCol(40)
    research_interest = pt.StringCol(30)
    gender = pt.StringCol(10)

class Publication(pt.IsDescription):
    publication_id = pt.StringCol(30)
    first_author = pt.StringCol(30) # uuid
    title = pt.StringCol(20)
    date = pt.StringCol(20)
    no_of_coauthors = pt.Int32Col()
    co_author_list = pt.StringCol(itemsize=30, shape=10)

class Similarity(pt.IsDescription):
    uuid = pt.StringCol(30)
    research_interest = pt.StringCol(50)
    hop_distance = pt.Int32Col(shape=5)
    cosine_sim = pt.Float32Col(shape=5)

class Similarity_UserArray(pt.IsDescription):
    id = pt.Int32Col()
    users = pt.StringCol(itemsize=30, shape=5)

class Converter:

    def __init__(self, h5file):
        self.h5file = h5file
    
    def convert_to_similarity_file(self, sim_file, hop_file):
        uarray = self.h5file.create_table(self.h5file.root, 'similarity_userarray', Similarity_UserArray)
        sim = self.h5file.create_table(self.h5file.root, 'similarity', Similarity)
        with open(sim_file) as csv_file:
            row_count = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row_count == 0:
                    row_count = 1
                    userarray_row = uarray.row

                    userarray_row['id'] = 1
                    userarray_row['users'] = row[2:len(row)]

                    userarray_row.append()
                else:
                    sim_row = sim.row

                    sim_row['uuid'] = row[0]
                    sim_row['research_interest'] = row[1]
                    sim_row['cosine_sim'] = row[2:len(row)]
                    
                    sim_row.append()
            uarray.flush()
            sim.flush()

        with open(hop_file) as csv_file:
            row_count = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            for hop_row in csv_reader:
                for tbl_row in sim.where("uuid == '" + str(hop_row[0]) + "'"):
                    tbl_row['hop_distance'] = hop_row[1:len(row)]
                    tbl_row.update()

        sim.flush()                

    def convert_to_user_info(self, csv_file):
        
        tbl = self.h5file.create_table(self.h5file.root, 'user_info', User)

        with open(csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            for csv_row in csv_reader:
                
                h5_row = tbl.row
                
                h5_row['uuid'] = csv_row[0]
                h5_row['first_name'] = csv_row[1]
                h5_row['last_name'] = csv_row[2]
                h5_row['affiliation'] = csv_row[3]
                h5_row['research_interest'] = csv_row[4]
                h5_row['gender'] = csv_row[5]
                
                h5_row.append()
                

        tbl.flush()

    def sample_from_user(self):
        
        tbl = self.h5file.root.user_info        
        for row in tbl.where("uuid == '" + 'xyz2' + "'"):
            print(row['first_name'])
    
    def sample_from_similarity(self):
        
        tbl = self.h5file.root.similarity
        for row in tbl.where("uuid == '" + 'xyz2' + "'"):
            print(row['hop_distance'])
            print(row['cosine_sim'])

    def sample_from_sim_user_array(self):
        
        tbl = self.h5file.root.similarity_userarray
        for row in tbl.where("id == " + str(1)):
            print(row['users'])
