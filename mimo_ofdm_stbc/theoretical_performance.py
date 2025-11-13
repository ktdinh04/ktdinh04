"""
Công thức tính hiệu năng lý thuyết cho hệ thống MIMO-OFDM-STBC
"""

import numpy as np
from scipy.special import erfc, comb


def ber_64qam_awgn(ebn0_db):
    """
    Tính BER lý thuyết cho 64-QAM trên kênh AWGN

    Args:
        ebn0_db: Eb/N0 tính bằng dB (có thể là array)

    Returns:
        ber: Bit Error Rate lý thuyết
    """
    # Chuyển Eb/N0 từ dB sang linear
    ebn0_linear = 10**(ebn0_db / 10)

    # Cho 64-QAM, M = 64, k = log2(M) = 6 bits/symbol
    M = 64
    k = 6

    # Es/N0 = k * Eb/N0
    esn0_linear = k * ebn0_linear

    # BER xấp xỉ cho M-QAM (Square QAM)
    # BER ≈ (4/k) * (1 - 1/sqrt(M)) * Q(sqrt(3*k*Eb/N0 / (M-1)))
    # Q(x) = 0.5 * erfc(x/sqrt(2))

    sqrt_M = np.sqrt(M)

    # Tính argument cho Q function
    arg = np.sqrt(3 * esn0_linear / (M - 1))

    # Q function
    Q = 0.5 * erfc(arg / np.sqrt(2))

    # BER approximation
    ber = (4 / k) * (1 - 1/sqrt_M) * Q

    return ber


def ber_64qam_rayleigh_diversity(ebn0_db, diversity_order=2):
    """
    Tính BER lý thuyết cho 64-QAM trên kênh Rayleigh fading với diversity

    Args:
        ebn0_db: Eb/N0 tính bằng dB (có thể là array)
        diversity_order: Bậc diversity (2 cho STBC Alamouti 2x2)

    Returns:
        ber: Bit Error Rate lý thuyết
    """
    # Chuyển Eb/N0 từ dB sang linear
    ebn0_linear = 10**(ebn0_db / 10)

    M = 64
    k = 6  # bits per symbol

    # Es/N0
    esn0_linear = k * ebn0_linear

    # Cho Rayleigh fading với diversity, sử dụng công thức xấp xỉ
    # BER ≈ [p * (1-p)]^L * sum_{i=0}^{L-1} C(L-1+i, i) * p^i
    # với p = probability tại high SNR

    # Một công thức xấp xỉ đơn giản hơn cho high SNR:
    # BER ≈ (c / gamma_avg)^L * constant
    # với L = diversity order

    # Sử dụng upper bound cho M-QAM trên Rayleigh với MRC diversity:
    L = diversity_order

    # Probability constant cho 64-QAM
    sqrt_M = np.sqrt(M)
    a = 3 / (M - 1)  # Normalization factor

    # Cho Rayleigh fading với MRC diversity (L antennas)
    # Average BER
    ber = np.zeros_like(ebn0_linear, dtype=float)

    for idx, gamma_b in enumerate(np.atleast_1d(ebn0_linear)):
        # Gamma tính theo symbol
        gamma_s = k * gamma_b

        # Xấp xỉ cho high SNR với diversity
        # BER ≈ (1 / (4 * gamma_s))^L * C(2L-1, L)

        if gamma_s > 0:
            # Công thức xấp xỉ tốt hơn cho 64-QAM Rayleigh với diversity
            p = 1 / (1 + a * gamma_s / L)

            # MRC diversity combination
            ber_sum = 0
            for i in range(L):
                ber_sum += comb(L - 1 + i, i) * (p ** i)

            ber_val = ((1 - p) ** L) * p ** L * ber_sum

            # Điều chỉnh cho 64-QAM
            ber_val = (4 / k) * (1 - 1/sqrt_M) * ber_val

            ber[idx] = ber_val if ber_val > 1e-10 else 1e-10
        else:
            ber[idx] = 0.5

    return ber


def ber_64qam_rayleigh_diversity_simplified(ebn0_db, diversity_order=2):
    """
    Công thức đơn giản hóa cho BER của 64-QAM trên Rayleigh với diversity
    Sử dụng asymptotic approximation tại high SNR

    Args:
        ebn0_db: Eb/N0 tính bằng dB
        diversity_order: Bậc diversity

    Returns:
        ber: Bit Error Rate
    """
    ebn0_linear = 10**(ebn0_db / 10)

    M = 64
    k = 6
    L = diversity_order

    # Es/N0
    gamma_s = k * ebn0_linear

    # Asymptotic approximation cho high SNR
    # BER ≈ G_c / (gamma_s)^L

    # Coding gain cho 64-QAM với STBC
    G_c = 0.5  # Approximate value

    ber = G_c / ((1 + gamma_s) ** L)

    # Clamp to reasonable values
    ber = np.clip(ber, 1e-10, 0.5)

    return ber


def ser_64qam_awgn(ebn0_db):
    """
    Tính SER lý thuyết cho 64-QAM trên kênh AWGN

    Args:
        ebn0_db: Eb/N0 tính bằng dB

    Returns:
        ser: Symbol Error Rate
    """
    ebn0_linear = 10**(ebn0_db / 10)

    M = 64
    k = 6

    # Es/N0
    esn0_linear = k * ebn0_linear

    # SER cho Square M-QAM
    # SER = 1 - (1 - P_L)^2
    # với P_L = 2*(1 - 1/sqrt(M)) * Q(sqrt(3*Es/N0 / (M-1)))

    sqrt_M = np.sqrt(M)

    # Argument cho Q function
    arg = np.sqrt(3 * esn0_linear / (M - 1))

    # Q function
    Q = 0.5 * erfc(arg / np.sqrt(2))

    # Probability of error per dimension
    P_L = 2 * (1 - 1/sqrt_M) * Q

    # SER
    ser = 1 - (1 - P_L) ** 2

    return ser


def ser_64qam_rayleigh_diversity(ebn0_db, diversity_order=2):
    """
    Tính SER lý thuyết cho 64-QAM trên Rayleigh với diversity

    Args:
        ebn0_db: Eb/N0 tính bằng dB
        diversity_order: Bậc diversity

    Returns:
        ser: Symbol Error Rate
    """
    # SER ≈ k * BER cho high order modulation (approximation)
    # Hoặc có thể tính chính xác hơn

    M = 64
    k = 6
    L = diversity_order

    ebn0_linear = 10**(ebn0_db / 10)
    gamma_s = k * ebn0_linear

    # Approximation: SER ≈ 4 * BER for high-order QAM
    ber = ber_64qam_rayleigh_diversity(ebn0_db, diversity_order)
    ser = np.minimum(4 * ber, 1.0)

    return ser


def calculate_theoretical_curves(ebn0_range_db):
    """
    Tính tất cả các đường cong lý thuyết

    Args:
        ebn0_range_db: Array các giá trị Eb/N0 (dB)

    Returns:
        dict chứa các kết quả lý thuyết
    """
    ebn0_array = np.array(ebn0_range_db, dtype=float)

    results = {
        'ebn0_db': ebn0_array,
        'ber_awgn': ber_64qam_awgn(ebn0_array),
        'ber_rayleigh_div2': ber_64qam_rayleigh_diversity(ebn0_array, diversity_order=2),
        'ber_rayleigh_div2_simple': ber_64qam_rayleigh_diversity_simplified(ebn0_array, diversity_order=2),
        'ser_awgn': ser_64qam_awgn(ebn0_array),
        'ser_rayleigh_div2': ser_64qam_rayleigh_diversity(ebn0_array, diversity_order=2),
    }

    return results


if __name__ == '__main__':
    # Test
    ebn0_test = np.arange(0, 26, 1)

    print("Testing theoretical performance calculations...")
    print("\nEb/N0 (dB)  BER (AWGN)  BER (Rayleigh+Div2)")
    print("-" * 50)

    ber_awgn = ber_64qam_awgn(ebn0_test)
    ber_rayleigh = ber_64qam_rayleigh_diversity(ebn0_test, diversity_order=2)

    for i in range(0, len(ebn0_test), 5):
        print(f"{ebn0_test[i]:5.0f}       {ber_awgn[i]:.6e}    {ber_rayleigh[i]:.6e}")

    print("\n✓ Theoretical calculations completed!")
