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
├── config.py           # Cấu hình tham số hệ thống
├── modulation.py       # Điều chế/giải điều chế 64-QAM
├── ofdm.py            # OFDM modulation/demodulation
├── stbc.py            # STBC Alamouti encoding/decoding
├── channel.py         # Mô hình kênh Rayleigh và AWGN
├── simulation.py      # Script mô phỏng chính
├── plot_results.py    # Vẽ đồ thị kết quả
├── requirements.txt   # Các thư viện cần thiết
└── README.md          # File này
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
