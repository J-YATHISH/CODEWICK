
import React, { useState, useRef } from 'react';
import { ArrowLeft, Send, Mic, Camera, Play, Volume2 } from 'lucide-react';
import ChatBubble from './ChatBubble';
import { callSTTAPI, callGPTAPI, callCVAPI, callTTSAPI } from '../api/apiCalls';

interface Message {
  id: string;
  sender: 'farmer' | 'ai';
  message: string;
  audioURL?: string;
  timestamp: Date;
  type?: 'text' | 'voice' | 'image';
}

interface FarmerChatProps {
  onBack: () => void;
}

const FarmerChat: React.FC<FarmerChatProps> = ({ onBack }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'ai',
      message: 'Hello! I\'m your AgriSaarthi assistant. How can I help you today? You can type, speak, or take a photo of your crops.',
      timestamp: new Date(),
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSendMessage = async (text: string, type: 'text' | 'voice' | 'image' = 'text') => {
    if (!text.trim() && type === 'text') return;

    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'farmer',
      message: text,
      timestamp: new Date(),
      type,
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Call GPT API with context
      const aiResponse = await callGPTAPI(text, 'farmer');
      
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

  const handleVoiceInput = async () => {
    setIsRecording(true);
    try {
      // Simulate audio recording - in real app, use Web Audio API
      const mockAudio = new Blob(['mock audio data'], { type: 'audio/wav' });
      const recognizedText = await callSTTAPI(mockAudio);
      await handleSendMessage(recognizedText, 'voice');
    } catch (error) {
      console.error('Voice input error:', error);
    } finally {
      setIsRecording(false);
    }
  };

  const handleImageInput = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      const analysisResult = await callCVAPI(file);
      await handleSendMessage(`Image Analysis: ${analysisResult}`, 'image');
    } catch (error) {
      console.error('Image analysis error:', error);
    }

    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-green-50 flex flex-col">
      {/* Header */}
      <div className="bg-green-600 text-white p-4 flex items-center shadow-lg">
        <button
          onClick={onBack}
          className="mr-3 p-2 hover:bg-green-700 rounded-lg transition-colors"
        >
          <ArrowLeft size={24} />
        </button>
        <div className="flex items-center space-x-2">
          <span className="text-2xl">👨‍🌾</span>
          <h1 className="text-xl font-semibold">AgriSaarthi — Farmer</h1>
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
                <div className="animate-spin w-4 h-4 border-2 border-green-600 border-t-transparent rounded-full"></div>
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
              placeholder="Type your message..."
              className="w-full bg-transparent outline-none text-green-800 placeholder-green-500"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSendMessage(inputText);
                }
              }}
            />
          </div>
          
          {/* Voice Input */}
          <button
            onClick={handleVoiceInput}
            disabled={isRecording || isLoading}
            className={`p-3 rounded-full transition-colors ${
              isRecording 
                ? 'bg-red-500 text-white' 
                : 'bg-green-600 hover:bg-green-700 text-white'
            }`}
          >
            <Mic size={20} />
          </button>

          {/* Camera Input */}
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
            className="p-3 bg-green-600 hover:bg-green-700 text-white rounded-full transition-colors"
          >
            <Camera size={20} />
          </button>

          {/* Send Button */}
          <button
            onClick={() => handleSendMessage(inputText)}
            disabled={!inputText.trim() || isLoading}
            className="p-3 bg-green-600 hover:bg-green-700 text-white rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageInput}
            className="hidden"
          />
        </div>
      </div>
    </div>
  );
};

export default FarmerChat;
