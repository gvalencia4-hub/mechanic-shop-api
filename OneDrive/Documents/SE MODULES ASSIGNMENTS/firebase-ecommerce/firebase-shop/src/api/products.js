import { db } from "../firebase";
import {
  collection,
  getDocs,
  addDoc,
  updateDoc,
  deleteDoc,
  doc,
} from "firebase/firestore";

const productsRef = collection(db, "products");

// READ: get all products
export const fetchAllProducts = async () => {
  const snapshot = await getDocs(productsRef);

  console.log("Firestore projectId:", db.app.options.projectId);

  // ✅ ADD THIS LINE RIGHT HERE
  console.log(
    "Doc IDs:",
    snapshot.docs.map((d) => d.id),
  );

  const products = snapshot.docs.map((d) => ({
    id: d.id,
    ...d.data(),
  }));

  console.log("Products docs:", products);

  return products;
};

// CREATE: add a product
export const createProduct = async (product) => {
  const docRef = await addDoc(productsRef, product);
  return { id: docRef.id, ...product };
};

// UPDATE: update a product
export const updateProduct = async (id, updates) => {
  const ref = doc(db, "products", id);
  await updateDoc(ref, updates);
  return true;
};

// DELETE: delete a product
export const deleteProduct = async (id) => {
  const ref = doc(db, "products", id);
  await deleteDoc(ref);
  return true;
};
