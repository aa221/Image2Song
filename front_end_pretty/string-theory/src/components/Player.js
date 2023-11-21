import React from 'react';
import AudioPlayer from 'react-h5-audio-player';
import 'react-h5-audio-player/lib/styles.css';

const Player = ({ audioUrl }) => (
  <AudioPlayer
    autoPlay
    src={audioUrl} // Use the provided audioUrl here
    onPlay={() => console.log("onPlay")}
    // other props here
  />
);

export default Player;
