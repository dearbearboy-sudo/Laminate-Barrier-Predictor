import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Barrier Prediction Web App", layout="wide")

st.title("🎬 Barrier Prediction Web App for Laminated Films")
st.markdown("ทำนายค่า OTR และ WVTR ของฟิล์มลามิเนตหลายชั้น (Multi-layer Laminated Films)")

# 1. ฐานข้อมูลตัวอย่างวัสดุ (Database Sample)
DATABASE = [
    {
        "material_category": "Metalized film",
        "film_name": "mPE(XE)-MDO",
        "ref_thickness_microns": 25.0,
        "ref_otr": 0.25,
        "ref_wvtr": 0.45,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
        },
    {
        "material_category": "Metalized film",
        "film_name": "mMDOPE",
        "ref_thickness_microns": 28.0,
        "ref_otr": 0.1,
        "ref_wvtr": 1.46,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
    },
    {
        "material_category": "Non-metalized film (AlOx)",
        "film_name": "MDOPE-AlOx",
        "ref_thickness_microns": 28.0,
        "ref_otr": 0.29,
        "ref_wvtr": 1.5,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
        },
    {
        "material_category": "Non-metalized film (EVOH)",
        "film_name": "LL-EVOH",
        "ref_thickness_microns": 70.0,
        "ref_otr": 0.48,
        "ref_wvtr": 1.81,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
         },
    {
        "material_category": "Non-metalized film (EVOH)",
        "film_name": "EF-F",
        "ref_thickness_microns": 12.0,
        "ref_otr": 0.60,
        "ref_wvtr": 86,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
        },
    {
        "material_category": "Base Film",
        "film_name": "LL50",
        "ref_thickness_microns": 50,
        "ref_otr": 4000,
        "ref_wvtr": 7.5,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
        },
    {
        "material_category": "Base Film",
        "film_name": "LL100",
        "ref_thickness_microns": 100,
        "ref_otr": 2000,
        "ref_wvtr": 4.0,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
    },
    {
        "material_category": "Base Film",
        "film_name": "MDOPE_adj",
        "ref_thickness_microns": 25.0,
        "ref_otr": 1852,
        "ref_wvtr": 4.56,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
        },
    {
        "material_category": "Base Film",
        "film_name": "MDOPE",
        "ref_thickness_microns": 25.0,
        "ref_otr": 4000.0,
        "ref_wvtr": 12,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
        },
    {
        "material_category": "Base Film",
        "film_name": "Alu",
        "ref_thickness_microns": 11,
        "ref_otr": 0.01,
        "ref_wvtr": 0.01,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "ASTM D3985",
        "standard_wvtr": "ASTM F1249"
    },
    {
        "material_category": "Custom",
        "film_name": "กำหนดเอง (Custom Material)",
        "ref_thickness_microns": 25.0,
        "ref_otr": 0.0,
        "ref_wvtr": 0.0,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day",
        "standard_otr": "Custom",
        "standard_wvtr": "Custom"
    }
]

# แปลงฐานข้อมูลเป็น DataFrame เพื่อให้ดึงข้อมูลง่าย
df_db = pd.DataFrame(DATABASE)

# ส่วนที่ 1: แสดงฐานข้อมูลอ้างอิง (Database Lookup)
with st.expander("🔍 ตรวจสอบฐานข้อมูลฟิล์ม (Database Lookup)"):
    st.dataframe(df_db)

st.write("---")

# ส่วนที่ 2: กำหนดโครงสร้างลามิเนต
st.header("🛠️ ออกแบบโครงสร้างชั้นฟิล์ม (Laminate Structure Design)")

# Step 1: ให้ผู้ใช้กำหนดจำนวนชั้น
num_layers = st.number_input("ขั้นตอนที่ 1: ระบุจำนวนชั้นฟิล์ม (Number of Layers)", min_value=1, max_value=10, value=3, step=1)

layers_data = []

# สร้างอินพุตสำหรับแต่ละชั้น
for i in range(int(num_layers)):
    st.subheader(f"ชั้นที่ {i+1} (Layer {i+1})")
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
    
    with col1:
        # Step 2: เลือกวัสดุจากตัวเลือก
        material_options = df_db["film_name"].tolist()
        selected_material = st.selectbox(f"เลือกวัสดุชั้นที่ {i+1}", material_options, key=f"mat_{i}")
        
        # ดึงข้อมูลจากฐานข้อมูลมาเป็นค่าเริ่มต้น
        mat_info = df_db[df_db["film_name"] == selected_material].iloc[0]
        
    with col2:
        # Step 3: ระบุความหนาจริงที่ต้องการใช้
        actual_thickness = st.number_input(f"ความหนาจริง (microns)", min_value=0.1, value=float(mat_info["ref_thickness_microns"]), key=f"thick_{i}")

    with col3:
        # สวิตช์เปิดปิดเปิดเพื่อป้อนค่าเองแมนนวล
        manual_toggle = st.toggle("กรอกค่าเอง (Overwrite)", value=(selected_material == "กำหนดเอง (Custom Material)"), key=f"toggle_{i}")

    with col4:
        # กำหนดค่า OTR/WVTR อ้างอิง
        if manual_toggle:
            ref_otr = st.number_input(f"ใส่ค่า OTR เอง ({mat_info['unit_otr']})", min_value=0.0, value=float(mat_info["ref_otr"]), key=f"otr_{i}")
            ref_wvtr = st.number_input(f"ใส่ค่า WVTR เอง ({mat_info['unit_wvtr']})", min_value=0.0, value=float(mat_info["ref_wvtr"]), key=f"wvtr_{i}")
            ref_thick = st.number_input(f"ความหนาอ้างอิงสำหรับค่าที่กรอก", min_value=1.0, value=25.0, key=f"ref_thick_{i}")
        else:
            ref_otr = mat_info["ref_otr"]
            ref_wvtr = mat_info["ref_wvtr"]
            ref_thick = mat_info["ref_thickness_microns"]
            st.write(f"📉 OTR อ้างอิง: {ref_otr} / WVTR อ้างอิง: {ref_wvtr} (ที่หนา {ref_thick} µm)")

    # ป้องกันค่าติดลบหรือเป็น 0 ที่จะทำให้บั๊ก
    ref_otr = max(ref_otr, 0.00001)
    ref_wvtr = max(ref_wvtr, 0.00001)

    # Step 4: คำนวณความต้านทานและค่าที่ปรับตามความหนาจริง (TR_actual = TR_ref * (Thickness_ref / Thickness_actual))
    actual_otr_layer = ref_otr * (ref_thick / actual_thickness)
    actual_wvtr_layer = ref_wvtr * (ref_thick / actual_thickness)

    layers_data.append({
        "layer_order": i + 1,
        "material": selected_material,
        "thickness": actual_thickness,
        "otr_layer": actual_otr_layer,
        "wvtr_layer": actual_wvtr_layer
    })

st.write("---")

# ส่วนที่ 3: คำนวณสรุปและแสดงผลแดชบอร์ด
st.header("📊 แดชบอร์ดสรุปผลการคำนวณ (Output Dashboard)")

total_thickness = sum(layer["thickness"] for layer in layers_data)

# Step 5: คำนวณรวมฟิล์มทุกลามิเนตด้วยสูตรอนุกรม (1 / TR_total = sum(1 / TR_layer))
inv_otr_total = sum(1 / layer["otr_layer"] for layer in layers_data)
inv_wvtr_total = sum(1 / layer["wvtr_layer"] for layer in layers_data)

predicted_otr = 1 / inv_otr_total
predicted_wvtr = 1 / inv_wvtr_total

# แสดงผลแบบ Metrics สวยงาม
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="📏 ความหนารวมลามิเนต (Total Thickness)", value=f"{total_thickness:.2f} microns")
with col_m2:
    st.metric(label="🌬️ ค่าทำนาย OTR (ASTM D3985)", value=f"{predicted_otr:.4f} cc/m².day")
with col_m3:
    st.metric(label="💧 ค่าทำนาย WVTR (ASTM F1249)", value=f"{predicted_wvtr:.4f} g/m².day")

# ตารางสรุปรายละเอียดแต่ละชั้นย่อย
st.subheader("📋 ตารางแจกแจงคุณสมบัติรายชั้น (Layer Analysis Table)")
summary_df = pd.DataFrame(layers_data)
summary_df.columns = ["ลำดับชั้น (Layer)", "วัสดุที่เลือก (Material)", "ความหนาจริง (microns)", "OTR ชั้นนี้ (cc/m².day)", "WVTR ชั้นนี้ (g/m².day)"]
st.dataframe(summary_df.style.format({
    "ความหนาจริง (microns)": "{:.2f}",
    "OTR ชั้นนี้ (cc/m².day)": "{:.4f}",
    "WVTR ชั้นนี้ (g/m².day)": "{:.4f}"
}))

st.info("💡 หมายเหตุ: การคำนวณอ้างอิงหลักการผกผันตามความหนาและแบบจำลองแรงต้านอนุกรม (Series Resistance Model)")

# อ่านไฟล์ HTML จากภายนอกเพื่อตัดปัญหา Syntax Error
with open("ui_design.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=600) # ปรับความสูงของหน้าจอตามต้องการ
