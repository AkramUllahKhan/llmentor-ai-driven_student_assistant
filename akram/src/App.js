import React from 'react';
import ChatBot from './Components/ChatBot';
import './App.css';
import Navbar from './Components/Navbar';
import Footer from './Components/Footer';
import HeroSection from './Components/HeroSection';
import ChatBotButton from './Components/ChatBotButton';

function App() {
  return (
    <div className="App">
      <Navbar />

      <HeroSection />
      <ChatBotButton />
      {/* <ChatBot /> */}


      <Footer />
    </div>
  );
}

export default App;