from bson import ObjectId

def check_required_keys_exist(request_dict: dict, required_keys: list) -> bool:
    for required_key in required_keys:
        if required_key not in request_dict:
            return False
    return True

def check_unknown_keys_exist(request_dict: dict, available_keys: list) -> bool:
    for request_key in request_dict:
        if request_key not in available_keys:
            return True
    return False

def list_missing_keys(request_dict: dict, required_keys: list) -> list:
    missing_keys = []
    for required_key in required_keys:
        if required_key not in request_dict:
            missing_keys.append(required_key)
    return missing_keys

def list_unknown_keys(request_dict: dict, available_keys: list) -> list:
    unknown_keys = []
    for request_key in request_dict:
        if request_key not in available_keys:
            unknown_keys.append(request_key)
    return unknown_keys

def valid_ObjectId_checks(request_dict: dict, id_keys: list) -> list:
    invalid_ObjectId_list = []
    for key in id_keys:
        if key in request_dict:
            if not ObjectId.is_valid(request_dict[key]):
                invalid_ObjectId_list.append(key)
    return invalid_ObjectId_list

def change_request_IDs_to_ObjectId(request_dict: dict, id_keys: list) -> dict:
    result = {}
    for key in id_keys:
        if key in request_dict:
            result[key] = ObjectId(request_dict[key])
    return result
