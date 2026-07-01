import sqlite3

con = sqlite3.connect("stocks.db")
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS Prediction_value")

con.commit()
con.close()

print("ลบตาราง Prediction_value ทิ้งเรียบร้อยแล้ว พร้อมเริ่มใหม่!")