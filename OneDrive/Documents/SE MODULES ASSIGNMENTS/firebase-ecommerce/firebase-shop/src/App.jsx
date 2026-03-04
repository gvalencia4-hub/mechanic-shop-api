import { Routes, Route, Link } from "react-router-dom";
import Products from "./pages/Products";
import CartPage from "./pages/CartPage";
import homeImg from "./assets/IMG_1081.png";
import Login from "./pages/Login";
import Register from "./pages/Register";

function Home() {
  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "48px 24px",
        background: "#f7f7fb",
      }}
    >
      <div
        style={{
          maxWidth: 900,
          margin: "0 auto",
          background: "white",
          padding: 32,
          borderRadius: 12,
          boxShadow: "0 6px 18px rgba(0,0,0,0.08)",
        }}
      >
        <img src={homeImg} alt="Home" className="homeHeroImg" />
        <h1 style={{ fontSize: 56, margin: 0 }}>Aubree Rose Valencia Shop</h1>
        <p style={{ marginTop: 10, fontSize: 18, opacity: 0.75 }}>
          Browse products, add to cart, adjust quantities, and checkout total.
        </p>

        <div style={{ marginTop: 24, display: "flex", gap: 16 }}>
          <Link
            to="/products"
            style={{
              padding: "12px 18px",
              borderRadius: 10,
              background: "#111827",
              color: "white",
              textDecoration: "none",
            }}
          >
            View Products
          </Link>
          <Link
            to="/cart"
            style={{
              padding: "12px 18px",
              borderRadius: 10,
              border: "1px solid #d1d5db",
              textDecoration: "none",
            }}
          >
            Go to Cart
          </Link>
        </div>

        <div style={{ marginTop: 16, display: "flex", gap: 12 }}>
          <Link to="/register">Create Account</Link>
          <Link to="/login">Login</Link>
        </div>
      </div>
    </div>
  );
}
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/products" element={<Products />} />
      <Route path="/cart" element={<CartPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}
