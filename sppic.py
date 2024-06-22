import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_s_line(df):
    fig, ax = plt.subplots()
    
    for col in df.columns:
        x = [col] * len(df)
        y = df[col].values
        ax.vlines(x, ymin=0, ymax=y, color='blue')
        ax.plot(x, y, color='blue', marker='o')
    
    ax.set_xlabel('Students')
    ax.set_ylabel('Scores')
    ax.set_title('S Line Plot')
    st.pyplot(fig)

def plot_p_line(df):
    fig, ax = plt.subplots()

    correct_counts = df.apply(lambda x: x[x > 0].count(), axis=1)
    
    for idx, count in enumerate(correct_counts):
        y = [count] * len(correct_counts)
        x = list(range(len(correct_counts)))
        ax.hlines(y[idx], xmin=0, xmax=x[idx], color='green')
        ax.plot(x, y, color='green', marker='o')
    
    ax.set_xlabel('Questions')
    ax.set_ylabel('Number of Students Correct')
    ax.set_title('P Line Plot')
    st.pyplot(fig)

st.title('S and P Line Plotter')

uploaded_file = st.file_uploader("Upload your S-P table", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        st.write("Data Preview:")
        st.write(df)

        st.write("S Line Plot:")
        plot_s_line(df)
        
        st.write("P Line Plot:")
        plot_p_line(df)
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
