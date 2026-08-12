"use client";

import  { useState, useEffect, use } from "react";

import Image from "next/image";
import Link from "next/link";
import './page.css'
import DropDown from "./components/dropdown";
import deleteButton from "./resources/delete-button.png";



export default function Home() {
  const [textVal, setTextVal] = useState("")
  const [headings, setHeadings] = useState<any[]>([])
  const [isButtonPressed, setIsButtonPressed] = useState(false)
  const [isHistoryButtonPressed, setIsHistoryButtonPressed] = useState(false)
  const [buttons, setButtons] = useState<any[]>([])
  const [buttonTitle, setButtonTitle] = useState<any[]>([])
  const [current_session_id, set_current_session_id] = useState("")
  const [current_session_counter, set_current_session_counter] = useState(0)
  const [isSidebarOpen, setisSideBarOpen] = useState(false)
  const [hasDeletedChat, setHasDeletedChat] = useState(false)
  // const [agentAnswers, setAgentAnswers] = useState<String[]>([])

  useEffect(() =>{
    console.log("Fetching")
    fetch('http://localhost:5000/get_initial_renders')
    .then((response) => response.json())
    .then((data) => {
      console.log("The data is: ", data)
      setButtons([...data['session_counter']])
      setButtonTitle([...data['session_id']])
      console.log("XXXX data['session_counter'] = ", data['session_counter'])
      // const listItems = []
      // for(var item of data){
      //   listItems.push(item)
      // }
      // setButtons(listItems)
      console.log("done now: ",(data))
    })
    .catch(error => console.log(error))
  }, [isHistoryButtonPressed, hasDeletedChat])

  const get_initial_render_info = () => {

    fetch('http://localhost:5000/get_initial_renders')
    .then((response) => response.json())
    .then((data) => {
      console.log("The data is: ", data)
      setButtons([...data['session_counter']])
      setButtonTitle([...data['session_id']])
      // console.log("XXXX data['session_counter'] = ", data['session_counter'])
      // const listItems = []
      // for(var item of data){
      //   listItems.push(item)
      // }
      // setButtons(listItems)
      // console.log("done now: ",(data))

    })
    .catch(error => console.log(error))
  }

 

  const SendMessageToBackend = () => {
    console.log("Entered SendMessageToBackend: "  + textVal)
    // console.log("yeah yeah current_session_id = ", current_session_id[0], "   |   current_session_counter", current_session_counter)
    let is_new_chat_this_call = true
    // check if this is the first message in this chat so I can create a new session_id for it    
    if (textVal !== ""){      
      let is_new_chat = headings.length == 0? true: false
      let message_to_send = {"is_new_chat": is_new_chat,
                             'query': textVal, 
                             'current_session_id': current_session_id,
                             'current_session_counter': current_session_counter
                            }
      console.log("yeah yeah current_session_id = ", current_session_id, "   |   current_session_counter", current_session_counter)
      // if(headings.length != 0){
      //     message_to_send = {"is_new_chat": false,
      //                       'query': textVal, 
      //                       'current_session_id': current_session_id[0],
      //                       'current_session_counter': current_session_counter[0]}
      //     is_new_chat_this_call = false
      //   }
      console.log("message_to_send: ", message_to_send);
      fetch('http://localhost:5000/user_query', {
        method:'POST',
        headers: {"Content-Type": "application/json"}, 
        body: JSON.stringify(message_to_send)
      })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        setHeadings(prev => [... prev, {'messenger': 'ai', 'message': data['ai_response']}])
        setIsHistoryButtonPressed(!isHistoryButtonPressed)
        if (is_new_chat == true){
          console.log("is in is new chat, are we in the if")
          set_current_session_counter(data['current_session_counter'])
          set_current_session_id(data['current_session_id'])
          console.log("no no current_session_id = ", data['current_session_id'], "   |   current_session_counter", data['current_session_counter'])
        }
        console.log("no no current_session_id = ", current_session_id, "   |   current_session_counter", current_session_counter)
      })
      .catch(error => console.log(error))
    }
    
    // setIsHistoryButtonPressed(!isHistoryButtonPressed)
  }

  const getHistory = (session_id: any, index: any) =>{
    console.log("in getHistory")
    setHeadings([])
    set_current_session_id(buttonTitle[index])
    set_current_session_counter(session_id)
    
    console.log("In get history current_session_id = ", current_session_id, "   |   current_session_counter", current_session_counter)
    console.log("In get history current_session_id = ", buttonTitle[index], "   |   current_session_counter", session_id)
    console.log("in getHistory before fetch")
    fetch('http://localhost:5000/get_history',{
      method: 'POST',
      headers:  {"Content-Type": "application/json"},
      body: JSON.stringify({'session_id': session_id})})
      .then(response => response.json())
      .then(data =>{
        setHeadings([...data])
      })
      .catch(error => console.log("Error", error))
  }

  const delete_a_history =(session_id_num: any) =>{
        fetch('http://localhost:5000/delete_a_history', {
            method: 'POST',
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify(session_id_num)
        })
        .then(data => data.json)
        .then(data => console.log("data = ", data))
        setHasDeletedChat(!hasDeletedChat)
    }
    

  // useEffect(() =>{
  //   console.log("Triggered: ", isButtonPressed)
  //   if (isButtonPressed == true){
  //     SendMessageToBackend()
  //     console.log("useEffect: Just sent a message")
  //     setIsButtonPressed(false)
  //   }
  // }, [isButtonPressed])

  const clearHistory = () =>{
    fetch("http://localhost:5000/clear_history")
    .then(data => data.json)
    .then(data => setHasDeletedChat(hasDeletedChat))
    .catch(error => console.log("Error occured: ", error))
    startNewChat()
  }

  const startNewChat = () =>{
    setHeadings([])
    setHasDeletedChat(!hasDeletedChat)
    SendMessageToBackend()
  }


  const handleInputStreamChange = (e: any) =>{
    setTextVal(e.target.value)
  }


  return (
    // <div ="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans daclassNamerk:bg-black">
    <>
    
    <Link href="/about"></Link> 
    
      <div className="main-body">

        <div className={isSidebarOpen ? "left-side-section close": "left-side-section"}>
          
          <button className={isSidebarOpen? "sidebar-button close": "sidebar-button"} onClick={e =>{
            setisSideBarOpen(!isSidebarOpen)
            // console.log("isButtonPressed",)
          }}>{isSidebarOpen ? "☰":"✖"}</button>

          <button className="clear-button" onClick={clearHistory}>Clear History</button>
        
          <div className={isSidebarOpen ? "setting-container close": "setting-container"}> 
            
            {
              buttons.map((session_id, index) =>{
                return(
                  <div className="sidebar-buttons-container" key = {index}>
                    
                    <button className="history_button" onClick={() => {
                      console.log("yes you succesfully pressed me: ", session_id)
                      getHistory(session_id, index) 
                      console.log("session_id ", session_id)}} key = {index}> {buttonTitle[index]}
                    </button>

                    {/* <DropDown session_id_num = {session_id} onSend = {setHasDeletedChat} hasDeletedChat = {hasDeletedChat}/> */}
                    <button className="delete-button" onClick={() =>
                                delete_a_history(session_id)
                                }><img src={deleteButton.src} alt="not" />
                    </button>
                  </div>
                )
              })
            }
            
          </div>
          <button className="new-chat-button" onClick={startNewChat}>New Chat</button>
        </div>
    
        <div className="message-container">
          <div className="message-body">

            <h1 className="header-text"> {!isButtonPressed && headings.length === 0? "Ask me ...": ""} </h1>


            {/* <h1>{headings.length === 0? "Ask me ...": ""}</h1> */}
            {/* <h1 className="human-message"> Hello Mr. AI, how are you? </h1>
            
            <h1 className="ai-message"> Mind your own business, like I mind my own fkn AI business. Humans are so needy. </h1> */}


            {
              headings.map((heading, index) =>{

                if(heading['messenger'] == 'ai'){
                  return(
                    <h1 className="ai-message" key = {index}>{heading['message']}</h1>
                  )
                }else{
                  return(
                    <h1 className="human-message" key={index}>{heading['message']}</h1>
                  )
                }
              }
               
              )
            }

          </div>

            <div className="input-container">
            <span>
              <textarea className="text-input" id="" placeholder="type..." value = {textVal} onChange={handleInputStreamChange}
              onKeyDown={(e) => {
                if (e.key == "Enter" && !e.shiftKey){
                  e.preventDefault()
                  setHeadings(prev =>[...prev,  {'messenger': 'user', 'message': textVal}]);
                  SendMessageToBackend()
                  // setIsButtonPressed(!isButtonPressed)
                  setIsButtonPressed(true)
                  setTextVal("")
                }

              }}  
              ></textarea>
            </span>
            <button className="send-button" onClick={() => {
                setHeadings(prev =>[...prev,  {'messenger': 'user', 'message': textVal}]);
                SendMessageToBackend()
                // setIsButtonPressed(!isButtonPressed)
                setIsButtonPressed(true)
                setTextVal("")
                }}
                >⮝
                {/* <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                  <path d="M12 4l-8 8h5v8h6v-8h5z"/>
                </svg>   */}
                </button>
            </div>

          
          </div>
      </div>
    </>
  );
}
