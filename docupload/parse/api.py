import requests



def get_data(qstn, similarText):
    api_key = "AIzaSyAwHJtMsF_sHOUhb1O8DDlse495WD-_C-w"
    api_url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={api_key}"
    final_result = ''
    final_request_body = {
        "prompt": {
            "text": similarText + '\n' + qstn
        },
        "temperature": 0.7,
        "candidate_count": 1
    }
    final_response = requests.post(api_url, json=final_request_body, headers={'Content-Type': 'application/json'})
    final_response_data = final_response.json()
    if 'candidates' in final_response_data:
        final_result += final_response_data['candidates'][0]['output']
        print(final_result)
    return final_result










    
   

