# Bonus — đã dừng theo yêu cầu người dùng

Ngày 08/10/2026, người dùng quyết định nộp phần đã hoàn thành và dừng chạy bonus.
Phần bắt buộc NB0–NB4 có notebook output, metrics, đánh giá và báo cáo thực nghiệm thật.

## Công việc bonus đã làm được

- Chuẩn bị notebook Colab resume và Kaggle cho NB3b (5 loss), NB5 (GGUF), NB6 (benchmark), NB7 (GRPO) và beta-sweep.
- Khôi phục SFT/DPO trên Kaggle từ checkpoint; checksum trọng số khớp bản gốc.
- Lượt DPO bonus tương tác chạy tới bước 21/38 rồi bị timeout. Không có kết quả đánh giá bonus hoàn chỉnh để báo cáo.
- Notebook lưu bằng chứng sau từng biến thể, xuất GGUF qua vùng tạm, tạo biểu đồ smoke test từ output và hỗ trợ checkpoint ZIP, BIN hoặc thư mục đã giải nén.
- Version1 đã hủy do không có log thực thi; Version2 còn chờ GPU khi người dùng yêu cầu dừng. Đã yêu cầu hủy phiên và tạm dừng theo dõi tự động.

## Giới hạn bài nộp

Không nhận NB3b, NB5, NB6, NB7, beta-sweep, chấm chéo API hoặc HF Hub đã hoàn thành.
Notebook bonus là mã chuẩn bị để chạy tiếp, không phải bằng chứng kết quả.
Checkpoint lớn lưu riêng, không commit vào Git. Phần bắt buộc và kết quả của nó được giữ nguyên.

Notebook Kaggle: https://www.kaggle.com/code/anhnguynv/lab22-nguyenvuanh-bonus/edit
