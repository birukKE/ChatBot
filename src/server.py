from rag import RagChain
from flask import Flask, jsonify, request
# from flask import jsonify, request
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



# Giving response from backend server to react 
@app.route('/get_initial_renders', methods = ['GET'])
def get_initial_renders():
    ai_response = "I am AI lol!"
    db_response = database_handler.get_all_session_ids()
    # if ai_response == "":
    #     return "Error: Due to unknown reasons, I am not getting your message. It maybe out of tokens for today or this model is currently experiencing high demand"
    return jsonify(db_response)


# Recieving message from frontend (frontend posts a request)
@app.route("/user_query", methods = ['POST'])
def user_query():
    print("HERE")
    data = request.json
    print("\n\n\n\n\nuser_query in server data = ", data)
    user_query = data['query']
    is_new_chat = data['is_new_chat']
    current_session_id = ""
    current_session_counter = 0

    if is_new_chat:
        print("Just now right?")
        vector_db.create_pubmed_db(user_query)
    
    if not is_new_chat:
        print("in is it new chat or not")
        current_session_id = data['current_session_id']
        current_session_counter = data['current_session_counter']
    try: 
        ai_response = rc.query_gemini(user_query)
        # ai_response = "DELETE ME"
    except:
        ai_response = "Error: Due to unknown reasons, I am not getting your message. It maybe out of tokens for today or this model is currently experiencing high demand"
    print(ai_response)

    # if is_new_chat:
    # print("\n\nhere in the user_query: ", is_new_chat)
    print(f"----------------------------------------------------\n session_name = {current_session_id} and session_num = {current_session_counter} \n------------------------------------------------------------")
    db_response = database_handler.add_a_new_chat_entry(user_query, ai_response, current_session_id, current_session_counter, is_new_chat)
    if db_response != None:
        current_session_id = db_response['current_session_id']
        current_session_counter = db_response['current_session_counter']
    # else:
    #     database_handler.add_a_new_chat_entry(user_query, ai_response, current_session_id, current_session_counter)
    return jsonify({"ai_response": ai_response, 
                    "current_session_id": current_session_id, 
                    "current_session_counter": current_session_counter})

@app.route("/get_history", methods = ['POST'])
def get_history():
    print("Getting history in python")
    data = request.json
    session_id = data['session_id']
    history_lst = []
    try:
        history_lst = database_handler.get_old_chat(session_id=session_id)
        print("List = ", history_lst)
    except:
        print("Error during database search.")
    print("\n\n history_lst:\n", history_lst, "\n\n")
    # rc.chat_object.clear_history()
    # rc.chat_object.add_many_to_history(history_lst)
    print("\n\n\n Did we reach here get_history server\n\n\n")
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


def add_many_to_history(messages):
    message_lst = [message['message'] for message in messages]


# def give_title_name():

    
# print("here")

# def handleBackend(user_input):
#     # toReturn =  movie.takeInput(favMovie, isDescription)
#     # ai_response = rag.rc.query_gemini(user_input)
#     ai_response = "Go away"
#     return jsonify(ai_response)


# @app.route("/handleUserInput", methods = ['POST'])
# def handleUserInput():
#     data = request.json
#     # toRet = handleBackend(data['value'], data['isDescription'])
#     toRet = handleBackend(data['value'])
#     return toRet

if __name__ == "__main__":
    app.run(debug= True)