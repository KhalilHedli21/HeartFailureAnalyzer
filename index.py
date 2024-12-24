import pandas as pd
from itertools import combinations
from collections import defaultdict
from tkinter import Tk, Label, Text, Button, END, Scrollbar, Toplevel, messagebox, ttk
from PIL import Image, ImageTk
from mlxtend.frequent_patterns import apriori, association_rules

# Load the dataset
file_path = "heart_failure_clinical_records_dataset.csv"
data = pd.read_csv(file_path)

# Define thresholds for binary conversion
thresholds = {
    'age': 50,
    'creatinine_phosphokinase': 200,
    'ejection_fraction': 50,
    'platelets': 150000,
    'serum_creatinine': 1.5,
    'serum_sodium': 135
}

# Convert columns to binary based on thresholds
for column, threshold in thresholds.items():
    if column in data.columns:
        data[column] = (data[column] > threshold).astype(int)

# Save the processed dataset
binary_file_path = "processed_heart_failure_data.csv"
data.to_csv(binary_file_path, index=False)
print(f"Processed data saved to {binary_file_path}")

# Create transactions for the Apriori algorithm
item_list = data.columns.tolist()
item_dict = {item: i + 1 for i, item in enumerate(item_list)}
transactions = [
    {item_dict[item] for item in item_list if row[item] == 1}
    for _, row in data.iterrows()
]

# Functions for Apriori Algorithm
def get_support(transactions, item_set):
    return sum(1 for transaction in transactions if item_set.issubset(transaction)) / len(transactions)

def generate_candidates(frequent_itemsets, k):
    return [
        frozenset(set1.union(set2))
        for i, set1 in enumerate(frequent_itemsets)
        for set2 in frequent_itemsets[i + 1:]
        if len(set1.union(set2)) == k
    ]

def apriori(transactions, min_support):
    frequent_itemsets = defaultdict(list)
    single_items = [frozenset([item]) for item in item_dict.values()]

    # Generate L1
    for item_set in single_items:
        support = get_support(transactions, item_set)
        if support >= min_support:
            frequent_itemsets[1].append((item_set, support))

    # Generate L2, L3, ...
    k = 2
    while True:
        candidates = generate_candidates([item for item, _ in frequent_itemsets[k - 1]], k)
        level_itemsets = []

        for item_set in candidates:
            support = get_support(transactions, item_set)
            if support >= min_support:
                level_itemsets.append((item_set, support))

        if not level_itemsets:
            break

        frequent_itemsets[k] = level_itemsets
        k += 1

    return frequent_itemsets

def extract_rules(frequent_itemsets, min_confidence):
    rules = []
    for k, itemsets in frequent_itemsets.items():
        for itemset, support in itemsets:
            if len(itemset) > 1:
                for subset in map(frozenset, combinations(itemset, len(itemset) - 1)):
                    confidence = support / get_support(transactions, subset)
                    if confidence >= min_confidence:
                        rules.append((subset, itemset - subset, confidence))
    return rules

# Parameters
min_support = 0.3
min_confidence = 0.6

# Run Apriori
frequent_itemsets = apriori(transactions, min_support)
association_rules_result = extract_rules(frequent_itemsets, min_confidence)

# Function to display CSV content
def display_csv():
    try:
        data = pd.read_csv(file_path)
        new_window = Toplevel(root)
        new_window.title("CSV Content")

        tree = ttk.Treeview(new_window, columns=list(data.columns), show="headings")
        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for _, row in data.iterrows():
            tree.insert("", "end", values=list(row))

        scroll_y = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")

    except Exception as e:
        messagebox.showerror("Error", f"Error loading CSV: {e}")

# GUI Functions
def display_results():
    text_box.delete(1.0, END)
    text_box.insert(END, "Frequent Itemsets:\n\n")
    for k, itemsets in frequent_itemsets.items():
        text_box.insert(END, f"Level {k}:\n")
        for itemset, support in itemsets:
            item_names = {key for key, val in item_dict.items() if val in itemset}
            text_box.insert(END, f"  {item_names}: {support:.2f}\n")
    text_box.insert(END, "\nAssociation Rules:\n\n")
    for antecedent, consequent, confidence in association_rules_result:
        antecedent_names = {key for key, val in item_dict.items() if val in antecedent}
        consequent_names = {key for key, val in item_dict.items() if val in consequent}
        text_box.insert(END, f"  {antecedent_names} -> {consequent_names} (Confidence: {confidence:.2f})\n")

# Main GUI Configuration
root = Tk()
root.title("Frequent Itemsets and Association Rules")

label = Label(root, text="Frequent Itemsets and Association Rules", font=("Helvetica", 16))
label.pack()

scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")

text_box = Text(root, wrap="word", yscrollcommand=scrollbar.set, font=("Courier", 12), width=90, height=30)
text_box.pack()
scrollbar.config(command=text_box.yview)

button_display_csv = Button(root, text="Show CSV", command=display_csv, font=("Helvetica", 14))
button_display_csv.pack()

button_show_results = Button(root, text="Show Results", command=display_results, font=("Helvetica", 14))
button_show_results.pack()

root.mainloop()
