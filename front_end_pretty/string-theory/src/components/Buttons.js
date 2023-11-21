// FileButton.js
import React, { useRef, useState } from "react";
import "./Buttons.css";
import { imageDb } from "../Config";
import { getDownloadURL, ref, uploadBytes } from "firebase/storage";
import { v4 } from "uuid";
import Player from './Player';
import Loader from "./Loader";  // Import the Loader component
import Spotify_comp from './Spotify_comp';
const style = { position: "fixed", top: "50%", left: "50%", transform: "translate(-50%, -50%)" };


const STYLES = ["btn--primary", "btn--outline", "btn--test"];
const SIZES = ["btn--medium", "btn--large"];

export const FileButton = ({
  children,
  type,
  buttonStyle,
  buttonSize,
  customPosition,
  customPositiontwo
}) => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fileInputRef = useRef(null);
  const checkButtonStyle = STYLES.includes(buttonStyle)
    ? buttonStyle
    : STYLES[0];
  const checkButtonSize = SIZES.includes(buttonSize) ? buttonSize : SIZES[0];
  const [img, setImg] = useState(null);
  const [imgUrl, setImgUrl] = useState([]);
  const [audioUrl, setAudioUrl] = useState('');
  const [spottyUrl, setSpottyUrl] = useState('');
  const uploadTaskRef = useRef(null);

const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setImg(selectedFile);
  };

  const handleButtonClick = () => {
    // Trigger the click event on the file input element
    fileInputRef.current.click();
  };
  
  const handleUploadButtonClick = async () => {
    setError(null);
    setLoading(true);

    if (img) {
      const imgRef = ref(imageDb, `images/${img.name + " " + v4()}`);
      const controller = new AbortController();
      uploadTaskRef.current = controller;
  
      try {
        await uploadBytes(imgRef, img, { signal: controller.signal });
        const url = await getDownloadURL(imgRef);
  
        setImgUrl((data) => [...data, url]);
  
        alert("File uploaded successfully!");
  
        try {
          const response = await fetch("/pipeline", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ url }),
          });

          if (response.ok) {
            const result = await response.json();
  
            if (
              result.hasOwnProperty("data") &&
              Array.isArray(result.data) &&
              result.data.length > 0
            ) {
              const fetchedAudioUrl = result.data[0];
              const fetchedSpottyUrl = result.data[1];
              console.log("lkdhjflkdhjaf");
              console.log(fetchedAudioUrl);
              setAudioUrl(fetchedAudioUrl);
              console.log("oooooooooooooh")
              setSpottyUrl(fetchedSpottyUrl);
              console.log(fetchedSpottyUrl);
            } else {
              console.error(
                "API response does not contain a valid audio URL array."
              );
              setError("No audio data found. Please try again!");
            }
          } else {
            throw new Error("Failed to submit data");
          }
        } catch (error) {
          console.error("API Error:", error);
          setError("Error communicating with the server. Please try again!");
        } finally {
          setLoading(false);
        }
      } catch (error) {
        if (error.name === "AbortError") {
          console.log("Upload canceled");
        } else {
          setError("Error uploading file. Please try again.");
          console.error("Error uploading file:", error);
        }
      } finally {
        uploadTaskRef.current = null;
      }
    } else {
      setError("Please select a file to upload.");
      setLoading(false);
    }
  };

 
  console.log('spottyUrl:', spottyUrl);

  return (
    <div style={{ position: 'relative', marginBottom: '100px' }}>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
      <button
        className={`btn ${checkButtonStyle} ${checkButtonSize} ${
          customPosition ? "btn-custom" : ""
        }`}
        onClick={handleButtonClick}
        type={type}
      >
        Select File
      </button>
      <button
        className={`btn ${checkButtonStyle} ${checkButtonSize} ${
          customPositiontwo ? "btn-custom-two" : ""
        }`}
        onClick={handleUploadButtonClick}
        type={type}
      >
        Upload
      </button>

      {loading && <Loader loading={loading} />} {/* Use the Loader component */}

      {error && (
        <div style={{ color: 'red', marginTop: '10px', position: 'absolute', bottom: '10px', left: '50%', transform: 'translateX(-50%)', fontSize: '18px' }}>
          <p>Error: {error}</p>
          <button onClick={() => setError(null)}>Try Again!</button>
        </div>
      )}


       
      


      <Player audioUrl={audioUrl} />

      {spottyUrl !== null && <Spotify_comp link={spottyUrl} />}
    </div>
  );
};

export default FileButton;
