import { useNavigate } from 'react-router-dom';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-center h-screen bg-gray-50">
      <button
        onClick={() => navigate('/cards')}
        className="px-8 py-4 text-xl font-semibold bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
      >
        Go to Check Cards
      </button>
    </div>
  );
}