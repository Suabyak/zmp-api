def serialize_user_list(user_list):
    new_list = list()
    for user in user_list:
        new_list.append(serialize_user(user))
    return new_list

def serialize_model_list(model_list):
    new_list = list()
    for element in model_list:
        new_list.append(element.serialize())
    return new_list

def serialize_user(user):
    from api.models import Profile
    profile = Profile.objects.filter(user_id=user.id).first()
    return {
        "id": user.id,
        "username": user.username,
        "file": profile.image}

def serialize_data(data):
    return {
        "second": data.second,
        "minute": data.minute,
        "hour": data.hour,
        "day": data.day,
        "month": data.month,
        "year": data.year,
    }