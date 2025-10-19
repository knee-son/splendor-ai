import { useNavigate } from 'react-router-dom';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
      <div className="flex flex-col w-[max-content] items-stretch gap-4">
        <button
          onClick={() => navigate('/cards')}
          className="w-full px-8 py-4 text-xl font-semibold bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
        >
          Check Splendor Cards
        </button>
        <button
          onClick={() => navigate('/nobles')}
          className="w-full px-8 py-4 text-xl font-semibold bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
        >
          Check Splendor Nobles
        </button>
      </div>
    </div>
  );
}