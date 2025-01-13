import React from "react";

const BestRateDisplay = ({ bestRate }: { bestRate: { best_bank: string; best_rate: number } }) => {
  return (
    <div className="text-center mt-6">
      <h2 className="text-xl font-medium">Best Interest Rate</h2>
      <p className="text-lg mt-2">
        <strong>{bestRate.best_bank}</strong> offers the best rate at <strong>{bestRate.best_rate}%</strong>.
      </p>
    </div>
  );
};

export default BestRateDisplay;
