import axios from "axios";

const api = axios.create({
  baseURL: "https://fakestoreapi.com",
});

export const fetchAllProducts = async () => {
  const { data } = await api.get("/products");
  return data;
};

export const fetchCategories = async () => {
  const { data } = await api.get("/products/categories");
  return data;
};

export const fetchProductsByCategory = async (category) => {
  const { data } = await api.get(`/products/category/${category}`);
  return data;
};
