"use client";

import  { useState, useEffect, use } from "react";

import Image from "next/image";
import Link from "next/link";
// import './page.css'
// import DropDown from "./components/dropdown";
import SideBar from "./components/sidebar";
import ChatInput from "./components/chat_input";
import Messages from "./components/message_layout";


export default function Home() {
  const [currentInputValue, setCurrentInputValue] = useState("")
  const [textMessage, setTextMessage] = useState<any[]>([])
  const [isButtonPressed, setIsButtonPressed] = useState(false)
  const [isHistoryButtonPressed, setIsHistoryButtonPressed] = useState(false)
  const [chatRoomButtons, setChatRoomButtons] = useState<any[]>([])
  const [buttonTitle, setButtonTitle] = useState<any[]>([])
  const [current_session_id, set_current_session_id] = useState("")
  const [current_session_counter, set_current_session_counter] = useState(0)
  const [hasDeletedChat, setHasDeletedChat] = useState(false)
  

  useEffect(() =>{
    fetch('http://localhost:5000/get_initial_renders')
    .then((response) => response.json())
    .then((data) => {
      setChatRoomButtons([...data['session_counter']])
      setButtonTitle([...data['session_id']])
    })
    .catch(error => console.log(error))
  }, [isHistoryButtonPressed, hasDeletedChat])

  const get_initial_render_info = () => {
    fetch('http://localhost:5000/get_initial_renders')
    .then((response) => response.json())
    .then((data) => {
      setChatRoomButtons([...data['session_counter']])
      setButtonTitle([...data['session_id']])
    })
    .catch(error => console.log(error))
  }


  const SendMessageToBackend = () => {
    let is_new_chat_this_call = true
    if (currentInputValue !== ""){      
      let is_new_chat = textMessage.length == 0? true: false
      let message_to_send = {"is_new_chat": is_new_chat,
                             'query': currentInputValue, 
                             'current_session_id': current_session_id,
                             'current_session_counter': current_session_counter
                            }

      fetch('http://localhost:5000/user_query', {
        method:'POST',
        headers: {"Content-Type": "application/json"}, 
        body: JSON.stringify(message_to_send)
      })
      .then(response => response.json())
      .then(data => {
        setTextMessage(prev => [... prev, {'messenger': 'ai', 'message': data['ai_response']}])
        setIsHistoryButtonPressed(!isHistoryButtonPressed)
        if (is_new_chat == true){
          set_current_session_counter(data['current_session_counter'])
          set_current_session_id(data['current_session_id'])
        }
      })
      .catch(error => console.log(error))
    }   
  }

  const startNewChat = () =>{
    setTextMessage([])
    setHasDeletedChat(!hasDeletedChat)
    SendMessageToBackend()
  }

  return (
    <>
      <Link href="/about"></Link> 
      
        <div className="main-body">

          <SideBar  startNewChat = {startNewChat} 
                    hasDeletedChat = {hasDeletedChat} 
                    chatRoomButtons = {chatRoomButtons}
                    buttonTitle = {buttonTitle}
                    setHasDeletedChat = {setHasDeletedChat}
                    setTextMessage = {setTextMessage}
                    set_current_session_id = {set_current_session_id}
                    set_current_session_counter = {set_current_session_counter}
                    />
      
          <div className="message-container">

              <Messages isButtonPressed = {isButtonPressed}
                        textMessage = {textMessage}/>

              <ChatInput  currentInputValue = {currentInputValue}
                          setTextMessage = {setTextMessage}
                          SendMessageToBackend = {SendMessageToBackend}
                          setIsButtonPressed = {setIsButtonPressed}
                          setCurrentInputValue = {setCurrentInputValue}/>
            </div>
        </div>
    </>
  );
}
