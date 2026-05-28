import { useAuth } from "../hooks/useAuth";

export default function Navbar() {
  const { user } = useAuth();

  return (
    <div className="h-14 px-4 flex items-center justify-between border-b border-gray-800 bg-gray-950">
      <h1 className="text-white font-semibold">DocMind</h1>

      <div className="text-sm text-gray-400">{user?.email}</div>
    </div>
  );
}
