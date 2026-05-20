import { useState } from "react";
function TabSwitcher() {
  const [activeTab, setactiveTab] = useState("email");

  return (
    <div>
      <button
        onClick={() => setactiveTab("email")}
        style={{
          backgroundColor: activeTab === "email" ? "blue" : "gray",
          color: "white",
          padding: "8px 16px",
          marginRight: "8px",
        }}
      >
        Email
      </button>

      {activeTab === "email" && (
        <div>
          <p> Email tab is active</p>
          <input type="email" placeholder="Your email" />
        </div>
      )}
      <button
        onClick={() => setactiveTab("phone")}
        style={{
          backgroundColor: activeTab === "phone" ? "green" : "gray",
          color: "white",
          padding: "8px 16px",
          MarginLeft: "10px",
        }}
      >
        Phone
      </button>

      {activeTab === "phone" && (
        <div>
          <p> Phone tab is active </p>
          <input type="tel" placeholder="Enter your phone no." />
        </div>
      )}
    </div>
  );
}
export default TabSwitcher;
