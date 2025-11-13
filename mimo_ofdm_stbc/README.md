# Mô phỏng hệ thống 2x2 MIMO-OFDM-STBC

## Giới thiệu

Dự án này mô phỏng một hệ thống thông tin vô tuyến **2x2 MIMO-OFDM** sử dụng **Space-Time Block Code (STBC) Alamouti** với điều chế **64-QAM** trên kênh truyền **Rayleigh fading** và nhiễu trắng **AWGN**.

## Đặc điểm hệ thống

- **Số anten phát (Tx):** 2
- **Số anten thu (Rx):** 2
- **Điều chế:** 64-QAM (6 bits/symbol)
- **OFDM:**
  - Số sóng mang con: 64
  - Kích thước FFT: 64
  - Độ dài Cyclic Prefix: 16
- **STBC:** Mã Alamouti (tốc độ mã = 1)
- **Kênh truyền:** Rayleigh flat fading
- **Nhiễu:** Additive White Gaussian Noise (AWGN)

## Cấu trúc thư mục

```
mimo_ofdm_stbc/
├── config.py                  # Cấu hình tham số hệ thống
├── modulation.py              # Điều chế/giải điều chế 64-QAM
├── ofdm.py                   # OFDM modulation/demodulation
├── stbc.py                   # STBC Alamouti encoding/decoding
├── channel.py                # Mô hình kênh Rayleigh và AWGN
├── theoretical_performance.py # Công thức BER/SER lý thuyết
├── simulation.py             # Script mô phỏng chính (đầy đủ)
├── simulation_quick.py       # Script mô phỏng nhanh (demo)
├── plot_results.py           # Vẽ đồ thị kết quả cơ bản
├── plot_comparison.py        # Vẽ đồ thị so sánh mô phỏng vs lý thuyết
├── test_modules.py           # Test suite cho tất cả modules
├── requirements.txt          # Các thư viện cần thiết
└── README.md                 # File này
```

## Cài đặt

### Yêu cầu

- Python 3.7 trở lên
- Các thư viện Python (xem `requirements.txt`)

### Cài đặt thư viện

```bash
pip install -r requirements.txt
```

## Sử dụng

### 1. Chạy mô phỏng

```bash
cd mimo_ofdm_stbc
python simulation.py
```

Mô phỏng sẽ:
- Tạo dữ liệu ngẫu nhiên
- Điều chế 64-QAM
- Mã hóa STBC Alamouti
- Điều chế OFDM
- Truyền qua kênh Rayleigh fading + AWGN
- Giải điều chế OFDM
- Giải mã STBC
- Giải điều chế 64-QAM
- Tính toán BER và SER

Kết quả sẽ được lưu vào file `simulation_results.pkl`.

### 2. Vẽ đồ thị kết quả

```bash
python plot_results.py
```

Script này sẽ:
- Đọc kết quả từ `simulation_results.pkl`
- In bảng kết quả BER và SER
- Vẽ đồ thị BER vs Eb/N0
- Vẽ đồ thị SER vs Eb/N0
- Lưu đồ thị vào các file PNG

## Kết quả đánh giá

Hệ thống được đánh giá qua hai chỉ số chính:

### 1. Bit Error Rate (BER)
- Tỷ lệ lỗi bit nhận được so với bit đã phát
- Được tính theo: BER = (Số bit lỗi) / (Tổng số bit)

### 2. Symbol Error Rate (SER)
- Tỷ lệ lỗi symbol nhận được so với symbol đã phát
- Được tính theo: SER = (Số symbol lỗi) / (Tổng số symbol)

### 3. So sánh kết quả mô phỏng và lý thuyết

Để xem so sánh chi tiết giữa kết quả mô phỏng và lý thuyết:

```bash
python plot_comparison.py
```

Script này sẽ tạo 3 đồ thị:
1. **ber_comparison.png** - So sánh BER mô phỏng vs lý thuyết
2. **ser_comparison.png** - So sánh SER mô phỏng vs lý thuyết
3. **ber_ser_combined.png** - Đồ thị kết hợp BER & SER

### 4. Kết quả mô phỏng thực tế

Kết quả từ mô phỏng nhanh (20 frames/SNR):

| Eb/N0 (dB) | BER (Mô phỏng) | BER (Lý thuyết) | SER (Mô phỏng) | SER (Lý thuyết) |
|------------|----------------|-----------------|----------------|-----------------|
| 0          | 2.21e-01       | 1.02e-02        | 6.58e-01       | 7.68e-02        |
| 5          | 9.35e-02       | 1.25e-03        | 3.16e-01       | 2.55e-01        |
| 10         | 1.65e-02       | 1.34e-04        | 6.09e-02       | 2.50e-01        |
| 15         | 1.30e-04       | 1.37e-05        | 7.81e-04       | 7.00e-02        |
| 20         | 0.00e+00       | 1.38e-06        | 0.00e+00       | 9.86e-03        |
| 25         | 0.00e+00       | 1.39e-07        | 0.00e+00       | 1.09e-03        |

**Nhận xét:**
- Tại **Eb/N0 = 10 dB**: BER ≈ 1.65%, SER ≈ 6.09% - Hệ thống hoạt động khá tốt
- Tại **Eb/N0 = 15 dB**: BER ≈ 0.013%, SER ≈ 0.078% - Hiệu năng rất tốt
- Tại **Eb/N0 ≥ 20 dB**: Không có lỗi (với 20 frames)
- Mã STBC Alamouti cung cấp **diversity order = 2**, cải thiện đáng kể hiệu năng

## Mô tả thuật toán

### STBC Alamouti

Mã Alamouti cho 2 anten phát:

```
Time slot 1:  [s0,  s1]
Time slot 2:  [-s1*, s0*]
```

Ưu điểm:
- Tốc độ mã = 1 (full rate)
- Đạt được diversity order = 2
- Giải mã đơn giản (tuyến tính)

### OFDM

- Sử dụng IFFT để chuyển từ miền tần số sang miền thời gian
- Thêm Cyclic Prefix để chống ISI (Inter-Symbol Interference)
- Sử dụng FFT để giải điều chế

### Kênh Rayleigh

- Mô hình fading phù hợp với môi trường đô thị
- Hệ số kênh tuân theo phân phối Rayleigh
- Flat fading (kênh không chọn lọc tần số)

## Tùy chỉnh

Để thay đổi tham số mô phỏng, chỉnh sửa file `config.py`:

```python
# Ví dụ: Thay đổi khoảng Eb/N0
EBN0_DB_RANGE = range(0, 31, 2)  # 0 đến 30 dB, bước 2 dB

# Thay đổi số frame mô phỏng
N_FRAMES = 100  # Càng nhiều frame, kết quả càng chính xác
```

## Lý thuyết

### Mối quan hệ giữa Eb/N0 và SNR

```
SNR (dB) = Eb/N0 (dB) + 10*log10(bits_per_symbol * code_rate)
```

Với 64-QAM: `bits_per_symbol = 6`

### Công thức tính BER

BER được ước lượng thông qua mô phỏng Monte Carlo:

```
BER = (Tổng số bit lỗi) / (Tổng số bit đã truyền)
```

## Tài liệu tham khảo

1. S. M. Alamouti, "A simple transmit diversity technique for wireless communications," IEEE Journal on Selected Areas in Communications, 1998.
2. A. F. Molisch, "Wireless Communications," 2nd Edition, Wiley-IEEE Press, 2011.
3. Andrea Goldsmith, "Wireless Communications," Cambridge University Press, 2005.

## Tác giả

Mô phỏng được phát triển cho mục đích học tập và nghiên cứu về hệ thống MIMO-OFDM-STBC.

## License

MIT License
