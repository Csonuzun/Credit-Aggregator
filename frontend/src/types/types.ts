// src/types/types.ts

export interface SplitStrategy {
    recommended_main_bank_deposit: number;
    best_bank: string;
    alternative_bank: string;
    recommended_alternative_deposit: number;
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