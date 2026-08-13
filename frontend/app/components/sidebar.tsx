import '../page.css'
import { use, useState } from 'react'
import deleteButton from "../resources/delete-button.png";
import newChat from "../resources/new-chat.png";
import clearChat from "../resources/broom.png";




const SideBar = ({startNewChat, hasDeletedChat, chatRoomButtons, buttonTitle, setHasDeletedChat,
                    setTextMessage, set_current_session_id, set_current_session_counter}: any) =>{
    const [isSidebarOpen, setisSideBarOpen] = useState(false)
    const [currChatRoomTracker, setCurrChatRoomTracker] = useState<boolean[]>([])


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

    const clearHistory = () =>{
        fetch("http://localhost:5000/clear_history")
        .then(data => data.json)
        .then(data => setHasDeletedChat(hasDeletedChat))
        .catch(error => console.log("Error occured: ", error))
        startNewChat()
    }

    
    const getHistory = (session_id: any, index: any) =>{
        setTextMessage([])
        set_current_session_id(buttonTitle[index])
        set_current_session_counter(session_id)
        fetch('http://localhost:5000/get_history',{
        method: 'POST',
        headers:  {"Content-Type": "application/json"},
        body: JSON.stringify({'session_id': session_id})})
        .then(response => response.json())
        .then(data =>{
            setTextMessage([...data])
        })
        .catch(error => console.log("Error", error))
    }
    
        

    return(
            <div className={isSidebarOpen ? "left-side-section close": "left-side-section"}>
            
                <button className={isSidebarOpen? "sidebar-button close": "sidebar-button"} onClick={e =>{
                    setisSideBarOpen(!isSidebarOpen)
                }}>{isSidebarOpen ? "☰":"✖"}</button>

                <button className="clear-button" onClick={clearHistory}> <img src={clearChat.src} alt="Clear All" /> </button>
                
                <div className={isSidebarOpen ? "setting-container close": "setting-container"}> 
                    
                    {
                    chatRoomButtons.map((session_id: any, index: any) =>{
                        return(
                        <div className="sidebar-buttons-container" key = {index}>
                            
                            <button className={currChatRoomTracker[index]? "history_button selected":"history_button"} onClick={() => {
                                getHistory(session_id, index) 
                                currChatRoomTracker[index] = true
                                setCurrChatRoomTracker((prev) => {
                                    const next = prev.map(() => false)
                                    next[index] = true
                                    return next
                                }
                                )
                            </button>

                            <button className="delete-button" onClick={() =>
                                        delete_a_history(session_id)
                                        }><img src={deleteButton.src} alt="not" />
                            </button>
                        </div>
                        )
                    })
                    }
                    
                </div>
                <button className={isSidebarOpen?"new-chat-button close":"new-chat-button"} onClick={startNewChat}><img src={newChat.src} alt="New" /> </button>
            </div>)

}

export default SideBar
