import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["tarkov"]
mycol = db["killers"]


def get_killer(server_id, killer_id):
    query = {"server_id": server_id, "killer_id":killer_id}
    killer = mycol.find_one(query)
    return killer


def add_killed(server_id, killer_id, killed_id):
    killer = get_killer(server_id, killer_id)

    if killer:
        if killed_id in killer["killed"]:
            aux_dict = killer["killed"]
            aux_dict[killed_id] += 1
            aux_total = killer["total"] + 1
            query = {"server_id": server_id, "killer_id": killer_id}
            new_values = {"$set": {"killed": aux_dict, "total": aux_total}}
            mycol.update_one(query, new_values)

        else:
            aux_dict = killer["killed"]
            aux_dict[killed_id] = 1
            aux_total = killer["total"] + 1
            query = {"server_id": server_id, "killer_id": killer_id}
            new_values = {"$set": {"killed": aux_dict, "total": aux_total}}
            mycol.update_one(query, new_values)

    else:
        killer = {"server_id": server_id, "killer_id": killer_id, "killed": { killed_id: 1}, "total": 1}
        mycol.insert_one(killer)


def get_leaderboard(server_id):
    doc = mycol.find({"server_id": server_id}, limit=5).sort("server_id", pymongo.DESCENDING)
    return doc




