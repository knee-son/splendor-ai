import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { appRoutes } from "@/routes";

function App() {
  return (
    <Router>
      <Routes>
        {appRoutes.map(({ path, element }) => (
          <Route key={path} path={path} element={element} />
        ))}
      </Routes>
    </Router>
  );
}

export default App;
