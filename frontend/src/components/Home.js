import React, { useEffect, useState } from 'react';
import api from '../services/api';

function Home() {
  const [welcomeMessage, setWelcomeMessage] = useState('');

  useEffect(() => {
    async function fetchMessage() {
      try {
        const response = await api.get('../rizzder_app/view/home'); // Adjust to your backend's endpoint
        setWelcomeMessage(response.data.message); // Backend returns { message: "Welcome!" }
      } catch (error) {
        console.error('Error fetching home data:', error);
      }
    }

    fetchMessage();
  }, []);

  return (
    <div>
      <h1>Welcome to the App</h1>
      <p>{welcomeMessage}</p>
    </div>
  );
}

export default Home;
