import type { ReactElement } from "react";

import LandingPage from "@/pages/LandingPage";
import CardsPage from "@/pages/CardsPage";
import NoblesPage from "@/pages/NoblesPage";
import InitialGameStatePage from "@/pages/InitialGameStatePage";
import ModelTrainingPage from "@/pages/ModelTrainingPage";

interface AppRoute {
  label: string;
  path: string;
  element: ReactElement;
}

export const landingRoutes: AppRoute[] = [
  { label: "Home", path: "/", element: <LandingPage /> },
  { label: "Check Splendor Cards", path: "/cards", element: <CardsPage /> },
  { label: "Check Splendor Nobles", path: "/nobles", element: <NoblesPage /> },
  {
    label: "View Initial Game State",
    path: "/initial-game-state",
    element: <InitialGameStatePage />,
  },
  { label: "Start training!", path: "/train", element: <ModelTrainingPage /> },
];

export const appRoutes: AppRoute[] = [...landingRoutes];
