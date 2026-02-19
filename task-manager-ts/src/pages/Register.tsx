import { useAuth0 } from "@auth0/auth0-react";

export default function Register() {
  const { loginWithRedirect } = useAuth0();

  return (
    <div style={{ padding: 24 }}>
      <h2>Register</h2>
      <button
        onClick={() =>
          loginWithRedirect({
            authorizationParams: { screen_hint: "signup" },
          })
        }
      >
        Create account with Auth0
      </button>
    </div>
  );
}
