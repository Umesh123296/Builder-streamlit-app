import pandas as pd
from rapidfuzz import process, fuzz

def map_promoter_to_builder(promoter_names, builderinfo_names, threshold=70):
    mapping = {}
    for p_name in promoter_names:
        match = process.extractOne(p_name, builderinfo_names, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= threshold:
            mapping[p_name] = match[0]
        else:
            mapping[p_name] = None
    return mapping

# Load your data
promoters_df = pd.read_csv('promoters.csv')  # Or use pd.read_excel('promoters.xlsx')
builders_df = pd.read_csv('builders.csv')    # Or pd.read_excel('builders.xlsx')

# Extract the lists
promoter_names = promoters_df['promotername'].dropna().unique().tolist()
builderinfo_names = builders_df['builderinfo_name'].dropna().unique().tolist()

# Map promoters to builders
mapping = map_promoter_to_builder(promoter_names, builderinfo_names)

# Add the mapped builder info as a new column in promoters_df
promoters_df['matched_builderinfo_name'] = promoters_df['promotername'].map(mapping)

# Save the result to a new file
promoters_df.to_csv('promoters_with_matched_builders.csv', index=False)

print("Mapping complete! Results saved to promoters_with_matched_builders.csv")
