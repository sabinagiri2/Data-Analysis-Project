import os
import pyreadstat

filepath1 = r"C:\Users\Apana Ale\OneDrive\Desktop\Major Project\dataset\NP_2022\NPBR81SV\NPBR81FL.SAV"
df1, meta = pyreadstat.read_sav(filepath1)
print("✅ File 1 loaded. Rows:", len(df1))

selected_df1 = df1[["M42A","M42C","M42D","M42E","M42F","M42G","M42H","M42I",
                    "M42L","M42M","M42N","S418L","S418M","S418N","M13A","M14","M1","M1A","M1D","M45",
                    "M46","M60","S1014AA","S1014AB","S1014AC","M57A","M57B","M57E","M57F","M57G","M57H",
                    "M57I","M57J","M57K","M57M","M57N","M57O","M57P","M57NB","M57NC","M57ND",
                    "M57X","M2A","M2B","M2C","M2G","M2H","M2K","MH17A","MH17B","MH17C","M82","SDV35BC",
                    "V401"]]

# Update this path to your user directory
output_folder = r"C:\Users\Apana Ale\OneDrive\Desktop\spyder"
os.makedirs(output_folder, exist_ok=True)

output_path1 = os.path.join(output_folder, "selected_file1.xlsx")
selected_df1.to_excel(output_path1, index=False)

print("📁 Exported to:", output_path1)
print("📂 File 1 exists:", os.path.exists(output_path1))


import os

folder = r"C:\Users\Apana Ale\OneDrive\Desktop\Major Project\dataset\NP_2022\NPBR81SV"

# List all files in the folder
files = os.listdir(folder)
sav_files = [f for f in files if f.lower().endswith('.sav')]

if not sav_files:
    print("❌ No .SAV file found in the folder!")
else:
    print("✅ .SAV file found:", sav_files[0])
    full_path = os.path.join(folder, sav_files[0])
    print("Using path:", full_path)
