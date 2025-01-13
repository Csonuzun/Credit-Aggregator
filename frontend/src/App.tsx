import React, {useState, useEffect} from "react";
import axios from "axios";
import InterestRateChart from "./components/InterestRateChart";
import BestRateDisplay from "./components/BestRateDisplay";
import {Button} from "@/components/ui/button"
import { Input } from "@/components/ui/input"


interface GraphData {
    labels: string[];
    getir_finans_rates: number[];
    enpara_rates: number[];
}

const App = () => {
    const [deposit, setDeposit] = useState<number>(0);
    const [bestRate, setBestRate] = useState<{ best_bank: string; best_rate: number } | null>(null);
    const [graphData, setGraphData] = useState<GraphData | null>(null);

    const handleCalculateBest = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:5000/calculate-best", {deposit});
            setBestRate(response.data);
        } catch (error) {
            console.error("Error calculating the best rate:", error);
        }
    };

    useEffect(() => {
        const fetchGraphData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/graph-data");
                setGraphData(response.data);
            } catch (error) {
                console.error("Error fetching graph data:", error);
            }
        };

        fetchGraphData();
    }, []);

    return (

        <div className="container mx-auto p-4 space-y-8">
            <header className="text-center">
                <h1 className="text-3xl font-bold">Bank Interest Rate Comparison</h1>
                <p className="text mt-2">Calculate and compare the best interest rates for your deposit.</p>
            </header>

            <div className="max-w-lg mx-auto">
                <label htmlFor="deposit" className="block text-sm font-medium">
                    Enter Deposit Amount (TL):
                </label>
                <Input
                    type="number"
                    id="deposit"
                    value={deposit}
                    onChange={(e) => setDeposit(Number(e.target.value))}
                />
                <Button variant="destructive" className="mt-4"
                        onClick={handleCalculateBest}
                >
                    Calculate Best Rate
                </Button>

            </div>

            {bestRate && <BestRateDisplay bestRate={bestRate}/>}

            {graphData && <InterestRateChart data={graphData}/>}
        </div>
    );
};

export default App;
