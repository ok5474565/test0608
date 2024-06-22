import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate covariance for sorting
def calculate_covariance(student_scores, problem_scores):
    return np.cov(student_scores, problem_scores)[0, 1]

# Function to load and process the data
def process_sp_chart(file):
    df = pd.read_excel(file, header=0, index_col=0)
    
    # Extracting student names and problem names
    student_names = df.index.tolist()
    problem_names = df.columns.tolist()
    
    # Calculating student scores and problem scores
    student_scores = df.sum(axis=1)
    problem_scores = df.sum(axis=0)
    
    # Sorting students by total score, then by covariance if scores are the same
    sorted_students = student_scores.sort_values(ascending=False).index.tolist()
    for i in range(len(sorted_students) - 1):
        for j in range(i + 1, len(sorted_students)):
            if student_scores[sorted_students[i]] == student_scores[sorted_students[j]]:
                cov_i = calculate_covariance(df.loc[sorted_students[i]], problem_scores)
                cov_j = calculate_covariance(df.loc[sorted_students[j]], problem_scores)
                if cov_i < cov_j:
                    sorted_students[i], sorted_students[j] = sorted_students[j], sorted_students[i]
    
    # Sorting problems by total score, then by covariance if scores are the same
    sorted_problems = problem_scores.sort_values(ascending=False).index.tolist()
    for i in range(len(sorted_problems) - 1):
        for j in range(i + 1, len(sorted_problems)):
            if problem_scores[sorted_problems[i]] == problem_scores[sorted_problems[j]]:
                cov_i = calculate_covariance(df[sorted_problems[i]], student_scores)
                cov_j = calculate_covariance(df[sorted_problems[j]], student_scores)
                if cov_i < cov_j:
                    sorted_problems[i], sorted_problems[j] = sorted_problems[j], sorted_problems[i]

    # Generating the sorted S-P table
    sorted_df = df.loc[sorted_students, sorted_problems]
    
    # Adding sorted student and problem names back to the table
    sorted_df.index.name = df.index.name
    sorted_df.columns.name = df.columns.name
    
    return sorted_df, sorted_students, sorted_problems

# Function to plot S-line and P-line from sorted data
def plot_sp_chart(sorted_df, sorted_students, sorted_problems):
    num_students, num_questions = sorted_df.shape
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    # S-line: For each student, draw vertical segments
    student_scores = sorted_df.sum(axis=1)
    for i, student in enumerate(sorted_students):
        ax[0].vlines(i, ymin=0, ymax=student_scores[student], color='b')
        if i < num_students - 1:
            ax[0].hlines(y=student_scores[student], xmin=i, xmax=i + 1, color='b')
    
    ax[0].set_xticks(np.arange(num_students))
    ax[0].set_xticklabels(sorted_students, rotation=90)
    ax[0].set_yticks(np.arange(num_questions + 1))
    ax[0].set_ylabel('Number of Correct Answers')
    ax[0].set_title('S-line: Student Performance')
    
    # P-line: For each question, draw horizontal segments
    problem_scores = sorted_df.sum(axis=0)
    for j, problem in enumerate(sorted_problems):
        ax[1].hlines(j, xmin=0, xmax=problem_scores[problem], color='r')
        if j < num_questions - 1:
            ax[1].vlines(x=problem_scores[problem], ymin=j, ymax=j + 1, color='r')
    
    ax[1].set_yticks(np.arange(num_questions))
    ax[1].set_yticklabels(sorted_problems)
    ax[1].set_xticks(np.arange(num_students + 1))
    ax[1].set_xlabel('Number of Students Answered Correctly')
    ax[1].set_title('P-line: Question Difficulty')
    
    plt.tight_layout()
    plt.show()

# Usage example
file_path = "path_to_your_file.xlsx"  # Replace with your file path

sorted_df, sorted_students, sorted_problems = process_sp_chart(file_path)
plot_sp_chart(sorted_df, sorted_students, sorted_problems)
