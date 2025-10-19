import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import CardsPage from './pages/CardsPage';
import NoblesPage from './pages/NoblesPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/cards" element={<CardsPage />} />
        <Route path="/nobles" element={<NoblesPage />} />
      </Routes>
    </Router>
  );
}

export default App;
