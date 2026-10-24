

import mysql.connector
from rag import RagChain
import random
import string
import config
import os
from dotenv import load_dotenv
from contextlib import contextmanager


load_dotenv()

class ChatDatabase:
    def __init__(self):
        self.config = {
            "host": os.getenv("HOST"),
            "user": os.getenv("USER"),
            "password": os.getenv("PASSWORD"),
            "database":  "chat_history",
            "ssl_disabled": True,
            "autocommit": True
            }

    @contextmanager
    def connect_to_db(self):
        try: 
            conn = mysql.connector.connect(**self.config)
            if conn.is_connected(): 
                print("Conneted to Database")
                yield conn
            else: print("Couldn't connect to Database.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            conn.close()

    
    def get_old_chat(self, session_id):
        query = "SELECT * FROM Chats WHERE session_counter = %s"
        with self.connect_to_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (session_id[0], ))
            returned_data = cursor.fetchall()
            chat_messages = []
            for i in range(len(returned_data)):
                chat_messages.extend([{'messenger': "human", 
                                    "message": returned_data[i][1]},
                                    {'messenger': "ai", 
                                    "message": returned_data[i][2]}
                                    ])
        return chat_messages

    def clear_all_chats(self):
        with self.connect_to_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chats")
            conn.commit()


    def delete_a_chat(self, chat_session_id):
        query = "DELETE FROM chats WHERE session_counter = (%s)"
        with self.connect_to_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (chat_session_id[0],))
            conn.commit()


    def get_all_session_ids(self):
        with self.connect_to_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT session_id FROM Chats")
            session_id = cursor.fetchall()

            cursor.execute("SELECT DISTINCT session_counter FROM Chats")
            session_counter = cursor.fetchall()

            result = {'session_id': session_id, 'session_counter': session_counter}
            return result

    def add_a_new_chat_entry(self, 
                            user_query, 
                            response, 
                            session_id, 
                            session_counter, 
                            is_new_chat):
    
        with self.connect_to_db() as conn:
            rag = RagChain()
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(session_counter) FROM chats")
            last_session_ctr = cursor.fetchall()
            # If this session is a new chat
            if last_session_ctr[0][0] == None or is_new_chat:
                curr_session_ctr = 0
                curr_session_name = ""
                if last_session_ctr[0][0] != None:
                    curr_session_ctr = last_session_ctr[0][0] + 1
                    curr_session_name = rag.query_database(user_query, config.promp_create_title)
                query1 = """INSERT INTO Chats(human, assistant, session_id, session_counter, title) 
                            VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query1, 
                                (user_query, response, curr_session_name, curr_session_ctr, "random title debugg"))
                conn.commit()
                return {"current_session_counter": curr_session_ctr, 
                        "current_session_id": curr_session_name}
            
            if isinstance(session_counter, list):
                session_counter = session_counter[0]
                session_id = session_id[0]
                query2 = """INSERT INTO Chats(human, assistant, session_id, session_counter, title) 
                            VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query2, (user_query, response, session_id, session_counter, "title there"))
                conn.commit()
        return None

        
