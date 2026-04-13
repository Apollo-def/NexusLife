// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA1EvjdlY3OWUc5KoR70O9r81MkNNCmec4",
  authDomain: "nexuslife-1409b.firebaseapp.com",
  projectId: "nexuslife-1409b",
  storageBucket: "nexuslife-1409b.firebasestorage.app",
  messagingSenderId: "162871176799",
  appId: "1:162871176799:web:5ddc2cc315a5c2f98075ea",
  measurementId: "G-D54PLMVJH7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

export { app, auth, db, storage, analytics };
