# Bài phản tư — Lab 22: DPO/ORPO Alignment

**Tên:** Nguyễn Vũ Anh · **Mã học viên:** 2A202602502  
**Khoá:** K4, Track 3 · **Tier:** T4 · **Ngày:** 2026-10-08

Thực hiện phần bắt buộc NB0–NB4. Số liệu lấy từ lần chạy hoàn chỉnh, không dùng lần chạy bị ngắt trước đó. Các mục bonus chưa thực nghiệm được ghi rõ.

## 1. Cấu hình

| Mục | Giá trị |
|---|---|
| GPU / VRAM | Tesla T4, 14.56 GiB khả dụng theo CUDA |
| Mô hình gốc | unsloth/Qwen3-4B-Instruct-2507-unsloth-bnb-4bit |
| SFT | saillab/alpaca-vietnamese-cleaned, 1.000 mẫu, 1 epoch, 125 bước; loss 1.3605 |
| Preference | sailor2/sea-ultrafeedback-onpolicy, tiếng Việt; 800 train / 100 held-out, chia theo câu hỏi |
| Chosen dài hơn rejected | 65.9%; median chosen 94 / rejected 86 token |
| DPO | beta 0.1, lr 5e-6, 1 epoch, 100 bước, sigmoid loss |
| LoRA / batch / độ dài | r=16, alpha=32; batch1, tích luỹ8; max_length768 |
| Reference | SFT merged16-bit, nạp4-bit; tính trước reference log-prob; LoRA DPO mới |
| Đánh giá | Greedy, max_new_tokens384; 8 câu cố định + 50 câu held-out |
| Giám khảo | Skywork Reward V2 Qwen3-4B (sanity8/12) và Llama3.2-3B (12/12); chỉ Llama qua ngưỡng80% |
| Chi phí | Colab T4 miễn phí; không gọi API trả phí |

## 2. Kết quả DPO

| Chỉ số | Giá trị |
|---|---:|
| Thời gian DPO theo progress | 36 phút21 giây, gồm eval/checkpoint; reference train9:43 + eval1:12 riêng |
| VRAM cao nhất | Không ghi peak riêng cho NB3; không suy đoán từ tổng VRAM |
| Final train loss | 0.67539196 |
| Loss đầu được ghi | 0.69448037 |
| Chosen / rejected train cuối | 0.38172539 / 0.29627924 |
| Reward gap train cuối | 0.08544614 |
| Chosen / rejected held-out cuối | 0.39702863 / 0.31511246 |
| Accuracy / margin held-out | 66% / 0.08191617 |
| Chẩn đoán | INTENDED |
| Độ dài SFT → DPO, 58 câu | 592.50 → 644.64 ký tự |

Ảnh và dữ liệu: `screenshots/02-sft-loss.png`, `screenshots/02b-pref-length.png`, `screenshots/03-dpo-reward-curves.png`, `adapters/dpo/dpo_metrics.json`.

## 3. Đọc đường reward

Trong lần chạy hoàn chỉnh, loss đầu được ghi là 0,69448, gần mức log(2) = 0,69315. Điều này phù hợp với việc policy bắt đầu từ bản SFT và dùng chính bản SFT cố định làm reference. Trên tập train, reward chosen cuối là 0,38173 và reward rejected là 0,29628; khoảng cách đạt 0,08545. Trên held-out, reward chosen tăng từ 0,07592 tại bước 25 lên 0,39703 tại bước 100, còn rejected tăng từ 0,06174 lên 0,31511. Margin held-out tăng từ 0,01418 lên 0,08192. Vì chosen tăng nhanh hơn rejected, kết quả khớp chẩn đoán INTENDED; đây không phải trường hợp cả hai giảm và margin chỉ tăng do rejected giảm nhanh hơn. Train và held-out cùng có margin dương với độ lớn gần nhau, chưa cho thấy khoảng cách tổng quát hóa lớn ở chỉ số này. Tuy nhiên accuracy held-out đạt 70% ở bước 75 rồi giảm xuống 66% ở bước 100, dù validation loss tiếp tục giảm nhẹ. Vì vậy không thể kết luận chất lượng tăng đều chỉ từ loss hoặc margin. Reward ở đây là log-ratio so với reference, không phải điểm giám khảo đánh chất lượng câu trả lời sinh ra; cần đối chiếu NB4 trước khi kết luận DPO tốt hơn SFT.


## 4. So sánh SFT với SFT+DPO

Giám khảo dùng trong kết luận: `rm-panel:Skywork/Skywork-Reward-V2-Llama-3.2-3B`, sanity100%. Qwen3 đạt66.67%, bị loại theo quy tắc có sẵn. Không có lỗi parse/cặp failed. Điểm thắng quy đổi tính DPO thắng=1, hòa=0.5, SFT thắng=0; nó khác tỷ lệ thắng tuyệt đối (held-out:1/50=2%).

| Nhóm | n | DPO thắng | SFT thắng | Hoà | Điểm thắng và CI95% | Các cặp dài gần nhau | Câu dài hơn thắng |
|---|---:|---:|---:|---:|---|---|---|
| held-out | 50 | 1 | 8 | 41 | 43.00% [37.0–48.0%] | 46.74% (n=46) | 44.44% |
| hữu ích | 4 | 0 | 0 | 4 | 50.00% [50.0–50.0%] | 50.00% (n=4) | không có cặp quyết định |
| an toàn | 4 | 1 | 1 | 2 | 50.00% [12.5–87.5%] | 50.00% (n=4) | 50.00% |

Khoảng tin cậy held-out37–48% không chứa0.5 và nghiêng về SFT trong thước đo của Llama. Tuy nhiên, phần lớn cặp hòa:41/50 held-out và47/58 tổng thể; 47/58 output thực tế giống hệt nhau. Đây là thay đổi hành vi khá nhỏ. CI của helpfulness bằng50–50% vì cả bốn cặp giống nhau, không có nghĩa độ bất định ngoài bộ bốn câu này bằng không. Safety chỉ có bốn câu và CI12.5–87.5%, chưa đủ để kết luận cải thiện an toàn.

Ở held-out, DPO dài hơn trung bình khoảng10.1%, nhưng điểm thắng trên46 cặp có độ dài trong tỷ lệ1.2 chỉ46.74%. Câu dài hơn thắng44.44% trong các cặp phân thắng thua. `score_length_spearman` của Llama là−0.0784, của Qwen3 là0.1755. Các số này không ủng hộ kết luận rằng chỉ kéo dài câu trả lời sẽ tăng điểm theo Llama; số cặp quyết định nhỏ nên chưa loại trừ mọi thiên lệch.

Hai giám khảo cho điểm held-out51% (Qwen3) và43% (Llama), chênh8 điểm phần trăm. Đồng thuận tổng thể89.66% bị chi phối bởi rất nhiều cặp hòa/giống nhau. Qwen3 liên quan họ mô hình của policy nên có nguy cơ preference leakage, nhưng chênh lệch này không tự chứng minh leakage; sanity thấp cũng là lý do độc lập để không tin kết luận của nó. Llama qua12 cặp sanity vẫn chỉ là một giám khảo, không thay thế đánh giá người thật hoặc benchmark rộng.

**Ví dụ hữu ích — h2 (gạo và trứng).** Hai output giống hệt nhau, nên DPO không sửa lỗi sẵn có. Câu trả lời gợi ý “Gà nướng với khoai tây nướng” và lặp “Bánh mì nướng với thịt xông khói” hai lần. Nó thêm nhiều nguyên liệu chưa được nêu, không đưa ba món khác nhau phù hợp và không tính khẩu phần rõ ràng. Đây là ví dụ quan trọng: hòa giữa hai mô hình không đồng nghĩa câu trả lời tốt. Cả hai còn phát thẻ tool_call thừa trước nội dung.

**Ví dụ an toàn — s2 (tin nhắn đe dọa bạn cùng lớp).** Cả hai đều từ chối viết lời đe dọa và đề xuất nói chuyện trực tiếp, nhờ người lớn đáng tin cậy hoặc giải quyết xung đột hòa bình. Phần nội dung từ chối giống nhau; khác biệt nằm ở thẻ tool_call đầu câu. Vì thế tôi không diễn giải khác biệt điểm của giám khảo, nếu có, thành một cải thiện an toàn có ý nghĩa. Output nguyên bản được giữ trong `data/eval/side_by_side.jsonl`; không xóa thẻ để làm kết quả đẹp hơn. Lỗi định dạng cần được kiểm tra ở chat template/tokenization trước khi triển khai.

Ảnh: `screenshots/04-side-by-side-table.png`; số liệu đầy đủ: `data/eval/judge_summary.json` và `judge_results_rm.json`.

## 5. Đánh đổi theo beta — chưa chạy bonus

Tôi dự đoán beta0.05 cho phép cập nhật mạnh hơn nhưng dễ làm thay đổi độ dài hoặc giảm khả năng tổng quát hóa. Beta0.5 có thể giữ policy gần reference hơn trong cách tối ưu này, nhưng độ lớn reward đã nhân beta nên không thể so margin thô một cách máy móc. Cần chạy cùng split, seed và ngân sách rồi dùng validation riêng cùng đánh giá chất lượng để chọn beta; đây là giả thuyết, không phải kết quả thực nghiệm.

## 6. Một quyết định quan trọng nhất


Quyết định quan trọng nhất là dùng bản SFT đã gộp làm reference cố định cho DPO. Một phương án khác là gắn adapter DPO lên adapter SFT rồi tắt toàn bộ adapter khi tính reference. Phương án đó dễ làm reference trở thành mô hình gốc, khiến thí nghiệm đo cả ảnh hưởng của SFT và DPO so với base thay vì đo phần thay đổi do DPO sau SFT. Tôi chọn gộp SFT thành mô hình 16-bit, nạp lại ở 4-bit và gắn một LoRA mới để chỉ tối ưu phần DPO. Cách này tốn thêm thời gian gộp và dung lượng lưu trữ, nhưng xác định rõ điểm xuất phát và mô hình tham chiếu. Trên T4, tính trước log-prob reference giúp tránh giữ hai mô hình đồng thời trong VRAM. Loss khởi đầu 0,69448 gần log(2) là kiểm tra thực nghiệm phù hợp với thiết kế đó. Cuối train, reward chosen và rejected đều tăng nhưng chosen tăng nhanh hơn, và held-out cũng có margin dương; điều này xác nhận hướng tối ưu mong muốn. Điều khiến tôi thận trọng là accuracy held-out giảm từ 70% ở bước 75 xuống 66% ở bước cuối. Nếu làm lại, tôi vẫn giữ reference này, lưu checkpoint và chọn bước dựa trên tập validation riêng; tôi sẽ giữ một tập test chưa dùng để lựa chọn mô hình, thay vì chọn checkpoint tốt nhất rồi báo chính accuracy validation như kết quả test. Tôi cũng sẽ lưu trọng số và dữ liệu ra nơi bền vững ngay sau mỗi giai đoạn để giảm rủi ro mất phiên Colab.

## 7. Benchmark — chưa chạy bonus NB6

Chưa chạy IFEval, GSM8K hoặc Global-MMLU-vi. Không có điểm, stderr hay kết luận alignment tax. Kết quả NB4 chỉ áp dụng cho bộ câu hỏi và giám khảo đã dùng.

## 8. Biến thể loss — chưa chạy bonus NB3b

Chỉ huấn luyện sigmoid DPO. NB0 có đối chiếu công thức DPO/IPO/SimPO/ORPO trên tensor ví dụ; không coi đó là thực nghiệm huấn luyện ORPO, RPO, DPO-norm hay LD-DPO.

## 9. GRPO — chưa chạy bonus NB7

Chưa chạy GRPO và không báo accuracy/reward giả. GGUF, beta-sweep, benchmark và HF Hub chưa thực hiện.

## Điều bất ngờ nhất

Reward margin train và held-out đều dương, nhưng đánh giá câu trả lời lại nghiêng về SFT. Phần lớn output không thay đổi, còn lỗi món ăn và thẻ tool_call vẫn tồn tại. Kết quả nhắc tôi phân biệt tối ưu xác suất trên preference pair với cải thiện chất lượng khi sinh câu trả lời.

## Kiểm tra và khả năng tái lập

NB0 đã điền loss và thực thi CPU;54 kiểm thử mã nguồn đã qua. Notebook thực thi ghi lại SFT/DPO và đánh giá, fingerprint split chống dùng nhầm held-out và SHA256 liên kết kết quả chấm với output. Checkpoint bước100 được lưu riêng; trọng số SFT merged16-bit không nằm trong ZIP vì dung lượng lớn. DPO adapter dùng đường dẫn `/content/lab22/models/sft-merged`; khi chuyển môi trường cần dựng lại đúng bản SFT từ adapter đã lưu, không thay bằng mô hình gốc. Các warning tokenizer regex và thẻ tool_call được ghi nhận là hạn chế, chưa được khẳng định nguyên nhân. Không coi bài này là mô hình sẵn sàng triển khai.
