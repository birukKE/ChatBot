import mysql.connector
from rag import RagChain
import random
import string
import config
rag = RagChain()

# just a function during development to create titles
def create_random_title():
    return str("".join(random.choices(string.ascii_letters, k=7)))
    

def create_conn():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "mysql",
            database = "chat_history",
            # buffered=True,
            ssl_disabled=True,
            autocommit=True
        )
        if conn.is_connected():
            print("\n\n\nYes connected lol\n\n\n")
        else:
            print("unfortunately, not connected")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return conn

conn = create_conn()
cursor = conn.cursor()


def get_old_chat(session_id):
    # global cursor
    conn = create_conn()
    cursor = conn.cursor()
    print("in get_old_chat: ", session_id)
    try:
        cursor.execute("SELECT * FROM Chats WHERE session_counter = %s", (session_id[0], ))
    except Exception as e:
        print("Da error: ", e)
    print("after db search get_old_chat")
    returned_data = cursor.fetchall()
    chat_messages = []
    for i in range(len(returned_data)):
        chat_messages.extend([{'messenger': "human", "message": returned_data[i][1]},
                              {'messenger': "ai", "message": returned_data[i][2]}
                              ])
    conn.close()
    return chat_messages

def get_all_session_ids():
    global cursor
    cursor.execute("SELECT DISTINCT session_id FROM Chats")
    session_id = cursor.fetchall()

    cursor.execute("SELECT DISTINCT session_counter FROM Chats")
    session_counter = cursor.fetchall()

    result = {'session_id': session_id, 'session_counter': session_counter}
    return result

def add_a_new_chat_entry(user_query, response, session_id, session_counter, is_new_chat):
    print("In add_a_new_chat_entry")
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(session_counter) FROM chats")
    print("In add_a_new_chat_entry 1: session_name = ", session_id)
    session_count = cursor.fetchall()
    
    # check if table is empty
    print("\n\n\n\nsession: ", session_count)
    # session:  [(None,)]
    
    if session_count[0][0] == None or is_new_chat:
        print("where we in if \n\n\n")
        session_num = 0
        session_name = create_random_title()
        if session_count[0][0] != None:
            session_num = session_count[0][0] + 1
            # session_name = create_random_title()
            session_name = rag.query_database(user_query, config.promp_create_title)
        print(f"If chat history is empty: session_name = {session_name} and session_num = {session_num} ")
        cursor.execute("INSERT INTO Chats(human, assistant, session_id, session_counter, title) VALUES (%s, %s, %s, %s, %s)", (user_query, response, session_name, session_num, "title lol"))
        conn.commit()
        return {"current_session_counter": session_num, "current_session_id": session_name}
    
    # session_name = "test"
    print("\n\n\ndid we get here dbhandler add_a_new")
    if isinstance(session_counter, list):
        session_counter = session_counter[0]
        session_id = session_id[0]
    print(f"If chat history is empty: session_name = {session_id} and session_num = {session_counter} ")
    cursor.execute("INSERT INTO Chats(human, assistant, session_id, session_counter, title) VALUES (%s, %s, %s, %s, %s)", (user_query, response, session_id, session_counter, "title there"))
    conn.commit()
    conn.close()
    return None

def clear_all_chats():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats")
    conn.commit()
    conn.close()

def delete_a_chat(chat_session_id):
    conn = create_conn()
    cursor = conn.cursor()
    # print("\n\nchat_session_id = ", chat_session_id)
    cursor.execute("DELETE FROM chats WHERE session_counter = (%s)", (chat_session_id[0], ))
    conn.commit()
    conn.close()

    
if __name__ == '__main__':

    cursor = conn.cursor()

    # cursor.execute("CREATE TABLE Chats(id INT AUTO_INCREMENT PRIMARY KEY, human TEXT, assistant TEXT, session_id VARCHAR(255), session_counter INT, title VARCHAR(250))")
    # conn.commit()
    count = 0
    while True:
        user_query = input("Your query: ")
        # response = rag.query_gemini(query=user_query)
        response = "LOL haha" + str(count)
        print(f"Bot: {response}")
        # cursor.execute("INSERT INTO Chats(human, assistant, session) VALUES (%s,%s,%s)", (user_query, response, "chat1"))
        cursor.execute("INSERT INTO Chats(human, assistant, session_id) VALUES (%s, %s, %s)", (user_query, response, "chat2"))
        # val = cursor.execute("SELECT * FROM Chats WHERE session_id = %s", ("chat1",))
        # conn.commit()
        cursor.execute("SELECT * FROM Chats WHERE session_id = %s", ("chat2",))
        val = cursor.fetchall()
        # conn.commit()
        print("Table\n", val)
        chat_messages = []

        for i in range(len(val)):
            chat_messages.extend([val[i][1], val[i][2]])
        print(chat_messages)
        count += 1