# Time-Series-Analysis-for-Thai-Bank-Stock-Prediction-

Stock Trend Prediction AI

โปรเจกต์นี้เป็นระบบวิเคราะห์และทำนายแนวโน้มราคาหุ้นธนาคาร โดยใช้ (1D-CNN และ Random Forest) พร้อมบันทึกผลการทำนายลงในฐานข้อมูล SQLite

Features
- Real-time Data : ดึงข้อมูลหุ้นสดๆ จาก Yahoo Finance
- AI-Powered : เลือกใช้โมเดลทำนายได้ทั้ง 1D-CNN (PyTorch) และ Random Forest (Scikit-Learn)
- Database : บันทึกประวัติการทำนายลง SQLite อัตโนมัติ
- Responsive UI : หน้าเว็บใช้งานง่าย เลือกหุ้นได้ผ่าน Dropdown

Tools
- Backend : FastAPI, Python
- AI/ML : PyTorch, Scikit-Learn, Pandas, Pandas-TA
- Database : SQLite
- Frontend : HTML, JavaScript (Fetch API)
  
สิ่งที่คาดว่าจะพัฒนาต่อ
1. พัฒนาให้โมเดลสามารถจับแพทเทิร์นของข้อมูลให้ได้มากขึ้น (ณ ปัจจุบันยังจับไม่ได้เยอะ โมเดลมักสุ่มคำตอบเอา ดูจาก confusion matrix)
2. ลองเปลี่ยนไปใช้โมเดลให้สอดคล้องกับงานวิจัยตัว LSTM, Transformer
3. เพิ่มโมเดลให้เลือกทำนายมากขึ้น และทำ dropdown สำหรับเลือกโมเดลสำหรับทำนายบนหน้าเว็ป
4. เปลี่ยนไปใช้ฐานข้อมูลที่รองรับข้อมูลได้มากขึ้น
5. เพิ่มธนาคารสำหรับการทำนาย

--------------------------------------------------------------------------------------------------------------------------------------------------------------

A comprehensive system for analyzing and predicting trends for Thai bank stocks using machine learning models (1D-CNN and Random Forest), with automated prediction logging via SQLite.

Features
- Real-time Data: Fetches live stock data directly from Yahoo Finance.
- AI-Powered: Supports dual prediction models, including 1D-CNN (PyTorch) and Random Forest (Scikit-Learn).
- Database Integration: Automatically logs all prediction history into a local SQLite database.
- Responsive UI: User-friendly interface with an intuitive stock selection dropdown.

Tech Stack
- Backend: FastAPI, Python
- AI/ML: PyTorch, Scikit-Learn, Pandas, Pandas-TA
- Database: SQLite
- Frontend: HTML, JavaScript (Fetch API)

Future Development Roadmap
Model Optimization: Enhance model architecture to better capture complex data patterns (addressing current limitations observed in the confusion matrix).
Advanced Architectures: Experiment with state-of-the-art models such as LSTM and Transformer networks.

Model Selection UI: Integrate a dynamic dropdown on the frontend, allowing users to select their preferred prediction model.

Scalable Database: Migrate to a more robust database system to handle larger datasets.

Expanded Coverage: Add more banks and financial institutions to the prediction portfolio.
