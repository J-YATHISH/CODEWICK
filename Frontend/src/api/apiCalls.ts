
// API placeholder functions for AgriSaarthi
// These are dummy implementations that will be replaced with real API calls

/**
 * Speech-to-Text API call
 * Converts audio to text using Whisper or similar service
 */
export async function callSTTAPI(audio: Blob): Promise<string> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  // Mock responses for demonstration
  const mockResponses = [
    "My tomato plants have yellow leaves",
    "When should I harvest my wheat crop?",
    "There are insects on my cucumber plants",
    "What fertilizer should I use for corn?",
    "My soil seems too dry"
  ];
  
  const randomResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)];
  
  console.log('STT API called with audio blob:', audio);
  console.log('STT Response:', randomResponse);
  
  return randomResponse;
}

/**
 * GPT API call for agricultural advice
 * Processes user input and provides contextual farming/gardening advice
 */
export async function callGPTAPI(input: string, userType: 'farmer' | 'gardener'): Promise<string> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  console.log('GPT API called:', { input, userType });
  
  // Enhanced context-aware responses
  const farmerResponses = {
    'tomato': 'Yellow leaves on tomatoes often indicate overwatering or nutrient deficiency. Check soil moisture and consider adding nitrogen fertilizer. Also ensure proper drainage.',
    'wheat': 'Wheat is typically ready for harvest when the grain moisture content is around 13-15%. Look for golden color and test grain hardness by biting.',
    'cucumber': 'For cucumber pests, try neem oil spray or introduce beneficial insects like ladybugs. Remove affected leaves and ensure good air circulation.',
    'corn': 'Corn benefits from nitrogen-rich fertilizer during vegetative growth. Apply 10-10-10 fertilizer at planting and side-dress with nitrogen when plants are knee-high.',
    'soil': 'Dry soil can be improved with organic matter like compost. Consider drip irrigation for efficient water use. Test soil pH - it should be 6.0-7.0 for most crops.',
    'default': 'As a farmer, focus on soil health, proper irrigation, and integrated pest management. Consider crop rotation and weather patterns for optimal yields.'
  };
  
  const gardenerResponses = {
    'water': 'Most garden plants need about 1 inch of water per week. Water deeply but less frequently to encourage deep root growth. Morning watering is best.',
    'plant': 'Spring and fall are typically the best times for planting. Consider your hardiness zone and last frost date. Prepare soil with compost before planting.',
    'flower': 'For vibrant flowers, ensure adequate sunlight (6+ hours for most), regular feeding with balanced fertilizer, and deadheading spent blooms.',
    'vegetable': 'Vegetable gardens need rich, well-draining soil. Start with easy crops like lettuce, radishes, and herbs. Succession plant for continuous harvest.',
    'pest': 'For garden pests, try companion planting, beneficial insects, or organic sprays like soap solution. Remove affected plants promptly.',
    'default': 'Gardening success comes from understanding your plants\' needs: light, water, soil, and nutrients. Start small and expand as you learn!'
  };
  
  const responses = userType === 'farmer' ? farmerResponses : gardenerResponses;
  
  // Find relevant response based on keywords
  let response = responses.default;
  for (const [keyword, advice] of Object.entries(responses)) {
    if (input.toLowerCase().includes(keyword)) {
      response = advice;
      break;
    }
  }
  
  // Add weather and market context for farmers
  if (userType === 'farmer') {
    const weatherTip = "\n\nWeather forecast: Sunny with 20% chance of rain. Good conditions for field work.";
    const marketTip = "\nMarket prices: Wheat ₹25/kg, Tomatoes ₹40/kg, Corn ₹22/kg.";
    response += weatherTip + marketTip;
  }
  
  console.log('GPT Response:', response);
  return response;
}

/**
 * Computer Vision API call
 * Analyzes images to detect crop diseases, pests, or growth issues
 */
export async function callCVAPI(image: File): Promise<string> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2500));
  
  console.log('CV API called with image:', image.name, image.size);
  
  // Mock image analysis responses
  const analysisResults = [
    "Detected: Early blight on tomato leaves. Recommend copper-based fungicide treatment and improved air circulation.",
    "Identified: Aphid infestation on crop. Suggest neem oil spray or introducing ladybugs for biological control.",
    "Analysis: Nutrient deficiency detected - likely nitrogen shortage. Leaves show yellowing pattern consistent with N-deficiency.",
    "Found: Powdery mildew on plant surface. Increase air circulation and apply sulfur-based fungicide.",
    "Detected: Healthy crop growth with no visible issues. Continue current care routine.",
    "Identified: Possible overwatering - leaves show signs of water stress. Reduce irrigation frequency."
  ];
  
  const randomResult = analysisResults[Math.floor(Math.random() * analysisResults.length)];
  
  console.log('CV Analysis Result:', randomResult);
  return randomResult;
}

/**
 * Text-to-Speech API call
 * Converts AI responses to audio for hands-free interaction
 */
export async function callTTSAPI(text: string): Promise<string> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  console.log('TTS API called with text:', text.substring(0, 50) + '...');
  
  // In a real implementation, this would return the actual audio file URL
  // For now, return a mock URL
  const mockAudioURL = `https://mock-tts-service.com/audio/${Date.now()}.mp3`;
  
  console.log('TTS Audio URL:', mockAudioURL);
  return mockAudioURL;
}

/**
 * Fallback function for when APIs fail
 * Provides local tips and advice when network calls fail
 */
export function showLocalTips(userType: 'farmer' | 'gardener'): string {
  const farmerTips = [
    "Always test your soil pH before planting - most crops prefer 6.0-7.0 pH.",
    "Rotate your crops annually to prevent soil depletion and pest buildup.",
    "Monitor weather patterns and plan irrigation accordingly.",
    "Keep detailed records of planting dates, treatments, and yields."
  ];
  
  const gardenerTips = [
    "Water plants early in the morning to reduce evaporation and disease risk.",
    "Mulch around plants to retain moisture and suppress weeds.",
    "Deadhead flowers regularly to encourage continued blooming.",
    "Companion plant to naturally deter pests and improve growth."
  ];
  
  const tips = userType === 'farmer' ? farmerTips : gardenerTips;
  const randomTip = tips[Math.floor(Math.random() * tips.length)];
  
  return `Here's a helpful tip while offline: ${randomTip}`;
}
