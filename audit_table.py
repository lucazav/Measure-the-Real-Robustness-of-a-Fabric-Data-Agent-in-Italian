# %%
import pandas as pd
import numpy as np
from pathlib import Path

# =============================================================================
# INPUT FILES
# =============================================================================
# Export prodotto da get_evaluation_details(..., get_all_rows=False)
export_path = "C:\\Users\\LucaZavarella\\OneDrive\\MVP\\Blogs\\Data Agent Evalutaion\\benchmark_export_20260315_165201.xlsx"

# Benchmark completo con expected_answer popolata
benchmark_path = "C:\\Users\\LucaZavarella\\OneDrive\\MVP\\Blogs\\Data Agent Evalutaion\\final_benchmark_with_expected_answers.xlsx"

# Output finale
output_xlsx = "C:\\Users\\LucaZavarella\\OneDrive\\MVP\\Blogs\\Data Agent Evalutaion\\audit_table_with_queries_expected_actual.xlsx"
output_csv = "C:\\Users\\LucaZavarella\\OneDrive\\MVP\\Blogs\\Data Agent Evalutaion\\audit_table_with_queries_expected_actual.csv"

# %%
# =============================================================================
# LOAD DATA
# =============================================================================
exp = pd.read_excel(export_path)
bench = pd.read_excel(benchmark_path)

# =============================================================================
# MERGE EXPORT + BENCHMARK
# =============================================================================
# Join sulla question, così recuperiamo intent_id, question_id ed expected_answer
audit = exp.merge(
    bench[["intent_id", "question_id", "question", "expected_answer"]],
    on="question",
    how="left",
    suffixes=("", "_bench")
)

# %%
# =============================================================================
# FILL MISSING EXPECTED ANSWERS FROM SAME INTENT
# =============================================================================
# Se per qualche riga il merge non recupera expected_answer,
# proviamo a usare la expected_answer non nulla dello stesso intent_id
canon_map = (
    bench.groupby("intent_id")["expected_answer"]
    .apply(lambda s: next((x for x in s if pd.notna(x)), np.nan))
    .to_dict()
)

audit["expected_answer_final"] = audit["expected_answer"]

mask = audit["expected_answer_final"].isna()
audit.loc[mask, "expected_answer_final"] = audit.loc[mask, "intent_id"].map(canon_map)

# %%
# =============================================================================
# BUILD FINAL AUDIT TABLE
# =============================================================================
# Qui assumo che nell'export di evaluation la colonna con il giudizio SDK
# si chiami "evaluation_message" e la risposta dell'agente "actual_answer".
# Se nel tuo file hanno nomi diversi, aggiornali qui sotto.

audit["sdk_verdict"] = audit["evaluation_message"]

final = audit[
    [
        "question_id",
        "question",
        "expected_answer_final",
        "actual_answer",
        "sdk_verdict",
    ]
].copy()

final = final.rename(
    columns={
        "question": "query",
        "expected_answer_final": "expected_answer",
    }
)

final = final.sort_values("question_id").reset_index(drop=True)

# %%
# =============================================================================
# SAVE OUTPUTS
# =============================================================================
final.to_excel(output_xlsx, index=False)
final.to_csv(output_csv, index=False)

print(f"Saved Excel: {output_xlsx}")
print(f"Saved CSV:   {output_csv}")

# %%
