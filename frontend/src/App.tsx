// src/App.tsx

import React, {useState, useEffect} from "react";
import axios from "axios";
import InterestRateChart from "./components/InterestRateChart";
import BestRateDisplay from "./components/BestRateDisplay";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import {ThemeToggle} from "./components/ThemeToggle";
import {BestRate, GraphData} from "./types/types"; // Import shared types
import {Checkbox} from "@/components/ui/checkbox.tsx";

interface CalculateBestRequest {
    deposit: number;
    banks: string[];
}

interface BankListResponse {
    banks: string[];
}

const App = () => {
    const [deposit, setDeposit] = useState<string>('');
    const [bestRate, setBestRate] = useState<BestRate | null>(null);
    const [graphData, setGraphData] = useState<GraphData | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [availableBanks, setAvailableBanks] = useState<string[]>([]);
    const [selectedBanks, setSelectedBanks] = useState<string[]>([]);

    useEffect(() => {
        const fetchBanks = async () => {
            try {
                const response = await axios.get<BankListResponse>("http://127.0.0.1:5000/banks");
                setAvailableBanks(response.data.banks);
            } catch (error: any) {
                console.error("Error fetching banks:", error);
                // Optionally set an error state here if you want to notify the user
            }
        };

        fetchBanks();
    }, []);

    useEffect(() => {
        const fetchGraphData = async () => {
            try {
                const response = await axios.get<GraphData>("http://127.0.0.1:5000/graph-data");
                setGraphData(response.data);
            } catch (error: any) {
                console.error("Error fetching graph data:", error);
                // Optionally set an error state here if you want to notify the user
            }
        };

        fetchGraphData();
    }, []);

    const handleBankSelection = (bank: string) => {
        setSelectedBanks(prevSelected => {
            if (prevSelected.includes(bank)) {
                // Remove the bank from selection
                return prevSelected.filter(b => b !== bank);
            } else {
                // Add the bank to selection
                return [...prevSelected, bank];
            }
        });
    };

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

        // Ensure at least one bank is selected
        if (selectedBanks.length === 0) {
            setError("Please select at least one bank.");
            setIsLoading(false);
            return;
        }

        try {
            const requestBody: CalculateBestRequest = {
                deposit: depositNumber,
                banks: selectedBanks
            };

            const response = await axios.post<BestRate>("http://127.0.0.1:5000/calculate-best", requestBody);
            setBestRate(response.data);
        } catch (error: any) {
            console.error("Error calculating the best rate:", error);
            setError("Failed to calculate the best rate. Please try again later.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-4 space-y-8">
            <header className="flex justify-between items-center">
                <h1 className="text-3xl font-bold">Bank Interest Rate Comparison</h1>
                <ThemeToggle/>
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

                <fieldset className="mt-4">
                    <legend className="text-sm font-medium">Select Banks You Have an Account With:</legend>
                    <div className="mt-2 space-y-2">
                        {availableBanks.map((bank) => (
                            <div key={bank} className="flex items-start">
                                <Checkbox
                                    id={bank}
                                    checked={selectedBanks.includes(bank)}
                                    onCheckedChange={() => handleBankSelection(bank)}
                                    className="h-4 w-4 text-blue-600 border-gray-300 rounded"
                                />
                                <label
                                    htmlFor={bank}
                                    className="ml-2 capitalize text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                                >
                                    {bank.replace(/_/g, " ")}
                                </label>
                            </div>
                        ))}
                    </div>
                </fieldset>


                <Button
                    variant="default"
                    className="mt-4"
                    onClick={handleCalculateBest}
                    disabled={isLoading || Number(deposit) <= 0 || selectedBanks.length === 0}
                >
                    {isLoading ? "Calculating..." : "Calculate Best Rate"}
                </Button>
                {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>

            {bestRate && <BestRateDisplay bestRate={bestRate}/>}

            {graphData && <InterestRateChart data={graphData}/>}
        </div>
    );
};

export default App;