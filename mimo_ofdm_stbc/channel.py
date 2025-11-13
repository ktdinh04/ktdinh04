"""
Mô hình kênh truyền: Rayleigh Fading và AWGN
"""

import numpy as np


def generate_rayleigh_channel(n_tx, n_rx, n_taps=1):
    """
    Tạo ma trận kênh Rayleigh fading

    Args:
        n_tx: Số anten phát
        n_rx: Số anten thu
        n_taps: Số tap của kênh (1 = flat fading)

    Returns:
        channel: Ma trận kênh phức [n_rx, n_tx, n_taps]
    """
    # Mỗi hệ số kênh là biến ngẫu nhiên phức Gaussian
    # Phần thực và ảo đều tuân theo phân phối Gaussian(0, 0.5)
    # để tổng công suất = 1
    h_real = np.random.randn(n_rx, n_tx, n_taps) / np.sqrt(2)
    h_imag = np.random.randn(n_rx, n_tx, n_taps) / np.sqrt(2)

    channel = h_real + 1j * h_imag

    return channel


def add_awgn(signal, snr_db):
    """
    Thêm nhiễu trắng Gaussian (AWGN)

    Args:
        signal: Tín hiệu đầu vào (có thể là mảng hoặc ma trận)
        snr_db: SNR tính bằng dB

    Returns:
        noisy_signal: Tín hiệu đã thêm nhiễu
        noise: Nhiễu đã thêm vào
    """
    # Tính công suất tín hiệu
    signal_power = np.mean(np.abs(signal)**2)

    # Chuyển SNR từ dB sang tuyến tính
    snr_linear = 10**(snr_db / 10)

    # Tính công suất nhiễu
    noise_power = signal_power / snr_linear

    # Tạo nhiễu phức Gaussian
    if np.iscomplexobj(signal):
        noise = np.sqrt(noise_power / 2) * (np.random.randn(*signal.shape) +
                                            1j * np.random.randn(*signal.shape))
    else:
        noise = np.sqrt(noise_power) * np.random.randn(*signal.shape)

    noisy_signal = signal + noise

    return noisy_signal, noise


def mimo_channel_apply(transmitted, channel):
    """
    Áp dụng kênh MIMO

    Args:
        transmitted: Ma trận tín hiệu phát [n_tx, n_samples]
        channel: Ma trận kênh [n_rx, n_tx]

    Returns:
        received: Ma trận tín hiệu nhận [n_rx, n_samples]
    """
    n_rx, n_tx = channel.shape
    n_samples = transmitted.shape[1]

    # Khởi tạo ma trận tín hiệu nhận
    received = np.zeros((n_rx, n_samples), dtype=complex)

    # Áp dụng kênh: r = H * s
    for i in range(n_rx):
        for j in range(n_tx):
            received[i, :] += channel[i, j] * transmitted[j, :]

    return received


def calculate_snr_from_ebn0(ebn0_db, bits_per_symbol, code_rate=1.0):
    """
    Tính SNR từ Eb/N0

    Args:
        ebn0_db: Eb/N0 tính bằng dB
        bits_per_symbol: Số bits trên mỗi symbol
        code_rate: Tốc độ mã (mặc định = 1 cho uncoded)

    Returns:
        snr_db: SNR tính bằng dB
    """
    # SNR = Eb/N0 + 10*log10(bits_per_symbol * code_rate)
    snr_db = ebn0_db + 10 * np.log10(bits_per_symbol * code_rate)
    return snr_db


def calculate_ebn0_from_snr(snr_db, bits_per_symbol, code_rate=1.0):
    """
    Tính Eb/N0 từ SNR

    Args:
        snr_db: SNR tính bằng dB
        bits_per_symbol: Số bits trên mỗi symbol
        code_rate: Tốc độ mã

    Returns:
        ebn0_db: Eb/N0 tính bằng dB
    """
    ebn0_db = snr_db - 10 * np.log10(bits_per_symbol * code_rate)
    return ebn0_db


def generate_frequency_selective_channel(n_tx, n_rx, n_taps, n_subcarriers):
    """
    Tạo kênh frequency selective cho OFDM

    Args:
        n_tx: Số anten phát
        n_rx: Số anten thu
        n_taps: Số tap của kênh
        n_subcarriers: Số sóng mang con

    Returns:
        channel_freq: Đáp ứng kênh trong miền tần số [n_rx, n_tx, n_subcarriers]
    """
    # Tạo kênh trong miền thời gian
    h_time = generate_rayleigh_channel(n_tx, n_rx, n_taps)

    # Chuyển sang miền tần số bằng FFT
    channel_freq = np.zeros((n_rx, n_tx, n_subcarriers), dtype=complex)

    for rx in range(n_rx):
        for tx in range(n_tx):
            # FFT của impulse response
            channel_freq[rx, tx, :] = np.fft.fft(h_time[rx, tx, :], n_subcarriers)

    return channel_freq
