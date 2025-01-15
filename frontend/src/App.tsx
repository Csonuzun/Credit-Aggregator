// App.tsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import InterestRateChart from "./components/InterestRateChart";
import BestRateDisplay from "./components/BestRateDisplay";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ThemeToggle } from "./components/ThemeToggle";

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

interface GraphData {
    labels: string[];
    getir_finans_rates: number[];
    enpara_rates: number[];
    odea_bank_hosgeldin_rates: number[];
    odea_bank_devam_rates: number[];
}

const App = () => {
    const [deposit, setDeposit] = useState<string>(''); // Changed to string
    const [bestRate, setBestRate] = useState<BestRate | null>(null);
    const [graphData, setGraphData] = useState<GraphData | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const handleCalculateBest = async () => {
        // Reset previous state
        setBestRate(null);
        setError(null);
        setIsLoading(true);

        // Convert deposit to a number
        const depositNumber = Number(deposit);

        // Validate the converted number
        if (isNaN(depositNumber) || depositNumber <= 0) {
            setError("Please enter a valid deposit amount.");
            setIsLoading(false);
            return;
        }

        try {
            const response = await axios.post("http://127.0.0.1:5000/calculate-best", { deposit: depositNumber });
            setBestRate(response.data);
        } catch (error: any) {
            console.error("Error calculating the best rate:", error);
            setError("Failed to calculate the best rate. Please try again later.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        const fetchGraphData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/graph-data");
                setGraphData(response.data);
            } catch (error: any) {
                console.error("Error fetching graph data:", error);
                // Optionally set an error state here if you want to notify the user
            }
        };

        fetchGraphData();
    }, []);

    return (
        <div className="container mx-auto p-4 space-y-8">
            <header className="flex justify-between items-center">
                <h1 className="text-3xl font-bold">Bank Interest Rate Comparison</h1>
                <ThemeToggle />
            </header>

            <section className="text-center">
                <p className="text mt-2">Calculate and compare the best interest rates for your deposit.</p>
            </section>

            <div className="max-w-lg mx-auto">
                <label htmlFor="deposit" className="block text-sm font-medium">
                    Enter Deposit Amount (TL):
                </label>
                <Input
                    type="number"
                    id="deposit"
                    value={deposit}
                    onChange={(e) => setDeposit(e.target.value)}
                    placeholder="e.g., 55000"
                    className="mt-1 block w-full"
                />
                <Button
                    variant="default"
                    className="mt-4"
                    onClick={handleCalculateBest}
                    disabled={isLoading || Number(deposit) <= 0}
                >
                    {isLoading ? "Calculating..." : "Calculate Best Rate"}
                </Button>
                {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>

            {bestRate && <BestRateDisplay bestRate={bestRate} />}

            {graphData && <InterestRateChart data={graphData} />}
        </div>
    );
};

export default App;