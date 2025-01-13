import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
interface GraphData {
  labels: string[];
  getir_finans_rates: number[];
  enpara_rates: number[];
}
const InterestRateChart = ({ data }: { data: GraphData }) => {
  // Ensure the data is valid before rendering
  console.log(data)
  if (!data || !data.labels || !data.getir_finans_rates || !data.enpara_rates) {
    return <p className="text-center">Loading graph data...</p>;
  }

  // Transform the graph data into a usable format for Recharts
  const chartData = data.labels.map((label: string, index: number) => ({
    deposit: label,
    getirFinans: data.getir_finans_rates[index],
    enpara: data.enpara_rates[index],
  }));

  return (
    <div className="bg-card p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-medium text-center mb-4">Interest Rate Graph</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="deposit" label={{ value: "Deposit Amount (TL)", position: "insideBottom", offset: -5 }} />
          <YAxis label={{ value: "Interest Rate (%)", angle: -90, position: "insideLeft" }} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="getirFinans" stroke="rgb(75, 192, 192)" />
          <Line type="monotone" dataKey="enpara" stroke="rgb(255, 99, 132)" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default InterestRateChart;
