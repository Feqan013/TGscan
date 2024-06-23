# Open the file
unique_lines = set()

with open('D:\\tgleaks\\tgleaks.txt', 'r',encoding='utf-8') as file:
    # Iterate through each line
    for line in file:
        # Check if the line contains "gps.az"
        if '.az' in line: # and "master" in line:
            # Print the line

            unique_lines.add(line.strip())
            print(line)

"""for line in unique_lines:
    with open(f'D:\\tgleaks\\tgleaks_site_all.txt', 'a',
              encoding='utf-8') as leakfile_daily:
        leakfile_daily.write(f"{line}\n")"""

print("say :",len(unique_lines))