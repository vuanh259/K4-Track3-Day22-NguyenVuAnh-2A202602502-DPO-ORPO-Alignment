# Bonus — chuẩn bị chạy tiếp, chưa có kết quả

Ngày 2026-10-08, Colab báo không thể cấp GPU vì tài khoản đạt hạn mức sử dụng.
Không có lượt bonus mới nào được huấn luyện hoặc đánh giá. Notebook core và báo cáo
core vẫn là bằng chứng thực nghiệm đã hoàn tất.

Notebook `colab/Lab22_NguyenVuAnh_bonus_resume.ipynb` chuẩn bị NB3b (5 loss), NB5
(GGUF Q4_K_M), NB6 (IFEval, GSM8K, Global-MMLU-vi), NB7 (GRPO) và beta-sweep.
Chạy trên CUDA GPU >=12GB; notebook giữ nguyên ngân sách T4 của source.
Không dùng notebook chưa chạy như bằng chứng đã hoàn tất bonus.

Khôi phục bằng file `Lab22_checkpoint_100.zip` đã lưu trên máy: SFT adapter và DPO
checkpoint-100 có trọng số. Script dựng lại SFT merged từ adapter đã học, sau đó
đặt DPO adapter trên đúng SFT merged; không huấn luyện lại core và không thay
reference bằng base. File checkpoint lớn không nằm trong Git; cần upload file
đó trong ô upload. Kết quả từng mục được tải xuống dưới dạng ZIP metadata/ảnh.
Notebook có output, adapter/GGUF lớn cần lưu riêng trước khi phiên Colab kết thúc.

Các mục bổ sung chấm chéo API, HF Hub và thử thách sản phẩm trong
`BONUS-CHALLENGE.md` chưa thực hiện. Chấm API cần tài khoản/khóa và ngân sách được
chấp thuận; HF Hub cần tài khoản đích. Thử thách sản phẩm riêng cần lựa chọn lĩnh
vực và phán đoán chuyên môn của học viên; không tự nhận dữ liệu AI tạo là dữ liệu
do học viên tự viết.

## Kaggle
Notebook colab/Lab22_NguyenVuAnh_Kaggle_bonus.ipynb đã được import tại https://www.kaggle.com/code/anhnguynv/lab22-nguyenvuanh-bonus/edit . Checkpoint đã được upload vào dataset private và gắn Input. Đã bật T4 x2 và Internet; code dùng CUDA0. Phiên hiện chờ cấp GPU (hàng đợi vị trí 7), chưa có kết quả bonus. Notebook hỗ trợ checkpoint ZIP hoặc thư mục Kaggle tự giải nén, kiểm tra SHA256 trước khi khôi phục.
