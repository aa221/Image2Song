import React from 'react';
import { FileButton } from './components/Buttons';
import './App.css';

function App() {
  const handleFileUpload = async (formData) => {
    try {
      // Perform the file upload to your API endpoint
      const response = await fetch('http://127.0.0.1:5000/pipeline', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('File uploaded successfully');
      } else {
        console.error('Failed to upload file');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className='App'>
      <FileButton customPosition={true} customPositiontwo={true} onFileUpload={handleFileUpload}>
      </FileButton>
      
      {/* Add another button or any other content as needed */}
    </div>
  );
}

export default App;