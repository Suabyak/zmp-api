def serialize_model_list(model_list):
    new_list = list()
    for element in model_list:
        new_list.append(element.serialize())
    return new_list

def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username}