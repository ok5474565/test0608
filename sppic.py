import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data(file):
    data = pd.read_csv(file)
    return data

def create_sp_table(data):
    # Transpose data to have students as columns and questions as rows
    sp_table = data.T
    return sp_table

def sort_sp_table(sp_table):
    # Sort students by total score (column sums)
    sp_table = sp_table.reindex(sp_table.sum().sort_values(ascending=False).index, axis=1)
    # Sort questions by total score (row sums)
    sp_table = sp_table.reindex(sp_table.sum(axis=1).sort_values(ascending=False).index)
    return sp_table

def handle_ties(sp_table):
    # Handle ties for student scores
    student_scores = sp_table.sum()
    unique_scores = student_scores.unique()
    for score in unique_scores:
        students_with_score = student_scores[student_scores == score].index
        if len(students_with_score) > 1:
            cov_matrix = np.cov(sp_table[students_with_score])
            cov_sums = cov_matrix.sum(axis=0)
            sorted_students = [students_with_score[i] for i in np.argsort(-cov_sums)]
            sp_table = sp_table[sorted_students]

    # Handle ties for question scores
    question_scores = sp_table.sum(axis=1)
    unique_scores = question_scores.unique()
    for score in unique_scores:
        questions_with_score = question_scores[question_scores == score].index
        if len(questions_with_score) > 1:
            cov_matrix = np.cov(sp_table.T[questions_with_score])
            cov_sums = cov_matrix.sum(axis=0)
            sorted_questions = [questions_with_score[i] for i in np.argsort(-cov_sums)]
            sp_table = sp_table.loc[sorted_questions]

    return sp_table

def plot_curves(sp_table):
    num_students = sp_table.shape[1]
    num_questions = sp_table.shape[0]

    s_curve = np.cumsum(sp_table, axis=0)
    p_curve = np.cumsum(sp_table, axis=1)

    fig, ax = plt.subplots(2, 1, figsize=(12, 8))

    for i in range(num_students):
        ax[0].step(range(num_questions), s_curve[:, i], where='mid', label=f'Student {i+1}')
    ax[0].set_title('S Curve')
    ax[0].set_xlabel('Questions')
    ax[0].set_ylabel('Cumulative Score')

    for i in range(num_questions):
        ax[1].step(range(num_students), p_curve[i, :], where='mid', label=f'Question {i+1}')
    ax[1].set_title('P Curve')
    ax[1].set_xlabel('Students')
    ax[1].set_ylabel('Cumulative Correct Answers')

    plt.tight_layout()
    st.pyplot(fig)

def main():
    st.title("S-P Table and Curves Generator")
    
    uploaded_file = st.file_uploader("Upload your score data", type=["csv"])
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.write("Uploaded Data:")
        st.dataframe(data)

        sp_table = create_sp_table(data)
        sp_table = sort_sp_table(sp_table)
        sp_table = handle_ties(sp_table)
        
        st.write("S-P Table:")
        st.dataframe(sp_table)
        
        plot_curves(sp_table)

if __name__ == "__main__":
    main()
