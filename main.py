"""⑤ 실행 (F6): ①공급 → ②수요 → ③병합·지표 → ④시각화 순서로 전체 파이프라인을 실행한다.

사용법 (코랩/로컬 공통):
    python main.py
결과: output/ 폴더에 지역별 결과표(CSV)와 그래프(PNG)가 저장된다.
"""
import os

import supply
import demand
import analysis

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "output")
SHELTER_CSV = os.path.join(DATA_DIR, "shelters.csv")
POPULATION_CSV = os.path.join(DATA_DIR, "population_dong.csv")


def run_pipeline(shelter_csv=SHELTER_CSV, population_csv=POPULATION_CSV, out_dir=OUT_DIR):
    os.makedirs(out_dir, exist_ok=True)

    # ① 공급 집계 (F1)
    shelters_raw = supply.load_shelters(shelter_csv)
    shelters, clean_log = supply.clean_shelters(shelters_raw)
    print("① 공급 집계 처리 로그:", clean_log)
    supply_df = supply.summarize_supply(shelters)

    # ② 수요 집계 (F2)
    pop_raw = demand.load_population(population_csv)
    demand_df = demand.summarize_demand(pop_raw)

    # ③ 병합 · 수용률 · 취약도 (F3, F4)
    merged = analysis.merge_data(supply_df, demand_df)
    merged = analysis.calc_ratio(merged)
    merged = analysis.calc_vulnerability(merged)
    ranked = analysis.rank_regions(merged)

    # ④ 시각화 (F5)
    ranked.to_csv(os.path.join(out_dir, "지역별_결과표.csv"), index=False, encoding="utf-8-sig")
    analysis.plot_results(ranked, save_path=os.path.join(out_dir, "지역별_그래프.png"))

    print("\n[지역별 결과 · 취약지역 순위]")
    print(ranked.to_string(index=False))
    return ranked


if __name__ == "__main__":
    run_pipeline()
