import { useNavigate } from "react-router-dom";
import { landingRoutes } from "@/routes";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
      <div className="flex flex-col w-max items-stretch gap-4">
        {landingRoutes
          .filter((route) => route.label !== "Home")
          .map(({ label, path }) => (
            <button
              key={path}
              onClick={() => navigate(path)}
              className="px-8 py-4 text-xl font-semibold bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
            >
              {label}
            </button>
          ))}
      </div>
    </div>
  );
}
