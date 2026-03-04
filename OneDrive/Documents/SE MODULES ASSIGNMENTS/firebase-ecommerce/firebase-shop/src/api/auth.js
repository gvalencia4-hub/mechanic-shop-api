import { auth, db } from "../firebase";

import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
} from "firebase/auth";

import { doc, setDoc, serverTimestamp } from "firebase/firestore";

export const registerUser = async (email, password) => {
  const cred = await createUserWithEmailAndPassword(auth, email, password);

  // ✅ Create matching Firestore user document
  await setDoc(doc(db, "users", cred.user.uid), {
    email: cred.user.email,
    createdAt: serverTimestamp(),
  });

  return cred.user;
};

export const loginUser = async (email, password) => {
  const cred = await signInWithEmailAndPassword(auth, email, password);
  return cred.user;
};

export const logoutUser = async () => {
  await signOut(auth);
};
