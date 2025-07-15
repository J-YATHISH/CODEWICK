
import React, { useState } from 'react';
import { Play, Volume2 } from 'lucide-react';

interface Message {
  id: string;
  sender: 'farmer' | 'gardener' | 'ai';
  message: string;
  audioURL?: string;
  timestamp: Date;
  type?: 'text' | 'voice' | 'image';
}

interface ChatBubbleProps {
  message: Message;
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ message }) => {
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const isUser = message.sender === 'farmer' || message.sender === 'gardener';
  
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  };

  const playAudio = async () => {
    if (!message.audioURL) return;
    
    setIsPlayingAudio(true);
    try {
      // In a real app, you would play the actual audio file
      // For now, we'll simulate audio playback
      console.log('Playing audio:', message.audioURL);
      
      // Simulate audio duration
      setTimeout(() => {
        setIsPlayingAudio(false);
      }, 3000);
    } catch (error) {
      console.error('Error playing audio:', error);
      setIsPlayingAudio(false);
    }
  };

  const getBubbleColor = () => {
    if (isUser) {
      return message.sender === 'farmer' 
        ? 'bg-green-600 text-white' 
        : 'bg-green-500 text-white';
    }
    return 'bg-white text-green-800 border border-green-200';
  };

  const getTypeIcon = () => {
    switch (message.type) {
      case 'voice':
        return <Volume2 size={14} className="inline mr-1" />;
      case 'image':
        return <span className="text-sm mr-1">📷</span>;
      default:
        return null;
    }
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-xs sm:max-w-md ${getBubbleColor()} rounded-2xl p-4 shadow-sm`}>
        {/* Message Type Indicator */}
        {message.type && message.type !== 'text' && (
          <div className="flex items-center mb-1 opacity-75">
            {getTypeIcon()}
            <span className="text-xs capitalize">{message.type}</span>
          </div>
        )}
        
        {/* Message Text */}
        <p className="text-sm sm:text-base leading-relaxed">{message.message}</p>
        
        {/* Audio Player for AI messages */}
        {!isUser && message.audioURL && (
          <div className="mt-3 pt-2 border-t border-green-100">
            <button
              onClick={playAudio}
              disabled={isPlayingAudio}
              className="flex items-center space-x-2 text-green-600 hover:text-green-700 transition-colors disabled:opacity-50"
            >
              <Play size={16} className={isPlayingAudio ? 'animate-pulse' : ''} />
              <span className="text-xs">
                {isPlayingAudio ? 'Playing...' : 'Play Audio'}
              </span>
            </button>
          </div>
        )}
        
        {/* Timestamp */}
        <div className={`text-xs mt-2 ${isUser ? 'text-green-100' : 'text-green-500'}`}>
          {formatTime(message.timestamp)}
        </div>
      </div>
    </div>
  );
};

export default ChatBubble;
