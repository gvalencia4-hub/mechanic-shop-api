import { createSlice } from "@reduxjs/toolkit";

const KEY = "cart";

const loadCart = () => {
  try {
    const raw = sessionStorage.getItem(KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
};

const saveCart = (items) => {
  sessionStorage.setItem(KEY, JSON.stringify(items));
};

const initialState = { items: loadCart() };

const cartSlice = createSlice({
  name: "cart",
  initialState,
  reducers: {
    addToCart: (state, action) => {
      const product = action.payload;
      const existing = state.items.find((x) => x.id === product.id);

      if (existing) existing.count += 1;
      else state.items.push({ ...product, count: 1 });

      saveCart(state.items);
    },
    removeFromCart: (state, action) => {
      state.items = state.items.filter((x) => x.id !== action.payload);
      saveCart(state.items);
    },
    updateCount: (state, action) => {
      const { id, count } = action.payload;
      const item = state.items.find((x) => x.id === id);
      if (item) item.count = count;
      saveCart(state.items);
    },

    clearCart: (state) => {
      state.items = [];
      sessionStorage.removeItem(KEY);
    },
  },
});

export const { addToCart, removeFromCart, updateCount, clearCart } =
  cartSlice.actions;
export default cartSlice.reducer;
