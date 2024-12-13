import requests

def update_collection(field_data: dict):
    # collection ID is the URL

    verify_dictionary_fields(field_data)
    field_data["author"] = "Citizen Insights AI"
    if verify_dictionary_fields(field_data):
        url = "https://api.webflow.com/v2/collections/675916f5dab2bcd62c392f72/items"
        headers = {
            "Authorization": "Bearer 3c80a854b7864f53ad11d598080e90974d52b3843ec990e93d5238cb288f68d1",
            "Content-Type": "application/json"
        }
        data = {
            "isArchived": False,
            "isDraft": False,
            "fieldData": field_data,
            #     {
            #     "data-source": "https://example.com/social-media-data",
            #     "last-updated": "2023-07-25T00:00:00.000Z",
            #     "key-visualisation-link": "https://example.com/social-media-visualisation",
            #     "name": "Test Social Media Report",
            #     "author": "Synthia",
            #     "reporting-agency": "Social Media Analytics",
            #     "key-insight": "<h1>Key Insights</h1><p>The social media landscape is rapidly changing, with video content dominating engagement metrics. Brands that leverage video are seeing a 50% increase in audience interaction.</p>",
            #     "methodology": "<h1>Methodology</h1><p>Data was collected from social media platforms and user engagement analytics. We analyzed trends in content consumption and audience preferences.</p>",
            #     "slug": "social-media-report-2023",
            #     "data-source-name": "Data.gov.sg",
            #     "source-name": "asdasdas"
            # }
        }
        response = requests.post(url, headers=headers, json=data)
        print(response.text)
    else:
        print("Missing fields")

def verify_dictionary_fields(data_dict):
    """
    Verify if the dictionary has all the relevant fields.

    Parameters:
        data_dict (dict): The dictionary to be verified.

    Returns:
        bool: True if all required fields are present, False otherwise.
        list: A list of missing fields if any.
    """
    # Define the set of required fields
    required_fields = {
        "data-source",
        "last-updated",
        # "key-visualisation-link",
        "name",
        # "author",
        "reporting-agency",
        "key-insight",
        # "methodology",
        "slug",
        "data-source-name",
        # "source-name"
    }
    # Get the missing fields
    missing_fields = required_fields - data_dict.keys()

    # Return the result
    if not missing_fields:
        return True, None  # All required fields are present
    else:
        return False, list(missing_fields)  # Return missing fields


