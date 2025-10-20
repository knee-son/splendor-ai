import LandingPage from "@/pages/LandingPage";
import CardsPage from "@/pages/CardsPage";
import NoblesPage from "@/pages/NoblesPage";
import InitialGameStatePage from "@/pages/InitialGameStatePage";

export const appRoutes = [
  { label: "Home", path: "/", element: <LandingPage /> },
  { label: "Check Splendor Cards", path: "/cards", element: <CardsPage /> },
  { label: "Check Splendor Nobles", path: "/nobles", element: <NoblesPage /> },
  { label: "View Initial Game State", path: "/initial-game-state", element: <InitialGameStatePage /> },
];
