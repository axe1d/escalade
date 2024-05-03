import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [user, setUser] = useState({ firstName: '', lastName: '' });
  const [accessCode, setAccessCode] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUser(prevState => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/generate-access-code', user);
      setAccessCode(response.data.accessCode);
    } catch (error) {
      console.error('Error fetching the access code:', error);
    }
  };

  return (
    <div className="App">
      <h1>Access Code Generator</h1>
      <form onSubmit={handleSubmit}>
        <input
          name="firstName"
          type="text"
          value={user.firstName}
          onChange={handleChange}
          placeholder="First Name"
          required
        />
        <input
          name="lastName"
          type="text"
          value={user.lastName}
          onChange={handleChange}
          placeholder="Last Name"
          required
        />
        <button type="submit">Get Access Code</button>
      </form>
      {accessCode && <p>Your access code is: {accessCode}</p>}
    </div>
  );
}

export default App;
