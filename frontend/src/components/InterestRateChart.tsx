import {LineChart, Line, XAxis, YAxis, CartesianGrid,} from "recharts";
import {ChartConfig, ChartContainer} from "@/components/ui/chart.tsx";
import {ChartTooltip, ChartTooltipContent} from "@/components/ui/chart"
import {Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle} from "./ui/card";
import {TrendingUp} from "lucide-react";
import {ChartLegend, ChartLegendContent} from "@/components/ui/chart"

interface GraphData {
    labels: string[];
    getir_finans_rates: number[];
    enpara_rates: number[];
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
} satisfies ChartConfig;

const InterestRateChart = ({data}: { data: GraphData }) => {
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
        <Card>
            <CardHeader>
                <CardTitle>Line Chart - Multiple</CardTitle>
                <CardDescription>January - June 2024</CardDescription>
            </CardHeader>
            <CardContent>

                <ChartContainer
                    config={chartConfig}
                    className="aspect-auto h-[500px] w-full">
                    <LineChart
                        accessibilityLayer
                        data={chartData}
                        margin={{
                            left: 12,
                            right: 12,
                        }}>
                        <CartesianGrid vertical={true}/>
                        <XAxis dataKey="deposit"
                               tickLine={true}
                               axisLine={true}
                               tickMargin={8}
                               minTickGap={32}
                               label={{value: "Deposit Amount (TL)", position: "insideBottom", offset: -5}}
                        />
                        <YAxis label={{value: "Interest Rate (%)", angle: -90, position: "insideLeft"}}/>
                        <ChartTooltip
                            content={
                                <ChartTooltipContent
                                    hideLabel
                                    formatter={(value, name) => (
                                        <div className="flex min-w-[180px] items-center text-sm text-muted-foreground">
                                            <span className="font-semibold">
                                                {chartConfig[name as keyof typeof chartConfig]?.label || name}
                                            </span>
                                            <div
                                                className="ml-auto flex items-baseline gap-0.5 font-mono font-medium tabular-nums text-foreground">
                                                {value}
                                                <span className="font-normal text-muted-foreground">%</span>
                                            </div>
                                        </div>
                                    )}
                                />
                            }
                            cursor={false}
                        /> <ChartLegend content={<ChartLegendContent/>}/>
                        <Line type="monotone" dataKey="getirFinans" stroke="rgb(75, 192, 192)" dot={false}
                              activeDot={true}/>
                        <Line type="monotone" dataKey="enpara" stroke="rgb(255, 99, 132)" dot={false} activeDot={true}/>
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
                            Showing total visitors for the last 6 months
                        </div>
                    </div>
                </div>
            </CardFooter>
        </Card>
    );
};

export default InterestRateChart;
