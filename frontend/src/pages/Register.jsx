import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    role: "creator",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");

      await api.post("/auth/register", form);

      alert("Account created successfully! Please sign in.");
      navigate("/login");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#0a0a0a] px-4 text-white">
      <div className="w-full max-w-md rounded-2xl border border-white/10 bg-[#151515] p-7 shadow-2xl">
        <div className="mb-7 text-center">
          <h1 className="text-4xl font-bold">
            Creator<span className="text-purple-500">IQ</span>
          </h1>
          <p className="mt-2 text-sm text-gray-500">
            Create your creator analytics account
          </p>
        </div>

        <h2 className="mb-5 text-xl font-semibold">Create Account</h2>

        {error && (
          <p className="mb-4 rounded-lg bg-red-500/10 p-3 text-sm text-red-400">
            {error}
          </p>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Full name"
            required
            value={form.full_name}
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
            className="w-full rounded-lg border border-white/10 bg-[#0f0f0f] px-4 py-3 outline-none focus:border-purple-500"
          />

          <input
            type="email"
            placeholder="Email address"
            required
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            className="w-full rounded-lg border border-white/10 bg-[#0f0f0f] px-4 py-3 outline-none focus:border-purple-500"
          />

          <input
            type="password"
            placeholder="Password"
            required
            minLength={8}
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            className="w-full rounded-lg border border-white/10 bg-[#0f0f0f] px-4 py-3 outline-none focus:border-purple-500"
          />

          <select
            value={form.role}
            onChange={(e) => setForm({ ...form, role: e.target.value })}
            className="w-full rounded-lg border border-white/10 bg-[#0f0f0f] px-4 py-3 text-white outline-none"
          >
            <option value="creator">Creator</option>
          </select>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-purple-600 px-4 py-3 font-semibold hover:bg-purple-500 disabled:opacity-50"
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-400">
          Already have an account?{" "}
          <Link to="/login" className="text-purple-400 hover:text-purple-300">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Register;