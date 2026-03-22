# 🏪 Superstore Profit Prediction

ทำนายกำไร/ขาดทุน (Profit) ของแต่ละ order ใน Superstore ด้วย Machine Learning

## 🎯 ปัญหาที่แก้

Superstore มี **18.7% ของ orders ที่ขาดทุน** รวมมูลค่ากว่า $156,000  
โปรเจคนี้สร้าง ML model ที่ทำนายได้ว่า order ไหนจะกำไรหรือขาดทุน  
เพื่อช่วยฝ่ายขายตัดสินใจเรื่อง pricing และ discount ก่อนขายจริง

## 📊 Dataset

- **ชื่อ:** [Sample Superstore](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) (Kaggle)
- **จำนวน:** 9,994 orders
- **ช่วงเวลา:** 2014–2017
- **ประเทศ:** United States

## 💡 Key Insights จาก EDA

1. ส่วนลด (Discount) เกิน 20% → Profit เฉลี่ยเป็นลบ
2. Tables และ Bookcases เป็น Sub-Category ที่ขาดทุนหนักที่สุด
3. Central region มีกำไรต่ำที่สุด
4. Sales และ Discount เป็น features ที่สำคัญที่สุดในการทำนาย Profit

## 🤖 Model

| รายละเอียด | ค่า |
|-----------|-----|
| Algorithm | Gradient Boosting Regressor |
| Features | 8 ตัว (5 categorical + 3 numerical) |
| Preprocessing | Pipeline (StandardScaler + OneHotEncoder) |
| Tuning | GridSearchCV with 5-Fold CV |
| R² Score | ≈ 0.87 |
| MAE | ≈ $25 |

## 🌐 Streamlit App

👉 **[เข้าใช้งาน App](https://superstore-profit-prediction.streamlit.app)**

App มี 3 หน้า:
- **ทำนาย Profit** — กรอกข้อมูล order แล้วดูผลทำนาย
- **สำรวจข้อมูล (EDA)** — กราฟ interactive + Feature Importance
- **เกี่ยวกับโปรเจค** — สรุปรายละเอียดทั้งหมด

## 📁 โครงสร้างไฟล์

```
├── app.py                  # Streamlit application
├── model.joblib            # Trained ML model
├── requirements.txt        # Python dependencies
├── data/
│   └── Sample_-_Superstore.csv   # Dataset
├── notebooks/
│   └── EDA.ipynb               # Exploratory Data Analysis
└── README.md
```

## ⚙️ วิธีรันบนเครื่องตัวเอง

```bash
# Clone repo
git clone https://github.com/Etihw175/superstore-profit-prediction.git
cd superstore-profit-prediction

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

## 🛠️ Tech Stack

- Python 3.10+
- scikit-learn (Pipeline, Gradient Boosting, GridSearchCV)
- Streamlit (Web App)
- pandas, numpy, matplotlib, seaborn

---

*ML Deployment Project — Burapha University*
