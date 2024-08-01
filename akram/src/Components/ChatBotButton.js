// src/components/ChatBotButton.js
import React, { useState } from 'react';
import ChatBot from './ChatBot';
import './ChatBotButton.css';
import { BiSolidMessageSquareDots, BiX } from "react-icons/bi";


const ChatBotButton = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div>
            <button
                className="btn btn-primary chatbot-button rounded-pill btn-lg text-center"
                onClick={toggleChat}
            >
                <div className='d-flex justify-content-center align-items-center'>
                    {<div className='d-flex justify-content-center align-items-center'>
                        {isOpen ? <BiX size={30} /> : <BiSolidMessageSquareDots size={30} />}
                    </div>}
                </div>
            </button>

            {isOpen && (
                <div className="chatbot-popup bg-light ">
                    <ChatBot />
                </div>
            )}
        </div>
    );
};

export default ChatBotButton;



