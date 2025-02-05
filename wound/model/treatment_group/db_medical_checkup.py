from wound.model.db_setting import *
from flask import Request, Response
from bson import ObjectId
import datetime
import json
import bson.json_util
from wound.helpers import service_h
from wound.model.treatment_group import db_treatment, db_checkup_tests, db_diabetes_tests
from wound.model import db_patient_info, db_healthcare_staff_info
from wound.controllers.treatment_group import medical_checkup

columns = ['_id', 'treatment_id', 'date', 'healthcare_staff_id', 'wound_type_id', 'treatment_type_id']
# id_keys = ['_id', 'treatment_id']
id_keys = ['Id', 'Treatment-Id', 'Healthcare-Staff-Id']

def get_one_medical_checkup_dict(id: ObjectId) -> dict: # return: dict | None
    pipeline = [
    {
        '$match': {
            '_id': id
        }
    },
    {
        '$lookup': {
            'from': "treatment",
            'localField': "treatment_id",
            'foreignField': "_id",
            'pipeline': [
                {
                    '$unset': "_id"
                }
            ],
            'as': "treatment"
        }
    },
    {
        '$lookup': {
            'from': "checkup_tests", 
            'localField': "_id", 
            'foreignField': "_id", 
            'pipeline': [
                {
                    '$lookup': {
                        'from': "diabetes_tests",
                        'localField': "_id",
                        'foreignField': "_id",
                        'pipeline': [
                            {
                                '$unset': "_id"
                            }
                        ],
                        'as': "diabetes_tests"
                    }
                },
                {
                    '$unwind': "$diabetes_tests"
                },
                {
                    '$unset': "_id"
                }
            ],
            'as': "checkup_tests"
        }
    },
    {
        '$unwind': {
            'path': "$treatment",
            'preserveNullAndEmptyArrays': True
        }
    },
    {
        '$unwind': {
            'path': "$checkup_tests",
            'preserveNullAndEmptyArrays': True
        }
    }
    ]
    result = list(aggregate_to_collection("medical_checkup", pipeline=pipeline))
    if len(result) == 0:
        return None
    result = dict(result[0])
    
    # treatment_dict = db_treatment.get_one_treatment_dict(id)
    # treatment_dict.pop('_id')
    # checkup_tests_dict = db_checkup_tests.get_one_checkup_tests_dict(id)
    # checkup_tests_dict.pop('_id')
    # filters = {
    #     '_id': id
    # }
    # result = get_one_from_collection("medical_checkup", filters=filters)
    # if result is None:
    #     return result
    # result = dict(result)
    # result.update({
    #     'treatment': treatment_dict,
    #     'checkup_tests': checkup_tests_dict
    # })
    return result

# def create_medical_checkup(request: Request) -> Response:
#     ids_not_found = []
#     invalid_columns = []
#     # request_form_IDs = {}
#     request_header_IDs = {}
#     treatment_dict: dict = None
#     new_id = ObjectId()
#     if 'Treatment-Id' in request.headers:
#         if len(request.headers['Treatment-Id']) == 0:
#         #     treatment_dict = bson.json_util.loads(db_treatment.create_treatment(request))
#             treatment_dict = db_treatment.create_treatment(request, new_id)
#         else:
#             treatment_document = db_treatment.get_one_treatment_dict(ObjectId(request.headers['Treatment-Id']))
#             if treatment_document is None:
#                 ids_not_found.append('treatment_id')
#     else:
#     #     treatment_dict = bson.json_util.loads(db_treatment.create_treatment(request))
#         treatment_dict = db_treatment.create_treatment(request, new_id)
#     request_header_IDs = service_h.change_request_IDs_to_ObjectId(dict(request.headers), medical_checkup.id_keys)
#     # request_form_IDs = service_h.change_request_IDs_to_ObjectId(request.form, id_keys)
#     date: datetime.date = None
#     if 'date' in request.form:
#         if len(request.form['date']) == 0:
#             date = None
#         else:
#             try:
#                 date = str(datetime.datetime.strptime(request.form['date'], "%Y-%m-%d").date())
#             except:
#                 invalid_columns.append('date')
#     else:
#         date = str(datetime.datetime.now().date())
#     patient_document = db_patient_info.get_one_patient_info({'user_id': request_header_IDs['Patient-Id']})
#     if patient_document is None:
#         ids_not_found.append('patient_id')
#     healthcare_staff_document = db_healthcare_staff_info.get_one_healthcare_staff_info({'user_id': request_header_IDs['Healthcare-Staff-Id']})
#     if healthcare_staff_document is None:
#         ids_not_found.append('healthcare_staff_id')
#     if len(ids_not_found) > 0 or len(invalid_columns) > 0:
#         db_treatment.delete_treatment(request, new_id)
#         return Response(response=json.dumps({
#             'message': "Please check invalid form inputs",
#             'IDs_not_found': ids_not_found,
#             'invalid_columns': invalid_columns
#         }), status=400 if len(invalid_columns) > 0 else 404, mimetype="application/json")
#     data = {
#         '_id': new_id,
#         'treatment_id': treatment_dict['_id'] if treatment_dict is not None else request_header_IDs['Treatment-Id'],
#         'date': date,
#         'healthcare_staff_id': request_header_IDs['Healthcare-Staff-Id'],
#         'wound_type_id': (int(request.form['wound_type_id']) if request.form['wound_type_id'].isdigit() else 0) if 'wound_type_id' in request.form else 0,
#         'treatment_type_id': (int(request.form['treatment_type_id']) if request.form['treatment_type_id'].isdigit() else 0) if 'treatment_type_id' in request.form else 0
#     }
#     # data.update(request_header_IDs)
#     new_medical_checkup_id: ObjectId = insert_to_collection("medical_checkup", data).inserted_id
#     # checkup_tests_request = []
#     # checkup_tests_available_keys = db_checkup_tests.columns[1:] + db_diabetes_tests.columns[1:]
#     # for key in request.form:
#     #     if key in checkup_tests_available_keys:
#     #         checkup_tests_request.append(key)
#     # db_checkup_tests._create_checkup_tests(checkup_tests_request, new_medical_checkup_id)
#     db_checkup_tests.create_checkup_tests(request, new_medical_checkup_id)
#     result = get_one_medical_checkup_dict(new_medical_checkup_id)
#     # result.update({
#     #     'treatment': treatment_dict
#     # })
#     return Response(response=bson.json_util.dumps(result), status=201, mimetype="application/json")

def get_all_medical_checkups(request: Request) -> Response:
    available_keys = columns
    unknown_query_parameter_keys = service_h.list_unknown_keys(request.args, available_keys)
    cursor_result = get_from_collection("medical_checkup", filters=request.args)
    document_list = []
    for bson_document in cursor_result:
        document_list.append(dict(bson_document))
    if len(unknown_query_parameter_keys) > 0:
        return Response(response=bson.json_util.dumps({
            'result': document_list,
            'available_query_parameter_keys': available_keys,
            'unknown_query_parameter_keys': unknown_query_parameter_keys
        }), status=200, mimetype="application/json")
    return Response(response=bson.json_util.dumps(document_list), status=200, mimetype="application/json")

def get_one_medical_checkup(request: Request, id: ObjectId) -> Response:
    document_result = get_one_medical_checkup_dict(id)
    if document_result is None:
        return Response(response=json.dumps({'message': f"Medical Checkup with ID \'{id}\' not found"}), status=404, mimetype="application/json")
    return Response(response=bson.json_util.dumps(document_result), status=200, mimetype="application/json")

def update_one_medical_checkup(request: Request, id: ObjectId) -> Response:
    medical_checkup_dict = get_one_medical_checkup_dict(id)
    if medical_checkup_dict is None:
        return Response(response=json.dumps({'message': f"Medical Checkup with ID \'{id}\' not found"}), status=404, mimetype="application/json")
    
    ids_not_found = []
    invalid_columns = []
    request_header_IDs = {}
    treatment_dict: dict = None
    if 'Treatment-Id' in request.headers and len(request.headers['Treatment-Id']) != 0:
        treatment_document = db_treatment.get_one_treatment_dict(ObjectId(request.headers['Treatment-Id']))
        if treatment_document is None:
            ids_not_found.append('treatment_id')
    request_header_IDs = service_h.change_request_IDs_to_ObjectId(dict(request.headers), medical_checkup.id_keys)
    date: datetime.date = None
    if 'date' in request.form:
        if len(request.form['date']) == 0:
            date = None
        else:
            try:
                date = str(datetime.datetime.strptime(request.form['date'], "%Y-%m-%d").date())
            except:
                invalid_columns.append('date')
    patient_document = None
    if 'Patient-Id' in request.headers:
        patient_document = db_patient_info.get_one_patient_info({'user_id': request_header_IDs['Patient-Id']})
    if patient_document is None:
        ids_not_found.append('patient_id')
    healthcare_staff_document = None
    if 'Healthcare-Staff-Id' in request.headers:
        healthcare_staff_document = db_healthcare_staff_info.get_one_healthcare_staff_info({'user_id': request_header_IDs['Healthcare-Staff-Id']})
    if healthcare_staff_document is None:
        ids_not_found.append('healthcare_staff_id')
    if len(ids_not_found) > 0 or len(invalid_columns) > 0:
        return Response(response=json.dumps({
            'message': "Please check invalid form inputs",
            'IDs_not_found': ids_not_found,
            'invalid_columns': invalid_columns
        }), status=400 if len(invalid_columns) > 0 else 404, mimetype="application/json")
    new_data = {
        'treatment_id': treatment_dict['_id'] if treatment_dict is not None else None,
        'date': date,
        'healthcare_staff_id': request_header_IDs['Healthcare-Staff-Id'] if 'Healthcare-Staff-Id' in request.headers else None,
        'wound_type_id': (int(request.form['wound_type_id']) if request.form['wound_type_id'].isdigit() else None) if 'wound_type_id' in request.form else None,
        'treatment_type_id': (int(request.form['treatment_type_id']) if request.form['treatment_type_id'].isdigit() else None) if 'treatment_type_id' in request.form else None
    }
    new_data_items = list(new_data.items())
    for key, value in new_data_items:
        if value is None:
            new_data.pop(key)
    
    treatment_id = ObjectId(medical_checkup_dict['treatment_id'])
    db_treatment.update_one_treatment(request, treatment_id)
    db_checkup_tests.update_one_checkup_tests(request, id)
    update_from_collection("medical_checkup", id, new_data)
    result = get_one_medical_checkup_dict(id)
    return Response(response=bson.json_util.dumps(result), status=201, mimetype="application/json")

def replace_one_medical_checkup(request: Request, id: ObjectId) -> Response:
    medical_checkup_dict = get_one_medical_checkup_dict(id)
    if medical_checkup_dict is None:
        return Response(response=json.dumps({'message': f"Medical Checkup with ID \'{id}\' not found"}), status=404, mimetype="application/json")
    
    ids_not_found = []
    invalid_columns = []
    request_header_IDs = {}
    treatment_dict: dict = None
    if 'Treatment-Id' in request.headers and len(request.headers['Treatment-Id']) != 0:
        treatment_document = db_treatment.get_one_treatment_dict(ObjectId(request.headers['Treatment-Id']))
        if treatment_document is None:
            ids_not_found.append('treatment_id')
    request_header_IDs = service_h.change_request_IDs_to_ObjectId(dict(request.headers), medical_checkup.id_keys)
    date: datetime.date = None
    if 'date' in request.form:
        if len(request.form['date']) == 0:
            date = None
        else:
            try:
                date = str(datetime.datetime.strptime(request.form['date'], "%Y-%m-%d").date())
            except:
                invalid_columns.append('date')
    patient_document = None
    if 'Patient-Id' in request.headers:
        patient_document = db_patient_info.get_one_patient_info({'user_id': request_header_IDs['Patient-Id']})
    if patient_document is None:
        ids_not_found.append('patient_id')
    healthcare_staff_document = None
    if 'Healthcare-Staff-Id' in request.headers:
        healthcare_staff_document = db_healthcare_staff_info.get_one_healthcare_staff_info({'user_id': request_header_IDs['Healthcare-Staff-Id']})
    if healthcare_staff_document is None:
        ids_not_found.append('healthcare_staff_id')
    if len(ids_not_found) > 0 or len(invalid_columns) > 0:
        return Response(response=json.dumps({
            'message': "Please check invalid form inputs",
            'IDs_not_found': ids_not_found,
            'invalid_columns': invalid_columns
        }), status=400 if len(invalid_columns) > 0 else 404, mimetype="application/json")
    new_data = {
        'treatment_id': treatment_dict['_id'] if treatment_dict is not None else None,
        'date': date,
        'healthcare_staff_id': request_header_IDs['Healthcare-Staff-Id'] if 'Healthcare-Staff-Id' in request.headers else None,
        'wound_type_id': (int(request.form['wound_type_id']) if request.form['wound_type_id'].isdigit() else 0) if 'wound_type_id' in request.form else 0,
        'treatment_type_id': (int(request.form['treatment_type_id']) if request.form['treatment_type_id'].isdigit() else 0) if 'treatment_type_id' in request.form else 0
    }
    for key, value in new_data:
        if value is None:
            new_data.pop(key)
    
    treatment_id = ObjectId(medical_checkup_dict['treatment_id'])
    db_treatment.replace_one_treatment(request, treatment_id)
    db_checkup_tests.replace_one_checkup_tests(request, id)
    replace_from_collection("medical_checkup", id, new_data)
    result = get_one_medical_checkup_dict(id)
    return Response(response=bson.json_util.dumps(result), status=201, mimetype="application/json")
