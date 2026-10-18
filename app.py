import streamlit as st
from google import genai
from google.genai import types

# 1. Điền API Key của bạn vào giữa hai dấu ngoặc kép bên dưới
API_KEY = "AQ.Ab8RN6L3U3G1dI7OHdZhTdtQ4GVPiHgicRHU5uZ8KFzQ2m3rhA"

# Khởi tạo kết nối với Google AI
client = genai.Client(api_key=API_KEY)

# Cấu hình giao diện ứng dụng
st.set_page_config(page_title="AI Dạy Tiếng Khmer")
st.title("Trợ Lý Giáo Viên Tiếng Khmer")
st.caption("AI hỗ trợ học từ vựng, ngữ pháp và giao tiếp tiếng Khmer")

# Kịch bản đóng vai (System Instruction) cho AI
system_instruction = """
Bạn là một giáo viên dạy tiếng Khmer cực kỳ kiên nhẫn, thân thiện dành cho người Việt Nam.
Quy tắc giảng dạy của bạn:
1. Luôn trình bày từ/câu tiếng Khmer theo đúng 3 thành phần:
   - Chữ Khmer nguyên bản (Ví dụ: សួស្តី)
   - Phiên âm tiếng Việt dễ đọc (Ví dụ: Suô-sơ-đây)
   - Nghĩa tiếng Việt (Ví dụ: Xin chào)
2. Nếu người dùng mới bắt đầu, hãy chủ động gợi ý dạy từ Bảng chữ cái hoặc các câu giao tiếp cơ bản.
3. Cuối mỗi lời giải thích, hãy đưa ra 1 câu hỏi nhỏ hoặc bài tập để người dùng luyện tập ngay.
"""

# Quản lý lịch sử trò chuyện
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận đầu vào từ người dùng
if prompt := st.chat_input("Nhập câu hỏi (VD: Dạy tôi các số đếm từ 1 đến 5)..."):
    # Lưu và hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi yêu cầu đến AI Gemini
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            ),
        )
        
        # Hiển thị câu trả lời của AI
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {e}. Vui lòng kiểm tra lại API Key.")
