// src/types/types.ts

// src/types/types.ts

export interface SplitStrategy {
  allocations: Allocation[];
  effective_rate: number;
  one_day_return: number;
}

export interface Allocation {
  bank: string;
  deposit: number;
  interest: number;
}

export interface DailyRecord {
  day: number;
  start_deposit: number;
  interest: number;
  end_deposit: number;
  splits: Record<string, {
    range_idx: number;
    deposit: number;
    interest: number;
  }>;
}

export interface BestRate {
  best_bank: string;
  best_rate: number;
  one_day_return: number;
  split_strategy?: SplitStrategy;
  daily_balances?: DailyRecord[];
}

export interface BestRate {
    best_bank: string;
    best_rate: number;
    one_day_return: number;
    split_strategy?: SplitStrategy;
    effective_rate_after_split?: number;
    one_day_return_after_split?: number;
}

export interface GraphData {
    labels: string[];
    getir_finans_rates: number[];
    enpara_rates: number[];
    odeabank_hosgeldin_rates: number[];
    odeabank_devam_rates: number[];
    onhesap_rates: number[];
    teb_marifetli_hesap_rates: number[];
}