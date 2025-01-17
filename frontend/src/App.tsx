// src/App.tsx

import React, { useState, useEffect } from "react"
import axios from "axios"
import BestRateDisplay from "./components/BestRateDisplay"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ThemeToggle } from "./components/ThemeToggle"
import { BestRate, GraphData } from "./types/types"
import { Checkbox } from "@/components/ui/checkbox"
import { DailyBalanceChart } from "./components/DailyBalanceChart"
import InterestRateChart from "./components/InterestRateChart" // Shadcn UI chart

interface CalculateBestRequest {
  deposit: number
  banks: string[]
  days: number
}

interface BankListResponse {
  banks: string[]
}

export default function App() {
  const [deposit, setDeposit] = useState<string>("")
  const [days, setDays] = useState<string>("")

  const [bestRate, setBestRate] = useState<BestRate | null>(null)
  const [graphData, setGraphData] = useState<GraphData | null>(null)
  const [trimmedGraphData, setTrimmedGraphData] = useState<GraphData | null>(null)

  // We store daily balances from server
  const [dailyBalances, setDailyBalances] = useState<number[]>([])

  // We'll store xMin, xMax => [initialDeposit..finalDeposit]
  const [xMin, setXMin] = useState<number | undefined>(undefined)
  const [xMax, setXMax] = useState<number | undefined>(undefined)

  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [availableBanks, setAvailableBanks] = useState<string[]>([])
  const [selectedBanks, setSelectedBanks] = useState<string[]>([])

  // -----------------------------
  // 1. Fetch the list of available banks
  // -----------------------------
  useEffect(() => {
    const fetchBanks = async () => {
      try {
        const response = await axios.get<BankListResponse>("http://127.0.0.1:5000/banks")
        setAvailableBanks(response.data.banks)
      } catch (error: any) {
        console.error("Error fetching banks:", error)
        setError("Failed to fetch available banks.")
      }
    }
    fetchBanks()
  }, [])

  // -----------------------------
  // 2. Fetch the original graph data
  // -----------------------------
  useEffect(() => {
    const fetchGraphData = async () => {
      try {
        const response = await axios.get<GraphData>("http://127.0.0.1:5000/graph-data")
        setGraphData(response.data)
        setTrimmedGraphData(response.data) // By default, show full range for all banks
      } catch (error: any) {
        console.error("Error fetching graph data:", error)
        setError("Failed to fetch graph data.")
      }
    }
    fetchGraphData()
  }, [])

  // -----------------------------
  // Toggle bank selection
  // -----------------------------
  const handleBankSelection = (bank: string) => {
    setSelectedBanks((prev) =>
      prev.includes(bank) ? prev.filter((b) => b !== bank) : [...prev, bank]
    )
  }

  // -----------------------------
  // Calculate best rate & daily balances
  // -----------------------------
  const handleCalculateBest = async () => {
    setBestRate(null)
    setError(null)
    setIsLoading(true)

    const depositNum = Number(deposit)
    const daysNum = Number(days)
    if (isNaN(depositNum) || depositNum <= 0) {
      setError("Please enter a valid deposit amount.")
      setIsLoading(false)
      return
    }
    if (selectedBanks.length === 0) {
      setError("Please select at least one bank.")
      setIsLoading(false)
      return
    }

    try {
      const requestBody: CalculateBestRequest = {
        deposit: depositNum,
        banks: selectedBanks,
        days: daysNum, // pass days to server
      }

      // server calculates best rate & daily balances
      const response = await axios.post<{
        best_bank: string
        best_rate: number
        one_day_return: number
        split_strategy?: any
        effective_rate_after_split?: number
        one_day_return_after_split?: number
        daily_balances: number[]
      }>("http://127.0.0.1:5000/calculate-best", requestBody)

      // store bestRate
      const { best_bank, best_rate, daily_balances, one_day_return } = response.data
      setBestRate({
        best_bank,
        best_rate,
        one_day_return
      } as BestRate)

      // store daily balances
      if (daily_balances && daily_balances.length > 0) {
        setDailyBalances(daily_balances)
        // set xMin and xMax based on daily_balances
        setXMin(daily_balances[0])
        setXMax(daily_balances[daily_balances.length - 1])
      } else {
        setDailyBalances([])
        setXMin(undefined)
        setXMax(undefined)
      }

      // After setting xMin and xMax, trimmedGraphData will be updated via useEffect

    } catch (error: any) {
      console.error("Error calculating the best rate:", error)
      setError("Failed to calculate the best rate. Please try again later.")
    } finally {
      setIsLoading(false)
    }
  }

  // -----------------------------
  // Trim the data to [xMin, xMax] and keep only best bank's data
  // -----------------------------
  useEffect(() => {
    if (!graphData) return

    let updated: GraphData = JSON.parse(JSON.stringify(graphData))

    if (xMin !== undefined && xMax !== undefined && xMax > xMin) {
      updated = trimGraphData(updated, xMin, xMax)
    }

    if (bestRate?.best_bank) {
      updated = reduceToBestBank(updated, bestRate.best_bank)
    }

    setTrimmedGraphData(updated)
  }, [graphData, xMin, xMax, bestRate])

  // -----------------------------
  // Helper Functions
  // -----------------------------
  /**
   * Trim the graph data to only include deposits between min and max.
   */
  const trimGraphData = (original: GraphData, min: number, max: number): GraphData => {
    const newLabels: string[] = []
    const depositValues: number[] = []
    const getirRates: number[] = []
    const enparaRates: number[] = []
    const hosgeldinRates: number[] = []
    const devamRates: number[] = []
    const onHesapRates: number[] = []
    const tebMarifetliRates: number[] = []

    original.depositValues.forEach((depositValue, i) => {
      if (depositValue >= min && depositValue <= max) {
        newLabels.push(original.labels[i])
        depositValues.push(depositValue)
        getirRates.push(original.getir_finans_rates[i])
        enparaRates.push(original.enpara_rates[i])
        hosgeldinRates.push(original.odeabank_hosgeldin_rates[i])
        devamRates.push(original.odeabank_devam_rates[i])
        onHesapRates.push(original.onhesap_rates[i])
        tebMarifetliRates.push(original.teb_marifetli_hesap_rates[i])
      }
    })

    return {
      labels: newLabels,
      depositValues: depositValues,
      getir_finans_rates: getirRates,
      enpara_rates: enparaRates,
      odeabank_hosgeldin_rates: hosgeldinRates,
      odeabank_devam_rates: devamRates,
      onhesap_rates: onHesapRates,
      teb_marifetli_hesap_rates: tebMarifetliRates,
    }
  }

  /**
   * Reduce the graph data to only include the best bank's rates.
   */
  const reduceToBestBank = (original: GraphData, bestBankKey: string): GraphData => {
    const length = original.labels.length
    let gfRates: number[] = new Array(length).fill(0)
    let enpRates: number[] = new Array(length).fill(0)
    let hosRates: number[] = new Array(length).fill(0)
    let devRates: number[] = new Array(length).fill(0)
    let onhRates: number[] = new Array(length).fill(0)
    let tebRates: number[] = new Array(length).fill(0)

    switch (bestBankKey) {
      case "getir_finans":
        gfRates = [...original.getir_finans_rates]
        break
      case "enpara":
        enpRates = [...original.enpara_rates]
        break
      case "odeabank_hosgeldin":
        hosRates = [...original.odeabank_hosgeldin_rates]
        break
      case "odeabank_devam":
        devRates = [...original.odeabank_devam_rates]
        break
      case "onhesap":
        onhRates = [...original.onhesap_rates]
        break
      case "teb_marifetli_hesap":
        tebRates = [...original.teb_marifetli_hesap_rates]
        break
      default:
        break
    }

    return {
      labels: [...original.labels],
      depositValues: [...original.depositValues],
      getir_finans_rates: gfRates,
      enpara_rates: enpRates,
      odeabank_hosgeldin_rates: hosRates,
      odeabank_devam_rates: devRates,
      onhesap_rates: onhRates,
      teb_marifetli_hesap_rates: tebRates,
    }
  }

  return (
    <div className="container mx-auto p-4 space-y-8">
      <header className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Bank Interest Rate Comparison</h1>
        <ThemeToggle />
      </header>

      <section className="text-center">
        <p className="mt-2">
          Calculate and compare the best interest rates for your deposit.
        </p>
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

        <label htmlFor="daysInput" className="block text-sm font-medium mt-4">
          How many days will you keep it in interest?
        </label>
        <Input
          type="number"
          id="daysInput"
          value={days}
          onChange={(e) => setDays(e.target.value)}
          placeholder="e.g., 30"
          className="mt-1 block w-full"
        />

        <fieldset className="mt-4">
          <legend className="text-sm font-medium">
            Select Banks You Have an Account With:
          </legend>
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
          disabled={isLoading || deposit === "" || selectedBanks.length === 0}
        >
          {isLoading ? "Calculating..." : "Calculate Best Rate"}
        </Button>

        {error && <p className="text-red-500 mt-2">{error}</p>}
      </div>

      {/* If we have trimmedGraphData, show the chart */}
      {trimmedGraphData && (
        <InterestRateChart
          data={trimmedGraphData}
          title="Interest Rates by Bank (Best Bank Only)"
        />
      )}

      {/* Show best rate display + daily balances side by side, if any */}
      {(bestRate || dailyBalances.length > 1) && (
        <div className="flex flex-col md:flex-row md:space-x-8">
          {bestRate && (
            <div className="flex-1">
              <BestRateDisplay bestRate={bestRate} />
            </div>
          )}
          {dailyBalances.length > 1 && (
            <div className="flex-1">
              <DailyBalanceChart
                dailyBalances={dailyBalances}
                title="Daily Balances (from backend)"
                daysLabel={days ? `Day 0 - Day ${days}` : undefined}
              />
            </div>
          )}
        </div>
      )}
    </div>
  )
}