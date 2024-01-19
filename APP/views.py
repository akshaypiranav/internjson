#INTERN AKSHAY PIRANAV B
#@akshaypiranavb@gmail.com

from django.shortcuts import render
from django.contrib import messages
import json


def home (request):
    class JsonValidator: #created a class as mentioned in the task 3

        def validate_schema(self, json_data: str, schema_file: str) -> bool:

            try:
            
                # Validate required fields based on the schema
                if not self.validate_required_fields(json_data, schema):
                    return False

                # Validate at least one of many fields based on the schema
                if not self.validate_at_least_one_of(json_data, schema):
                    return False

                # Validate either one field or another field based on the schema
                if not self.validate_either_one_or_another(json_data, schema):
                    print("inner")
                    return False

                # Validate mutually exclusive fields based on the schema
                if not self.validate_mutually_exclusive_fields(json_data, schema):
                    return False

                # Validate field value to be one of a set of values based on schema
                if not self.validate_field_values(json_data, schema):
                    return False

                return True

            except :
                return False

        def validate_required_fields(self, json_data, schema) -> bool:
            """
                Validates if the required fields specified in the schema are present in the provided JSON data.
                :param json_data: The JSON data to be validated.
                :type json_data: dict
                :param schema: The schema containing information about required fields.
                :type schema: dict
                :return: True if all required fields are in the json file, False otherwise.
                :rtype: bool
            """
            required_fields = schema.get("required", [])
            for field in required_fields:
                if field not in json_data:
                    messages.warning(request,f"{field} not in the Uploaded Json file")
                    return False
            return True

        def validate_at_least_one_of(self, json_data, schema) -> bool:
            """
                Validates that at least one of the fields specified in the 'oneOf' section of the schema is present in the JSON data.
                :param json_data: The JSON data to be validated.
                :type json_data: dict
                :param schema: The schema containing information about 'oneOf' fields.
                :type schema: dict
                :return: True if at least one of the specified fields is present, False otherwise.
                :rtype: bool
            """
            one_of_fields = schema.get("oneOf", [])
            print(one_of_fields)
            if not any(field in json_data for field in one_of_fields):
                messages.warning(request,"home_phone or cell_phone or work_phone need atleast one of these fields")
                return False
            return True

        def validate_either_one_or_another(self, json_data, schema) -> bool:
            """
                Validates that either one or both of the fields specified in the 'either' section of the schema are present in the JSON data.
                :param json_data: The JSON data to be validated.
                :type json_data: dict
                :param schema: The schema containing information about 'either' fields.
                :type schema: dict
                :return: True if either one or both of the specified fields are present, False otherwise.
                :rtype: bool
            """
            either_fields = schema.get("either", [])
            present_either_fields = set(either_fields).intersection(set(json_data.keys()))
            if len(present_either_fields) not in [1, 2]:
                messages.warning(request," either birth_date field or govt_id_number field need to be in")
                print("Birthday or govt id")
                return False
            return True

        def validate_mutually_exclusive_fields(self, json_data, schema) -> bool:
            """
                Validates that mutually exclusive fields, specified in the 'mutuallyExclusive' section of the schema, are not both present in the JSON data.
                :param json_data: The JSON data to be validated.
                :type json_data: dict
                :param schema: The schema containing information about mutually exclusive fields.
                :type schema: dict
                :return: True if mutually exclusive fields are not both present, False otherwise.
                :rtype: bool
            """
            mutually_exclusive_fields = schema.get("mutuallyExclusive", [])
            for group in mutually_exclusive_fields:
                present_fields = set(group).intersection(set(json_data.keys()))
                if len(present_fields) > 1:
                    messages.warning(request,f"Mutually exclusive fields {group} are both present.")
                    print("Number")
                    return False
            return True

        def validate_field_values(self, json_data, schema) -> bool:
            """
                Validates that the values of certain fields specified in the 'enum' section of the schema are among the allowed values.
                :param json_data: The JSON data to be validated.
                :type json_data: dict
                :param schema: The schema containing information about fields with allowed values.
                :type schema: dict
                :return: True if the values of specified fields are allowed, False otherwise.
                :rtype: bool
            """
            enum_fields = schema.get("enum", {})
            for field, allowed_values in enum_fields.items():
                if field in json_data and json_data[field] not in allowed_values:
                    messages.warning(request,'Value of day should be "SU", "MO", "TU", "WE", "TH", "FR", "SA"')
                    print("problem in enum so failed")
                    return False
            return True


    if request.method == 'POST':
        
        if request.FILES.get("jsonFile") is not None:
            json_file = request.FILES.get('jsonFile')
            try:
                json_data = json.load(json_file)
            except :
                messages.error(request,"Need a Json File to Validate")

            json_validator = JsonValidator()
                
            schema = {
                        "required": ["id", "name"],
                        "oneOf": ["home_phone", "cell_phone", "work_phone"],
                        "either": ["birth_date", "govt_id_number"],
                        "mutuallyExclusive": [["home_phone", "work_phone"]],
                        "enum": {
                        "day": ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]
                                }
                    }

            #Below validation is based on the given example in the task 3
            if json_validator.validate_schema(json_data, schema): #passing the json data and the schema to the validate_schema method
                messages.success(request,"Json Validation succesfully done")

        else:
            messages.warning(request,"Need a Json File to Validate")
            print("hhhh")
    return render(request,"index.htm")