import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import os
import sys

# Add parent dir to path to find other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -----------------------------------------------------------------------------
# TEAM MODULE IMPORTS (The "Integration" Part)
# -----------------------------------------------------------------------------
try:
    from src.config import DATA_FILE
    from src.db import init_db, save_patient, get_validated_patients # Mocked imports matching structure
    from src.clinical_rules import get_warnings
    from src.ui.ui_theme_config import apply_theme # Mocked
except ImportError:
    # Fallback if running standalone for testing
    pass

# -----------------------------------------------------------------------------
# CORE LOGIC (Purnendu's Work)
# -----------------------------------------------------------------------------

@st.cache_resource
def load_and_train_model():
    """
    Loads data, balances classes with SMOTE, scales features, and trains the SVM.
    Returns: model, scaler, test_data (X_test, y_test)
    """
    # Load Data (Simulating Srija's Loader)
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'indian_liver_patient.csv')
        df = pd.read_csv(data_path)
    except:
        st.error("Dataset not found. Please ensure 'data/indian_liver_patient.csv' exists.")
        return None, None, None, None

    # Preprocessing
    df = df.fillna(df.mean(numeric_only=True))
    df['Gender'] = df['Gender'].apply(lambda x: 1 if x == 'Male' else 0)
    df['Dataset'] = df['Dataset'].map({1: 1, 2: 0}) # 1=Disease, 0=Healthy

    X = df.drop('Dataset', axis=1)
    y = df['Dataset']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # SMOTE (Critical Step)
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_train, y_train)

    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_res)
    X_test_scaled = scaler.transform(X_test)

    # SVM Training
    model = SVC(kernel='rbf', probability=True, random_state=42)
    model.fit(X_train_scaled, y_res)

    return model, scaler, X_test_scaled, y_test

def main():
    st.set_page_config(page_title="HepaGuard AI | Enterprise Edition", layout="wide", page_icon="🏥")
    
    # 1. Init Database
    # init_db() 
    
    # 2. Load Model
    model, scaler, X_test, y_test = load_and_train_model()
    if model is None: return

    # 3. Sidebar Navigation
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3004/3004458.png", width=50)
    st.sidebar.title("HepaGuard AI")
    st.sidebar.caption("System Architect: Purnendu")
    app_mode = st.sidebar.radio("Module Selection", ["New Prediction", "Model Analytics", "Patient Records"])
    st.sidebar.markdown("---")

    # -------------------------------------------------------------------------
    # MODULE A: NEW PREDICTION
    # -------------------------------------------------------------------------
    if app_mode == "New Prediction":
        st.title("🏥 Patient Diagnostics Interface")
        
        with st.expander("👤 Patient Details", expanded=True):
            col1, col2 = st.columns(2)
            name = col1.text_input("Name")
            age = col2.number_input("Age", 1, 100, 45)
            gender = col1.selectbox("Gender", ["Male", "Female"])
            
        with st.expander("🧪 Clinical Vitals (Biomarkers)", expanded=True):
            c1, c2, c3 = st.columns(3)
            tb = c1.number_input("Total Bilirubin", 0.1, 50.0, 0.9)
            db = c2.number_input("Direct Bilirubin", 0.1, 20.0, 0.2)
            alp = c3.number_input("Alkaline Phosphotase", 10, 2000, 200)
            
            c4, c5, c6 = st.columns(3)
            alt = c4.number_input("Alamine Aminotransferase", 10, 2000, 25)
            ast = c5.number_input("Aspartate Aminotransferase", 10, 2000, 30)
            prot = c6.number_input("Total Proteins", 1.0, 10.0, 6.5)
            
            c7, c8 = st.columns(2)
            alb = c7.number_input("Albumin", 1.0, 6.0, 3.3)
            ag = c8.number_input("A/G Ratio", 0.1, 3.0, 0.9)
            
        if st.button("🚀 Analyze Risk Probability"):
            # Prepare Input
            gen_val = 1 if gender == 'Male' else 0
            input_vector = pd.DataFrame([[age, gen_val, tb, db, alp, alt, ast, prot, alb, ag]], 
                                      columns=['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 
                                               'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
                                               'Aspartate_Aminotransferase', 'Total_Protiens', 
                                               'Albumin', 'Albumin_and_Globulin_Ratio'])
            
            # Scale & Predict
            input_scaled = scaler.transform(input_vector)
            prob = model.predict_proba(input_scaled)[0][1]
            pred = model.predict(input_scaled)[0]
            
            # Display Results
            st.divider()
            r1, r2 = st.columns([1, 2])
            
            with r1:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = prob * 100,
                    title = {'text': "Liver Disease Probability"},
                    gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#ff4b4b" if prob > 0.5 else "#4ecdc4"}}
                ))
                st.plotly_chart(fig, use_container_width=True)
                
            with r2:
                if prob > 0.6:
                    st.error(f"### ⚠️ HIGH RISK DETECTED ({prob*100:.1f}%)")
                    st.markdown("The SVM model indicates a strong likelihood of liver pathology.")
                else:
                    st.success(f"### ✅ LOW RISK ({prob*100:.1f}%)")
                    st.markdown("Biomarkers appear within safe operational ranges.")
                    
                # Clinical Logic Injection (Simulating src.clinical_rules)
                st.markdown("#### 🩺 Clinical Insights:")
                if tb > 1.2: st.warning("- **Total Bilirubin** is elevated (>1.2). Possible Jaundice.")
                if alt > 50: st.warning("- **ALT** is elevated. Liver inflammation indicated.")
                if alb < 3.5: st.warning("- **Albumin** is low. Synthetic function impaired.")

    # -------------------------------------------------------------------------
    # MODULE B: MODEL ANALYTICS
    # -------------------------------------------------------------------------
    elif app_mode == "Model Analytics":
        st.title("📊 SVM Model Performance Audit")
        
        y_pred = model.predict(X_test)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Confusion Matrix")
            cm = confusion_matrix(y_test, y_pred)
            fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale='Blues',
                               labels=dict(x="Predicted", y="Actual"))
            st.plotly_chart(fig_cm)
            
        with col2:
            st.subheader("ROC Curve")
            y_prob = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)
            
            fig_roc = go.Figure()
            fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, name=f'AUC = {roc_auc:.2f}'))
            fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], line=dict(dash='dash'), name='Random'))
            st.plotly_chart(fig_roc)

    # -------------------------------------------------------------------------
    # MODULE C: DATABASE HISTORY
    # -------------------------------------------------------------------------
    elif app_mode == "Patient Records":
        st.title("🗄️ Secure Database Records")
        st.info("Start Database Service to view records.")
        # df_hist = get_all_patients()
        # st.dataframe(df_hist)

if __name__ == "__main__":
    main()
