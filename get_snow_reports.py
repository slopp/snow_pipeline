from google.cloud import storage
import requests 
import json
from datetime import datetime

def handle_report(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    data_to_store = get_resorts()
    if len(data_to_store) < 1:
        return 'All attempts to get resort data failed, nothing to upload'

    temp_file_base = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    for i in data_to_store:
        file_name = temp_file_base + '_' + data_to_store[i][0]['id'] +'_snowreport.json'
        # print(json.dumps(data_to_store[i][0]))
        upload_blob('snow-data-staging', json.dumps(data_to_store[i][0]), file_name)

    return f'Success'
    

def get_resorts():
    ids = ["303001", "303007", "303009", "303011", "303014", "303015", "303017"]
    resorts = dict()
    for i in ids:
        request_url = 'http://feeds.snocountry.net/conditions.php?apiKey=SnoCountry.example&ids=' + i
        response = requests.get(request_url)
        if response.status_code != 200:
            print("Something failed requesting: "+request_url)
        else:
            resorts[i] = response.json()['items']
    return resorts


def upload_blob(bucket_name, data, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    print(
        "Data uploaded to {}.".format(
            destination_blob_name
        )
    )

# if __name__ == "__main__":
#     handle_report({})