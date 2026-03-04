import { db, auth } from "../firebase";
import { addDoc, collection, serverTimestamp } from "firebase/firestore";
import { onAuthStateChanged } from "firebase/auth";

// Wait for Firebase auth to finish loading the user
const waitForUser = () =>
  new Promise((resolve) => {
    const unsub = onAuthStateChanged(auth, (user) => {
      unsub();
      resolve(user);
    });
  });

// Remove ALL undefined values (Firestore does NOT allow undefined)
const stripUndefined = (value) => {
  if (Array.isArray(value)) {
    return value.map(stripUndefined);
  }
  if (value && typeof value === "object") {
    const out = {};
    for (const [k, v] of Object.entries(value)) {
      if (v === undefined) continue;
      out[k] = stripUndefined(v);
    }
    return out;
  }
  return value;
};

export const createOrder = async (items) => {
  const user = auth.currentUser || (await waitForUser());

  if (!user) {
    throw new Error("Please login first, then try checkout again.");
  }

  const total = items.reduce(
    (sum, item) => sum + (item.price ?? 0) * (item.count ?? 0),
    0,
  );

  const order = stripUndefined({
    userId: user.uid,
    userEmail: user.email,
    createdAt: serverTimestamp(),
    total,
    items: items.map((i) => ({
      id: i.id,
      title: i.title,
      price: i.price,
      count: i.count,
      image: i.image,
      category: i.category,
    })),
  });

  const ref = await addDoc(collection(db, "orders"), order);
  return ref.id;
};
