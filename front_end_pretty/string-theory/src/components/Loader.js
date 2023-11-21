// Loader.js
import React from "react";
import ClipLoader from "react-spinners/ClipLoader";

const Loader = ({ loading }) => {
  return (
    <div style={{ position: "fixed", top: "50%", left: "50%"}}>
      <ClipLoader color={"#ffffff"} loading={loading} size={150} aria-label="Loading Spinner" data-testid="loader" />
    </div>
  );
};

export default Loader;
