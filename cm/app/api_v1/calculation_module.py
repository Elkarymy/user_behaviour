import numpy as np
import pandas as pd
import os
#from ..helper import generate_output_file_csv, generate_output_file_tif, create_zip_shapefiles
#from ..constant import CM_NAME

from ..api_v1.my_calculation_module_directory.setpoint_filtering import filter_data_general

path2data = os.path.split(os.path.abspath(__file__))[0]
#needs to be added
temperature_data_path = os.path.join(path2data, "my_calculation_module_directory/data/thermal_expectations.csv")
#needs to be added
#unfiltered_interventions_csv = os.path.join(path2data, "my_calculation_module_directory/data/interventions_per_nuts0.csv")
unfiltered_setpoints_csv = os.path.join(path2data, "my_calculation_module_directory/data/setpoints_per_nuts0.csv")

#this part provides filtering the setpoints and overheating limits for space cooling, customized to the country specific legislative background
#get data from csv
unfiltered_setpoints_dataframe = pd.read_csv(unfiltered_setpoints_csv, sep=";")
#unfiltered_interventions_dataframe = pd.read_csv(unfiltered_interventions_csv, sep=";")
#not sure this will be dataframe or numpy
preferred_temperatures_dataframe = pd.read_csv(unfiltered_interventions_csv, sep=",")

def calculation(output_directory, inputs_parameter_selection):
    result = dict()
    result['name'] = CM_NAME
    #this part filters the setpoints
    nuts_code = str(inputs_parameter_selection["nuts0_code"])
    nuts_id = unfiltered_setpoints_dataframe['NUTS_ID'].values
    filtered_setpoints_dataframe = filter_data_general(unfiltered_setpoints_dataframe, nuts_code, 'NUTS_ID')

    indicator_names = filtered_setpoints_dataframe.iloc[:, 1]
    indicator_name = indicator_names.tolist()
    indicator_values = filtered_setpoints_dataframe.iloc[:, 2]
    indicator_value = indicator_values.tolist()

    #needs to be figured out still
    #if nuts_code='ALL':

    #maximum 5 custom indicators can be plotted for the setpoints

    if len(indicator_name) > 0:
       result['indicator'] = [
            {"unit": " ", "name":str(indicator_name[0]), "value": str(indicator_value[0])},
                       ]
       if len(indicator_name) > 1:
            result['indicator'] = [
                {"unit": " ", "name": str(indicator_name[0]), "value": str(indicator_value[0])},
                {"unit": " ", "name": str(indicator_name[1]), "value": str(indicator_value[1])},
                           ]
            if len(indicator_name) > 2:
                result['indicator'] = [
                    {"unit": " ", "name": str(indicator_name[0]), "value": str(indicator_value[0])},
                    {"unit": " ", "name": str(indicator_name[1]), "value": str(indicator_value[1])},
                    {"unit": " ", "name": str(indicator_name[2]), "value": str(indicator_value[2])},
                ]
                if len(indicator_name) > 3:
                    result['indicator'] = [
                        {"unit": " ", "name": str(indicator_name[0]), "value": str(indicator_value[0])},
                        {"unit": " ", "name": str(indicator_name[1]), "value": str(indicator_value[1])},
                        {"unit": " ", "name": str(indicator_name[2]), "value": str(indicator_value[2])},
                        {"unit": " ", "name": str(indicator_name[3]), "value": str(indicator_value[3])},
                    ]
                    if len(indicator_name) > 4:
                        result['indicator'] = [
                            {"unit": " ", "name": str(indicator_name[0]), "value": str(indicator_value[0])},
                            {"unit": " ", "name": str(indicator_name[1]), "value": str(indicator_value[1])},
                            {"unit": " ", "name": str(indicator_name[2]), "value": str(indicator_value[2])},
                            {"unit": " ", "name": str(indicator_name[3]), "value": str(indicator_value[3])},
                            {"unit": " ", "name": str(indicator_name[4]), "value": str(indicator_value[4])},
                        ]
    else:
        print("no available data")

    # this part filters the interventions
    intervention_type = str(inputs_parameter_selection["intervention_type"])
    building_type = str(inputs_parameter_selection["building_type"])

 #   filtered_interventions_dataframe = filter_data_general(unfiltered_interventions_dataframe, nuts_code, 'NUTS_ID')

    #intervention_names = filtered_interventions_dataframe.iloc[:, 1]
    #intervention_name = intervention_names.tolist()
    #intervention_values = filtered_interventions_dataframe.iloc[:, 2]
    #intervention_value = intervention_values.tolist()

#this part extends the results with interventions
    result["indicator"].extend(
            [ {"unit": " ", "name": str(intervention_name[0]), "value": str(intervention_value[0])}]
                        )
    #not sure if needed, this was here:https://github.com/HotMaps/biomass_potential/blob/develop/cm/app/api_v1/calculation_module.py#L255
    #result["indicator"].extend(indicators)
    # could be useful      {"unit": "-", "name": msg, "value": 0} for msg in warnings]

 #------- needs to be cleaned-------

    # Filter the data
    #filtered_intervention_data = filter_data_general(df, intervention_type=intervention_type,
     #                           building_type=building_type)


    #path_nuts_id_tif = inputs_raster_selection["nuts_id_number"]
    #nuts0_codes = return_nuts_codes(path_nuts_id_tif)
    #temperature_data = pd.read_csv(temperature_data_path)
    #ids = temperature_data['NUTS_ID'].values
    #selected_areas = ", ".join(nuts0_codes)


    #this third part shows the pie chart

    filtered_pref_temp_dataframe = filter_data_general(preferred_temperatures_dataframe, nuts_code, 'NUTS_ID')
    temperature_categories = filtered_pref_temp_dataframe.iloc[:, 1]
    temperature_values = filtered_pref_temp_dataframe.iloc[:, 2]

#colours from Hotmaps. Check labelling, not sure
    graphics = [{
                "type": "pie",
                "data": {
                    "labels": temperature_categories.tolist(),
                    "datasets": [
                        {
                            "label": "Preferred indoor comfort temperatures in %s" %nuts_code,
                            "backgroundColor": ['#0072B2', '#E69F00', '#F0E442', '#009E73', '#56B4E9', '#D55E00'],
                            "data": temperature_values.tolist()
                        }
                    ]
                        }
            }]

    result['graphics'] = graphics


    return result
