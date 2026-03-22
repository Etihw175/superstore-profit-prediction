import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ==================== Page Config ====================
st.set_page_config(
    page_title="Superstore Profit Prediction",
    page_icon="🏪",
    layout="wide"
)

# ==================== Load Model ====================
@st.cache_resource
def load_model():
    return joblib.load('model.joblib')

model = load_model()

# ==================== Load Data (for EDA tab) ====================
@st.cache_data
def load_data():
    return pd.read_csv('Sample - Superstore.csv', encoding='latin-1')

df = load_data()

# ==================== Sidebar ====================
st.sidebar.title("🏪 Superstore Profit Prediction")
st.sidebar.markdown("ทำนายกำไร/ขาดทุนของ order จาก Superstore")
st.sidebar.markdown("---")

page = st.sidebar.radio("เลือกหน้า", ["🔮 ทำนาย Profit", "📊 สำรวจข้อมูล (EDA)", "ℹ️ เกี่ยวกับโปรเจค"])

# ==================== Sub-Category by Category ====================
sub_cat_map = {
    'Furniture': ['Bookcases', 'Chairs', 'Furnishings', 'Tables'],
    'Office Supplies': ['Appliances', 'Art', 'Binders', 'Envelopes', 'Fasteners', 'Labels', 'Paper', 'Storage', 'Supplies'],
    'Technology': ['Accessories', 'Copiers', 'Machines', 'Phones']
}

# ==================== PAGE 1: Prediction ====================
if page == "🔮 ทำนาย Profit":
    st.title("🔮 ทำนาย Profit ของ Order")
    st.markdown("กรอกข้อมูลด้านล่าง แล้วกดปุ่มเพื่อดูผลการทำนาย")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 ข้อมูลสินค้า")
        category = st.selectbox("Category (หมวดสินค้า)", ['Furniture', 'Office Supplies', 'Technology'],
                                help="Furniture = เฟอร์นิเจอร์, Office Supplies = อุปกรณ์สำนักงาน, Technology = เทคโนโลยี")
        
        sub_category = st.selectbox("Sub-Category (หมวดย่อย)", sub_cat_map[category],
                                    help="หมวดย่อยของสินค้า ขึ้นอยู่กับ Category ที่เลือก")
        
        sales = st.number_input("Sales — ยอดขาย (USD)", min_value=0.1, max_value=25000.0, value=200.0, step=10.0,
                                help="ยอดขายรวมของ order นี้")
        
        quantity = st.slider("Quantity — จำนวนสินค้า", min_value=1, max_value=14, value=3,
                             help="จำนวนสินค้าใน order")
        
        discount = st.slider("Discount — ส่วนลด", min_value=0.0, max_value=0.8, value=0.0, step=0.05,
                             help="0.0 = ไม่ลด, 0.2 = ลด 20%, 0.8 = ลด 80%",
                             format="%.0f%%") * 100

    with col2:
        st.subheader("🚚 ข้อมูลการจัดส่ง & ลูกค้า")
        ship_mode = st.selectbox("Ship Mode (วิธีจัดส่ง)", 
                                 ['Standard Class', 'Second Class', 'First Class', 'Same Day'],
                                 help="Standard Class = ช้าสุดแต่ถูกสุด, Same Day = เร็วสุดแต่แพงสุด")
        
        segment = st.selectbox("Segment (กลุ่มลูกค้า)", 
                               ['Consumer', 'Corporate', 'Home Office'],
                               help="Consumer = ลูกค้าทั่วไป, Corporate = บริษัท, Home Office = ทำงานที่บ้าน")
        
        region = st.selectbox("Region (ภูมิภาค)", 
                              ['West', 'East', 'Central', 'South'],
                              help="ภูมิภาคของลูกค้าในสหรัฐอเมริกา")

    st.markdown("---")

    # Discount warning
    if discount > 0.2:
        st.warning(f"⚠️ ส่วนลด {discount*100:.0f}% ค่อนข้างสูง — จากข้อมูลพบว่าส่วนลดเกิน 20% มักทำให้ขาดทุน")

    # Predict
    if st.button("🔮 ทำนาย Profit", type="primary", use_container_width=True):
        
        input_data = pd.DataFrame([{
            'Ship Mode': ship_mode,
            'Segment': segment,
            'Region': region,
            'Category': category,
            'Sub-Category': sub_category,
            'Sales': sales,
            'Quantity': quantity,
            'Discount': discount
        }])

        prediction = model.predict(input_data)[0]

        st.markdown("---")
        st.subheader("📋 ผลการทำนาย")

        # แสดงผล
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if prediction >= 0:
                st.metric("Predicted Profit", f"${prediction:,.2f}", delta="กำไร ✅")
            else:
                st.metric("Predicted Profit", f"${prediction:,.2f}", delta="ขาดทุน ❌", delta_color="inverse")
        
        with col_b:
            margin = (prediction / sales * 100) if sales > 0 else 0
            st.metric("Profit Margin", f"{margin:.1f}%")
        
        with col_c:
            st.metric("ยอดขาย", f"${sales:,.2f}")

        # คำอธิบาย
        st.markdown("### 💡 วิเคราะห์ผล")
        if prediction >= 0:
            st.success(f"Order นี้คาดว่าจะ **กำไร ${prediction:,.2f}** (margin {margin:.1f}%)")
        else:
            st.error(f"Order นี้คาดว่าจะ **ขาดทุน ${abs(prediction):,.2f}**")
            st.markdown("**สาเหตุที่เป็นไปได้:**")
            reasons = []
            if discount > 0.2:
                reasons.append(f"- ส่วนลดสูง ({discount*100:.0f}%) — ลดกำไรอย่างมาก")
            if sub_category in ['Tables', 'Bookcases', 'Supplies']:
                reasons.append(f"- {sub_category} เป็นหมวดที่มักขาดทุน")
            if region == 'Central':
                reasons.append("- Central region มีกำไรเฉลี่ยต่ำที่สุด")
            if not reasons:
                reasons.append("- อาจเป็นผลรวมจากหลายปัจจัย")
            st.markdown("\n".join(reasons))

        # Disclaimer
        st.caption("⚠️ ผลทำนายเป็นการประมาณจาก ML model เท่านั้น ไม่ใช่ค่าจริง ใช้เป็นแนวทางประกอบการตัดสินใจ")


# ==================== PAGE 2: EDA ====================
elif page == "📊 สำรวจข้อมูล (EDA)":
    st.title("📊 สำรวจข้อมูล Superstore")
    
    st.markdown(f"Dataset มี **{len(df):,} orders** จากปี 2014–2017")
    st.markdown("---")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Orders ทั้งหมด", f"{len(df):,}")
    col2.metric("กำไรรวม", f"${df['Profit'].sum():,.0f}")
    col3.metric("Orders ที่ขาดทุน", f"{(df['Profit']<0).sum():,} ({(df['Profit']<0).mean()*100:.1f}%)")
    col4.metric("ขาดทุนรวม", f"${df[df['Profit']<0]['Profit'].sum():,.0f}")

    st.markdown("---")

    # เลือกกราฟ
    chart = st.selectbox("เลือกกราฟที่ต้องการดู", [
        "Profit แบ่งตาม Sub-Category",
        "ผลกระทบของ Discount ต่อ Profit", 
        "Profit แบ่งตาม Region",
        "Feature Importance"
    ])

    fig, ax = plt.subplots(figsize=(10, 6))

    if chart == "Profit แบ่งตาม Sub-Category":
        sub_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values()
        colors = ['#e74c3c' if v < 0 else '#2ecc71' for v in sub_profit.values]
        ax.barh(sub_profit.index, sub_profit.values, color=colors, edgecolor='white')
        ax.axvline(0, color='black', linewidth=0.8)
        ax.set_title('Total Profit by Sub-Category (แดง = ขาดทุน)')
        ax.set_xlabel('Profit (USD)')

    elif chart == "ผลกระทบของ Discount ต่อ Profit":
        df_temp = df.copy()
        df_temp['Discount_Range'] = pd.cut(df_temp['Discount'], 
            bins=[-0.01, 0, 0.2, 0.4, 0.8],
            labels=['ไม่ลด (0%)', 'ลดน้อย (1-20%)', 'ลดปานกลาง (21-40%)', 'ลดเยอะ (41-80%)'])
        avg_profit = df_temp.groupby('Discount_Range')['Profit'].mean()
        colors = ['#2ecc71' if v >= 0 else '#e74c3c' for v in avg_profit.values]
        bars = ax.bar(avg_profit.index, avg_profit.values, color=colors, edgecolor='white')
        ax.axhline(0, color='black', linewidth=0.8)
        ax.set_title('Profit เฉลี่ย แบ่งตามระดับส่วนลด')
        ax.set_ylabel('Avg Profit (USD)')
        ax.tick_params(axis='x', rotation=15)

    elif chart == "Profit แบ่งตาม Region":
        region_profit = df.groupby('Region')['Profit'].sum().sort_values()
        ax.barh(region_profit.index, region_profit.values, color='#3498db', edgecolor='white')
        ax.set_title('Total Profit by Region')
        ax.set_xlabel('Profit (USD)')

    elif chart == "Feature Importance":
        model_step = model.named_steps['model']
        preprocessor_step = model.named_steps['preprocessor']
        cat_encoder = preprocessor_step.named_transformers_['cat']
        cat_features = ['Ship Mode', 'Segment', 'Region', 'Category', 'Sub-Category']
        num_features = ['Sales', 'Quantity', 'Discount']
        cat_names = cat_encoder.get_feature_names_out(cat_features).tolist()
        all_names = num_features + cat_names
        feat_imp = pd.Series(model_step.feature_importances_, index=all_names).sort_values(ascending=False)
        top15 = feat_imp.head(15).sort_values()
        ax.barh(top15.index, top15.values, color='steelblue', edgecolor='white')
        ax.set_title('Top 15 Feature Importance')
        ax.set_xlabel('Importance')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ==================== PAGE 3: About ====================
elif page == "ℹ️ เกี่ยวกับโปรเจค":
    st.title("ℹ️ เกี่ยวกับโปรเจค")
    
    st.markdown("""
    ### 🎯 เป้าหมาย
    ทำนายกำไร/ขาดทุน (Profit) ของแต่ละ order ใน Superstore  
    เพื่อช่วยให้ฝ่ายขายตัดสินใจเรื่อง pricing และ discount ได้ดีขึ้น
    
    ### 📊 Dataset
    - **ชื่อ:** Sample Superstore (Kaggle)
    - **จำนวน:** 9,994 orders
    - **ช่วงเวลา:** 2014–2017
    
    ### 🤖 Model
    - **Algorithm:** Gradient Boosting Regressor
    - **Features:** 8 ตัว (5 categorical + 3 numerical)
    - **Evaluation:** R² ≈ 0.87, MAE ≈ $25
    
    ### 💡 Key Insights จาก EDA
    1. **18.7%** ของ orders ขาดทุน (รวม -$156,000)
    2. **Discount > 20%** → Profit เฉลี่ยเป็นลบ
    3. **Tables & Bookcases** ขาดทุนหนักที่สุด
    4. **Sales & Discount** เป็น features ที่สำคัญที่สุด
    
    ### ⚙️ Tech Stack
    - Python, scikit-learn, Streamlit
    - Preprocessing: Pipeline (StandardScaler + OneHotEncoder)
    - Tuning: GridSearchCV with 5-Fold CV
    
    ---
    *ML Deployment Project — Burapha University*
    """)
