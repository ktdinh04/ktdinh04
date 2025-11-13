"""
OFDM Modulation và Demodulation
"""

import numpy as np


def ofdm_modulate(symbols, n_fft, cp_len):
    """
    OFDM Modulation với IFFT và thêm Cyclic Prefix

    Args:
        symbols: Các ký tự điều chế (độ dài = n_fft)
        n_fft: Kích thước FFT
        cp_len: Độ dài Cyclic Prefix

    Returns:
        ofdm_signal: Tín hiệu OFDM trong miền thời gian
    """
    if len(symbols) != n_fft:
        raise ValueError(f"Số symbols ({len(symbols)}) phải bằng n_fft ({n_fft})")

    # IFFT để chuyển từ miền tần số sang miền thời gian
    time_signal = np.fft.ifft(symbols, n_fft)

    # Thêm Cyclic Prefix (sao chép cp_len mẫu cuối lên đầu)
    cyclic_prefix = time_signal[-cp_len:]
    ofdm_signal = np.concatenate([cyclic_prefix, time_signal])

    return ofdm_signal


def ofdm_demodulate(ofdm_signal, n_fft, cp_len):
    """
    OFDM Demodulation: Loại bỏ CP và FFT

    Args:
        ofdm_signal: Tín hiệu OFDM nhận được
        n_fft: Kích thước FFT
        cp_len: Độ dài Cyclic Prefix

    Returns:
        symbols: Các ký tự trong miền tần số
    """
    # Loại bỏ Cyclic Prefix
    time_signal = ofdm_signal[cp_len:]

    # FFT để chuyển từ miền thời gian sang miền tần số
    symbols = np.fft.fft(time_signal, n_fft)

    return symbols


def create_ofdm_frame(symbols, n_fft, cp_len):
    """
    Tạo một frame OFDM từ nhiều symbols

    Args:
        symbols: Mảng symbols (có thể nhiều hơn n_fft)
        n_fft: Kích thước FFT
        cp_len: Độ dài Cyclic Prefix

    Returns:
        ofdm_frame: Frame OFDM hoàn chỉnh
    """
    n_symbols = len(symbols)
    n_ofdm_symbols = int(np.ceil(n_symbols / n_fft))

    # Padding nếu cần thiết
    if n_symbols % n_fft != 0:
        padding_len = n_fft - (n_symbols % n_fft)
        symbols = np.concatenate([symbols, np.zeros(padding_len)])

    # Reshape thành các OFDM symbols
    symbols_reshaped = symbols.reshape(n_ofdm_symbols, n_fft)

    # Điều chế OFDM cho mỗi symbol
    ofdm_frame = []
    for ofdm_symbol in symbols_reshaped:
        ofdm_sig = ofdm_modulate(ofdm_symbol, n_fft, cp_len)
        ofdm_frame.extend(ofdm_sig)

    return np.array(ofdm_frame)


def decode_ofdm_frame(ofdm_frame, n_fft, cp_len, n_ofdm_symbols):
    """
    Giải mã frame OFDM

    Args:
        ofdm_frame: Frame OFDM nhận được
        n_fft: Kích thước FFT
        cp_len: Độ dài Cyclic Prefix
        n_ofdm_symbols: Số lượng OFDM symbols trong frame

    Returns:
        symbols: Các symbols đã giải mã
    """
    ofdm_symbol_len = n_fft + cp_len

    symbols = []
    for i in range(n_ofdm_symbols):
        start_idx = i * ofdm_symbol_len
        end_idx = start_idx + ofdm_symbol_len
        ofdm_sig = ofdm_frame[start_idx:end_idx]

        # Giải điều chế OFDM
        demod_symbols = ofdm_demodulate(ofdm_sig, n_fft, cp_len)
        symbols.extend(demod_symbols)

    return np.array(symbols)
