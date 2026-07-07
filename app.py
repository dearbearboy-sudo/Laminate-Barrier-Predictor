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

import streamlit as st
import streamlit.components.v1 as components
# เอาโค้ด HTML/CSS ที่ออกแบบจาก Google มาแปะในเครื่องหมายคำพูดด้านล่างนี้
html_code = """<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Material Database | BarrierPredict</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "primary": "#00478d",
                    "on-primary-fixed": "#001b3d",
                    "surface-bright": "#fcf9f8",
                    "on-secondary-fixed-variant": "#004f4f",
                    "secondary-fixed-dim": "#6fd7d6",
                    "on-primary-fixed-variant": "#00468c",
                    "surface-container-lowest": "#ffffff",
                    "surface": "#fcf9f8",
                    "background": "#fcf9f8",
                    "on-secondary-fixed": "#002020",
                    "on-error-container": "#93000a",
                    "on-tertiary-fixed-variant": "#3d484f",
                    "on-surface": "#1c1b1b",
                    "surface-tint": "#005db6",
                    "tertiary-fixed-dim": "#bcc8d0",
                    "primary-container": "#005eb8",
                    "error-container": "#ffdad6",
                    "tertiary-container": "#566168",
                    "tertiary-fixed": "#d8e4ec",
                    "tertiary": "#3e4950",
                    "inverse-surface": "#313030",
                    "surface-container": "#f0edec",
                    "surface-variant": "#e5e2e1",
                    "on-primary": "#ffffff",
                    "outline-variant": "#c2c6d4",
                    "inverse-primary": "#a9c7ff",
                    "on-error": "#ffffff",
                    "error": "#ba1a1a",
                    "on-secondary": "#ffffff",
                    "surface-container-highest": "#e5e2e1",
                    "primary-fixed-dim": "#a9c7ff",
                    "outline": "#727783",
                    "inverse-on-surface": "#f3f0ef",
                    "on-tertiary": "#ffffff",
                    "on-secondary-container": "#007070",
                    "secondary": "#006a6a",
                    "on-primary-container": "#c8daff",
                    "surface-dim": "#dcd9d9",
                    "on-tertiary-container": "#d0dce4",
                    "on-background": "#1c1b1b",
                    "surface-container-high": "#ebe7e7",
                    "surface-container-low": "#f6f3f2",
                    "secondary-container": "#8cf3f3",
                    "on-tertiary-fixed": "#121d23",
                    "on-surface-variant": "#424752",
                    "secondary-fixed": "#8cf3f3",
                    "primary-fixed": "#d6e3ff"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "spacing": {
                    "margin-mobile": "16px",
                    "sm": "8px",
                    "base": "4px",
                    "xs": "4px",
                    "md": "16px",
                    "gutter": "12px",
                    "lg": "24px",
                    "xl": "32px",
                    "margin-desktop": "32px"
            },
            "fontFamily": {
                    "headline-lg-mobile": ["Inter"],
                    "data-mono": ["JetBrains Mono"],
                    "body-lg": ["Inter"],
                    "headline-md": ["Inter"],
                    "headline-lg": ["Inter"],
                    "body-md": ["Inter"],
                    "display-lg": ["Inter"],
                    "label-sm": ["Inter"]
            },
            "fontSize": {
                    "headline-lg-mobile": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                    "data-mono": ["14px", {"lineHeight": "20px", "letterSpacing": "0em", "fontWeight": "500"}],
                    "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                    "headline-md": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                    "headline-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
                    "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                    "display-lg": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                    "label-sm": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600"}]
            }
          },
        },
      }
    </script>
<style>
        body { font-family: 'Inter', sans-serif; }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .custom-scrollbar::-webkit-scrollbar { width: 4px; height: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #c2c6d4; border-radius: 2px; }
        .scientific-border { border: 1px solid #e5e2e1; }
        .data-table-row:nth-child(even) { background-color: #f6f3f2; }
    </style>
</head>
<body class="bg-surface text-on-surface flex flex-col min-h-screen">
<!-- TopNavBar -->
<header class="bg-surface flex justify-between items-center w-full px-margin-desktop h-16 sticky top-0 z-50 border-b border-outline-variant">
<div class="flex items-center gap-lg">
<span class="font-headline-md text-headline-md font-bold text-primary">BarrierPredict</span>
<div class="hidden md:flex gap-md h-full items-center ml-lg">
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:opacity-80">Calculator</a>
<a class="font-body-md text-body-md text-primary border-b-2 border-primary pb-1 transition-colors cursor-pointer active:opacity-80">Database</a>
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:opacity-80">History</a>
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:opacity-80">Settings</a>
</div>
</div>
<div class="flex items-center gap-md">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors p-sm">notifications</button>
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors p-sm">settings</button>
<div class="w-8 h-8 rounded-full bg-primary-fixed flex items-center justify-center text-primary font-bold overflow-hidden">
<img class="w-full h-full object-cover" data-alt="A professional headshot of a laboratory researcher in a clean white environment, high-key lighting, minimalist industrial aesthetic with cool blue tones." src="https://lh3.googleusercontent.com/aida-public/AB6AXuDe-e3Lctfyw1KJCfqF4TFkrjjHcPqfeLlWNHj0CRDCz4S9j5FfvT6zRB41et9TZgndCDKkC29Ik46NLgb44S6zWCBAffgBJBP5MRAlh96Qu8KxHc3QcwKp-Fh4rIGQynDUCjT239yo4Cjc35SeP1u4w4YVM18SlhjfkVKlUay7jgccOTo1XiTGPsQNemYxEb70RJwQrwFGYAIBY4rRaeFBfqW5wFrCv8HASTcKTt00GRvqMobTPBCK3g"/>
</div>
</div>
</header>
<div class="flex flex-1">
<!-- SideNavBar -->
<aside class="fixed left-0 top-16 h-[calc(100vh-64px)] w-64 p-md flex flex-col gap-base bg-surface-container-low border-r border-outline-variant hidden md:flex">
<div class="mb-lg p-sm">
<h3 class="font-headline-lg text-headline-lg text-primary leading-tight">Project Alpha</h3>
<p class="font-body-md text-body-md text-on-surface-variant opacity-70">Laminate Design V2</p>
</div>
<nav class="flex flex-col gap-base">
<div class="flex items-center gap-sm p-md text-on-surface-variant hover:bg-surface-variant transition-all rounded-lg cursor-pointer">
<span class="material-symbols-outlined">calculate</span>
<span class="font-body-md text-body-md">Calculator</span>
</div>
<div class="flex items-center gap-sm p-md bg-secondary-container text-on-secondary-container font-bold rounded-lg cursor-pointer">
<span class="material-symbols-outlined">database</span>
<span class="font-body-md text-body-md">Database</span>
</div>
<div class="flex items-center gap-sm p-md text-on-surface-variant hover:bg-surface-variant transition-all rounded-lg cursor-pointer">
<span class="material-symbols-outlined">history</span>
<span class="font-body-md text-body-md">History</span>
</div>
<div class="flex items-center gap-sm p-md text-on-surface-variant hover:bg-surface-variant transition-all rounded-lg cursor-pointer">
<span class="material-symbols-outlined">settings</span>
<span class="font-body-md text-body-md">Settings</span>
</div>
</nav>
<div class="mt-auto pt-lg">
<button class="w-full bg-primary text-on-primary py-md px-lg rounded-lg font-bold flex items-center justify-center gap-sm hover:brightness-110 active:opacity-80 transition-all">
<span class="material-symbols-outlined">add</span>
<span>New Calculation</span>
</button>
</div>
</aside>
<!-- Main Content Canvas -->
<main class="flex-1 md:ml-64 p-margin-desktop bg-surface overflow-x-hidden">
<!-- Header Section -->
<div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-md mb-xl">
<div>
<h1 class="font-headline-lg text-headline-lg text-on-surface">Material Database</h1>
<p class="font-body-md text-body-md text-on-surface-variant">Central repository for film barrier properties and testing standards.</p>
</div>
<button class="bg-primary text-on-primary px-lg py-md rounded font-bold flex items-center gap-sm hover:shadow-md transition-shadow">
<span class="material-symbols-outlined">add_circle</span>
<span>Add Custom Material</span>
</button>
</div>
<!-- Dashboard Metric Overview (Minimalist) -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-gutter mb-xl">
<div class="scientific-border bg-white p-lg rounded">
<span class="text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider">Total Materials</span>
<div class="flex items-end justify-between mt-base">
<span class="font-display-lg text-display-lg text-primary">1,284</span>
<span class="text-secondary font-bold flex items-center gap-xs">
<span class="material-symbols-outlined">trending_up</span>
                            12%
                        </span>
</div>
</div>
<div class="scientific-border bg-white p-lg rounded">
<span class="text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider">Last Sync</span>
<div class="flex items-end justify-between mt-base">
<span class="font-display-lg text-display-lg text-on-surface">02:45</span>
<span class="text-on-surface-variant font-body-md text-body-md">PM Today</span>
</div>
</div>
<div class="scientific-border bg-white p-lg rounded">
<span class="text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider">Active Standards</span>
<div class="flex items-end justify-between mt-base">
<span class="font-display-lg text-display-lg text-on-surface">18</span>
<span class="text-on-surface-variant font-body-md text-body-md">ASTM/ISO</span>
</div>
</div>
</div>
<!-- Controls & Table Container -->
<div class="scientific-border bg-white rounded overflow-hidden flex flex-col">
<!-- Table Toolbar -->
<div class="p-md flex flex-col md:flex-row gap-md bg-surface-container-low border-b border-outline-variant">
<div class="relative flex-1">
<span class="material-symbols-outlined absolute left-sm top-1/2 -translate-y-1/2 text-outline">search</span>
<input class="w-full bg-white border border-outline-variant rounded pl-10 pr-md py-sm focus:ring-2 focus:ring-primary focus:border-primary outline-none font-body-md text-body-md" placeholder="Search film name, manufacturer or standard..." type="text"/>
</div>
<div class="flex gap-sm overflow-x-auto pb-xs md:pb-0 custom-scrollbar">
<select class="bg-white border border-outline-variant rounded px-md py-sm font-body-md text-body-md outline-none">
<option>All Categories</option>
<option>Metalized</option>
<option>EVOH</option>
<option>Base Film</option>
<option>Coated</option>
</select>
<button class="bg-white border border-outline-variant rounded px-md py-sm font-body-md text-body-md flex items-center gap-sm hover:bg-surface-variant transition-colors whitespace-nowrap">
<span class="material-symbols-outlined text-primary">filter_list</span>
                            Advanced Filters
                        </button>
<button class="bg-white border border-outline-variant rounded px-md py-sm font-body-md text-body-md flex items-center gap-sm hover:bg-surface-variant transition-colors">
<span class="material-symbols-outlined text-on-surface-variant">download</span>
                            Export
                        </button>
</div>
</div>
<!-- Scientific Data Table -->
<div class="overflow-x-auto custom-scrollbar">
<table class="w-full text-left border-collapse">
<thead>
<tr class="bg-surface-container-high border-b-2 border-tertiary">
<th class="p-md font-label-sm text-label-sm text-on-surface-variant uppercase whitespace-nowrap">Material Category</th>
<th class="p-md font-label-sm text-label-sm text-on-surface-variant uppercase whitespace-nowrap border-l border-outline-variant">Film Name</th>
<th class="p-md font-label-sm text-label-sm text-on-surface-variant uppercase whitespace-nowrap border-l border-outline-variant">Ref Thickness (µm)</th>
<th class="p-md font-label-sm text-label-sm text-on-surface-variant uppercase whitespace-nowrap border-l border-outline-variant">Ref OTR (cc/m²/day)</th>
<th class="p-md font-label-sm text-label-sm text-on-surface-variant uppercase whitespace-nowrap border-l border-outline-variant">Ref WVTR (g/m²/day)</th>
<th class="p-md font-label-sm text-label-sm text-on-surface-variant uppercase whitespace-nowrap border-l border-outline-variant">Standards</th>
<th class="p-md font-label-sm text-label-sm text-on-surface-variant uppercase whitespace-nowrap border-l border-outline-variant text-center">Actions</th>
</tr>
</thead>
<tbody class="divide-y divide-outline-variant">
<!-- Row 1 -->
<tr class="data-table-row hover:bg-primary/5 transition-colors group">
<td class="p-md">
<span class="px-sm py-xs rounded bg-blue-100 text-primary font-label-sm text-label-sm">Metalized</span>
</td>
<td class="p-md font-body-md text-body-md font-semibold text-on-surface border-l border-outline-variant">MET-PET Barrier H</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">12.00</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">0.50</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">0.80</td>
<td class="p-md font-body-md text-body-md border-l border-outline-variant">ASTM D3985 / F1249</td>
<td class="p-md text-center border-l border-outline-variant">
<button class="text-primary font-bold font-body-md text-body-md hover:underline flex items-center justify-center gap-xs mx-auto">
                                        View Research <span class="material-symbols-outlined text-[18px]">open_in_new</span>
</button>
</td>
</tr>
<!-- Row 2 -->
<tr class="data-table-row hover:bg-primary/5 transition-colors group">
<td class="p-md">
<span class="px-sm py-xs rounded bg-green-100 text-on-secondary-container font-label-sm text-label-sm">EVOH</span>
</td>
<td class="p-md font-body-md text-body-md font-semibold text-on-surface border-l border-outline-variant">EVOH-32 Layer Pro</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">3.00</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">0.12</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">12.50</td>
<td class="p-md font-body-md text-body-md border-l border-outline-variant">ASTM D3985</td>
<td class="p-md text-center border-l border-outline-variant">
<button class="text-primary font-bold font-body-md text-body-md hover:underline flex items-center justify-center gap-xs mx-auto">
                                        View Research <span class="material-symbols-outlined text-[18px]">open_in_new</span>
</button>
</td>
</tr>
<!-- Row 3 -->
<tr class="data-table-row hover:bg-primary/5 transition-colors group">
<td class="p-md">
<span class="px-sm py-xs rounded bg-gray-200 text-on-surface-variant font-label-sm text-label-sm">Base Film</span>
</td>
<td class="p-md font-body-md text-body-md font-semibold text-on-surface border-l border-outline-variant">BOPP Standard Matte</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">20.00</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">1600.00</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">5.50</td>
<td class="p-md font-body-md text-body-md border-l border-outline-variant">ASTM F1249</td>
<td class="p-md text-center border-l border-outline-variant">
<button class="text-primary font-bold font-body-md text-body-md hover:underline flex items-center justify-center gap-xs mx-auto">
                                        View Research <span class="material-symbols-outlined text-[18px]">open_in_new</span>
</button>
</td>
</tr>
<!-- Row 4 -->
<tr class="data-table-row hover:bg-primary/5 transition-colors group">
<td class="p-md">
<span class="px-sm py-xs rounded bg-purple-100 text-purple-800 font-label-sm text-label-sm">Coated</span>
</td>
<td class="p-md font-body-md text-body-md font-semibold text-on-surface border-l border-outline-variant">PVDC Coated PET</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">14.00</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">5.00</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">2.00</td>
<td class="p-md font-body-md text-body-md border-l border-outline-variant">ASTM D3985 / F1249</td>
<td class="p-md text-center border-l border-outline-variant">
<button class="text-primary font-bold font-body-md text-body-md hover:underline flex items-center justify-center gap-xs mx-auto">
                                        View Research <span class="material-symbols-outlined text-[18px]">open_in_new</span>
</button>
</td>
</tr>
<!-- Row 5 -->
<tr class="data-table-row hover:bg-primary/5 transition-colors group">
<td class="p-md">
<span class="px-sm py-xs rounded bg-blue-100 text-primary font-label-sm text-label-sm">Metalized</span>
</td>
<td class="p-md font-body-md text-body-md font-semibold text-on-surface border-l border-outline-variant">Alu-Foil Lamination</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">7.00</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">0.00</td>
<td class="p-md font-data-mono text-data-mono border-l border-outline-variant">0.00</td>
<td class="p-md font-body-md text-body-md border-l border-outline-variant">ISO 15106-2</td>
<td class="p-md text-center border-l border-outline-variant">
<button class="text-primary font-bold font-body-md text-body-md hover:underline flex items-center justify-center gap-xs mx-auto">
                                        View Research <span class="material-symbols-outlined text-[18px]">open_in_new</span>
</button>
</td>
</tr>
</tbody>
</table>
</div>
<!-- Pagination Footer -->
<div class="p-md flex justify-between items-center bg-surface-container-low border-t border-outline-variant">
<span class="font-body-md text-body-md text-on-surface-variant">Showing 1 to 5 of 1,284 entries</span>
<div class="flex gap-xs">
<button class="w-8 h-8 flex items-center justify-center rounded border border-outline-variant hover:bg-surface-variant transition-colors">
<span class="material-symbols-outlined text-[18px]">chevron_left</span>
</button>
<button class="w-8 h-8 flex items-center justify-center rounded bg-primary text-on-primary font-bold">1</button>
<button class="w-8 h-8 flex items-center justify-center rounded border border-outline-variant hover:bg-surface-variant transition-colors">2</button>
<button class="w-8 h-8 flex items-center justify-center rounded border border-outline-variant hover:bg-surface-variant transition-colors">3</button>
<button class="w-8 h-8 flex items-center justify-center rounded border border-outline-variant hover:bg-surface-variant transition-colors">
<span class="material-symbols-outlined text-[18px]">chevron_right</span>
</button>
</div>
</div>
</div>
<!-- Contextual Information Card -->
<div class="mt-xl grid grid-cols-1 md:grid-cols-2 gap-lg">
<div class="scientific-border bg-tertiary-fixed p-lg rounded flex gap-md items-start">
<span class="material-symbols-outlined text-primary p-sm bg-white rounded-full">info</span>
<div>
<h4 class="font-bold text-on-tertiary-fixed font-body-lg text-body-lg mb-xs">Reference Data Standards</h4>
<p class="font-body-md text-body-md text-on-tertiary-fixed-variant">All reference OTR values are measured at 23°C, 0% RH. WVTR values are measured at 38°C, 90% RH according to ASTM standards unless specified otherwise in the research source.</p>
</div>
</div>
<div class="scientific-border bg-white p-lg rounded flex gap-md items-center">
<div class="w-12 h-12 flex-shrink-0 bg-secondary-container rounded flex items-center justify-center">
<span class="material-symbols-outlined text-on-secondary-container">science</span>
</div>
<div class="flex-1">
<h4 class="font-bold text-on-surface font-body-lg text-body-lg">Missing a material?</h4>
<p class="font-body-md text-body-md text-on-surface-variant">Request a laboratory test or submit your proprietary data to include in your private workspace.</p>
</div>
<button class="text-primary font-bold border-b border-primary hover:opacity-80 transition-opacity">Request Lab</button>
</div>
</div>
</main>
</div>
<!-- Mobile Navigation Bar -->
<nav class="md:hidden fixed bottom-0 left-0 right-0 h-16 bg-surface border-t border-outline-variant flex justify-around items-center z-50">
<button class="flex flex-col items-center gap-xs text-on-surface-variant">
<span class="material-symbols-outlined">calculate</span>
<span class="text-[10px] font-bold">Calc</span>
</button>
<button class="flex flex-col items-center gap-xs text-primary">
<span class="material-symbols-outlined">database</span>
<span class="text-[10px] font-bold">Data</span>
</button>
<button class="flex flex-col items-center gap-xs text-on-surface-variant">
<span class="material-symbols-outlined">history</span>
<span class="text-[10px] font-bold">History</span>
</button>
<button class="flex flex-col items-center gap-xs text-on-surface-variant">
<span class="material-symbols-outlined">settings</span>
<span class="text-[10px] font-bold">Settings</span>
</button>
</nav>
<script>
        // Simple search interactivity
        const searchInput = document.querySelector('input[type="text"]');
        searchInput.addEventListener('focus', () => {
            searchInput.parentElement.classList.add('ring-2', 'ring-primary/20');
        });
        searchInput.addEventListener('blur', () => {
            searchInput.parentElement.classList.remove('ring-2', 'ring-primary/20');
        });

        // Row hover interaction log (simulated)
        document.querySelectorAll('.data-table-row').forEach(row => {
            row.addEventListener('click', () => {
                console.log('Material detail requested for: ' + row.cells[1].innerText);
            });
        });
    </script>
</body></html>"""
<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
    <h2 style="color: #1E3A8A;">Barrier Prediction Web App</h2>
    <p>ยินดีต้อนรับสู่ระบบทำนายค่า OTR/WVTR</p>
</div>
""" #

# สั่งให้แสดงผลบนหน้าเว็บ
components.html(html_code, height=200)
