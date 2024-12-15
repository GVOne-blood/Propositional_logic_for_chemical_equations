import streamlit as st 
from dieuCheHoaHoc import dieuCheHoaHoc

# Khởi tạo dieuCheHoaHoc
file_path = "F:/Document/AI_SIC/Chemical_reactions_crawling/Chemical reactions datasetV2.xlsx"
inference_engine = dieuCheHoaHoc(file_path)

# Thiết lập trang
st.set_page_config(page_title="Từ điển phương trình hóa học", layout="centered")
# Tùy chỉnh CSS
st.markdown("""
<style>
    body{
        background : #111826ff;
    }
    .stApp {
        background-color: #1E1E1E;
        color: white;
    }
    .search-container {
        background-color: #2D2D2D;
        border: 1px solid #3D3D3D;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        width : 500px;
    }
    .stButton>button {
        background-color: #4C8BF5;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #2D2D2D;
        color: white;
    }
    .stAlert {
        background-color: transparent;
        border: 1px solid #FF4B4B;
        color: #FF4B4B;
    }
    .result-box {
        background-color: #1f2a38ff;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        border: 1px solid #3D3D3D;
    }
    .result-equation {
        font-size: 24px;
        color: rgb(164, 124, 207);
        margin-bottom: 15px;
        font-weight : bold;
    }
    .result-inference_engine {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        color: #B0B0B0;
        margin-bottom: 10px;
    }
    .result-inference_engine span {
        margin: 10px;
        
    }
    .view-inference_engine {
        color: #4C8BF5;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)
# Tiêu đề
st.title("Tìm kiếm phương trình hóa học")

# Hướng dẫn
st.write("Hãy nhập vào chất tham gia và chất sản phẩm để bắt đầu tìm kiếm")

# Tạo hai cột cho input
col1, col2 = st.columns(2)

with col1:
    chat_tham_gia = st.text_input("Chất tham gia", key="chat_tham_gia")

with col2:
    chat_san_pham = st.text_input("Chất sản phẩm", key="chat_san_pham")

# Lưu ý
st.markdown('<p style="color: #FF4B4B;">Lưu ý: mỗi chất cách nhau 1 dấu phẩy, ví dụ: H2,O2</p> ', unsafe_allow_html=True)
# Nút tìm kiếm
if st.button("Tìm kiếm"):
    if chat_tham_gia and chat_san_pham:
        # Chuyển đổi input thành list các chất tham gia
        initial_facts = [x.strip() for x in chat_tham_gia.split(',')]
        
        # Thực hiện suy diễn
        result, reactions = inference_engine.run_inference(initial_facts, chat_san_pham)
        if result: 
            st.subheader(f"Có thể tạo ra {chat_san_pham} từ các chất ban đầu.")
            st.write(f"Số phương trình hóa học phù hợp: {len(reactions)}")
            st.write(f"Chất tham gia: {', '.join(initial_facts)}")
            st.write("Thứ tự các phản ứng:")
            
            for idx, reaction in enumerate(reactions, 1):

                
                st.markdown(f"""
                           
                <div class="result-box">
                    <div class="result-equation">{idx}. {reaction}</div>
                    <div class="result-inference_engine">
                     
                    </div>
                    <div class="view-inference_engine">
                        <a href="#">> Xem chi tiết</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"Không thể tạo ra {chat_san_pham} từ các chất ban đầu.")
    else:
        st.warning("Vui lòng nhập cả chất tham gia và chất sản phẩm.")