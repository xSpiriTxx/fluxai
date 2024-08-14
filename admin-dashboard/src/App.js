import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [url, setUrl] = useState('');
  const [chatInput, setChatInput] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [message, setMessage] = useState('');

  // Function to scrape data from a URL and save it to FAISS
  const handleAddUrl = async () => {
    try {
      const response = await axios.post('http://localhost:8000/add-url', { url });
      setMessage(response.data.message);
      setUrl('');
    } catch (error) {
      console.error('Error adding URL:', error);
      setMessage('Error adding URL.');
    }
  };

  // Function to remove data related to a URL from FAISS
  const handleRemoveUrl = async () => {
    try {
      const response = await axios.post('http://localhost:8000/remove-url', { url });
      setMessage(response.data.message);
      setUrl('');
    } catch (error) {
      console.error('Error removing URL:', error);
      setMessage('Error removing URL.');
    }
  };

  // Function to send a chat message
  const handleChat = async () => {
    try {
      const response = await axios.post('http://localhost:8000/chat', { input: chatInput });
      setChatResponse(response.data.response);
    } catch (error) {
      console.error('Error generating chat response:', error);
      setChatResponse('Error generating chat response.');
    }
  };

  return (
    <div>
      <h1>FluxAI Dashboard</h1>

      {/* URL Management */}
      <div>
        <h2>Add or Remove URL</h2>
        <input
          type="text"
          placeholder="Enter URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button onClick={handleAddUrl}>Add URL</button>
        <button onClick={handleRemoveUrl}>Remove URL</button>
        <p>{message}</p>
      </div>

      {/* Chat Interface */}
      <div>
        <h2>Chat with Scraped Data</h2>
        <input
          type="text"
          placeholder="Ask a question"
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
        />
        <button onClick={handleChat}>Send</button>
        <p>Response: {chatResponse}</p>
      </div>
    </div>
  );
}

export default App;
