import json

if __name__ == '__main__':
    record_dict = {
        'uid': 1
    }

    dicts = [record_dict, record_dict, record_dict]
    dicts_str = json.dumps(dicts)
    print(dicts_str)
    print(json.loads(dicts_str))
    print(1+True)
    print(1+False)
