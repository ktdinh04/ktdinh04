"""
Space-Time Block Code (STBC) - Mã Alamouti cho 2 anten phát
"""

import numpy as np


def alamouti_encode(symbols):
    """
    Mã hóa Alamouti cho 2 anten phát

    Ma trận mã Alamouti:
    Anten 1: [s0,  -s1*]
    Anten 2: [s1,   s0*]

    Args:
        symbols: Các ký tự cần mã hóa (độ dài chẵn)

    Returns:
        encoded: Ma trận mã hóa [2, n_time_slots]
                 encoded[0, :] - tín hiệu cho anten 1
                 encoded[1, :] - tín hiệu cho anten 2
    """
    if len(symbols) % 2 != 0:
        # Padding nếu số symbols lẻ
        symbols = np.concatenate([symbols, [0]])

    n_symbol_pairs = len(symbols) // 2

    # Khởi tạo ma trận mã hóa
    encoded = np.zeros((2, 2 * n_symbol_pairs), dtype=complex)

    for i in range(n_symbol_pairs):
        s0 = symbols[2 * i]
        s1 = symbols[2 * i + 1]

        # Time slot 1
        encoded[0, 2 * i] = s0      # Anten 1: s0
        encoded[1, 2 * i] = s1      # Anten 2: s1

        # Time slot 2
        encoded[0, 2 * i + 1] = -np.conj(s1)  # Anten 1: -s1*
        encoded[1, 2 * i + 1] = np.conj(s0)   # Anten 2: s0*

    return encoded


def alamouti_decode(received, channel):
    """
    Giải mã Alamouti với kênh đã biết

    Args:
        received: Ma trận tín hiệu nhận [n_rx, n_time_slots]
        channel: Ma trận kênh [n_rx, n_tx]
                channel[i, j] = hệ số kênh từ anten phát j đến anten thu i

    Returns:
        symbols: Các ký tự đã giải mã
    """
    n_rx, n_time_slots = received.shape
    n_symbol_pairs = n_time_slots // 2

    symbols = []

    for i in range(n_symbol_pairs):
        # Tín hiệu nhận tại 2 time slots
        r0 = received[:, 2 * i]      # Time slot 1
        r1 = received[:, 2 * i + 1]  # Time slot 2

        # Kết hợp tín hiệu từ tất cả các anten thu
        # Ước lượng s0
        s0_est = 0
        # Ước lượng s1
        s1_est = 0

        for rx_idx in range(n_rx):
            h0 = channel[rx_idx, 0]  # Kênh từ TX1 đến RXi
            h1 = channel[rx_idx, 1]  # Kênh từ TX2 đến RXi

            # Kết hợp tuyến tính tối ưu (Maximum Ratio Combining)
            s0_est += np.conj(h0) * r0[rx_idx] + h1 * np.conj(r1[rx_idx])
            s1_est += np.conj(h1) * r0[rx_idx] - h0 * np.conj(r1[rx_idx])

        # Chuẩn hóa với tổng công suất kênh
        channel_power = np.sum(np.abs(channel)**2)
        s0_est = s0_est / channel_power
        s1_est = s1_est / channel_power

        symbols.append(s0_est)
        symbols.append(s1_est)

    return np.array(symbols)


def alamouti_decode_no_csi(received):
    """
    Giải mã Alamouti không cần CSI (Channel State Information) hoàn hảo
    Sử dụng ước lượng kênh đơn giản

    Args:
        received: Ma trận tín hiệu nhận [n_rx, n_time_slots]

    Returns:
        symbols: Các ký tự đã giải mã
    """
    # Đây là phiên bản đơn giản, trong thực tế cần ước lượng kênh
    # Giả sử kênh đơn giản nhất (all-ones)
    n_rx = received.shape[0]
    n_tx = 2
    channel = np.ones((n_rx, n_tx), dtype=complex)

    return alamouti_decode(received, channel)


def calculate_stbc_rate():
    """
    Tính toán tốc độ mã của STBC Alamouti

    Returns:
        rate: Tốc độ mã (symbols/time_slot)
    """
    # Alamouti: 2 symbols trong 2 time slots
    return 1.0  # Rate = 1 (full rate)
