interface CardFooterProps {
  cardNumber: number;
  setCardNumber: React.Dispatch<React.SetStateAction<number>>;
}

export default function CardFooter({ cardNumber, setCardNumber }: CardFooterProps) {
  const handlePrev = () => setCardNumber((prev) => Math.max(1, prev - 1));
  const handleNext = () => setCardNumber((prev) => Math.min(90, prev + 1));

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    if (!isNaN(value) && value >= 1 && value <= 90) {
      setCardNumber(value);
    } else if (value % 100 <= 90) {
      setCardNumber(value % 100);
    } else if (isNaN(value)) {
      setCardNumber(1);
    }
  };

  return (
    <div className="flex items-center gap-4">
      <button
        onClick={handlePrev}
        className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 transition disabled:opacity-50"
        disabled={cardNumber <= 1}
      >
        &lt;
      </button>

      <input
        type="string"
        value={cardNumber}
        onChange={handleInputChange}
        min={1}
        max={90}
        className="w-16 text-center border rounded border-gray-300 px-2 py-1"
      />

      <button
        onClick={handleNext}
        className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 transition disabled:opacity-50"
        disabled={cardNumber >= 90}
      >
        &gt;
      </button>
    </div>
  );
}
