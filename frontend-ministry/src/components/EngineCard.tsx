interface CardProps {
  cardNumber: number;
}

export default function EngineCard({ cardNumber }: CardProps) {
  return (
    <div className="w-80 h-96 border-2 border-gray-800 flex items-center justify-center text-2xl font-semibold rounded-lg bg-white shadow-md">
      This is card number {cardNumber}
    </div>
  );
}
