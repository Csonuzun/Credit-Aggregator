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
import {TrendingUp} from "lucide-react";

interface GraphData {
    labels: string[];
    getir_finans_rates: number[];
    enpara_rates: number[];
    odea_bank_hosgeldin_rates: number[];
    odea_bank_devam_rates: number[];
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
} satisfies ChartConfig;

const InterestRateChart = ({data}: { data: GraphData }) => {
    if (!data || !data.labels) {
        return <p className="text-center">Loading graph data...</p>;
    }

    const chartData = data.labels.map((label, index) => ({
        deposit: label,
        getirFinans: data.getir_finans_rates[index],
        enpara: data.enpara_rates[index],
        odeaBankHosgeldin: data.odea_bank_hosgeldin_rates[index],
        odeaBankDevam: data.odea_bank_devam_rates[index],
    }));

    return (
        <Card>
            <CardHeader>
                <CardTitle>Interest Rate Comparison</CardTitle>
                <CardDescription>
                    Compare interest rates for multiple banks over different deposit amounts.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <ChartContainer config={chartConfig} className="aspect-auto h-[500px] w-full">
                    <LineChart
                        data={chartData}
                        margin={{
                            left: 12,
                            right: 12,
                        }}
                    >
                        <CartesianGrid vertical={false}/>
                        <XAxis
                            dataKey="deposit"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            label={{value: "Deposit Amount (TL)", position: "insideBottom", offset: -5}}
                        />
                        <YAxis
                            tickLine={false}
                            axisLine={false}
                            label={{value: "Interest Rate (%)", angle: -90, position: "insideLeft"}}
                        />
                        <ChartTooltip
                            content={
                                <ChartTooltipContent
                                    formatter={(value, name) => (
                                        <div className="flex items-center gap-2 text-sm">
                                            <div
                                                className="h-2.5 w-2.5 shrink-0 rounded-[2px]"
                                                style={{
                                                    backgroundColor: `var(--color-${name})`,
                                                }}
                                            />
                                            <span className="font-medium">
                        {chartConfig[name as keyof typeof chartConfig]?.label || name}
                      </span>
                                            <div className="ml-auto text-muted-foreground font-mono">
                                                {value}%
                                            </div>
                                        </div>
                                    )}
                                />
                            }
                        />
                        <ChartLegend content={<ChartLegendContent/>}/>
                        {/* Lines for all banks */}
                        <Line
                            type="monotone"
                            dataKey="getirFinans"
                            stroke="hsl(var(--chart-1))"
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                        <Line
                            type="monotone"
                            dataKey="enpara"
                            stroke="hsl(var(--chart-2))"
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                        <Line
                            type="monotone"
                            dataKey="odeaBankHosgeldin"
                            stroke="hsl(var(--chart-3))"
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                        <Line
                            type="monotone"
                            dataKey="odeaBankDevam"
                            stroke="hsl(var(--chart-4))"
                            strokeWidth={2}
                            dot={false}
                            activeDot={true}
                        />
                    </LineChart>
                </ChartContainer>
            </CardContent>
            <CardFooter>
                <div className="flex w-full items-start gap-2 text-sm">
                    <div className="grid gap-2">
                        <div className="flex items-center gap-2 font-medium leading-none">
                            Trending up by 5.2% this month <TrendingUp className="h-4 w-4"/>
                        </div>
                        <div className="flex items-center gap-2 leading-none text-muted-foreground">
                            Showing total visitors for the last 6 months.
                        </div>
                    </div>
                </div>
            </CardFooter>
        </Card>
    );
};

export default InterestRateChart;