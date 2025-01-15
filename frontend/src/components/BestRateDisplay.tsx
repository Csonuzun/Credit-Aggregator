// BestRateDisplay.tsx

import React from "react";

interface SplitStrategy {
    recommended_best_deposit: number;
    best_bank: string;
    alternative_bank: string;
    recommended_alternative_deposit: number;
}

interface BestRate {
    best_bank: string;
    best_rate: number;
    one_day_return: number;
    split_strategy?: SplitStrategy;
    effective_rate_after_split?: number;
    one_day_return_after_split?: number;
}

interface Props {
    bestRate: BestRate;
}

const BestRateDisplay: React.FC<Props> = ({ bestRate }) => {
    return (
        <div className="max-w-lg mx-auto p-4 border rounded shadow">
            <h2 className="text-2xl font-semibold">Best Rate</h2>
            <p className="mt-2">
                <strong>Bank:</strong> {bestRate.best_bank}
            </p>
            <p>
                <strong>Rate:</strong> {bestRate.best_rate}%
            </p>
            <p>
                <strong>1-Day Return:</strong> {bestRate.one_day_return.toLocaleString()} TL
            </p>

            {bestRate.split_strategy && bestRate.split_strategy.recommended_alternative_deposit > 0 && (
                <div className="mt-4">
                    <h3 className="text-xl font-semibold">Recommended Split Strategy</h3>
                    <p>
                        <strong>Deposit {bestRate.split_strategy.recommended_best_deposit.toLocaleString()} TL</strong> in{" "}
                        {bestRate.split_strategy.best_bank}
                    </p>
                    <p>
                        <strong>Deposit {bestRate.split_strategy.recommended_alternative_deposit.toLocaleString()} TL</strong> in{" "}
                        {bestRate.split_strategy.alternative_bank}
                    </p>

                    {bestRate.effective_rate_after_split !== undefined && (
                        <>
                            <p>
                                <strong>Effective Rate After Split:</strong> {bestRate.effective_rate_after_split}%
                            </p>
                            <p>
                                <strong>1-Day Return After Split:</strong> {bestRate.one_day_return_after_split?.toLocaleString()} TL
                            </p>
                        </>
                    )}
                </div>
            )}
        </div>
    );
};

export default BestRateDisplay;