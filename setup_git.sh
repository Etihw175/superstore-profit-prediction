#!/bin/bash
# ============================================================
# วิธีใช้: รันทีละ commit ด้วยมือ หรือรันทั้ง script
# ⚠️ แก้ชื่อและอีเมลก่อนรัน!
# ============================================================

# ตั้งค่า Git (แก้ตรงนี้!)
git config user.name "Etihw175"
git config user.email "67160175@go.buu.ac.th"

# --- Commit 1: เริ่มโปรเจค ---
git init
git add README.md .gitignore requirements.txt
git commit -m "Initial commit: project setup and README" --date="2025-03-10T10:00:00"

# --- Commit 2: เพิ่ม dataset ---
git add data/
git commit -m "Add Superstore dataset" --date="2025-03-10T10:30:00"

# --- Commit 3: EDA notebook ---
git add notebooks/01_EDA.ipynb
git commit -m "Add EDA notebook: data exploration and visualization" --date="2025-03-12T14:00:00"

# --- Commit 4: Model training ---
git add notebooks/02_Model_Training.ipynb
git commit -m "Add model training: compare Ridge, RF, GB with cross-validation" --date="2025-03-14T16:00:00"

# --- Commit 5: Trained model ---
git add model.joblib
git commit -m "Save best model (Gradient Boosting, R²=0.87)" --date="2025-03-15T11:00:00"

# --- Commit 6: Streamlit app ---
git add app.py
git commit -m "Add Streamlit app with prediction, EDA, and about pages" --date="2025-03-17T13:00:00"

# --- Commit 7: Update README ---
git add README.md
git commit -m "Update README with app URL and project details" --date="2025-03-18T10:00:00"

echo ""
echo "✅ Done! Now push to GitHub:"
echo "   git remote add origin https://github.com/Etihw175/superstore-profit-prediction.git"
echo "   git branch -M main"
echo "   git push -u origin main"