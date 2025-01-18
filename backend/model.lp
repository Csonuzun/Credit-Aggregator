\* Maximize_Interest *\
Maximize
OBJ: 0.000876712328767 interest_enpara_0 + 0.000958904109589 interest_enpara_1
 + 0.00104109589041 interest_enpara_2 + 0.00112328767123 interest_enpara_3
 + 0.00139726027397 interest_teb_marifetli_hesap_1
 + 0.00139726027397 interest_teb_marifetli_hesap_10
 + 0.00139726027397 interest_teb_marifetli_hesap_2
 + 0.00139726027397 interest_teb_marifetli_hesap_3
 + 0.00139726027397 interest_teb_marifetli_hesap_4
 + 0.00139726027397 interest_teb_marifetli_hesap_5
 + 0.00139726027397 interest_teb_marifetli_hesap_6
 + 0.00139726027397 interest_teb_marifetli_hesap_7
 + 0.00139726027397 interest_teb_marifetli_hesap_8
 + 0.00139726027397 interest_teb_marifetli_hesap_9
Subject To
ExactlyOneRange_enpara: range_enpara_0 + range_enpara_1 + range_enpara_2
 + range_enpara_3 = 1
ExactlyOneRange_teb_marifetli_hesap: range_teb_marifetli_hesap_0
 + range_teb_marifetli_hesap_1 + range_teb_marifetli_hesap_10
 + range_teb_marifetli_hesap_2 + range_teb_marifetli_hesap_3
 + range_teb_marifetli_hesap_4 + range_teb_marifetli_hesap_5
 + range_teb_marifetli_hesap_6 + range_teb_marifetli_hesap_7
 + range_teb_marifetli_hesap_8 + range_teb_marifetli_hesap_9 = 1
Interest_Lower_enpara_0: - deposit_enpara_0 + interest_enpara_0
 - 55000 range_enpara_0 >= -55000
Interest_Lower_enpara_1: - deposit_enpara_1 + interest_enpara_1
 - 55000 range_enpara_1 >= -55000
Interest_Lower_enpara_2: - deposit_enpara_2 + interest_enpara_2
 - 55000 range_enpara_2 >= -55000
Interest_Lower_enpara_3: - deposit_enpara_3 + interest_enpara_3
 - 55000 range_enpara_3 >= -55000
Interest_Lower_teb_marifetli_hesap_0: - deposit_teb_marifetli_hesap_0
 + interest_teb_marifetli_hesap_0 - 55000 range_teb_marifetli_hesap_0
 >= -55000
Interest_Lower_teb_marifetli_hesap_1: - deposit_teb_marifetli_hesap_1
 + interest_teb_marifetli_hesap_1 - 55000 range_teb_marifetli_hesap_1
 >= -60000
Interest_Lower_teb_marifetli_hesap_10: - deposit_teb_marifetli_hesap_10
 + interest_teb_marifetli_hesap_10 - 55000 range_teb_marifetli_hesap_10
 >= -255000
Interest_Lower_teb_marifetli_hesap_2: - deposit_teb_marifetli_hesap_2
 + interest_teb_marifetli_hesap_2 - 55000 range_teb_marifetli_hesap_2
 >= -62500
Interest_Lower_teb_marifetli_hesap_3: - deposit_teb_marifetli_hesap_3
 + interest_teb_marifetli_hesap_3 - 55000 range_teb_marifetli_hesap_3
 >= -70000
Interest_Lower_teb_marifetli_hesap_4: - deposit_teb_marifetli_hesap_4
 + interest_teb_marifetli_hesap_4 - 55000 range_teb_marifetli_hesap_4
 >= -85000
Interest_Lower_teb_marifetli_hesap_5: - deposit_teb_marifetli_hesap_5
 + interest_teb_marifetli_hesap_5 - 55000 range_teb_marifetli_hesap_5
 >= -105000
Interest_Lower_teb_marifetli_hesap_6: - deposit_teb_marifetli_hesap_6
 + interest_teb_marifetli_hesap_6 - 55000 range_teb_marifetli_hesap_6
 >= -105000
Interest_Lower_teb_marifetli_hesap_7: - deposit_teb_marifetli_hesap_7
 + interest_teb_marifetli_hesap_7 - 55000 range_teb_marifetli_hesap_7
 >= -130000
Interest_Lower_teb_marifetli_hesap_8: - deposit_teb_marifetli_hesap_8
 + interest_teb_marifetli_hesap_8 - 55000 range_teb_marifetli_hesap_8
 >= -155000
Interest_Lower_teb_marifetli_hesap_9: - deposit_teb_marifetli_hesap_9
 + interest_teb_marifetli_hesap_9 - 55000 range_teb_marifetli_hesap_9
 >= -205000
Interest_NonNeg_enpara_0: interest_enpara_0 >= 0
Interest_NonNeg_enpara_1: interest_enpara_1 >= 0
Interest_NonNeg_enpara_2: interest_enpara_2 >= 0
Interest_NonNeg_enpara_3: interest_enpara_3 >= 0
Interest_NonNeg_teb_marifetli_hesap_0: interest_teb_marifetli_hesap_0 >= 0
Interest_NonNeg_teb_marifetli_hesap_1: interest_teb_marifetli_hesap_1 >= 0
Interest_NonNeg_teb_marifetli_hesap_10: interest_teb_marifetli_hesap_10 >= 0
Interest_NonNeg_teb_marifetli_hesap_2: interest_teb_marifetli_hesap_2 >= 0
Interest_NonNeg_teb_marifetli_hesap_3: interest_teb_marifetli_hesap_3 >= 0
Interest_NonNeg_teb_marifetli_hesap_4: interest_teb_marifetli_hesap_4 >= 0
Interest_NonNeg_teb_marifetli_hesap_5: interest_teb_marifetli_hesap_5 >= 0
Interest_NonNeg_teb_marifetli_hesap_6: interest_teb_marifetli_hesap_6 >= 0
Interest_NonNeg_teb_marifetli_hesap_7: interest_teb_marifetli_hesap_7 >= 0
Interest_NonNeg_teb_marifetli_hesap_8: interest_teb_marifetli_hesap_8 >= 0
Interest_NonNeg_teb_marifetli_hesap_9: interest_teb_marifetli_hesap_9 >= 0
Interest_Upper1_enpara_0: - deposit_enpara_0 + interest_enpara_0
 + 55000 range_enpara_0 <= 55000
Interest_Upper1_enpara_1: - deposit_enpara_1 + interest_enpara_1
 + 55000 range_enpara_1 <= 55000
Interest_Upper1_enpara_2: - deposit_enpara_2 + interest_enpara_2
 + 55000 range_enpara_2 <= 55000
Interest_Upper1_enpara_3: - deposit_enpara_3 + interest_enpara_3
 + 55000 range_enpara_3 <= 55000
Interest_Upper1_teb_marifetli_hesap_0: - deposit_teb_marifetli_hesap_0
 + interest_teb_marifetli_hesap_0 + 55000 range_teb_marifetli_hesap_0 <= 55000
Interest_Upper1_teb_marifetli_hesap_1: - deposit_teb_marifetli_hesap_1
 + interest_teb_marifetli_hesap_1 + 55000 range_teb_marifetli_hesap_1 <= 50000
Interest_Upper1_teb_marifetli_hesap_10: - deposit_teb_marifetli_hesap_10
 + interest_teb_marifetli_hesap_10 + 55000 range_teb_marifetli_hesap_10
 <= -145000
Interest_Upper1_teb_marifetli_hesap_2: - deposit_teb_marifetli_hesap_2
 + interest_teb_marifetli_hesap_2 + 55000 range_teb_marifetli_hesap_2 <= 47500
Interest_Upper1_teb_marifetli_hesap_3: - deposit_teb_marifetli_hesap_3
 + interest_teb_marifetli_hesap_3 + 55000 range_teb_marifetli_hesap_3 <= 40000
Interest_Upper1_teb_marifetli_hesap_4: - deposit_teb_marifetli_hesap_4
 + interest_teb_marifetli_hesap_4 + 55000 range_teb_marifetli_hesap_4 <= 25000
Interest_Upper1_teb_marifetli_hesap_5: - deposit_teb_marifetli_hesap_5
 + interest_teb_marifetli_hesap_5 + 55000 range_teb_marifetli_hesap_5 <= 5000
Interest_Upper1_teb_marifetli_hesap_6: - deposit_teb_marifetli_hesap_6
 + interest_teb_marifetli_hesap_6 + 55000 range_teb_marifetli_hesap_6 <= 5000
Interest_Upper1_teb_marifetli_hesap_7: - deposit_teb_marifetli_hesap_7
 + interest_teb_marifetli_hesap_7 + 55000 range_teb_marifetli_hesap_7
 <= -20000
Interest_Upper1_teb_marifetli_hesap_8: - deposit_teb_marifetli_hesap_8
 + interest_teb_marifetli_hesap_8 + 55000 range_teb_marifetli_hesap_8
 <= -45000
Interest_Upper1_teb_marifetli_hesap_9: - deposit_teb_marifetli_hesap_9
 + interest_teb_marifetli_hesap_9 + 55000 range_teb_marifetli_hesap_9
 <= -95000
Interest_Upper2_enpara_0: interest_enpara_0 - 55000 range_enpara_0 <= 0
Interest_Upper2_enpara_1: interest_enpara_1 - 55000 range_enpara_1 <= 0
Interest_Upper2_enpara_2: interest_enpara_2 - 55000 range_enpara_2 <= 0
Interest_Upper2_enpara_3: interest_enpara_3 - 55000 range_enpara_3 <= 0
Interest_Upper2_teb_marifetli_hesap_0: interest_teb_marifetli_hesap_0
 - 55000 range_teb_marifetli_hesap_0 <= 0
Interest_Upper2_teb_marifetli_hesap_1: interest_teb_marifetli_hesap_1
 - 55000 range_teb_marifetli_hesap_1 <= 0
Interest_Upper2_teb_marifetli_hesap_10: interest_teb_marifetli_hesap_10
 - 55000 range_teb_marifetli_hesap_10 <= 0
Interest_Upper2_teb_marifetli_hesap_2: interest_teb_marifetli_hesap_2
 - 55000 range_teb_marifetli_hesap_2 <= 0
Interest_Upper2_teb_marifetli_hesap_3: interest_teb_marifetli_hesap_3
 - 55000 range_teb_marifetli_hesap_3 <= 0
Interest_Upper2_teb_marifetli_hesap_4: interest_teb_marifetli_hesap_4
 - 55000 range_teb_marifetli_hesap_4 <= 0
Interest_Upper2_teb_marifetli_hesap_5: interest_teb_marifetli_hesap_5
 - 55000 range_teb_marifetli_hesap_5 <= 0
Interest_Upper2_teb_marifetli_hesap_6: interest_teb_marifetli_hesap_6
 - 55000 range_teb_marifetli_hesap_6 <= 0
Interest_Upper2_teb_marifetli_hesap_7: interest_teb_marifetli_hesap_7
 - 55000 range_teb_marifetli_hesap_7 <= 0
Interest_Upper2_teb_marifetli_hesap_8: interest_teb_marifetli_hesap_8
 - 55000 range_teb_marifetli_hesap_8 <= 0
Interest_Upper2_teb_marifetli_hesap_9: interest_teb_marifetli_hesap_9
 - 55000 range_teb_marifetli_hesap_9 <= 0
Max_Deposit_enpara_0: deposit_enpara_0 - 55000 range_enpara_0 <= 0
Max_Deposit_enpara_1: deposit_enpara_1 - 55000 range_enpara_1 <= 0
Max_Deposit_enpara_2: deposit_enpara_2 - 55000 range_enpara_2 <= 0
Max_Deposit_enpara_3: deposit_enpara_3 - 55000 range_enpara_3 <= 0
Max_Deposit_teb_marifetli_hesap_0: deposit_teb_marifetli_hesap_0
 - 5000 range_teb_marifetli_hesap_0 <= 0
Max_Deposit_teb_marifetli_hesap_1: deposit_teb_marifetli_hesap_1
 - 49999 range_teb_marifetli_hesap_1 <= 0
Max_Deposit_teb_marifetli_hesap_10: deposit_teb_marifetli_hesap_10
 - 55000 range_teb_marifetli_hesap_10 <= 0
Max_Deposit_teb_marifetli_hesap_2: deposit_teb_marifetli_hesap_2
 - 55000 range_teb_marifetli_hesap_2 <= 0
Max_Deposit_teb_marifetli_hesap_3: deposit_teb_marifetli_hesap_3
 - 55000 range_teb_marifetli_hesap_3 <= 0
Max_Deposit_teb_marifetli_hesap_4: deposit_teb_marifetli_hesap_4
 - 55000 range_teb_marifetli_hesap_4 <= 0
Max_Deposit_teb_marifetli_hesap_5: deposit_teb_marifetli_hesap_5
 - 55000 range_teb_marifetli_hesap_5 <= 0
Max_Deposit_teb_marifetli_hesap_6: deposit_teb_marifetli_hesap_6
 - 55000 range_teb_marifetli_hesap_6 <= 0
Max_Deposit_teb_marifetli_hesap_7: deposit_teb_marifetli_hesap_7
 - 55000 range_teb_marifetli_hesap_7 <= 0
Max_Deposit_teb_marifetli_hesap_8: deposit_teb_marifetli_hesap_8
 - 55000 range_teb_marifetli_hesap_8 <= 0
Max_Deposit_teb_marifetli_hesap_9: deposit_teb_marifetli_hesap_9
 - 55000 range_teb_marifetli_hesap_9 <= 0
Min_Balance_enpara_0: deposit_enpara_0 >= 0
Min_Balance_enpara_1: deposit_enpara_1 >= 0
Min_Balance_enpara_2: deposit_enpara_2 >= 0
Min_Balance_enpara_3: deposit_enpara_3 >= 0
Min_Balance_teb_marifetli_hesap_0: deposit_teb_marifetli_hesap_0 >= 0
Min_Balance_teb_marifetli_hesap_1: deposit_teb_marifetli_hesap_1
 - 5000 range_teb_marifetli_hesap_1 >= 0
Min_Balance_teb_marifetli_hesap_10: deposit_teb_marifetli_hesap_10
 - 200000 range_teb_marifetli_hesap_10 >= 0
Min_Balance_teb_marifetli_hesap_2: deposit_teb_marifetli_hesap_2
 - 7500 range_teb_marifetli_hesap_2 >= 0
Min_Balance_teb_marifetli_hesap_3: deposit_teb_marifetli_hesap_3
 - 15000 range_teb_marifetli_hesap_3 >= 0
Min_Balance_teb_marifetli_hesap_4: deposit_teb_marifetli_hesap_4
 - 30000 range_teb_marifetli_hesap_4 >= 0
Min_Balance_teb_marifetli_hesap_5: deposit_teb_marifetli_hesap_5
 - 50000 range_teb_marifetli_hesap_5 >= 0
Min_Balance_teb_marifetli_hesap_6: deposit_teb_marifetli_hesap_6
 - 50000 range_teb_marifetli_hesap_6 >= 0
Min_Balance_teb_marifetli_hesap_7: deposit_teb_marifetli_hesap_7
 - 75000 range_teb_marifetli_hesap_7 >= 0
Min_Balance_teb_marifetli_hesap_8: deposit_teb_marifetli_hesap_8
 - 100000 range_teb_marifetli_hesap_8 >= 0
Min_Balance_teb_marifetli_hesap_9: deposit_teb_marifetli_hesap_9
 - 150000 range_teb_marifetli_hesap_9 >= 0
Min_Deposit_enpara_0: deposit_enpara_0 >= 0
Min_Deposit_enpara_1: deposit_enpara_1 - 100001 range_enpara_1 >= 0
Min_Deposit_enpara_2: deposit_enpara_2 - 500001 range_enpara_2 >= 0
Min_Deposit_enpara_3: deposit_enpara_3 - 1000001 range_enpara_3 >= 0
Min_Deposit_teb_marifetli_hesap_0: deposit_teb_marifetli_hesap_0 >= 0
Min_Deposit_teb_marifetli_hesap_1: deposit_teb_marifetli_hesap_1
 - 5000 range_teb_marifetli_hesap_1 >= 0
Min_Deposit_teb_marifetli_hesap_10: deposit_teb_marifetli_hesap_10
 - 3000001 range_teb_marifetli_hesap_10 >= 0
Min_Deposit_teb_marifetli_hesap_2: deposit_teb_marifetli_hesap_2
 - 50000 range_teb_marifetli_hesap_2 >= 0
Min_Deposit_teb_marifetli_hesap_3: deposit_teb_marifetli_hesap_3
 - 100000 range_teb_marifetli_hesap_3 >= 0
Min_Deposit_teb_marifetli_hesap_4: deposit_teb_marifetli_hesap_4
 - 250000 range_teb_marifetli_hesap_4 >= 0
Min_Deposit_teb_marifetli_hesap_5: deposit_teb_marifetli_hesap_5
 - 500000 range_teb_marifetli_hesap_5 >= 0
Min_Deposit_teb_marifetli_hesap_6: deposit_teb_marifetli_hesap_6
 - 750000 range_teb_marifetli_hesap_6 >= 0
Min_Deposit_teb_marifetli_hesap_7: deposit_teb_marifetli_hesap_7
 - 1000000 range_teb_marifetli_hesap_7 >= 0
Min_Deposit_teb_marifetli_hesap_8: deposit_teb_marifetli_hesap_8
 - 1500001 range_teb_marifetli_hesap_8 >= 0
Min_Deposit_teb_marifetli_hesap_9: deposit_teb_marifetli_hesap_9
 - 2000001 range_teb_marifetli_hesap_9 >= 0
Total_Deposit: deposit_enpara_0 + deposit_enpara_1 + deposit_enpara_2
 + deposit_enpara_3 + deposit_teb_marifetli_hesap_0
 + deposit_teb_marifetli_hesap_1 + deposit_teb_marifetli_hesap_10
 + deposit_teb_marifetli_hesap_2 + deposit_teb_marifetli_hesap_3
 + deposit_teb_marifetli_hesap_4 + deposit_teb_marifetli_hesap_5
 + deposit_teb_marifetli_hesap_6 + deposit_teb_marifetli_hesap_7
 + deposit_teb_marifetli_hesap_8 + deposit_teb_marifetli_hesap_9 = 55000
Bounds
 deposit_enpara_0 <= 55000
 deposit_enpara_1 <= 55000
 deposit_enpara_2 <= 55000
 deposit_enpara_3 <= 55000
 deposit_teb_marifetli_hesap_0 <= 5000
 deposit_teb_marifetli_hesap_1 <= 49999
 deposit_teb_marifetli_hesap_10 <= 55000
 deposit_teb_marifetli_hesap_2 <= 55000
 deposit_teb_marifetli_hesap_3 <= 55000
 deposit_teb_marifetli_hesap_4 <= 55000
 deposit_teb_marifetli_hesap_5 <= 55000
 deposit_teb_marifetli_hesap_6 <= 55000
 deposit_teb_marifetli_hesap_7 <= 55000
 deposit_teb_marifetli_hesap_8 <= 55000
 deposit_teb_marifetli_hesap_9 <= 55000
Binaries
range_enpara_0
range_enpara_1
range_enpara_2
range_enpara_3
range_teb_marifetli_hesap_0
range_teb_marifetli_hesap_1
range_teb_marifetli_hesap_10
range_teb_marifetli_hesap_2
range_teb_marifetli_hesap_3
range_teb_marifetli_hesap_4
range_teb_marifetli_hesap_5
range_teb_marifetli_hesap_6
range_teb_marifetli_hesap_7
range_teb_marifetli_hesap_8
range_teb_marifetli_hesap_9
End
