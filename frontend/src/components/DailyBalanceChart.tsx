// src/components/DailyBalanceChart.tsx
import React from "react"
import { TrendingUp } from "lucide-react"
import {
  AreaChart,
  Area,
  CartesianGrid,
  XAxis,
  YAxis, // Optional Y-axis for clarity
} from "recharts"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

/**
 * dailyBalances: array of numbers, e.g. [1000, 1002.7, 1005.4, ...]
 * daysLabel: optional textual label for the card (e.g. 'Days 0 - 30')
 */
interface DailyBalanceChartProps {
  dailyBalances: number[]
  title?: string
  daysLabel?: string
}

/**
 * Example color configuration for our single dataset
 */
const chartConfig = {
  balance: {
    label: "Daily Balance",
    color: "hsl(var(--chart-1))", // or any custom Tailwind variable
  },
}

export function DailyBalanceChart({
  dailyBalances,
  title = "Daily Balances",
  daysLabel,
}: DailyBalanceChartProps) {
  // Transform dailyBalances into Recharts data format:
  // e.g. [{ day: 0, balance: 1000 }, { day: 1, balance: 1002.7 }, ...]
  const chartData = dailyBalances.map((balance, i) => ({
    day: i,
    balance,
  }))

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>
          {daysLabel || "Projection of deposit over selected days"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <AreaChart
            accessibilityLayer
            data={chartData}
            margin={{
              left: 12,
              right: 12,
            }}
          >
            {/* Basic grid */}
            <CartesianGrid vertical={false} />

            {/* X-axis: show 'Day 0', 'Day 1', etc. */}
            <XAxis
              dataKey="day"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tickFormatter={(value) => `Day ${value}`}
            />
            {/* Optional Y-axis for clarity */}
            <YAxis
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              // e.g. to format with commas or currency
              tickFormatter={(val) => Intl.NumberFormat().format(val)}
            />

            {/* Tooltip */}
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />

            {/* Gradients */}
            <defs>
              <linearGradient id="fillBalance" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-balance)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-balance)"
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>

            <Area
              dataKey="balance"
              type="monotone"
              fill="url(#fillBalance)"
              fillOpacity={0.4}
              stroke="var(--color-balance)"
              strokeWidth={2}
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
      <CardFooter>
        <div className="flex w-full items-start gap-2 text-sm">
          <div className="grid gap-2">
            <div className="flex items-center gap-2 font-medium leading-none">
              Projected growth
              <TrendingUp className="h-4 w-4" />
            </div>
            <div className="flex items-center gap-2 leading-none text-muted-foreground">
              {daysLabel || "Day 0 - Day N"}
            </div>
          </div>
        </div>
      </CardFooter>
    </Card>
  )
}