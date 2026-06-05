'''
All the business logic will be here


'''
from database.fake_db import users_db

def get_all_users():
    return users_db


def get_user_by_id(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    return None


def create_user(user_data):
    new_user = {
        "id": len(users_db) + 1,
        **user_data.dict()
    }

    users_db.append(new_user)

    return new_user


def update_user(user_id: int, update_data):
    for user in users_db:

        if user["id"] == user_id:

            if update_data.name:
                user["name"] = update_data.name

            if update_data.age:
                user["age"] = update_data.age

            return user

    return None


def delete_user(user_id: int):

    for index, user in enumerate(users_db):

        if user["id"] == user_id:
            return users_db.pop(index)

    return None