# Bộ bài Lab22 — Nguyễn Vũ Anh · 2A202602502

Phần bắt buộc NB0–NB4 đã chạy trên Colab T4. Xem submission/REFLECTION.md, notebook thực thi, bốn biểu đồ và data/eval. Không chạy các bonus huấn luyện ORPO/GRPO/benchmark/GGUF.

54 kiểm thử mã nguồn đã qua; verify core đã qua trong Colab. Kết luận thực nghiệm: DPO accuracy preference held-out66%, nhưng điểm thắng quy đổi chất lượng43% theo Llama (CI95%37–48%); không kết luận DPO tốt hơn SFT.

ZIP này chứa source và bằng chứng, không chứa trọng số. Checkpoint bước100 được lưu riêng ở Lab22_checkpoint_100.zip, gồm SFT adapter và DPO checkpoint/optimizer. SFT merged16-bit không được tải về; để sinh lại câu trả lời cần dựng lại bản merged từ đúng SFT adapter. Adapter config trong bộ ZIP được đổi từ đường dẫn Colab sang models/sft-merged để dễ di chuyển; kiểm tra local chạy từ root repo. Cấu hình original được ghi trong RUN_MANIFEST.json, checkpoint gốc vẫn nguyên.

Notebook có output train/eval được tải từ Colab. Các ô báo cáo/verify cuối được đồng bộ từ những lần thực thi Colab sau lần tải notebook, có ảnh verify-colab.png làm bằng chứng. Mã và output thí nghiệm không bị thay bằng số giả.

Nếu nộp bằng repo URL theo rubric: giải nén bộ này vào repo bài cá nhân rồi push, không thêm ZIP checkpoint lớn vào Git thường. Bài chưa được gửi lên LMS hoặc xuất bản GitHub.
