import pandas as pd
import re

path= input ("enter file path to csv:")
cleaned_input = path.strip('"\'')
file_path = input("enter destination path and file name:")
cleaned_file = file_path.strip('"\'')
#finds users documents folder on windows and uses it as export path

df = pd.read_csv(f"{cleaned_input}")


# #finds rows where pattern matches and extracts stack number and suture quantity
def extract_stack_number(error_message):
     match = re.findall(r' (\"quantity\":\s.,\s\"stackNumber\":\s"[^"]+"),\s"barcode":\s"[^"]*",\s"status":\s"Picked"'
 , error_message, re.IGNORECASE)
     if match:
        return match
     return None

# #creates column with pick stack numbers and quantities and removes rows that were not pick receipts
df['pick_info'] = df['message_content'].apply(extract_stack_number)
df_cleaned = df.dropna(subset=['pick_info'])


#Flatten the list of lists into a single list
all_numbers = [num for sublist in df_cleaned['pick_info'] for num in sublist]
df2 = pd.DataFrame(all_numbers)
df2.columns=['info']

#separates quantity and stack into separate columns
df2['suture quantity'] = df2['info'].str.extract(r'"quantity":\s(\d+)').astype(int)
df2['stack number'] = df2['info'].str.extract(r'"stackNumber":\s"(\d+)"')

# groups by stack number and adds suture quantities for each stack number group
df_grouped = df2.groupby('stack number')['suture quantity'].sum().reset_index()
df_grouped.to_csv(f"{cleaned_file}.csv", index=False)