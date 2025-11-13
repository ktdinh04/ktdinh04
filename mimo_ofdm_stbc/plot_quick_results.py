"""
Script vẽ đồ thị kết quả mô phỏng nhanh
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Sử dụng backend không cần GUI
import matplotlib.pyplot as plt
import pickle


def plot_ber_quick(results, save_path='ber_plot_quick.png'):
    """
    Vẽ đồ thị BER theo Eb/N0

    Args:
        results: Dictionary chứa kết quả mô phỏng
        save_path: Đường dẫn lưu hình ảnh
    """
    ebn0_db = results['ebn0_db']
    ber = results['ber']

    # Thay thế BER = 0 bằng giá trị rất nhỏ để hiển thị trên log scale
    ber_plot = [b if b > 0 else 1e-6 for b in ber]

    plt.figure(figsize=(12, 8))

    # Vẽ BER
    plt.semilogy(ebn0_db, ber_plot, 'b-o', linewidth=2.5, markersize=10,
                 label='BER (Simulation)', markerfacecolor='white', markeredgewidth=2)

    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.xlabel('Eb/N0 (dB)', fontsize=14, fontweight='bold')
    plt.ylabel('Bit Error Rate (BER)', fontsize=14, fontweight='bold')
    plt.title('BER vs Eb/N0\n2x2 MIMO-OFDM-STBC, 64-QAM, Rayleigh Channel',
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='best')
    plt.xlim([min(ebn0_db) - 1, max(ebn0_db) + 1])
    plt.ylim([1e-6, 1])

    # Thêm lưới phụ
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', alpha=0.3)

    # Thêm thông tin cấu hình
    info_text = "Configuration:\n" \
                "• Antennas: 2 Tx × 2 Rx\n" \
                "• Modulation: 64-QAM\n" \
                "• OFDM: 64 subcarriers\n" \
                "• FFT Size: 64, CP: 16\n" \
                "• STBC: Alamouti Code\n" \
                "• Channel: Rayleigh Fading + AWGN"

    plt.text(0.98, 0.97, info_text,
             transform=plt.gca().transAxes,
             fontsize=11,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Đồ thị BER đã được lưu vào: {save_path}")

    return save_path


def print_results_table(results):
    """
    In bảng kết quả BER

    Args:
        results: Dictionary chứa kết quả mô phỏng
    """
    ebn0_db = results['ebn0_db']
    ber = results['ber']

    print("\n" + "=" * 50)
    print("KẾT QUẢ MÔ PHỎNG HỆ THỐNG 2x2 MIMO-OFDM-STBC")
    print("=" * 50)
    print(f"{'Eb/N0 (dB)':<15} {'BER':<20}")
    print("-" * 50)

    for i in range(len(ebn0_db)):
        print(f"{ebn0_db[i]:<15} {ber[i]:<20.6e}")

    print("=" * 50)


if __name__ == '__main__':
    # Load kết quả mô phỏng
    try:
        with open('simulation_results_quick.pkl', 'rb') as f:
            results = pickle.load(f)

        # In bảng kết quả
        print_results_table(results)

        # Vẽ đồ thị
        plot_path = plot_ber_quick(results)

        print(f"\n✓ Hoàn tất! Xem kết quả tại: {plot_path}")

    except FileNotFoundError:
        print("Không tìm thấy file 'simulation_results_quick.pkl'")
        print("Vui lòng chạy simulation_quick.py trước!")
