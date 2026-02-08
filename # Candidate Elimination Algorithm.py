# Candidate Elimination Algorithm
import pandas as pd

# Step 0: Load dataset
data = {
    'age_cat': ['Adult', 'Adult', 'Adult', 'Young', 'Old'],
    'bmi_cat': ['High', 'High', 'High', 'High', 'High'],
    'smoker': ['yes', 'yes', 'no', 'no', 'no'],
    'Cost_Level': ['High', 'High', 'Low', 'Low', 'Low']
}

df = pd.DataFrame(data)

# Attributes
attributes = ['age_cat', 'bmi_cat', 'smoker']

# Step 1: Initialize S and G
S = df[df['Cost_Level'] == 'High'].iloc[0][attributes].tolist()  # most specific
G = [['?' for _ in range(len(attributes))]]  # most general

print("Initial S:", S)
print("Initial G:", G)

# Step 2: Process each example
for index, row in df.iterrows():
    example = row[attributes].tolist()
    label = row['Cost_Level']
    
    if label == 'High':  # positive example
        for i in range(len(S)):
            if S[i] != example[i]:
                S[i] = '?'  # generalize S
        # Remove hypotheses from G inconsistent with S
        G = [g for g in G if all(g[i] == '?' or g[i] == S[i] for i in range(len(S)))]
        
    else:  # negative example
        new_G = []
        for g in G:
            if all(g[i] == '?' or g[i] == example[i] for i in range(len(S))):
                # g covers negative example → specialize g
                for i in range(len(g)):
                    if g[i] == '?':
                        if S[i] != example[i]:
                            new_hypothesis = g.copy()
                            new_hypothesis[i] = S[i]
                            new_G.append(new_hypothesis)
            else:
                new_G.append(g)
        # Remove duplicates
        G = [list(x) for x in set(tuple(x) for x in new_G)]

    print(f"\nAfter example {index+1} ({example}, {label}):")
    print("S:", S)
    print("G:", G)

# Final hypotheses
print("\nFinal Most Specific Hypothesis S:", S)
print("Final Most General Hypotheses G:", G)
