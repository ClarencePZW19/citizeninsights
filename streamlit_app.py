import streamlit as st
import re
import json
import pandas as pd
import datasets_list
import vertex_integration
import webflow_integration
import time
import importlib

# import csv

# the below is to take a response python code and run it within the code
# result = subprocess.run(['python', 'your_script.py'], capture_output=True, text=True)
# Initialize session state for JSON data and selected name
if 'json_data' not in st.session_state:
    st.session_state.json_data = None

if 'selected_name' not in st.session_state:
    st.session_state.selected_name = "Please select"

if 'generated_insights' not in st.session_state:
    st.session_state.generated_insights = ""

if 'generated_visualisation' not in st.session_state:
    st.session_state.generated_visualisation = ""

# if 'generated_' not in st.session_state:
#     st.session_state.generated_text = None
def reset_session():
    st.session_state.json_data = None
    st.session_state.selected_name = "Please select"
    st.session_state.generated_insights = ""

def display_json_data():
    """
    This function takes a JSON array of objects, creates a dropdown for each object's 'name' key,
    and displays the JSON objects as rows in a table.

    :param json_data: List of JSON objects
    """
    if not st.session_state.json_data:
        st.error("No data available to display.")
        return

    json_data = st.session_state.json_data
    names_to_objects = {obj["name"]: obj for obj in json_data if "name" in obj}
    sorted_names = sorted(names_to_objects.keys())

    if not sorted_names:
        st.error("No 'name' keys found in the JSON data.")
        return

    try:
        dataframe = pd.DataFrame(json_data)
        st.write("### Table displaying JSON objects as rows:")
        st.dataframe(dataframe)
    except Exception as e:
        st.error(f"Error converting JSON data to a table: {e}")

    selected_name = st.selectbox(
        "Please select from one of the following datasets",
        options=["Please select"] + sorted_names,
        index=sorted_names.index(
            st.session_state.selected_name) + 1 if st.session_state.selected_name in sorted_names else 0
    )

    st.session_state.selected_name = selected_name
    print(selected_name)

import importlib


def handle_visualisation(viz_type,**kwargs):
    """
    Dynamically find and invoke a function in 'visualisations.py' based on the given `viz_type`.

    Parameters:
        viz_type (str): The name of the visualization function to call.
        *args: Positional arguments to pass to the visualization function.
        **kwargs: Keyword arguments to pass to the visualization function.

    Returns:
        The result of the visualization function, or an error message if not found.
    """
    try:
        # Dynamically import the visualisations module
        visualisations = importlib.import_module("visualisations")

        # Check if the function exists in the module
        if hasattr(visualisations, viz_type):
            # Fetch the function based on viz_type
            visualization_function = getattr(visualisations, viz_type)
            # Call the function and return the result
            # print(**args)
            # print(visualization_function)
            # print(
            #     f"Calling visualization function '{viz_type}' with args: {args}"
            # )
            print(kwargs)
            print(visualization_function(kwargs))
            return visualization_function(kwargs)
        else:
            raise AttributeError(f"No visualization function named '{viz_type}' found in 'visualisations.py'.")
    except ModuleNotFoundError:
        return "Error: 'visualisations.py' module not found."
    except AttributeError as e:
        return str(e)
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


# start of app code
st.title("This is the start of our AI journey zoom zoom bam bam")
st.write(
    "Let's start building! Jeng Jeng"
)

if st.button("click me to send a collection to webflow"):
    update_collection = webflow_integration.update_collection()

if st.button("click me to view list of blobs in cloud storage"):
    try:
        st.session_state.json_data = datasets_list.download_blob()
        st.write("Data loaded")
    except Exception as e:
        st.error(f"Error loading data: {e}")

if st.session_state.json_data:
    display_json_data()

# Check if a valid selection is made
if st.session_state.selected_name != "Please select":
    st.write(f"You selected: {st.session_state.selected_name}")
    selected_object = {obj["name"]: obj for obj in st.session_state.json_data}.get(st.session_state.selected_name)
    if selected_object:
        print("there is an object")
        if st.button("Generate content for selected dataset"):
            try:
                dataset_id = selected_object['datasetId']
                st.write(f"Generating content for datasetID: {dataset_id}")

                # doublecheck the format
                response = None
                try:
                    format = selected_object['format']
                    if format == 'XLSX':
                        response = vertex_integration.datagov_xlsx_request(dataset_id)
                    elif format == 'GEOJSON':
                        response = vertex_integration.datagov_geojson_request(dataset_id)
                    elif format == 'CSV':
                        response = vertex_integration.datagov_csv_request(dataset_id)
                    else:
                        st.error("Invalid format. Please select a valid format.")
                    # st.write(response)
                    #generating insights
                    # if response is not None:
                    #     model_data = vertex_integration.generate(response,dataset_id)
                    #     for data in model_data:
                    #         st.session_state.generated_insights = st.session_state.generated_insights + data.text

                    #generating visualisation
                    if response is not None:
                        model_data = vertex_integration.generate_visualisation(response,dataset_id)
                        for data in model_data:
                            st.session_state.generated_visualisation = st.session_state.generated_visualisation + data.text

                except Exception as e:
                    st.error(f"Error generating content: {e}")

            except Exception as e:
                st.error(f"Error generating content: {e}")
    print('reached the end')

# need to update this and check both insights and visualisation

sample_data = {"viz_type":"line_chart","data":[{"financial_year":"2010","arrears_rate":1.29},{"financial_year":"2011","arrears_rate":0.94},{"financial_year":"2012","arrears_rate":0.79},{"financial_year":"2013","arrears_rate":0.77},{"financial_year":"2014","arrears_rate":0.81},{"financial_year":"2015","arrears_rate":0.62},{"financial_year":"2016","arrears_rate":0.68},{"financial_year":"2017","arrears_rate":0.68},{"financial_year":"2018","arrears_rate":0.87},{"financial_year":"2019","arrears_rate":0.79},{"financial_year":"2020","arrears_rate":0.72},{"financial_year":"2021","arrears_rate":0.64},{"financial_year":"2022","arrears_rate":0.59},{"financial_year":"2023","arrears_rate":0.64}],"x_col":"financial_year","y_col":"arrears_rate"}
if st.button("test visualisations"):
    # Filter parameters to only send the non-empty ones
    filtered_params = {key: value for key, value in sample_data.items() if value is not None}
    # print(filtered_params)
    viz_type = filtered_params.pop('viz_type')
    # print(filtered_params)
    print("viz_type is:" + viz_type)
    print(filtered_params)
    handle_visualisation(viz_type,filtered_params)

    handle_visualisation()


if st.session_state.generated_visualisation != "":
    # change it to json
        pass





if st.session_state.generated_insights != "":
    #
    # st.write(st.session_state.generated_insights)
    # json_string = st.session_state.generated_insights
    #
    # # Find the start index of the JSON part
    # start_index = json_string.find("{")
    #
    # # Assuming the JSON is well-formed, find the end index
    # end_index = json_string.rfind("}") + 1
    #
    # json_string_sliced = json_string[start_index:end_index]
    # webflow_payload = json.loads(json_string_sliced)
    # st.write(webflow_payload)
    # webflow_integration.update_collection(webflow_payload)
    # reset_session()
    # print(json.loads(st.session_state.generated_insights))
    print("reached this checkpoint")





