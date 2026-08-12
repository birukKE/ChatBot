import Link from "next/link";
import React from "react";
import './dropdown.css'

const DropDown = ({session_id_num, onSend, hasDeletedChat}:any) =>{

    const delete_a_history =(session_id_num: any) =>{
        fetch('http://localhost:5000/delete_a_history', {
            method: 'POST',
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify(session_id_num)
        })
        .then(data => data.json)
        .then(data => console.log("data = ", data))
    }

  return (
    <>
      <div className="dropdown-menu">
        <button className="three-dot-btn">⋮</button>
        <div className="menu-content">
            <button onClick= {() => {
                delete_a_history(session_id_num)
                onSend(!hasDeletedChat)
            }} >Delete</button>
        </div>
      </div>


    </>
  );
}


export default DropDown