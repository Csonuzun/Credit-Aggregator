import React from "react";
import { BestRate } from "../types/types"; // Import shared types
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";

interface Props {
  bestRate: BestRate;
}

const BestRateDisplay: React.FC<Props> = ({ bestRate }) => {
  const benefits = bestRate.split_strategy
    ? {
        rateDifference: bestRate.effective_rate_after_split! - bestRate.best_rate,
        oneDayReturnDifference:
          bestRate.one_day_return_after_split! - bestRate.one_day_return,
      }
    : null;

  return (
    <Card className="max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle>Best Rate Overview</CardTitle>
        <CardDescription>
          Compare and analyze the best rates and strategies for your deposit.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col md:flex-row md:space-x-8">
          {/* Best Rate Section */}
          <div className="flex-1">
            <h3 className="text-lg font-medium mb-2">Best Rate</h3>
            <p className="mb-1">
              <span className="font-semibold">Bank:</span>{" "}
              {bestRate.best_bank.replace(/_/g, " ")}
            </p>
            <p className="mb-1">
              <span className="font-semibold">Rate:</span> {bestRate.best_rate}%
            </p>
            <p className="mb-1">
              <span className="font-semibold">1-Day Return:</span>{" "}
              {bestRate.one_day_return.toLocaleString()} TL
            </p>
          </div>

          <Separator className="my-4 md:hidden" />

          {/* Recommended Split Strategy Section */}
          {bestRate.split_strategy && (
            <div className="flex-1">
              <h3 className="text-lg font-medium mb-2">
                Recommended Split Strategy
              </h3>
              <p className="mb-1">
                <span className="font-semibold">Deposit:</span>{" "}
                {bestRate.split_strategy.recommended_main_bank_deposit.toLocaleString()}{" "}
                TL in {bestRate.split_strategy.best_bank.replace(/_/g, " ")}
              </p>
              <p className="mb-1">
                <span className="font-semibold">Deposit:</span>{" "}
                {bestRate.split_strategy.recommended_alternative_deposit.toLocaleString()}{" "}
                TL in{" "}
                {bestRate.split_strategy.alternative_bank.replace(/_/g, " ")}
              </p>
              {bestRate.effective_rate_after_split !== undefined && (
                <>
                  <p className="mb-1">
                    <span className="font-semibold">
                      Effective Rate After Split:
                    </span>{" "}
                    {bestRate.effective_rate_after_split}%
                  </p>
                  <p className="mb-1">
                    <span className="font-semibold">
                      1-Day Return After Split:
                    </span>{" "}
                    {bestRate.one_day_return_after_split?.toLocaleString()} TL
                  </p>
                </>
              )}
            </div>
          )}
        </div>

        {/* Benefits Section */}
        {benefits && (
          <Alert className="mt-6" variant="success">
            <AlertTitle>Benefits of Splitting</AlertTitle>
            <AlertDescription>
              <p className="mb-1">
                <span className="font-semibold">Increased Effective Rate:</span>{" "}
                {benefits.rateDifference.toFixed(2)}%
              </p>
              <p className="mb-1">
                <span className="font-semibold">Additional 1-Day Return:</span>{" "}
                {benefits.oneDayReturnDifference.toLocaleString()} TL
              </p>
            </AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default BestRateDisplay;