import { useAuth0 } from "@auth0/auth0-react";

export default function Login() {
  const { loginWithRedirect, isAuthenticated, user, logout } = useAuth0();

  return (
    <div style={{ padding: 24 }}>
      <h2>Login</h2>

      {!isAuthenticated ? (
        <button onClick={() => loginWithRedirect()}>Log in with Auth0</button>
      ) : (
        <>
          <p>Logged in as: {user?.email}</p>
          <button
            onClick={() =>
              logout({ logoutParams: { returnTo: window.location.origin } })
            }
          >
            Log out
          </button>
        </>
      )}
    </div>
  );
}
