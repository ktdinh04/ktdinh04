"""
Điều chế và giải điều chế 64-QAM
"""

import numpy as np


def qam64_modulate(bits):
    """
    Điều chế 64-QAM

    Args:
        bits: Mảng bits đầu vào (phải chia hết cho 6)

    Returns:
        symbols: Các ký tự 64-QAM đã được chuẩn hóa
    """
    if len(bits) % 6 != 0:
        raise ValueError("Số bits phải chia hết cho 6 cho điều chế 64-QAM")

    # Constellation points for 64-QAM: [-7, -5, -3, -1, 1, 3, 5, 7]
    # Chuẩn hóa để công suất trung bình = 1
    constellation_1d = np.array([-7, -5, -3, -1, 1, 3, 5, 7])

    # Tính công suất trung bình
    Es = np.mean(constellation_1d**2)
    constellation_1d = constellation_1d / np.sqrt(Es)

    # Reshape bits thành các nhóm 6 bits
    bits_reshaped = bits.reshape(-1, 6)

    symbols = []
    for bit_group in bits_reshaped:
        # 3 bits đầu cho I (in-phase) - chuyển thành index
        i_index = bit_group[0] * 4 + bit_group[1] * 2 + bit_group[2]

        # 3 bits sau cho Q (quadrature) - chuyển thành index
        q_index = bit_group[3] * 4 + bit_group[4] * 2 + bit_group[5]

        # Ánh xạ tuyến tính (không dùng Gray mapping để đơn giản)
        i_val = constellation_1d[i_index]
        q_val = constellation_1d[q_index]

        symbols.append(i_val + 1j * q_val)

    return np.array(symbols)


def qam64_demodulate(symbols):
    """
    Giải điều chế 64-QAM (hard decision)

    Args:
        symbols: Các ký tự nhận được

    Returns:
        bits: Mảng bits ước lượng
    """
    # Bảng constellation đã chuẩn hóa
    constellation_1d = np.array([-7, -5, -3, -1, 1, 3, 5, 7])
    Es = np.mean(constellation_1d**2)
    constellation_1d = constellation_1d / np.sqrt(Es)

    bits = []

    for symbol in symbols:
        # Tách I và Q
        i_val = np.real(symbol)
        q_val = np.imag(symbol)

        # Tìm điểm constellation gần nhất cho I
        i_index = np.argmin(np.abs(constellation_1d - i_val))

        # Tìm điểm constellation gần nhất cho Q
        q_index = np.argmin(np.abs(constellation_1d - q_val))

        # Chuyển index thành 3 bits
        i_bits = [(i_index >> 2) & 1, (i_index >> 1) & 1, i_index & 1]
        q_bits = [(q_index >> 2) & 1, (q_index >> 1) & 1, q_index & 1]

        bits.extend(i_bits + q_bits)

    return np.array(bits, dtype=int)


def generate_random_bits(n_bits):
    """
    Tạo chuỗi bits ngẫu nhiên

    Args:
        n_bits: Số lượng bits cần tạo

    Returns:
        bits: Mảng bits ngẫu nhiên
    """
    return np.random.randint(0, 2, n_bits)
