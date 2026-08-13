from rag import RagChain
from flask import Flask, jsonify, request
from flask_cors import CORS
import database_handler
from data_base import VectorDatabase
app = Flask(__name__)

isRecived = False
user_query = ""
ai_response = ""

CORS(app)
rc = RagChain()
vector_db = VectorDatabase()

@app.route("/gemini_connect")
def gemini_connect():
    return "gemini_connect"



@app.route('/get_initial_renders', methods = ['GET'])
def get_initial_renders():
    ai_response = "I am AI lol!"
    db_response = database_handler.get_all_session_ids()
    return jsonify(db_response)



@app.route("/user_query", methods = ['POST'])
def user_query():
    data = request.json
    user_query = data['query']
    is_new_chat = data['is_new_chat']
    current_session_id = ""
    current_session_counter = 0

    if is_new_chat:
        vector_db.create_pubmed_db(user_query)
    else: # is_new_chat
        current_session_id = data['current_session_id']
        current_session_counter = data['current_session_counter']
    try: 
        ai_response = rc.query_gemini(user_query)
    except:
        ai_response = "Error: Due to unknown reasons, I am not getting your message. It maybe out of tokens for today or this model is currently experiencing high demand"

    db_response = database_handler.add_a_new_chat_entry(user_query, ai_response, current_session_id, current_session_counter, is_new_chat)
    if db_response != None:
        current_session_id = db_response['current_session_id']
        current_session_counter = db_response['current_session_counter']
    return jsonify({"ai_response": ai_response, 
                    "current_session_id": current_session_id, 
                    "current_session_counter": current_session_counter})

@app.route("/get_history", methods = ['POST'])
def get_history():
    data = request.json
    session_id = data['session_id']
    history_lst = []
    try:
        history_lst = database_handler.get_old_chat(session_id=session_id)
    except:
        print("Error during database search.")
    return jsonify(history_lst)
    

@app.route('/delete_a_history', methods = ['POST'])
def delete_a_history():
    chat_session_id = request.json
    database_handler.delete_a_chat(chat_session_id)
    return jsonify("Action was succesful!")

@app.route('/clear_history', methods = ['GET'])
def clear_history():
    database_handler.clear_all_chats()
    return jsonify("Action was succesful!")

