import { useQuery } from "@tanstack/react-query";
import { fetchAllProducts } from "../api/products";
import { useDispatch } from "react-redux";
import { addToCart } from "../features/cart/cartSlice";
import { Link } from "react-router-dom";

export default function Products() {
  const dispatch = useDispatch();

  const {
    data = [],
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["products"],
    queryFn: fetchAllProducts,
  });

  if (isLoading) return <h2>Loading products...</h2>;
  if (isError) return <pre>Error: {String(error?.message || error)}</pre>;

  return (
    <div style={{ padding: 16 }}>
      <h1>Products</h1>

      <div style={{ display: "flex", gap: 16, marginBottom: 16 }}>
        <Link to="/">Home</Link>
        <Link to="/cart">Go to Cart</Link>
      </div>

      <div
        style={{
          display: "grid",
          gap: 16,
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          marginTop: 16,
        }}
      >
       {data.length === 0 ? (
  <p>No products found.</p>
) : (
  data.map((p) => (
    <div
      key={p.id}
      style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}
    >
      <img
        src={p.image}
        alt={p.name}
        style={{ width: "100%", height: 180, objectFit: "contain" }}
      />
      <h3 style={{ fontSize: 14 }}>{p.name}</h3>
      <p>
        <b>${p.price}</b>
      </p>

      <button
        onClick={() =>
          dispatch(
            addToCart({
              id: p.id,
              title: p.name,
              price: p.price,
              image: p.image,
            })
          )
        }
      >
        Add to Cart
      </button>
    </div>
  ))
)}      </div>
    </div>
  );
}