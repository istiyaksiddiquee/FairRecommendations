# import time
# import json
# import itertools
# import numpy as np
# import pandas as pd
# import networkx_query
# import networkx as nx
# from node2vec import Node2Vec
# import matplotlib.pyplot as plt
# from networkx_query import search_nodes, search_edges


# class Paper:
#     uuid: str
#     title: str
#     abstract: str
#     pType: str

#     def __init__(self, uuid, title, abstract, pType):
#         self.uuid = uuid
#         self.title = title
#         self.abstract = abstract
#         self.pType = pType

#     def __repr__(self):
#         return f'Paper(uuid:{self.uuid},"title":{self.title}, "abstract":{self.abstract}, "pType":{self.pType})'


#     def __str__(self):
#         return {"uuid": self.uuid, "title": self.title, "abstract": self.abstract, "pType": self.pType}


#     # return f'{{"uuid":{self.uuid},"title":{self.title}, "abstract":{self.abstract}}}'

#     def to_json(python_object):
#         if isinstance(python_object, Paper):
#             return (python_object.__str__())
#         # {"uuid":python_object.uuid,"title":python_object.title,"abstract":python_object.abstract}
#         raise TypeError((python_object.__str__()) + ' is not JSON serializable')


# # @dataclass
# class Person:
#     uuid: str
#     name: str
#     nationality: str
#     gender: str
#     research_interest: list()
#     paper_count: list()
#     papers: list()

#     def __init__(self, uuid, name, nationality, gender, research_interest, paper_count, papers):
#         self.uuid = uuid
#         self.name = name
#         self.nationality = nationality
#         self.gender = gender
#         self.research_interest = research_interest
#         self.paper_count = paper_count
#         self.papers = []
#         for i in range(0, len(papers)):
#             # print(papers[i].uuid,papers[i].title,papers[i].abstract, papers[i].pType)
#             self.papers.append(Paper(papers[i].uuid, papers[i].title, papers[i].abstract, papers[i].pType))

#     def __str__(self):
#         # print(len(self.papers))
#         papers = []
#         for i in range(0, len(self.papers)):
#             papers.append(self.papers[i].__str__())
#         return {"name": self.name, "uuid": self.uuid, "nationality": self.nationality, "gender": self.gender,
#                 "research_interest": self.research_interest, "paper_count": self.paper_count, "papers": papers}

#     def __repr__(self):
#         papers = ""
#         for i in range(0, len(self.papers)):
#             papers += self.papers[i].__repr__()
#         return f'Person(name:{self.name},uuid:{self.uuid},nationality:{self.nationality}, gender:{self.gender},research_interest:{self.research_interest},paper_count:{self.paper_count},papers:{papers})'

#     def to_json(self):
#         if isinstance(self, Person):
#             return (self.__str__())
#         raise TypeError((self.__str__()) + ' is not JSON serializable')


# class Data:
#     # Get node embeddings from node2vec

#     # Number of walks: Number of random walks to be generated from each node in the graph
#     # Walk length: How many nodes are in each random walk
#     # P: Return hyperparameter
#     # Q: Inout hyperaprameter
#     # self.personsIds: all people nodes in the system both GEI(only academic) and externalPersons
#     # self.personsNames: all people names in the system both GEI(only academic) and externalPersons

#     #     def __init__(self,node2vec_G,model,G):
#     #         self.node2vec_G,self.model,self.G=node2vec_G,model,G
#     def __init__(self, pickle_file_path, file_path_with_mapped_research_interest):

#         start = time.time()
#         print("info level: 1")

#         self.node2vec_G, self.model, self.G = self.setUp(pickle_file_path)
#         print("info level: 2 with time: " + str(time.time() - start))  # took 1498.3578605651855 seconds / 24.97 minutes

#         self.personsIds, _, self.personsName_GEI, self.personId_GEI = self.get_person_details(self.G)
#         print("info level: 3 with time: " + str(time.time() - start))  # did not estimate

#         self.personIds, self.researchInt_ids = self.get_personIDs_and_researchinterestIDs(self.G)
#         print("info level: 4 with time: " + str(time.time() - start))  # took 0.0488798618 seconds

#         self.p_ids_withRI, self.research_interests_nameasKey, self.research_interests_IDasKey, person_name_withRI = self.get_researchInterests(
#             self.G, self.personIds, self.researchInt_ids)
#         print("info level: 5 with time: " + str(time.time() - start))  # took 0.0781748295 seconds

#         self.sim_matrix, self.hop_matrix = self.get_hop_dist_or_similarity(self.G, self.model, (
#                     self.personsIds + list(self.researchInt_ids.keys())), top_n=500, cutoff_hop_dist=8)
#         print("info level: 6 with time: " + str(time.time() - start))  # took 927.598469 / 15.46 minutes

#         self.scores_List, self.persons_dict = self.write_scoresToList(self.sim_matrix, self.hop_matrix)
#         print("info level: 7 with time: " + str(time.time() - start))  # took 9.98162937 seconds

#         self.persons = self.get_personsList(self.G, file_path_with_mapped_research_interest)
#         print("info level: 8 with time: " + str(time.time() - start))  # took 27.5489626 seconds

#     def get_embeddings(self, G, d=25, walk_len=25, no_walks=100, param_p=1, param_q=1):

#         node2vec_subgraph_comb2 = Node2Vec(G, dimensions=d, walk_length=walk_len, num_walks=no_walks, p=param_p,
#                                            q=param_q)
#         model = node2vec_subgraph_comb2.fit(window=10, min_count=1)

#         return node2vec_subgraph_comb2, model

#     # read the graph data from pickle file

#     def setUp(self, pickle_file_path):
#         G = nx.read_gpickle(pickle_file_path)
#         # print(G)

#         node2vec_G, model = self.get_embeddings(G, d=50, walk_len=50, no_walks=50, param_p=0.5, param_q=2)
#         return node2vec_G, model, G

#     # to do: how to load model and model weights
#     # print the nodes from the graph
#     # def print_nodes(self, G):
#     #     for nodes in G.nodes:
#     #         print(nodes)

#     # Get person name and ids
#     def get_person_details(self, G):
#         totalExternalPersonsIds = []
#         totalPersonsIds = []
#         totalExternalPersonsName = []
#         totalPersonsName = []
#         personsName_GEI = []
#         personId_GEI = []

#         # Find total persons counts.
#         for node_id in search_nodes(G, {"==": [("label",), "Person"]}):
#             if G.nodes[node_id]['staffType'] == "Academic":
#                 totalPersonsIds.append(node_id)
#                 # Getting Total external persons names in list.
#                 totalPersonsName.append(G.nodes[node_id]['name'] + "(P)")
#                 personsName_GEI.append(G.nodes[node_id]['name'])
#                 personId_GEI.append(node_id)

#         # Find total external persons counts.
#         totalExternalPersonsIds = list()
#         for node_id in search_nodes(G, {"==": [("label",), "External person"]}):
#             totalExternalPersonsIds.append(node_id)
#             # Getting Total persons names in list.
#             totalExternalPersonsName.append(G.nodes[node_id]['name'] + "(EP)")

#         totalPeopleIds = totalPersonsIds + totalExternalPersonsIds
#         totalPeopleNames = totalPersonsName + totalExternalPersonsName

#         # TODO: remove 
#         print(f"-- debugging: {len(totalPeopleIds)}")

#         return totalPeopleIds, totalPeopleNames, personsName_GEI, personId_GEI

#     def get_personIDs_and_researchinterestIDs(self, G):
#         personIds = {}
#         researchInt_ids = {}
#         for node_id in search_edges(G, {"==": [("label",), "interestedIn"]}):
#             personIds[node_id[0]] = G.nodes[node_id[0]]
#             researchInt_ids[node_id[1]] = G.nodes[node_id[1]]
#         return personIds, researchInt_ids

#     def get_researchInterests(self, G, personIds, researchInt_ids):
#         research_interests_nameasKey = {}
#         research_interests_IDasKey = {}
#         p_ids_withRI = []  # people Ids with Research Interests.
#         person_name_withRI = []  # people names with Research Interests.
#         # personIds, researchInt_ids = self.get_personIDs_and_researchinterestIDs(G)
#         for personId, researchInt_id in search_edges(G, {"==": [("label",), "interestedIn"]}):
#             p_ids_withRI.append(personId)
#             person_name_withRI.append(personIds[personId]['name'])
#             if personIds[personId]['name'] not in research_interests_nameasKey.keys():
#                 res_Ints = []
#                 res_Ints.append(researchInt_ids[researchInt_id]['name'])

#                 res_Ints1 = []
#                 res_Ints1.append(researchInt_ids[researchInt_id]['name'])

#                 research_interests_nameasKey[personIds[personId]['name']] = res_Ints
#                 research_interests_IDasKey[personId] = res_Ints1
#             else:
#                 research_interests_nameasKey[personIds[personId]['name']].append(
#                     researchInt_ids[researchInt_id]['name'])
#                 research_interests_IDasKey[personId].append(researchInt_ids[researchInt_id]['name'])
#         return p_ids_withRI, research_interests_nameasKey, research_interests_IDasKey, person_name_withRI

#     def create_empty_df(self, COLUMN_NAMES):
#         zero_data = np.zeros(shape=(len(COLUMN_NAMES), len(COLUMN_NAMES)))

#         dataframe = pd.DataFrame(zero_data, columns=COLUMN_NAMES, index=COLUMN_NAMES)
#         return dataframe

#     # NOTE:person has less similarity then external person even thought all perons are connected via GEI.
#     # to compute the Similarity_matrix for all available usrs in the graph use this instead of p_ids. totalPeopleIds.
#     # p_ids is the nodeIds of people who have ResearchInterest in the graphDB.

#     def get_hop_dist_or_similarity(self, G, model, p_ids, top_n=52, cutoff_hop_dist=8):
#         sim_matrix = self.create_empty_df(p_ids)
#         hop_matrix = self.create_empty_df(p_ids)
#         for p_id in p_ids:
#             similarNodes = model.wv.most_similar(p_id, topn=len(p_ids))
#             similarPeople = []
#             x = '(EP)' if (G.nodes[p_id]['label'] == "External person") else '(P)'
#             col_name = p_id

#             for similarity in similarNodes:
#                 similarNode = similarity[0]
#                 distance = 0
#                 if ((G.nodes[similarNode]['label'] == "Person" and G.nodes[similarNode]['staffType'] == "Academic") or
#                         G.nodes[similarNode]['label'] == "External person"):

#                     s = '(EP)' if (G.nodes[similarNode]['label'] == "External person") else '(P)'
#                     row_name = similarNode
#                     hop_dist = 0
#                     if (similarNode in nx.single_source_shortest_path_length(G, p_id, cutoff=cutoff_hop_dist).keys()):
#                         hop_dist = nx.single_source_shortest_path_length(G, p_id, cutoff=cutoff_hop_dist)[similarNode]
#                         hop_matrix.loc[row_name, col_name] = hop_dist
#                         hop_matrix.loc[col_name, row_name] = hop_dist
#                     distance = similarity[1]
#                     sim_matrix.loc[row_name, col_name] = distance
#                     sim_matrix.loc[col_name, row_name] = distance

#         return sim_matrix, hop_matrix

#     def get_personsList(self, G, file_path_with_mapped_research_interest):
#         with open(file_path_with_mapped_research_interest, 'r') as fp:
#             file = pd.read_csv(fp)
#         del file['Unnamed: 0']
#         authors_list = []
#         researchInterest_list = []
#         for row in range(0, len(file)):
#             a = file.loc[row][9].replace("[", "").replace("]", "").lstrip().rstrip().replace("'", "").split(",")
#             b = file.loc[row][8].replace("[", "").replace("]", "").lstrip().rstrip().replace("'", "").split(",")
#             gen = (itertools.product(a, b))
#             for u, v in gen:
#                 # print(u.lstrip().rstrip(), ":", v.lstrip().rstrip())
#                 authors_list.append(u.lstrip().rstrip())
#                 researchInterest_list.append(v.lstrip().rstrip())

#         auth_reseachDF = pd.DataFrame({"Autors": authors_list, "ResearchList": researchInterest_list})
#         # auth_reseachDF['ResearchList'] = [x if x != 'Eductaion' else 'Education' for x in auth_reseachDF['ResearchList']]
#         # auth_reseachDF['ResearchList'] = [x if x != 'Information Retrieval' else 'Information retrieval' for x in auth_reseachDF['ResearchList']]

#         # auth_reseachDF['ResearchList'] = [x if x != 'Natural langauge processing' else 'Natural language processing' for x in auth_reseachDF['ResearchList']]

#         # auth_reseachDF['ResearchList'] = [x if x != 'Natural language processing' else 'Natural language processing' for x in auth_reseachDF['ResearchList']]

#         # auth_reseachDF['ResearchList'] = [x if x != 'Political sciences.' else 'Political sciences' for x in auth_reseachDF['ResearchList']]

#         df = auth_reseachDF.groupby(['Autors', 'ResearchList']).size().unstack(fill_value=0)
#         s = df.mask(df == 0).stack().astype(int).astype(str).reset_index(level=1).apply('-'.join, 1).add(',').sum(
#             level=0).str[:-1]
#         arrays = np.where(df != 0, df.columns.values + '-' + df.values.astype('str'), None)

#         new = []
#         for array in arrays:
#             new.append(list(filter(None, array)))

#         s = df.mask(df == 0).stack(). \
#                 astype(int).astype(str). \
#  \
#                 reset_index(level=1).apply('-'.join, 1).add('-').sum(level=0).str[:-1]

#         s = pd.DataFrame({'authorsUUID': s.index, 'count': s.values})

#         temp = {}
#         ri_lst = []
#         cnt_lst = []
#         for cnt in range(0, len(s)):
#             x = (s['count'][cnt]).split("-")
#             ri_lst.append(x[0::2])
#             cnt_lst.append([int(i) for i in x[1::2]])

#         research_int = {}
#         cnt = 0

#         for auth in s['authorsUUID']:
#             if auth not in research_int.keys():
#                 lst = {}
#                 lst['research_interest'] = (ri_lst[cnt])
#                 lst['paper_count'] = (cnt_lst[cnt])
#                 research_int[auth] = lst
#                 cnt += 1
#             #   print(auth,research_int[auth])

#         persons = []
#         for node_id in self.personsIds:
#             # print(G.nodes[node_id])
#             if ("staffType" in G.nodes[node_id].keys() and G.nodes[node_id]['staffType'] == "Academic") or G.nodes[node_id][
#                 'label'] == "External person":

#                 nation = G.nodes[node_id]['nationality'] if (G.nodes[node_id]['label'] == "Person") else G.nodes[node_id][
#                     'country']

#                 gen = G.nodes[node_id]['gender'] if (G.nodes[node_id]['label'] == "Person") else "Not-Given"
#                 papers = []
#                 for auth_id, researchOutput_id in search_edges(G, {"==": [("label",), "writtenBy"]}):
#                     if (auth_id == node_id):

#                         papers.append(Paper(uuid=researchOutput_id, title=G.nodes[researchOutput_id]['title'],
#                                             abstract=G.nodes[researchOutput_id]['abstract'],
#                                             pType=G.nodes[researchOutput_id]['type']))
#                         pc = []
#                         ri = []
#                         if node_id in research_int.keys():
#                             pc = research_int[node_id]['paper_count']
#                             ri = research_int[node_id]['research_interest']
#                         if node_id in self.research_interests_IDasKey.keys():
#                             x = list(set(np.unique(self.research_interests_IDasKey[node_id])) - set(ri))
#                             ri = ri + x
#                             pc = pc + list(np.zeros(len(x)))
#                 persons.append(Person(uuid=node_id, name=G.nodes[node_id]['name'], nationality=nation, gender=gen,
#                                     research_interest=ri, paper_count=pc, papers=papers))
                                    
#         # TODO: remove 
#         print(f"-- debugging: {len(persons)}")
#         return persons


#     def write_scoresToList(self, sim_matrix, hop_matrix):
#         persons_dict = {}
#         scores_List = []
#         for ind, i in enumerate(sim_matrix):
#             s = []
#             h = []
#             empty_list = {}
#             for _, j in enumerate(sim_matrix):
#                 s.append(sim_matrix[i][j])
#                 h.append(hop_matrix[i][j])
#                 empty_list['uuid'] = sim_matrix.index[ind]
#                 empty_list["hop_dist"] = h
#                 empty_list["sim_score"] = s
#             scores_List.append(empty_list)
#             persons_dict[sim_matrix.index[ind]] = i
#         return scores_List, persons_dict