from flask import Blueprint, jsonify, request
from datetime import datetime
import db


items = Blueprint("items", __name__)
inventory = Blueprint("inventory", __name__)



@items.route("/", methods=['POST'])
def post_items():
    request_data = request.get_json()
    request_data["createdDate"] = datetime.now()
    db.mongo.db.schema.insert_one(request_data)
    print (request_data)
    del request_data['_id']
    return jsonify(request_data)



@inventory.route("/", methods=['GET'])
def get_inventory():
    # Aggregation pipeline to sum the quantities of items with the same name
    pipeline = [
        {"$group": {"_id": "$name", "quantity": {"$sum": "$quantity"}}},
        {"$project": {"_id": 0, "name": "$_id", "quantity": "$quantity"}}
    ]
    
    # Execute the aggregation
    aggregated_result = list(db.mongo.db.schema.aggregate(pipeline))
    
    # Return the aggregated results as JSON
    return jsonify(aggregated_result), 200
