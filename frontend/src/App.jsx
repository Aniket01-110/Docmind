import Loginform from "./components/pracloginform";
import FakeSignUp from "./components/prc";
/*import SimpleForm from "./components/SimpleForm";*/
import TabSwitcher from "./components/TabSwitcher";

function App() {
  return (
    <div
      style={{
        backgroundColor: "#0f0f0f",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        color: "white",
        fontFamily: "Arial",
      }}
    >
      <h1> DocMind</h1>
      <p>AI-powered document assistant</p>
      <p style={{ color: "#4ade80" }}>✅ React frontend is working!</p>

      <Loginform />
      <TabSwitcher />
      <FakeSignUp />
    </div>
  );
}

export default App;
