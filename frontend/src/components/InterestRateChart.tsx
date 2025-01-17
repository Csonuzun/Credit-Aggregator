// InterestRateChart.tsx
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
} from "recharts";
import {
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
    ChartLegend,
    ChartLegendContent,
} from "@/components/ui/chart";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "./ui/card";
import { TrendingUp } from "lucide-react";

interface GraphData {
    labels: string[];
    getir_finans_rates: number[];
    enpara_rates: number[];
    odeabank_hosgeldin_rates: number[];
    odeabank_devam_rates: number[];
    onhesap_rates: number[]; // Added On Hesap
    teb_marifetli_hesap_rates: number[]; // Added Teb Marifetli Hesap
}

const chartConfig = {
    getirFinans: {
        label: "Getir Finans",
        color: "hsl(var(--chart-1))",
    },
    enpara: {
        label: "Enpara",
        color: "hsl(var(--chart-2))",
    },
    odeaBankHosgeldin: {
        label: "Odea Bank - Hoşgeldin",
        color: "hsl(var(--chart-3))",
    },
    odeaBankDevam: {
        label: "Odea Bank - Devam",
        color: "hsl(var(--chart-4))",
    },
    onHesap: { // Added On Hesap
        label: "On Hesap",
        color: "hsl(var(--chart-5))",
    },
    tebMarifetliHesap: { // Added Teb Marifetli Hesap
        label: "Teb Marifetli Hesap",
        color: "hsl(var(--chart-6))",
    }
} satisfies ChartConfig;

const InterestRateChart = ({ data }: { data: GraphData }) => {
    if (!data || !data.labels) {
        return <p className="text-center">Loading graph data...</p>;
    }

    const chartData = data.labels.map((label, index) => ({
        deposit: label,
        getirFinans: data.getir_finans_rates[index],
        enpara: data.enpara_rates[index],
        odeaBankHosgeldin: data.odeabank_hosgeldin_rates[index],
        odeaBankDevam: data.odeabank_devam_rates[index],
        onHesap: data.onhesap_rates[index], // Added On Hesap
        tebMarifetliHesap: data.teb_marifetli_hesap_rates[index], // Added Teb Marifetli Hesap
    }));

    // Function to calculate peak values for each bank
    const calculatePeakValues = () => {
        const peakValues: { [key: string]: { deposit: string; rate: number } } = {};

        Object.keys(chartConfig).forEach((bankKey) => {
            const rateKey = bankKey as keyof typeof chartConfig;
            let peakRate = -Infinity;
            let peakDeposit = "";

            chartData.forEach((dataPoint) => {
                const rate = dataPoint[rateKey];
                if (rate > peakRate) {
                    peakRate = rate;
                    peakDeposit = dataPoint.deposit;
                }
            });

            if (peakRate !== -Infinity) {
                peakValues[bankKey] = {
                    deposit: peakDeposit,
                    rate: peakRate,
                };
            }
        });

        return peakValues;
    };

    const peakValues = calculatePeakValues();

    return (
        <Card>
            <CardHeader>
                <CardTitle className="text-lg">Interest Rate Comparison</CardTitle>
                <CardDescription className="text-sm">
                    Compare interest rates for multiple banks over different deposit amounts.
                </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col md:flex-row">
                <ChartContainer config={chartConfig} className="flex-1 aspect-auto h-[500px] w-full">
                    <LineChart
                        data={chartData}
                        margin={{
                            left: 12,
                            right: 12,
                        }}
                    >
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="deposit"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            label={{ value: "Deposit Amount (TL)", position: "insideBottom", offset: -5, fontSize: 12 }}
                            fontSize={10}
                        />
                        <YAxis
                            tickLine={false}
                            axisLine={false}
                            label={{ value: "Interest Rate (%)", angle: -90, position: "insideLeft", fontSize: 12 }}
                            fontSize={10}
                        />
                        <ChartTooltip
                            content={
                                <ChartTooltipContent
                                    formatter={(value, name) => (
                                        <div className="flex items-center gap-2 text-sm">
                                            <div
                                                className="h-2.5 w-2.5 shrink-0 rounded-[2px]"
                                                style={{
                                                    backgroundColor: chartConfig[name as keyof typeof chartConfig]?.color || "#000",
                                                }}
                                            />
                                            <span className="font-medium text-xs">
                                                {chartConfig[name as keyof typeof chartConfig]?.label || name}
                                            </span>
                                            <div className="ml-auto text-muted-foreground font-mono text-xs">
                                                {value}%
                                            </div>
                                        </div>
                                    )}
                                />
                            }
                        />
                        <ChartLegend content={<ChartLegendContent />} />
                        {/* Lines for all banks */}
                        <Line
                            type="monotone"
                            dataKey="getirFinans"
                            stroke={chartConfig.getirFinans.color}
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                        <Line
                            type="monotone"
                            dataKey="enpara"
                            stroke={chartConfig.enpara.color}
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                        <Line
                            type="monotone"
                            dataKey="odeaBankHosgeldin"
                            stroke={chartConfig.odeaBankHosgeldin.color}
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                        <Line
                            type="monotone"
                            dataKey="odeaBankDevam"
                            stroke={chartConfig.odeaBankDevam.color}
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                        <Line // Added On Hesap Line
                            type="monotone"
                            dataKey="onHesap"
                            stroke={chartConfig.onHesap.color}
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                        <Line // Added Teb Marifetli Hesap Line
                            type="monotone"
                            dataKey="tebMarifetliHesap"
                            stroke={chartConfig.tebMarifetliHesap.color}
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                    </LineChart>
                </ChartContainer>
                {/* Peak Values Info Section */}
                <div className="mt-4 md:mt-0 md:ml-4 w-full md:w-1/4">
                    <Card className="p-3">
                        <CardHeader>
                            <CardTitle className="text-md">Peak Rates</CardTitle>
                        </CardHeader>
                        <CardContent className="px-2">
                            <ul className="text-sm">
                                {Object.entries(peakValues).map(([bankKey, peak]) => (
                                    <li key={bankKey} className="flex justify-between py-1">
                                        <span className="font-medium">
                                            {chartConfig[bankKey as keyof typeof chartConfig].label}
                                        </span>
                                        <span className="text-xs">
                                            {peak.rate}% @ {peak.deposit}
                                        </span>
                                    </li>
                                ))}
                            </ul>
                        </CardContent>
                    </Card>
                </div>
            </CardContent>
            <CardFooter>
                <div className="flex w-full items-start gap-2 text-sm">
                    <div className="grid gap-2">
                        <div className="flex items-center gap-2 font-medium leading-none">
                        </div>
                        <div className="flex items-center gap-2 leading-none text-muted-foreground">
                            Showing interest rates for various banks over different deposit amounts.
                        </div>
                    </div>
                </div>
            </CardFooter>
        </Card>
    );

};

export default InterestRateChart;