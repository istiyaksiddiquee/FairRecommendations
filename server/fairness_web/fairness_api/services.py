import tables as pt 

from h5.repository_access import RepoAccess


class RecommendationService():

    def __init__(self, filename):
        self.read_mode = pt.open_file(filename, 'r')
        self.access = RepoAccess(self.read_mode)

    def get_recommendation(self, req_uuid, req_research_interest, weight_for_similarity):
        obj_array = self.access.get_similarity(req_uuid, req_research_interest)
        self.read_mode.close()

        scored_items = []
        for item in obj_array:

            scored_items.append(ResponseStructure(item.uuid, item.first_name, 
                                item.last_name, item.affiliation, 
                                item.research_interest, item.gender, 
                                item.hop_distance, item.cosine_sim, 
                                (float(weight_for_similarity)*item.hop_distance + (1-float(weight_for_similarity)) *item.cosine_sim)))
        
        with_bias = self.sort_biased_array(scored_items)
        bias_corrected = self.sort_bias_processed_array(scored_items)
        bias_corrected = self.add_reference_to_bias_corrected_data(with_bias, bias_corrected)
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
                output_arr.append ({
                    'uuid': item.uuid, 
                    'first_name': item.first_name,
                    'last_name': item.last_name, 
                    'affiliation': item.affiliation,
                    'research_interest': item.research_interest,
                    'gender': item.gender, 
                    'hop_distance': item.hop_distance,
                    'cosine_sim': item.cosine_sim,
                    'score': item.score
                })
        else:
            for item in obj_array:
                output_arr.append ({
                    'uuid': item.uuid, 
                    'first_name': item.first_name,
                    'last_name': item.last_name, 
                    'affiliation': item.affiliation,
                    'research_interest': item.research_interest,
                    'gender': item.gender, 
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


class ResponseStructure():
    def __init__(self, uuid, first_name, last_name, affiliation, research_interest, gender, hop_distance, cosine_sim, score):
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name
        self.affiliation = affiliation
        self.research_interest = research_interest
        self.gender = gender
        self.hop_distance = hop_distance
        self.cosine_sim = cosine_sim
        self.score = score
        