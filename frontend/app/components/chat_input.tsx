

import React from "react"


const ChatInput = ({currentInputValue, setTextMessage, SendMessageToBackend, 
                    setIsButtonPressed, setCurrentInputValue}:any) =>{

    const handleInputStreamChange = (e: any) =>{
        setCurrentInputValue(e.target.value)
    }

    const handleSendingMessage = () =>{
        setTextMessage((prev: any) =>[...prev,  {'messenger': 'user', 'message': currentInputValue}]);
        SendMessageToBackend()
        // setIsButtonPressed(!isButtonPressed)
        setIsButtonPressed(true)
        setCurrentInputValue("")
    }

    return(
            <div className="input-container">
            <span>
              <textarea className="text-input" id="" 
                        placeholder="type..." 
                        value = {currentInputValue} 
                        onChange={handleInputStreamChange}
              onKeyDown={(e) => {
                if (e.key == "Enter" && !e.shiftKey){
                    e.preventDefault()
                    handleSendingMessage()
                }

              }}  
              ></textarea>
            </span>
            <button className="send-button" 
                    onClick={() => {handleSendingMessage()}}>⮝</button>
            </div>
    )
    
}

export default ChatInput