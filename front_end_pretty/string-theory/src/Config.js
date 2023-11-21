import { initializeApp } from "firebase/app";
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey: "AIzaSyAuh8Dt26N7g4kV5yHItu7NOs__DSRAWxA",
  authDomain: "string-theory-f2ce4.firebaseapp.com",
  projectId: "string-theory-f2ce4",
  storageBucket: "string-theory-f2ce4.appspot.com",
  messagingSenderId: "198064938630",
  appId: "1:198064938630:web:291c352b81f4f11f24fb07"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const imageDb = getStorage(app)