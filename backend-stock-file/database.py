import sqlite3

# เชื่อมต่อฐานข้อมูล
con = sqlite3.connect("stocks.db")
cur = con.cursor()

cur.execute("SELECT * FROM Prediction_value")

rows = cur.fetchall()

print(f"พบข้อมูลทั้งหมด {len(rows)} แถว:")
print("-" * 50)
for row in rows:
    print(row)
print("-" * 50)

con.close()