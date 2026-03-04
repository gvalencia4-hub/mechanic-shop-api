import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { createOrder } from "../api/orders";
import {
  updateCount,
  removeFromCart,
  clearCart,
} from "../features/cart/cartSlice";

export default function CartPage() {
  const dispatch = useDispatch();
  const items = useSelector((state) => state.cart.items);

  const total = items.reduce((sum, item) => sum + item.price * item.count, 0);

  const handleCheckout = async () => {
    try {
      const orderId = await createOrder(items);
      alert(`Order placed! Order ID: ${orderId}`);
      dispatch(clearCart());
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div style={{ padding: 16 }}>
      <h1>Cart</h1>
      <div style={{ display: "flex", gap: 12 }}>
        <Link to="/">Home</Link>
        <Link to="/products">Back to Products</Link>
        <button onClick={() => dispatch(clearCart())}>Clear Cart</button>
      </div>

      {items.length === 0 ? (
        <p style={{ marginTop: 16 }}>Cart is empty.</p>
      ) : (
        <div style={{ marginTop: 16, display: "grid", gap: 12 }}>
          {items.map((item) => (
            <div
              key={item.id}
              style={{
                border: "1px solid #ddd",
                borderRadius: 8,
                padding: 12,
                display: "flex",
                gap: 12,
              }}
            >
              <img
                src={item.image}
                alt={item.title}
                style={{ width: 80, height: 80, objectFit: "contain" }}
              />
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600 }}>{item.title}</div>
                <div>${item.price}</div>

                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    marginTop: 8,
                  }}
                >
                  <button
                    onClick={() =>
                      dispatch(
                        updateCount({ id: item.id, count: item.count - 1 }),
                      )
                    }
                  >
                    -
                  </button>
                  <span>Qty: {item.count}</span>
                  <button
                    onClick={() =>
                      dispatch(
                        updateCount({ id: item.id, count: item.count + 1 }),
                      )
                    }
                  >
                    +
                  </button>

                  <button
                    onClick={() => dispatch(removeFromCart(item.id))}
                    style={{ marginLeft: "auto" }}
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          ))}

          <button onClick={handleCheckout} disabled={items.length === 0}>
            Checkout
          </button>
          <h2>Total: ${total.toFixed(2)}</h2>
        </div>
      )}
    </div>
  );
}
