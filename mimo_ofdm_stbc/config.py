"""
Cấu hình tham số cho hệ thống MIMO-OFDM-STBC
"""

# Tham số hệ thống MIMO
N_TX = 2  # Số anten phát
N_RX = 2  # Số anten thu

# Tham số OFDM
N_SUBCARRIERS = 64  # Số sóng mang con
N_FFT = 64  # Kích thước FFT
CP_LEN = 16  # Độ dài Cyclic Prefix

# Tham số điều chế
MODULATION = '64QAM'
M = 64  # Số mức điều chế
BITS_PER_SYMBOL = 6  # log2(64) = 6 bits

# Tham số mô phỏng
EBN0_DB_RANGE = range(0, 31, 2)  # Eb/N0 từ 0 đến 30 dB
N_FRAMES = 100  # Số frame mô phỏng cho mỗi SNR

# Tham số STBC
STBC_TYPE = 'ALAMOUTI'  # Mã Alamouti cho 2 anten phát

# Tham số kênh truyền
CHANNEL_TYPE = 'RAYLEIGH'  # Kênh Rayleigh fading
NOISE_TYPE = 'AWGN'  # Additive White Gaussian Noise

# Số bits mỗi frame
BITS_PER_FRAME = N_SUBCARRIERS * BITS_PER_SYMBOL
