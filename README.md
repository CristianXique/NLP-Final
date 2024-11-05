# NLP-Final
COSC 426 NLP Final

Overview

This project involves creating a decade-based classifier for English texts using the Wikisource dataset from Hugging Face (wikimedia/wikisource). Our objective is to train a model that can predict the decade a text was written, allowing for temporal classification of historical texts. This README outlines the steps to preprocess the data, create a model using NLPScholar, and evaluate the model's performance.

Steps to Achieve the Final Evaluation Metrics

1. Data Extraction and Year Identification
Dataset: We will work with the English subset of the Wikisource dataset on Hugging Face, focusing on historical texts without a year column.
Python Script for Year Extraction:
Objective: Develop a script to identify and label each text with the appropriate year.
Method:
For titles that fall under known categories (e.g., "Category: 1890s"), the script will assign a year based on the category.
For texts outside these categories, the script will search the HTML source or metadata to identify the year.
Output: The script will generate a year label for each text to use for grouping by decade.

2. Decade Grouping
Purpose: To ensure each group has sufficient data, we will aggregate texts into decades (e.g., 1880s, 1890s).
Implementation:
After identifying years, map each year to its respective decade.
Group the texts accordingly, maintaining consistency and balance across decades.

3. Data Split into Training and Testing Sets
TSV File Format:
Create two TSV files, one for training and another for testing. Each file will have:
Text column: The raw text from Wikisource.
Decade column: The decade label for the text.
Data Splitting:
Randomly split the dataset to ensure no text overlaps between training and testing sets.
Aim for a balanced split, with representative samples across decades.

4. Model Training with NLPScholar
Purpose: Train a model to classify texts by decade.
NLPScholar Setup:
Load the training data into NLPScholar’s toolkit for Text Classification.
Configure the model to use the training TSV file.
Experiment with parameters to find the optimal setup for text classification.
Training Process:
Run training on the texts with decade labels, saving the model checkpoints and relevant configuration files.

5. Evaluation Process
Objective: Use the trained model to predict the decade labels for the texts in the test set and evaluate the predictions.
Evaluation Metrics:
Accuracy: Calculate the percentage of correct predictions, measuring the model’s ability to identify the correct decade.
Near Decade Analysis:
For incorrect predictions, examine if the model selected a nearby decade (e.g., predicting 1880s instead of the actual 1890s).
This will help us understand how well the model understands temporal proximity and to what extent the predictions are “close” to the correct answer.
Results Storage:
Save results as a CSV file, with columns for the text, actual decade, predicted decade, and a flag indicating if the prediction was in the "near decade."

6. Generating Final Tables and Figures
Accuracy Table: Present the accuracy of predictions for each decade, highlighting trends or anomalies.
Near Decade Analysis Table:
Show the count of “close” predictions by decade, offering insight into temporal misclassifications.
Visualizations:
Confusion Matrix: Plot a matrix showing true vs. predicted decades, with color coding to indicate accuracy.
Decade-Wise Accuracy Plot: Graph the accuracy rate for each decade, which can reveal periods that are more challenging for the model.

