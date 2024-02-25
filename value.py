import requests

def json_data(var_id, region_id):
    payload = {
        'var-id': var_id
        }
    response = requests.get('https://bdl.stat.gov.pl/api/v1/data/by-unit/{region}'.format(region = region_id), params=payload)
    response_json = response.json()
    return response_json

def processing_data_with_tags (data, quarter_tag, region_tag):
    response_array = []
    for result in data['results']:
        for value in result['values']:
            data_dict = {
                'year': value['year'],
                'value': value['val'],
                'quarter': quarter_tag,
                'region': region_tag
                }
            response_array.append(data_dict)
    return response_array
   
# main function
def get_from_api(var_id_list):
    answer_array = []
    #iterating through list
    for i in range(0, len(var_id_list), 2):
        #region indicies [i]:
        var_id_region_dict = var_id_list[i]
        #quarter indicies [i+1]:
        var_id_quarter_dict = var_id_list[i+1]

        for var_id_region_dict_key, var_id_region_dict_value in var_id_region_dict.items():
            for var_id_quarter_dict_key, var_id_quarter_dict_value in var_id_quarter_dict.items():
                answer = processing_data_with_tags(
                    json_data(var_id_quarter_dict_value,var_id_region_dict_value ),
                    var_id_quarter_dict_key, var_id_region_dict_key
                )
                answer_array += answer
    return answer_array

# For testing module:
# calling main function
#print (get_from_api())
