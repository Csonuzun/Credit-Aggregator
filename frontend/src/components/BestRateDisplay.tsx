// src/components/BestRateDisplay.tsx
import React from "react";
import { BestRate } from "../types/types"; // Import shared types

interface Props {
    bestRate: BestRate;
}

const BestRateDisplay: React.FC<Props> = ({ bestRate }) => {
    // Calculate benefits if split strategy is available
    const benefits = bestRate.split_strategy
        ? {
              rateDifference: bestRate.effective_rate_after_split! - bestRate.best_rate,
              oneDayReturnDifference:
                  bestRate.one_day_return_after_split! - bestRate.one_day_return,
          }
        : null;

    return (
        <div className="max-w-4xl mx-auto p-6 border rounded shadow">
            <h2 className="text-2xl font-semibold mb-4">Best Rate Overview</h2>
            <div className="flex flex-col md:flex-row md:space-x-8">
                {/* Best Rate Section */}
                <div className="flex-1">
                    <h3 className="text-xl font-medium mb-2">Best Rate</h3>
                    <p className="mb-1">
                        <strong>Bank:</strong> {bestRate.best_bank.replace(/_/g, " ")}
                    </p>
                    <p className="mb-1">
                        <strong>Rate:</strong> {bestRate.best_rate}%
                    </p>
                    <p className="mb-1">
                        <strong>1-Day Return:</strong> {bestRate.one_day_return.toLocaleString()} TL
                    </p>
                </div>

                {/* Recommended Split Strategy Section */}
                {bestRate.split_strategy && (
                    <div className="flex-1 mt-4 md:mt-0">
                        <h3 className="text-xl font-medium mb-2">Recommended Split Strategy</h3>
                        <p className="mb-1">
                            <strong>Deposit:</strong> {bestRate.split_strategy.recommended_main_bank_deposit.toLocaleString()} TL in{" "}
                            {bestRate.split_strategy.best_bank.replace(/_/g, " ")}
                        </p>
                        <p className="mb-1">
                            <strong>Deposit:</strong> {bestRate.split_strategy.recommended_alternative_deposit.toLocaleString()} TL in{" "}
                            {bestRate.split_strategy.alternative_bank.replace(/_/g, " ")}
                        </p>
                        {bestRate.effective_rate_after_split !== undefined && (
                            <>
                                <p className="mb-1">
                                    <strong>Effective Rate After Split:</strong> {bestRate.effective_rate_after_split}%
                                </p>
                                <p className="mb-1">
                                    <strong>1-Day Return After Split:</strong> {bestRate.one_day_return_after_split?.toLocaleString()} TL
                                </p>
                            </>
                        )}
                    </div>
                )}
            </div>

            {/* Benefits Section */}
            {benefits && (
                <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded">
                    <h3 className="text-xl font-medium mb-2">Benefits of Splitting</h3>
                    <p className="mb-1">
                        <strong>Increased Effective Rate:</strong> {benefits.rateDifference.toFixed(2)}%
                    </p>
                    <p className="mb-1">
                        <strong>Additional 1-Day Return:</strong> {benefits.oneDayReturnDifference.toLocaleString()} TL
                    </p>
                </div>
            )}
        </div>
    );

};

export default BestRateDisplay;