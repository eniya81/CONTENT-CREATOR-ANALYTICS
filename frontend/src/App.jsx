import {
  HashRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import Dashboard from "./pages/Dashboard";
import ContentAnalytics from "./pages/ContentAnalytics";
import AudienceAnalytics from "./pages/AudienceAnalytics";
import GrowthTrends from "./pages/GrowthTrends";
import Revenue from "./pages/Revenue";
import Sponsorships from "./pages/Sponsorships";
import Notifications from "./pages/Notifications";
import Reports from "./pages/Reports";
import Login from "./pages/Login";
import Register from "./pages/Register";

function DashboardLayout() {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#0a0a0a] text-white">
      <Sidebar />

      <div className="flex min-w-0 flex-1 flex-col">
        <Header />

        <main className="min-h-0 flex-1 overflow-y-auto">
          <div className="w-full p-6 lg:p-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/content" element={<ContentAnalytics />} />
              <Route path="/audience" element={<AudienceAnalytics />} />
              <Route path="/growth" element={<GrowthTrends />} />
              <Route path="/revenue" element={<Revenue />} />
              <Route path="/sponsorships" element={<Sponsorships />} />
              <Route path="/notifications" element={<Notifications />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="*"
          element={
            localStorage.getItem("access_token")
              ? <DashboardLayout />
              : <Navigate to="/login" replace />
          }
        />
      </Routes>
    </HashRouter>
  );
}

export default App;