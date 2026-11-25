"""Streamlit 화면: main.py의 파이프라인 결과를 브라우저에 표시한다.

Streamlit Cloud 설정의 Main file path를 'disaster_shelter/streamlit_app.py'
(또는 저장소 구조에 맞는 경로)로 지정해야 화면이 뜬다.
"""
import os

import streamlit as st

import main as pipeline

st.set_page_config(page_title="지역별 재난대피소 분석", layout="wide")
st.title("지역별 재난대피소 수요·공급 불균형 분석")
st.caption("공급(대피시설 수용인원) ÷ 수요(인구)로 수용률을 구하고, 고령 비율을 반영해 취약도를 계산합니다.")


@st.cache_data
def load_result():
    return pipeline.run_pipeline()


try:
    ranked = load_result()
except FileNotFoundError as e:
    st.error("데이터 파일을 찾지 못했습니다. 저장소에 data/ 폴더(또는 같은 폴더)에 CSV 두 개를 올려 주세요.")
    st.code(str(e))
    st.stop()

st.subheader("지역별 결과 · 취약지역 순위")
st.dataframe(ranked, hide_index=True)

st.subheader("그래프")
chart_path = os.path.join(pipeline.OUT_DIR, "지역별_그래프.png")
if os.path.isfile(chart_path):
    st.image(chart_path)
else:
    st.info("그래프 파일이 없습니다. requirements.txt에 matplotlib이 있는지 확인하세요.")
