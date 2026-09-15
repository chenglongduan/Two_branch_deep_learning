import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sys import argv


#label_files = [
#    "./labels/labels_scalogram_base.csv",
#    "./labels/labels_scalogram_enam.csv",
#    "./labels/labels_scalogram_gasc.csv",
#]

#perc_train = 70
#perc_valid = 15
#perc_test = 15

#output_dir = "./labels/split_8/"

label_files = argv[1:-6]
perc_train = float(argv[-6])
perc_valid = float(argv[-5])
perc_test  = float(argv[-4])
output_dir = argv[-3]
how_many_features = int(argv[-2])
TF_stratify = argv[-1]
idx_label = how_many_features
#===============================================

print(f"split method: train = {perc_train}%, valid = {perc_valid}%, test = {perc_test}%")
print(f"feature number: {idx_label}")
if TF_stratify=='True':
    print("stratify sampling: Yes")
else:
    print("stratify sampling: No")

os.makedirs(output_dir, exist_ok=True)

frac_split1 = (1.0-perc_train/100.0)
frac_split2 = perc_test/(perc_valid+perc_test)

train_all = []
valid_all = []
test_all = []

for csv_file in label_files:
    
    print("\nProcessing:", csv_file)
    
    df = pd.read_csv(csv_file, header=None)
    N = len(df)
    print("  total samples:", N)
    
    
    if TF_stratify=='True':
        # First split: TRAIN vs (VALID+TEST)
        df_train, df_tmp = train_test_split(df, test_size=frac_split1, shuffle=True, random_state=42, stratify=df.iloc[:,idx_label])
        
        # Second split: VALID vs TEST
        df_valid, df_test = train_test_split(df_tmp, test_size=frac_split2, shuffle=True, random_state=42, stratify=df_tmp.iloc[:,idx_label])
    else:
        # First split: TRAIN vs (VALID+TEST)
        df_train, df_tmp = train_test_split(df, test_size=frac_split1, shuffle=True, random_state=42)
        
        # Second split: VALID vs TEST
        df_valid, df_test = train_test_split(df_tmp, test_size=frac_split2, shuffle=True, random_state=42)
    
    
    print(f"  train: {len(df_train)} ({len(df_train)/N:.2f}), valid: {len(df_valid)} ({len(df_valid)/N:.2f}), test: {len(df_test)} ({len(df_test)/N:.2f})")
    
    train_all.append(df_train)
    valid_all.append(df_valid)
    test_all.append(df_test)


# Combine all datasets
df_train_final = pd.concat(train_all, axis=0, ignore_index=True)
df_valid_final = pd.concat(valid_all, axis=0, ignore_index=True)
df_test_final  = pd.concat(test_all, axis=0, ignore_index=True)

# save
df_train_final.to_csv(os.path.join(output_dir, "labels_train.csv"), header=False, index=False)
df_valid_final.to_csv(os.path.join(output_dir, "labels_valid.csv"), header=False, index=False)
df_test_final.to_csv(os.path.join(output_dir, "labels_test.csv"), header=False, index=False)


N_all = len(df_train_final)+len(df_valid_final)+len(df_test_final)
print("\n---------------------------------------")
print("FINAL COUNTS:")
print(f"Train: {len(df_train_final)} ({len(df_train_final)/N_all:.2f})")
print(f"Valid: {len(df_valid_final)} ({len(df_valid_final)/N_all:.2f})")
print(f"Test : {len(df_test_final)} ({len(df_test_final)/N_all:.2f})")
print("Train label counts:")
print(df_train_final.iloc[:, idx_label].value_counts(normalize=False))
print("Valid label counts:")
print(df_valid_final.iloc[:, idx_label].value_counts(normalize=False))
print("Test label counts:")
print(df_test_final.iloc[:, idx_label].value_counts(normalize=False))
print("Train label distribution:")
print(df_train_final.iloc[:, idx_label].value_counts(normalize=True))
print("Valid label distribution:")
print(df_valid_final.iloc[:, idx_label].value_counts(normalize=True))
print("Test label distribution:")
print(df_test_final.iloc[:, idx_label].value_counts(normalize=True))
print("-----------------------------------------")
print("Done. Files saved to:", output_dir)



