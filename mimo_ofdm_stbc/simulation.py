"""
Script mô phỏng chính cho hệ thống MIMO-OFDM-STBC
"""

import numpy as np
from tqdm import tqdm
import pickle

from config import *
from modulation import qam64_modulate, qam64_demodulate, generate_random_bits
from ofdm import ofdm_modulate, ofdm_demodulate
from stbc import alamouti_encode, alamouti_decode
from channel import (generate_rayleigh_channel, add_awgn,
                     mimo_channel_apply, calculate_snr_from_ebn0)


def calculate_ber(transmitted_bits, received_bits):
    """
    Tính Bit Error Rate (BER)

    Args:
        transmitted_bits: Bits đã phát
        received_bits: Bits đã nhận

    Returns:
        ber: Bit Error Rate
    """
    n_errors = np.sum(transmitted_bits != received_bits)
    ber = n_errors / len(transmitted_bits)
    return ber


def calculate_ser(transmitted_symbols, received_symbols):
    """
    Tính Symbol Error Rate (SER)

    Args:
        transmitted_symbols: Symbols đã phát
        received_symbols: Symbols đã nhận

    Returns:
        ser: Symbol Error Rate
    """
    n_errors = np.sum(transmitted_symbols != received_symbols)
    ser = n_errors / len(transmitted_symbols)
    return ser


def simulate_mimo_ofdm_stbc_single_frame(ebn0_db):
    """
    Mô phỏng một frame MIMO-OFDM-STBC

    Args:
        ebn0_db: Eb/N0 tính bằng dB

    Returns:
        n_bit_errors: Số lỗi bit
        n_bits: Tổng số bits
        n_symbol_errors: Số lỗi symbol
        n_symbols: Tổng số symbols
    """
    # 1. Tạo bits ngẫu nhiên
    tx_bits = generate_random_bits(BITS_PER_FRAME)

    # 2. Điều chế 64-QAM
    tx_symbols = qam64_modulate(tx_bits)

    # 3. STBC Alamouti encoding
    stbc_encoded = alamouti_encode(tx_symbols)  # [2, n_time_slots]

    # 4. OFDM modulation cho mỗi anten
    n_time_slots = stbc_encoded.shape[1]
    ofdm_signals = []

    for tx_idx in range(N_TX):
        # Chia symbols thành các OFDM symbols
        tx_antenna_symbols = stbc_encoded[tx_idx, :]

        # Pad để đủ N_SUBCARRIERS
        if len(tx_antenna_symbols) < N_SUBCARRIERS:
            padding = np.zeros(N_SUBCARRIERS - len(tx_antenna_symbols))
            tx_antenna_symbols = np.concatenate([tx_antenna_symbols, padding])
        elif len(tx_antenna_symbols) > N_SUBCARRIERS:
            # Chia thành nhiều OFDM symbols
            n_ofdm_syms = int(np.ceil(len(tx_antenna_symbols) / N_SUBCARRIERS))
            padding_len = n_ofdm_syms * N_SUBCARRIERS - len(tx_antenna_symbols)
            tx_antenna_symbols = np.concatenate([tx_antenna_symbols,
                                                 np.zeros(padding_len)])

        # OFDM modulation
        ofdm_sig = ofdm_modulate(tx_antenna_symbols[:N_SUBCARRIERS], N_FFT, CP_LEN)
        ofdm_signals.append(ofdm_sig)

    # Chuyển thành ma trận [N_TX, signal_length]
    tx_signals = np.array(ofdm_signals)

    # 5. Tạo kênh Rayleigh
    channel = generate_rayleigh_channel(N_TX, N_RX, n_taps=1)
    channel = channel[:, :, 0]  # Flat fading [N_RX, N_TX]

    # 6. Áp dụng kênh MIMO
    rx_signals = mimo_channel_apply(tx_signals, channel)

    # 7. Thêm nhiễu AWGN
    snr_db = calculate_snr_from_ebn0(ebn0_db, BITS_PER_SYMBOL)
    rx_signals_noisy = np.zeros_like(rx_signals)

    for rx_idx in range(N_RX):
        rx_signals_noisy[rx_idx, :], _ = add_awgn(rx_signals[rx_idx, :], snr_db)

    # 8. OFDM demodulation cho mỗi anten thu
    rx_symbols_ofdm = []
    for rx_idx in range(N_RX):
        demod_symbols = ofdm_demodulate(rx_signals_noisy[rx_idx, :], N_FFT, CP_LEN)
        rx_symbols_ofdm.append(demod_symbols[:N_SUBCARRIERS])

    # Chuyển thành ma trận [N_RX, N_SUBCARRIERS]
    rx_symbols_matrix = np.array(rx_symbols_ofdm)

    # 9. STBC Alamouti decoding
    # Cần reshape để phù hợp với decoder
    # Decoder expect [N_RX, n_time_slots]
    rx_symbols_reshaped = rx_symbols_matrix[:, :n_time_slots]
    rx_symbols_decoded = alamouti_decode(rx_symbols_reshaped, channel)

    # 10. Giải điều chế 64-QAM
    rx_symbols_decoded = rx_symbols_decoded[:len(tx_symbols)]
    rx_bits = qam64_demodulate(rx_symbols_decoded)

    # 11. Tính BER và SER
    rx_bits = rx_bits[:len(tx_bits)]
    n_bit_errors = np.sum(tx_bits != rx_bits)
    n_bits = len(tx_bits)

    # Để tính SER, cần so sánh symbols
    n_symbol_errors = 0
    n_symbols = len(tx_symbols)
    # Không tính SER chính xác trong trường hợp này vì cần hard decision trên symbols

    return n_bit_errors, n_bits, n_symbol_errors, n_symbols


def run_simulation():
    """
    Chạy mô phỏng hoàn chỉnh cho tất cả các giá trị Eb/N0
    """
    print("=" * 70)
    print("MÔ PHỎNG HỆ THỐNG 2x2 MIMO-OFDM-STBC")
    print("=" * 70)
    print(f"Cấu hình:")
    print(f"  - Số anten phát: {N_TX}")
    print(f"  - Số anten thu: {N_RX}")
    print(f"  - Điều chế: {MODULATION}")
    print(f"  - Số sóng mang con: {N_SUBCARRIERS}")
    print(f"  - Kích thước FFT: {N_FFT}")
    print(f"  - Độ dài CP: {CP_LEN}")
    print(f"  - Mã STBC: {STBC_TYPE}")
    print(f"  - Kênh truyền: {CHANNEL_TYPE} + {NOISE_TYPE}")
    print(f"  - Số frame mỗi SNR: {N_FRAMES}")
    print("=" * 70)

    results = {
        'ebn0_db': [],
        'ber': [],
        'ser': []
    }

    for ebn0_db in tqdm(EBN0_DB_RANGE, desc="Đang mô phỏng"):
        total_bit_errors = 0
        total_bits = 0
        total_symbol_errors = 0
        total_symbols = 0

        for frame_idx in range(N_FRAMES):
            n_bit_errors, n_bits, n_sym_errors, n_syms = \
                simulate_mimo_ofdm_stbc_single_frame(ebn0_db)

            total_bit_errors += n_bit_errors
            total_bits += n_bits
            total_symbol_errors += n_sym_errors
            total_symbols += n_syms

        # Tính BER và SER trung bình
        ber = total_bit_errors / total_bits if total_bits > 0 else 0
        ser = total_symbol_errors / total_symbols if total_symbols > 0 else 0

        results['ebn0_db'].append(ebn0_db)
        results['ber'].append(ber)
        results['ser'].append(ser)

        print(f"\nEb/N0 = {ebn0_db:2d} dB: BER = {ber:.6e}")

    # Lưu kết quả
    with open('simulation_results.pkl', 'wb') as f:
        pickle.dump(results, f)

    print("\n" + "=" * 70)
    print("Mô phỏng hoàn tất! Kết quả đã được lưu vào 'simulation_results.pkl'")
    print("=" * 70)

    return results


if __name__ == '__main__':
    results = run_simulation()
