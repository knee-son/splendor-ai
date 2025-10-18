import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import CardsPage from './pages/CardsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/cards" element={<CardsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
