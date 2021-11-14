from database import *

conversation_collection = get_conversation_collection()
starred_collection = get_starred_collection()


def get_all_conversations():
    conversations = []
    try:
        res = conversation_collection.find({}, {"_id": 0})
        for record in res:
            conversations.append(record)
    except Exception as e:
        print("An exception occurred", e)
    return conversations


def insert_conversation(conversation_to_insert):
    try:
        conversation_collection.insert_one(conversation_to_insert)
        return True
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def delete_conversation(conversation_id):
    try:
        resp = conversation_collection.delete_one(conversation_id)
        return resp.deleted_count > 0
    except Exception as e:
        print("An exception occurred ::", e)
        return 0, False


def star_conversation(conversation_to_star):
    try:
        update = {"author": conversation_to_star["author"]}
        push = {"$push": {"messages": conversation_to_star["conversation"]}}
        resp = starred_collection.update_one(update, push, True)
        return resp.modified_count > 0
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def unstar_conversation(conversation_to_unstar):
    try:
        update = {"author": conversation_to_unstar["author"]}
        push = {"$pull": {"messages": conversation_to_unstar["conversation"]}}
        resp = starred_collection.update_one(update, push)
        return resp.modified_count > 0
    except Exception as e:
        print("An exception occurred ::", e)
        return False
