import React from "react"


const Messages = ({isButtonPressed, textMessage}:any) =>{
    return(
        <div className="message-body">
            <h1 className="header-text"> {!isButtonPressed && textMessage.length === 0? "Ask me ...": ""} </h1>
            {
              textMessage.map((textMessage:any, index:any) =>{

                if(textMessage['messenger'] == 'ai'){
                  return(
                    <h1 className="ai-message" key = {index}>{textMessage['message']}</h1>
                  )
                }else{
                  return(
                    <h1 className="human-message" key={index}>{textMessage['message']}</h1>
                  )
                }
              }
              )
            }
        </div>
    )
}

export default Messages