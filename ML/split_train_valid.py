import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sys import argv


#label_files = [
#    "./labels/labels_scalogram_base.csv",
#    "./labels/labels_scalogram_enam.csv",
#    "./labels/labels_scalogram_gasc.csv",
#]

#perc_train = 80
#perc_valid = 20

#output_dir = "./labels/split_8/"

label_files = argv[1:-5]
perc_train = float(argv[-5])
perc_valid = float(argv[-4])
output_dir = argv[-3]
how_many_features = int(argv[-2])
TF_stratify = argv[-1]
idx_label = how_many_features
#===============================================

print(f"split method: train = {perc_train}%, valid = {perc_valid}%")
print(f"feature number: {idx_label}")
if TF_stratify=='True':
    print("stratify sampling: Yes")
else:
    print("stratify sampling: No")

os.makedirs(output_dir, exist_ok=True)

frac_train = perc_train/100.0
frac_valid = perc_valid/100.0

train_all = []
valid_all = []

for csv_file in label_files:
    
    print("\nProcessing:", csv_file)
    
    df = pd.read_csv(csv_file, header=None)
    N = len(df)
    print("  total samples:", N)
    
    
    # split: TRAIN vs VALID
    if TF_stratify=='True':
        df_train, df_valid = train_test_split(df, test_size=frac_valid, shuffle=True, random_state=42, stratify=df.iloc[:,idx_label])
    else:
        df_train, df_valid = train_test_split(df, test_size=frac_valid, shuffle=True, random_state=42)
    
    
    print(f"  train: {len(df_train)} ({len(df_train)/N:.2f}), valid: {len(df_valid)} ({len(df_valid)/N:.2f})")
    
    train_all.append(df_train)
    valid_all.append(df_valid)


# Combine all datasets
df_train_final = pd.concat(train_all, axis=0, ignore_index=True)
df_valid_final = pd.concat(valid_all, axis=0, ignore_index=True)

# save
df_train_final.to_csv(os.path.join(output_dir, "labels_train.csv"), header=False, index=False)
df_valid_final.to_csv(os.path.join(output_dir, "labels_valid.csv"), header=False, index=False)


N_all = len(df_train_final)+len(df_valid_final)
print("\n---------------------------------------")
print("FINAL COUNTS:")
print(f"Train: {len(df_train_final)} ({len(df_train_final)/N_all:.2f})")
print(f"Valid: {len(df_valid_final)} ({len(df_valid_final)/N_all:.2f})")
print("Train label counts:")
print(df_train_final.iloc[:, idx_label].value_counts(normalize=False))
print("Valid label counts:")
print(df_valid_final.iloc[:, idx_label].value_counts(normalize=False))
print("Train label distribution:")
print(df_train_final.iloc[:, idx_label].value_counts(normalize=True))
print("Valid label distribution:")
print(df_valid_final.iloc[:, idx_label].value_counts(normalize=True))
print("-----------------------------------------")
print("Done. Files saved to:", output_dir)



