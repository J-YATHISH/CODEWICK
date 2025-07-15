
import React, { useState } from 'react';
import { ArrowLeft, Send } from 'lucide-react';
import ChatBubble from './ChatBubble';
import { callGPTAPI, callTTSAPI } from '../api/apiCalls';

interface Message {
  id: string;
  sender: 'gardener' | 'ai';
  message: string;
  audioURL?: string;
  timestamp: Date;
}

interface GardenerChatProps {
  onBack: () => void;
}

const GardenerChat: React.FC<GardenerChatProps> = ({ onBack }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'ai',
      message: 'Hello! I\'m your AgriSaarthi gardening assistant. Ask me anything about plants, gardening tips, or plant care!',
      timestamp: new Date(),
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'gardener',
      message: inputText,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputText;
    setInputText('');
    setIsLoading(true);

    try {
      // Call GPT API for gardening advice
      const aiResponse = await callGPTAPI(currentInput, 'gardener');
      
      // Call TTS API for audio response
      const audioURL = await callTTSAPI(aiResponse);

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        message: aiResponse,
        audioURL,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error processing message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        message: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-green-50 flex flex-col">
      {/* Header */}
      <div className="bg-green-500 text-white p-4 flex items-center shadow-lg">
        <button
          onClick={onBack}
          className="mr-3 p-2 hover:bg-green-600 rounded-lg transition-colors"
        >
          <ArrowLeft size={24} />
        </button>
        <div className="flex items-center space-x-2">
          <span className="text-2xl">🌿</span>
          <h1 className="text-xl font-semibold">AgriSaarthi — Gardener</h1>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <ChatBubble key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl p-4 shadow-sm">
              <div className="flex items-center space-x-2">
                <div className="animate-spin w-4 h-4 border-2 border-green-500 border-t-transparent rounded-full"></div>
                <span className="text-green-600">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Bar */}
      <div className="bg-white border-t border-green-200 p-4">
        <div className="flex items-center space-x-2">
          <div className="flex-1 bg-green-50 rounded-2xl px-4 py-3 border border-green-200">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask about gardening..."
              className="w-full bg-transparent outline-none text-green-800 placeholder-green-500"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSendMessage();
                }
              }}
            />
          </div>
          
          {/* Send Button */}
          <button
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
            className="p-3 bg-green-500 hover:bg-green-600 text-white rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default GardenerChat;
