import React from 'react';
import { Spotify } from 'react-spotify-embed';
import './Spotify_comp.css'; // Import the CSS file

const Spotify_comp = ({ link }) => {
  // Check if uri is null before rendering
  if (link === null || link === '') {
    
    return null; // If null, don't render anything
  }
  console.log(link)
  console.log("akjdkjashdkjash")

  return (
    <div className="spotify-container">
      <Spotify
        link={link}
        view="list"
        theme="black"
        className="custom-spotify-size" // Apply a custom class to the Spotify component
      />
    </div>
  );
};

export default Spotify_comp;
