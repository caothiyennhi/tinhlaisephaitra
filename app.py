import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(page_title="Ứng dụng tính khoản vay", layout="wide")

st.title("🏦 ỨNG DỤNG TÍNH TIỀN VAY NGÂN HÀNG")

st.write("### Nhập thông tin khoản vay")

# ==========================
# Lãi suất theo mục đích vay
# ==========================

lai_suat = {
    "Mua nhà": 7.5,
    "Mua ô tô": 8.5,
    "Kinh doanh": 10,
    "Tiêu dùng": 12,
    "Du học": 9
}

col1, col2 = st.columns(2)

with col1:
    so_tien = st.number_input(
        "Số tiền vay (triệu đồng)",
        min_value=1.0,
        value=500.0,
        step=10.0
    )

    muc_dich = st.selectbox(
        "Mục đích vay",
        list(lai_suat.keys())
    )

with col2:
    thoi_han = st.slider(
        "Thời hạn vay (năm)",
        1,
        30,
        10
    )

    lai_nam = lai_suat[muc_dich]

st.success(f"Lãi suất áp dụng: **{lai_nam}%/năm**")

#==========================
# Tính toán
#==========================

thang = thoi_han * 12
lai_thang = lai_nam / 100 / 12

#==========================
# PHƯƠNG THỨC 1
# Dư nợ giảm dần
#==========================

goc_thang = so_tien / thang

du_no = so_tien

bang1 = []

tong_lai1 = 0

for i in range(1, thang + 1):

    lai = du_no * lai_thang

    tong = goc_thang + lai

    du_no -= goc_thang

    tong_lai1 += lai

    bang1.append([
        i,
        round(goc_thang,2),
        round(lai,2),
        round(tong,2),
        max(round(du_no,2),0)
    ])

df1 = pd.DataFrame(
    bang1,
    columns=[
        "Tháng",
        "Gốc",
        "Lãi",
        "Thanh toán",
        "Dư nợ còn lại"
    ]
)

#==========================
# PHƯƠNG THỨC 2
# Trả góp đều (Annuity)
#==========================

A = so_tien * lai_thang * (1+lai_thang)**thang / ((1+lai_thang)**thang -1)

du_no = so_tien

bang2=[]

tong_lai2=0

for i in range(1,thang+1):

    lai=du_no*lai_thang

    goc=A-lai

    du_no-=goc

    tong_lai2+=lai

    bang2.append([
        i,
        round(goc,2),
        round(lai,2),
        round(A,2),
        max(round(du_no,2),0)
    ])

df2=pd.DataFrame(
    bang2,
    columns=[
        "Tháng",
        "Gốc",
        "Lãi",
        "Thanh toán",
        "Dư nợ còn lại"
    ]
)

#==========================
# KẾT QUẢ
#==========================

st.header("KẾT QUẢ")

c1,c2=st.columns(2)

with c1:

    st.subheader("Phương thức 1")
    st.write("### Trả gốc đều - lãi giảm dần")

    st.metric(
        "Tổng tiền lãi",
        f"{tong_lai1:,.2f} triệu"
    )

    st.metric(
        "Tổng thanh toán",
        f"{so_tien+tong_lai1:,.2f} triệu"
    )

    st.dataframe(df1,height=350)

with c2:

    st.subheader("Phương thức 2")
    st.write("### Trả đều hàng tháng")

    st.metric(
        "Tổng tiền lãi",
        f"{tong_lai2:,.2f} triệu"
    )

    st.metric(
        "Tổng thanh toán",
        f"{so_tien+tong_lai2:,.2f} triệu"
    )

    st.dataframe(df2,height=350)

#==========================
# SO SÁNH
#==========================

st.header("SO SÁNH HAI PHƯƠNG THỨC")

ss = pd.DataFrame({
    "Tiêu chí":[
        "Tổng lãi",
        "Tổng thanh toán"
    ],
    "Dư nợ giảm dần":[
        round(tong_lai1,2),
        round(so_tien+tong_lai1,2)
    ],
    "Trả đều":[
        round(tong_lai2,2),
        round(so_tien+tong_lai2,2)
    ]
})

st.table(ss)

if tong_lai1 < tong_lai2:

    st.success("""
### 💡 TƯ VẤN

**Nên chọn phương thức trả gốc đều (dư nợ giảm dần)**

✔ Tổng lãi thấp hơn.

✔ Tiết kiệm chi phí.

✔ Phù hợp người có thu nhập cao ở giai đoạn đầu.
""")

else:

    st.info("""
### 💡 TƯ VẤN

**Nên chọn phương thức trả đều hàng tháng (Annuity)**

✔ Khoản thanh toán cố định.

✔ Dễ cân đối tài chính.

✔ Phù hợp người có thu nhập ổn định.
""")


#==========================
#==========================
#==========================
# BIỂU ĐỒ CỘT THEO NĂM
#==========================

st.header("📊 Biểu đồ số tiền còn lại phải trả theo năm")

# Lấy dữ liệu cuối mỗi năm
df_nam = df1[df1["Tháng"] % 12 == 0].copy()

# Tạo cột năm
df_nam["Năm"] = range(1, len(df_nam) + 1)

# Hiển thị biểu đồ
st.bar_chart(
    df_nam.set_index("Năm")["Dư nợ còn lại"]
)
st.pyplot(fig)
