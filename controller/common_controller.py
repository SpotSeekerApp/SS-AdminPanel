from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import requests
from http import HTTPStatus
import pyrebase
from flask_login import login_required
import re

# custom modules
from model.place import Place
from config import API_URL
from services.logger import logger


def is_meaningful_string(text):
    # Check for only whitespace or emptiness
    if not text.strip():
        return False

    # Check for other meaningless characters (e.g., hyphens, underscores)
    if re.match(r'^[\s\-_]*$', text):
        return False

    return True

@login_required
def list_places_page():
    logger.info(f"List places user_id:{session['uid']}")

    res_user_type = session["user_type"]

    if res_user_type == "place_owner":
        user_id = session["uid"]
        response = requests.get(f'{API_URL}/GetAllPlaces?user_id={user_id}')
    else:
        response = requests.get(f'{API_URL}/GetAllPlaces')

    status = response.json()['StatusCode']
    if status == HTTPStatus.OK:
        msg = f"Places listed successfully"
        logger.info(msg)
    else:
        msg = f"Error failed to list places {HTTPStatus.INTERNAL_SERVER_ERROR}"
        logger.error(msg)
        flash(msg)

    place_dict = response.json()['Data'] 

    # Convert tags to comma seperated string for UI 
    # Assuming tags will come from db in the following format: ("tagname", rating<float>)
    for place_id in place_dict.keys():
        place_tags = place_dict[place_id]["tags"]
        if place_tags == None: 
            place_dict[place_id]["tags"] = ""
        else: 
            # only send if tag has 1 as rating to UI 
            tags = ','.join(tag[1] for tag in place_tags if len(tag)==2 and tag[1] == 1 and is_meaningful_string(tag))
            place_dict[place_id]["tags"] = ','.join(tags)

    tags = requests.get(f'{API_URL}/GetAllTags').json()["Data"]["all_tags"]
    return render_template("list_places.html", places=place_dict.values(), tags=tags)

@login_required
def update_places_page():
    place_data = Place( place_id=request.form['place_id'],
                        place_name=request.form['name'],
                        main_category=request.form['main_category'],
                        tags=request.form['tags'],
                        link=request.form['link'],
                        user_id=session["uid"]).to_json()

    # only send tags with value 1 to db
    place_data["tags"] = [(tag, 1) for tag in place_data["tags"].split(",")]
    
    logger.info(f"Update place user_id:{session['uid']}, place:{place_data}")

    response = requests.post(f'{API_URL}/UpdatePlace', json=place_data)
    status = response.json()['StatusCode']

    if status == HTTPStatus.OK:
        msg = f"Place edited successfully"
        logger.info(msg)
        flash(msg)
    else:
        msg = f"Error failed to edit place {HTTPStatus.INTERNAL_SERVER_ERROR}"
        logger.error(msg)
        flash(msg)

    return redirect(url_for("list_places_page"))

@login_required
def create_places_page():
    place = Place( place_name=request.form['name'],
                        main_category=request.form['main_category'],
                        tags=None,
                        link=request.form['link'],
                        user_id=session["uid"])
    
    # only send tags with value 1 to db
    if request.form['tags'] is not []:
        place.tags = {tag: 1.0 for tag in request.form['tags'].split(",")}
        
    place_data = place.to_json()

    logger.info(f"Create place user_id:{session['uid']}, place:{place_data}")

    response = requests.post(f'{API_URL}/AddPlace', json=place_data)
    status = response.json()['StatusCode']

    if status == HTTPStatus.OK:
        msg = f"Place added successfully"
        logger.info(msg)
        flash(msg)
    else:
        msg = f"Error failed to add place {HTTPStatus.INTERNAL_SERVER_ERROR}"
        logger.error(msg)
        flash(msg)

    return redirect(url_for("list_places_page"))

@login_required
def delete_places_page(place_id):
    place_data = Place(place_id=place_id).to_json()

    logger.info(f"Delete place user_id:{session['uid']}, place:{place_data}")
    response = requests.post(f'{API_URL}/RemovePlace', json=place_data)
    status = response.json()['StatusCode']

    if status == HTTPStatus.OK:
        msg = f"Place deleted successfully"
        logger.info(msg)
        flash(msg)
    else:
        msg = f"Error failed to delete place {HTTPStatus.INTERNAL_SERVER_ERROR}"
        logger.error(msg)
        flash(msg)

    return redirect(url_for("list_places_page"))
