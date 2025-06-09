import { useState } from 'react';

function App() {
  const [name, setName] = useState('');
  const [comment, setComment] = useState('');
  const [status, setStatus] = useState(null);

  const API_URL = import.meta.env.VITE_API_URL;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);

    try {
      const response = await fetch(`${API_URL}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, comment }),
      });

      const data = await response.json();

      if (response.ok) {
        setStatus('Thank you for your feedback!');
        setName('');
        setComment('');
      } else {
        setStatus(`Error: ${data.error || 'Failed to submit'}`);
      }
    // eslint-disable-next-line no-unused-vars
    } catch (error) {
      setStatus('Something went wrong. Please try again.');
    }
  };

  return (
    <main style={{ padding: '2rem', maxWidth: '600px', margin: 'auto' }}>
      <h1>Feedback Form</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Name:<br />
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </label>
        <br /><br />
        <label>
          Comment:<br />
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            required
          />
        </label>
        <br /><br />
        <button type="submit">Submit</button>
      </form>
      {status && <p>{status}</p>}
    </main>
  );
}

export default App;
