
# AgriSaarthi - AI-Powered Agricultural Assistant

AgriSaarthi is a mobile-first web application that provides AI-powered assistance for farmers and gardeners. The app features role-based chat interfaces with voice, text, and image input capabilities.

## 🌟 Features

### Role Selector
- Choose between Farmer and Gardener roles
- Farm-friendly green theme with intuitive design
- Large touch targets optimized for mobile use

### Farmer Chat Interface
- **Voice Input**: Speak your questions and get voice responses
- **Image Analysis**: Take photos of crops for AI-powered disease/pest detection
- **Text Chat**: Traditional text-based conversation
- **Integrated APIs**: STT → GPT → CV → TTS pipeline
- **Context-Aware**: Includes soil, weather, and market data

### Gardener Chat Interface
- **Text-Only Chat**: Simple, focused gardening advice
- **Audio Responses**: Listen to AI advice hands-free
- **Plant Care Tips**: Specialized guidance for home gardening

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm installed
- Modern web browser with microphone and camera access

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd agrisaarthi
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open in browser**
   Navigate to `http://localhost:8080` or the URL shown in your terminal

## 📱 Mobile Usage

The app is optimized for mobile browsers. For the best experience:
- Allow microphone and camera permissions when prompted
- Use in landscape mode for better chat visibility
- Ensure stable internet connection for API calls

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory with the following keys:

```bash
# Speech-to-Text API (Whisper/AssemblyAI)
VITE_STT_API_KEY=your_stt_api_key
VITE_STT_API_URL=https://api.whisper.example.com

# GPT API (OpenAI/Anthropic)
VITE_GPT_API_KEY=your_gpt_api_key
VITE_GPT_API_URL=https://api.openai.com/v1

# Computer Vision API (Roboflow/Google Vision)
VITE_CV_API_KEY=your_cv_api_key
VITE_CV_API_URL=https://api.roboflow.com

# Text-to-Speech API (ElevenLabs/AWS Polly)
VITE_TTS_API_KEY=your_tts_api_key
VITE_TTS_API_URL=https://api.elevenlabs.io/v1
```

### API Integration

The app currently uses placeholder API calls in `src/api/apiCalls.ts`. To integrate real services:

1. **Replace placeholder functions** with actual API calls
2. **Add error handling** for network failures
3. **Implement authentication** for your chosen services
4. **Configure webhooks** for Zapier/Make integration

## 🏗️ Project Structure

```
/AgriSaarthi
├── /src
│   ├── /components
│   │   ├── RoleSelector.tsx      # Role selection screen
│   │   ├── FarmerChat.tsx        # Farmer chat interface
│   │   ├── GardenerChat.tsx      # Gardener chat interface
│   │   └── ChatBubble.tsx        # Message bubble component
│   ├── /api
│   │   └── apiCalls.ts           # API placeholder functions
│   ├── /pages
│   │   └── Index.tsx             # Main app component
│   └── main.tsx                  # App entry point
├── .env.example                  # Environment variables template
├── README.md                     # This file
└── package.json                  # Dependencies and scripts
```

## 🔌 API Functions

### Speech-to-Text (STT)
```typescript
callSTTAPI(audio: Blob): Promise<string>
```
Converts recorded audio to text for voice input processing.

### GPT Processing
```typescript
callGPTAPI(input: string, userType: 'farmer' | 'gardener'): Promise<string>
```
Processes user input with context-aware agricultural advice.

### Computer Vision
```typescript
callCVAPI(image: File): Promise<string>
```
Analyzes crop images for disease detection and growth assessment.

### Text-to-Speech (TTS)
```typescript
callTTSAPI(text: string): Promise<string>
```
Converts AI responses to audio for hands-free interaction.

## 🌐 Deployment

### Deploy to GitHub Pages

1. **Build the project**
   ```bash
   npm run build
   ```

2. **Deploy to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial AgriSaarthi deployment"
   git branch -M main
   git remote add origin https://github.com/yourusername/agrisaarthi.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Select "Deploy from a branch"
   - Choose "main" branch and "/dist" folder
   - Your app will be available at `https://yourusername.github.io/agrisaarthi`

### Deploy to Netlify/Vercel

1. **Connect your GitHub repository**
2. **Set build command**: `npm run build`
3. **Set publish directory**: `dist`
4. **Add environment variables** in the platform's settings

## 🛠️ Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Adding New Features

1. **New API Integration**: Add functions to `src/api/apiCalls.ts`
2. **UI Components**: Create components in `src/components/`
3. **Chat Features**: Extend message types in chat interfaces
4. **Styling**: Modify Tailwind classes for theme changes

## 🤝 Integration with External Services

### Zapier Integration
Replace API placeholders with Zapier webhook URLs:

```typescript
// Example Zapier webhook integration
const response = await fetch('https://hooks.zapier.com/hooks/catch/YOUR_HOOK_ID/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: userInput, userType })
});
```

### Make.com Integration
Similar to Zapier, replace with Make.com webhook endpoints.

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the [Issues](https://github.com/yourusername/agrisaarthi/issues) section
2. Review API documentation for your chosen services
3. Test with mock data first before integrating real APIs

## 🚀 Next Steps

1. **Replace mock APIs** with real services
2. **Add user authentication** for personalized advice
3. **Implement data persistence** for chat history
4. **Add offline functionality** with service workers
5. **Enhance CV capabilities** with more crop types
6. **Add location-based** weather and market data

---

Built with ❤️ for farmers and gardeners worldwide 🌱
