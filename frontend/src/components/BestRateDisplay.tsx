// src/components/BestRateDisplay.tsx

import React from "react";
import { BestRate, DailyRecord } from "../types/types";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";
import { Table } from "@/components/ui/table"; // Ensure you have a Table component
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { Disclosure } from "@headlessui/react";
import { ChevronUpIcon } from "@heroicons/react/24/solid"; // Updated import path for Heroicons v2

interface Props {
  bestRate: BestRate;
}

const BestRateDisplay: React.FC<Props> = ({ bestRate }) => {
  const benefits = bestRate.split_strategy
    ? {
        rateDifference:
          bestRate.split_strategy.effective_rate - bestRate.best_rate,
        oneDayReturnDifference:
          bestRate.split_strategy.one_day_return - bestRate.one_day_return,
      }
    : null;

  // Prepare data for the chart
  const chartData =
    bestRate.daily_balances?.map((record: DailyRecord) => ({
      day: record.day,
      end_deposit: record.end_deposit,
    })) || [];

  return (
    <Card className="max-w-6xl mx-auto my-8 p-6">
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
              {bestRate.split_strategy.allocations.map((alloc, index) => (
                <p className="mb-1" key={index}>
                  <span className="font-semibold">Deposit:</span>{" "}
                  {alloc.deposit.toLocaleString()} TL in{" "}
                  {alloc.bank.replace(/_/g, " ")}
                </p>
              ))}
              <p className="mb-1">
                <span className="font-semibold">
                  Effective Rate After Split:
                </span>{" "}
                {bestRate.split_strategy.effective_rate}%
              </p>
              <p className="mb-1">
                <span className="font-semibold">
                  1-Day Return After Split:
                </span>{" "}
                {bestRate.split_strategy.one_day_return.toLocaleString()} TL
              </p>
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

        {/* Interactive Chart */}
        {chartData.length > 0 && (
          <>
            <Separator className="my-6" />
            <h3 className="text-lg font-medium mb-4">Deposit Growth Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={chartData}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="day"
                  label={{
                    value: "Day",
                    position: "insideBottomRight",
                    offset: -5,
                  }}
                />
                <YAxis
                  label={{
                    value: "Deposit (TL)",
                    angle: -90,
                    position: "insideLeft",
                  }}
                  tickFormatter={(value) => value.toLocaleString()}
                />
                <Tooltip
                  formatter={(value: number) => value.toLocaleString()}
                  labelFormatter={(label: number) => `Day ${label}`}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="end_deposit"
                  name="End Deposit"
                  stroke="#8884d8"
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </>
        )}

        {/* Daily Allocation Breakdown */}
        {bestRate.daily_balances && bestRate.daily_balances.length > 0 && (
          <>
            <Separator className="my-6" />
            <h3 className="text-lg font-medium mb-4">
              Daily Allocation Breakdown
            </h3>
            <div className="overflow-x-auto">
              <Table>
                <thead>
                  <tr>
                    <th>Day</th>
                    <th>Start Deposit (TL)</th>
                    <th>Interest Earned (TL)</th>
                    <th>End Deposit (TL)</th>
                  </tr>
                </thead>
                <tbody>
                  {bestRate.daily_balances.map((record: DailyRecord) => (
                    <tr key={record.day}>
                      <td>{record.day}</td>
                      <td>{record.start_deposit.toLocaleString()}</td>
                      <td>{record.interest.toLocaleString()}</td>
                      <td>{record.end_deposit.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>

            {/* Detailed Splits per Day with Accordions */}
            <div className="mt-6">
              {bestRate.daily_balances.map((record: DailyRecord) => (
                <Disclosure key={record.day} className="mb-4">
                  {({ open }) => (
                    <>
                      <Disclosure.Button className="flex justify-between w-full px-4 py-2 text-sm font-medium text-left text-purple-900 bg-purple-100 rounded-lg hover:bg-purple-200 focus:outline-none focus-visible:ring focus-visible:ring-purple-500 focus-visible:ring-opacity-75">
                        <span>Day {record.day} Allocations</span>
                        <ChevronUpIcon
                          className={`${
                            open ? "transform rotate-180" : ""
                          } w-5 h-5 text-purple-500`}
                        />
                      </Disclosure.Button>
                      <Disclosure.Panel className="px-4 pt-4 pb-2 text-sm text-gray-500">
                        <div className="overflow-x-auto">
                          <Table>
                            <thead>
                              <tr>
                                <th>Bank</th>
                                <th>Range Index</th>
                                <th>Deposit (TL)</th>
                                <th>Interest Earned (TL)</th>
                              </tr>
                            </thead>
                            <tbody>
                              {Object.entries(record.splits).map(
                                ([bank, splitInfo]) => (
                                  <tr key={`${record.day}-${bank}`}>
                                    <td>{bank.replace(/_/g, " ")}</td>
                                    <td>{splitInfo.range_idx}</td>
                                    <td>
                                      {splitInfo.deposit.toLocaleString()}
                                    </td>
                                    <td>
                                      {splitInfo.interest.toLocaleString()}
                                    </td>
                                  </tr>
                                )
                              )}
                            </tbody>
                          </Table>
                        </div>
                      </Disclosure.Panel>
                    </>
                  )}
                </Disclosure>
              ))}
            </div>
          </>
        )}

        {/* Additional Interactive Chart for Enhanced Visualization */}
        {chartData.length > 0 && (
          <>
            <Separator className="my-6" />
            <h3 className="text-lg font-medium mb-4">
              Visualize Deposit Growth
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={chartData}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="day"
                  label={{
                    value: "Day",
                    position: "insideBottomRight",
                    offset: -5,
                  }}
                />
                <YAxis
                  label={{
                    value: "Deposit (TL)",
                    angle: -90,
                    position: "insideLeft",
                  }}
                  tickFormatter={(value) => value.toLocaleString()}
                />
                <Tooltip
                  formatter={(value: number) => value.toLocaleString()}
                  labelFormatter={(label: number) => `Day ${label}`}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="end_deposit"
                  name="End Deposit"
                  stroke="#82ca9d"
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default BestRateDisplay;