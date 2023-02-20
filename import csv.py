import csv

# Open the CSV file
with open("data.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    
    # Get the header row
    header = next(reader)
    
    # Create the INSERT SQL template
    sql_template = "INSERT INTO state_management ({}) VALUES ({});".format(
        ", ".join(header),
        ", ".join(["%s"] * len(header))
    )
    
    # Generate the SQL statements
    for row in reader:
        # Escape double quotes and surround each value with quotes
        row = ['"{}"'.format(value.replace('"', '\\"')) for value in row]
        sql = sql_template % tuple(row)
        print(sql)
    




