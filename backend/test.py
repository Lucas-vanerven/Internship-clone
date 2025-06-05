from ArpY.rainbow import Drive


drive = Drive(r"C:\Users\lucas\Cronbach-WebApp\ArpY\file-request-automation-a62dd7fbdc0f.json")
statements_df = drive.spreadsheet("Statements", "Statements-aliases-strategies")
statements_df = statements_df[statements_df["Client"] == "ALC"]

print(statements_df)