from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures as a list"""
    if data:
        return jsonify(data), 200
    return {"message": "No pictures found"}, 404
######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a specific picture by its id"""
    # Find the picture by its `id` field, not the array index
    picture = next((item for item in data if item.get("id") == id), None)
    
    if picture:
        return jsonify(picture), 200
    return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    # Extract the picture data from the request body
    picture = request.get_json()

    # Check if the request body contains the required fields
    if not picture or "id" not in picture:
        return jsonify({"message": "Invalid data"}), 400

    # Check if a picture with the same ID already exists
    if any(item.get("id") == picture["id"] for item in data):
        return (
            jsonify({"Message": f"picture with id {picture['id']} already present"}),
            302,
        )

    # Append the new picture to the data list
    data.append(picture)

    # Return a success response with the created picture
    return jsonify(picture), 201
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture by its id"""
    # Extract the picture data from the request body
    updated_picture = request.get_json()

    # Check if the request body contains valid data
    if not updated_picture:
        return jsonify({"message": "Invalid data"}), 400

    # Find the picture in the data list by matching the id
    for index, picture in enumerate(data):
        if picture.get("id") == id:
            # Update the existing picture
            data[index] = updated_picture
            return jsonify(updated_picture), 200

    # If no picture with the given id is found, return a 404 error
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by its id"""
    # Find the picture in the data list by matching the id
    for index, picture in enumerate(data):
        if picture.get("id") == id:
            # Remove the picture from the data list
            del data[index]
            # Return an empty response with HTTP 204 No Content
            return "", 204

    # If no picture with the given id is found, return a 404 error
    return jsonify({"message": "picture not found"}), 404
