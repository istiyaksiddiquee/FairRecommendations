import tables as pt 

from converter import Converter
from repository_access import RepoAccess




h5file = pt.open_file('output_test.h5', 'w')
converter = Converter(h5file)
converter.convert_to_user_info('persons_list.json')
# converter.convert_to_similarity_file('similarity_sim.csv', 'similarity_hop.csv')
converter.sample_from_user()
h5file.close()


# output_arr = []
# read_mode = pt.open_file('output.h5', 'r')
# access = RepoAccess(read_mode)
# obj_array = access.get_similarity_for_uuid('xyz1')
# for item in obj_array:
#     output_arr.append ({
#         'uuid': item.uuid, 
#         'first_name': item.first_name,
#         'last_name': item.last_name, 
#         'affiliation': item.affiliation,
#         'research_interest': item.research_interest,
#         'gender': item.gender, 
#         'hop_distance': item.hop_distance,
#         'cosine_sim': item.cosine_sim
#     })

# print(output_arr)