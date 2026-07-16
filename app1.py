import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Loan Calculator",
    page_icon="🏦",
    layout="wide"
) 
st.markdown("""
<style>

/* ====== Background ====== */

.stApp{
    background: linear-gradient(135deg,#edf4ff,#d8e9ff);
}

/* ====== Tiêu đề ====== */

.main-title{
    text-align:center;
    font-size:48px;
    font-weight:800;
    color:#0B3558;
    margin-bottom:0px;
}

.sub-title{
    text-align:center;
    color:#666;
    font-size:18px;
    margin-bottom:30px;
}

/* ====== Card ====== */

.card{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 10px 25px rgba(0,0,0,.08);
    margin-bottom:25px;
}

/* ====== Tiêu đề từng mục ====== */

.section-title{
    font-size:30px;
    font-weight:bold;
    color:#0B3558;
    margin-bottom:15px;
}

/* ====== Metric ====== */

div[data-testid="metric-container"]{
    background:white;
    border-radius:18px;
    padding:18px;
    box-shadow:0px 8px 18px rgba(0,0,0,.08);
    border-left:8px solid #0D6EFD;
}

/* ====== Nút ====== */

.stButton>button{
    width:100%;
    height:55px;
    background:#0D6EFD;
    color:white;
    border:none;
    border-radius:15px;
    font-size:20px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#0A58CA;
}

/* ====== Selectbox ====== */

div[data-baseweb="select"]{
    border-radius:12px;
}

/* ====== Input ====== */

input{
    border-radius:12px !important;
}

/* ====== DataFrame ====== */

[data-testid="stDataFrame"]{
    border-radius:15px;
}

</style>
""",unsafe_allow_html=True)
st.markdown("""
<div class="main-title">
🏦 ỨNG DỤNG TÍNH KHOẢN VAY NGÂN HÀNG
</div>

<div class="sub-title">
Tính toán khoản vay • So sánh phương thức trả nợ • Tư vấn tối ưu
</div>
""",unsafe_allow_html=True)
st.markdown("""
<div class="card">
<div class="section-title">
📝 Thông Tin Khoản Vay
</div>
</div>
""",unsafe_allow_html=True)
col1,col2,col3=st.columns(3)

with col1:

    so_tien=st.number_input(
        "💰 Số tiền vay (triệu đồng)",
        min_value=1.0,
        value=500.0
    )

with col2:

    thoi_han=st.slider(
        "📅 Thời hạn vay (năm)",
        1,
        30,
        10
    )

with col3:

    muc_dich=st.selectbox(
        "🎯 Mục đích vay",
        list(lai_suat.keys())
    )

st.info(f"📈 Lãi suất áp dụng: **{lai_nam}%/năm**")
st.button("🚀 TÍNH TOÁN")
st.markdown("""
<div class="section-title">
📊 KẾT QUẢ TÍNH TOÁN
</div>
""",unsafe_allow_html=True)
c1,c2,c3=st.columns(3)

with c1:

    st.metric(
        "💰 Tổng tiền lãi",
        f"{tong_lai1:,.2f} triệu"
    )

with c2:

    st.metric(
        "💳 Tổng phải trả",
        f"{so_tien+tong_lai1:,.2f} triệu"
    )

with c3:

    st.metric(
        "📅 Trả tháng đầu",
        f"{df1.iloc[0]['Thanh toán']:,.2f} triệu"
    )
  st.markdown("""
<div class="section-title">
⚖️ SO SÁNH HAI PHƯƠNG THỨC
</div>
""",unsafe_allow_html=True)
if tong_lai1 < tong_lai2:

    st.success("""
## ✅ Khuyến nghị

**Nên chọn phương thức Dư nợ giảm dần**

✔ Tổng tiền lãi thấp hơn

✔ Tiết kiệm chi phí vay

✔ Phù hợp khách hàng có khả năng trả cao thời gian đầu
""")

else:

    st.info("""
## 📌 Khuyến nghị

**Nên chọn phương thức Trả góp đều**

✔ Khoản trả cố định

✔ Dễ cân đối thu nhập

✔ Phù hợp người có thu nhập ổn định
""")
  st.markdown("""
<div class="section-title">
📈 BIỂU ĐỒ DƯ NỢ CÒN LẠI
</div>
""",unsafe_allow_html=True)
