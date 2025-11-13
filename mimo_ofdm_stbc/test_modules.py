"""
Script test các module của hệ thống MIMO-OFDM-STBC
"""

import numpy as np
import sys

from modulation import qam64_modulate, qam64_demodulate, generate_random_bits
from ofdm import ofdm_modulate, ofdm_demodulate
from stbc import alamouti_encode, alamouti_decode
from channel import generate_rayleigh_channel, add_awgn, mimo_channel_apply


def test_qam64():
    """Test điều chế/giải điều chế 64-QAM"""
    print("\n" + "="*60)
    print("TEST 1: Điều chế/Giải điều chế 64-QAM")
    print("="*60)

    # Tạo 12 bits ngẫu nhiên (2 symbols)
    bits = generate_random_bits(12)
    print(f"Bits gốc: {bits}")

    # Điều chế
    symbols = qam64_modulate(bits)
    print(f"Số symbols: {len(symbols)}")
    print(f"Symbols: {symbols}")

    # Giải điều chế
    bits_recovered = qam64_demodulate(symbols)
    print(f"Bits phục hồi: {bits_recovered}")

    # Kiểm tra
    if np.array_equal(bits, bits_recovered):
        print("✓ TEST PASSED: Bits phục hồi chính xác!")
        return True
    else:
        print("✗ TEST FAILED: Bits không khớp!")
        return False


def test_ofdm():
    """Test OFDM modulation/demodulation"""
    print("\n" + "="*60)
    print("TEST 2: OFDM Modulation/Demodulation")
    print("="*60)

    n_fft = 64
    cp_len = 16

    # Tạo symbols ngẫu nhiên
    symbols = np.random.randn(n_fft) + 1j * np.random.randn(n_fft)
    print(f"Số symbols: {len(symbols)}")

    # OFDM modulation
    ofdm_sig = ofdm_modulate(symbols, n_fft, cp_len)
    print(f"Độ dài tín hiệu OFDM: {len(ofdm_sig)} (FFT={n_fft}, CP={cp_len})")

    # OFDM demodulation
    symbols_recovered = ofdm_demodulate(ofdm_sig, n_fft, cp_len)
    print(f"Symbols phục hồi: {len(symbols_recovered)}")

    # Kiểm tra
    error = np.max(np.abs(symbols - symbols_recovered))
    print(f"Lỗi tối đa: {error:.10f}")

    if error < 1e-10:
        print("✓ TEST PASSED: OFDM modulation/demodulation chính xác!")
        return True
    else:
        print("✗ TEST FAILED: OFDM có lỗi lớn!")
        return False


def test_stbc_alamouti():
    """Test STBC Alamouti encoding/decoding"""
    print("\n" + "="*60)
    print("TEST 3: STBC Alamouti Encoding/Decoding")
    print("="*60)

    # Tạo 4 symbols
    symbols = np.array([1+1j, 2-1j, -1+2j, 1-2j])
    print(f"Symbols gốc: {symbols}")

    # Alamouti encoding
    encoded = alamouti_encode(symbols)
    print(f"Ma trận mã hóa shape: {encoded.shape}")
    print(f"Anten 1: {encoded[0, :]}")
    print(f"Anten 2: {encoded[1, :]}")

    # Giả sử kênh đơn giản
    n_rx = 2
    n_tx = 2
    channel = np.ones((n_rx, n_tx), dtype=complex) * 0.7

    # Truyền qua kênh
    received = mimo_channel_apply(encoded, channel)
    print(f"Tín hiệu nhận shape: {received.shape}")

    # Alamouti decoding
    symbols_decoded = alamouti_decode(received, channel)
    print(f"Symbols giải mã: {symbols_decoded}")

    # Kiểm tra
    # Symbols decoded đã được chuẩn hóa trong decoder
    error = np.max(np.abs(symbols - symbols_decoded))
    print(f"Lỗi tối đa: {error:.6f}")

    if error < 0.01:
        print("✓ TEST PASSED: STBC Alamouti hoạt động tốt!")
        return True
    else:
        print("✗ TEST FAILED: STBC Alamouti có lỗi!")
        return False


def test_channel():
    """Test kênh Rayleigh và AWGN"""
    print("\n" + "="*60)
    print("TEST 4: Kênh Rayleigh và AWGN")
    print("="*60)

    # Tạo kênh Rayleigh
    n_tx = 2
    n_rx = 2
    channel = generate_rayleigh_channel(n_tx, n_rx, n_taps=1)
    print(f"Kênh Rayleigh shape: {channel.shape}")
    print(f"Kênh:\n{channel[:, :, 0]}")

    # Kiểm tra công suất trung bình
    avg_power = np.mean(np.abs(channel)**2)
    print(f"Công suất trung bình: {avg_power:.4f} (lý thuyết: 1.0)")

    # Test AWGN
    signal = np.ones(1000, dtype=complex)
    snr_db = 10
    noisy_signal, noise = add_awgn(signal, snr_db)

    signal_power = np.mean(np.abs(signal)**2)
    noise_power = np.mean(np.abs(noise)**2)
    snr_measured = 10 * np.log10(signal_power / noise_power)

    print(f"\nTín hiệu gốc power: {signal_power:.4f}")
    print(f"Noise power: {noise_power:.6f}")
    print(f"SNR đặt: {snr_db} dB")
    print(f"SNR đo được: {snr_measured:.2f} dB")

    if abs(snr_measured - snr_db) < 1.0:
        print("✓ TEST PASSED: Kênh và nhiễu hoạt động tốt!")
        return True
    else:
        print("✗ TEST FAILED: SNR không khớp!")
        return False


def test_end_to_end():
    """Test end-to-end hệ thống đơn giản"""
    print("\n" + "="*60)
    print("TEST 5: End-to-End System Test")
    print("="*60)

    # Tham số
    n_bits = 24  # 4 symbols * 6 bits
    n_tx = 2
    n_rx = 2
    snr_db = 20

    # 1. Tạo bits
    tx_bits = generate_random_bits(n_bits)
    print(f"Phát {n_bits} bits")

    # 2. Điều chế 64-QAM
    tx_symbols = qam64_modulate(tx_bits)
    print(f"Điều chế thành {len(tx_symbols)} symbols")

    # 3. STBC encoding
    stbc_encoded = alamouti_encode(tx_symbols)
    print(f"STBC encoded: {stbc_encoded.shape}")

    # 4. Kênh Rayleigh
    channel = generate_rayleigh_channel(n_tx, n_rx, n_taps=1)[:, :, 0]

    # 5. Truyền qua kênh
    received = mimo_channel_apply(stbc_encoded, channel)

    # 6. Thêm nhiễu
    rx_noisy = np.zeros_like(received)
    for i in range(n_rx):
        rx_noisy[i, :], _ = add_awgn(received[i, :], snr_db)

    # 7. STBC decoding
    rx_symbols = alamouti_decode(rx_noisy, channel)
    rx_symbols = rx_symbols[:len(tx_symbols)]

    # 8. Giải điều chế
    rx_bits = qam64_demodulate(rx_symbols)
    rx_bits = rx_bits[:len(tx_bits)]

    # 9. Tính BER
    n_errors = np.sum(tx_bits != rx_bits)
    ber = n_errors / len(tx_bits)

    print(f"\nBits lỗi: {n_errors}/{len(tx_bits)}")
    print(f"BER: {ber:.6f}")

    if ber < 0.5:  # Ngưỡng khá lỏng cho test
        print("✓ TEST PASSED: Hệ thống hoạt động end-to-end!")
        return True
    else:
        print("✗ TEST FAILED: BER quá cao!")
        return False


if __name__ == '__main__':
    print("\n" + "="*60)
    print("BẮT ĐẦU KIỂM TRA CÁC MODULE")
    print("="*60)

    results = []

    # Chạy các test
    results.append(("QAM-64", test_qam64()))
    results.append(("OFDM", test_ofdm()))
    results.append(("STBC Alamouti", test_stbc_alamouti()))
    results.append(("Channel", test_channel()))
    results.append(("End-to-End", test_end_to_end()))

    # Tổng kết
    print("\n" + "="*60)
    print("TỔNG KẾT KẾT QUẢ TEST")
    print("="*60)

    passed = 0
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name:<20} {status}")
        if result:
            passed += 1

    print("-"*60)
    print(f"Tổng: {passed}/{len(results)} tests passed")
    print("="*60)

    sys.exit(0 if passed == len(results) else 1)
