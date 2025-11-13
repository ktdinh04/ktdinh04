"""
Script vẽ đồ thị kết quả mô phỏng BER và SER
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle


def plot_ber_ser(results, save_path='ber_ser_plot.png'):
    """
    Vẽ đồ thị BER và SER theo Eb/N0

    Args:
        results: Dictionary chứa kết quả mô phỏng
        save_path: Đường dẫn lưu hình ảnh
    """
    ebn0_db = results['ebn0_db']
    ber = results['ber']
    ser = results['ser']

    # Tạo figure với 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Vẽ BER
    ax1.semilogy(ebn0_db, ber, 'b-o', linewidth=2, markersize=8, label='BER (Simulation)')
    ax1.grid(True, which='both', linestyle='--', alpha=0.6)
    ax1.set_xlabel('Eb/N0 (dB)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Bit Error Rate (BER)', fontsize=12, fontweight='bold')
    ax1.set_title('BER vs Eb/N0 - 2x2 MIMO-OFDM-STBC (64-QAM)\nRayleigh Channel',
                  fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.set_xlim([min(ebn0_db), max(ebn0_db)])

    # Thêm lưới phụ
    ax1.minorticks_on()
    ax1.grid(which='minor', linestyle=':', alpha=0.3)

    # Vẽ SER (nếu có dữ liệu)
    if any(ser):
        ax2.semilogy(ebn0_db, ser, 'r-s', linewidth=2, markersize=8, label='SER (Simulation)')
    else:
        # Nếu không có SER, vẽ BER để so sánh
        ax2.semilogy(ebn0_db, ber, 'b-o', linewidth=2, markersize=8, label='BER')

    ax2.grid(True, which='both', linestyle='--', alpha=0.6)
    ax2.set_xlabel('Eb/N0 (dB)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Symbol Error Rate (SER)', fontsize=12, fontweight='bold')
    ax2.set_title('SER vs Eb/N0 - 2x2 MIMO-OFDM-STBC (64-QAM)\nRayleigh Channel',
                  fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.set_xlim([min(ebn0_db), max(ebn0_db)])

    # Thêm lưới phụ
    ax2.minorticks_on()
    ax2.grid(which='minor', linestyle=':', alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Đồ thị đã được lưu vào: {save_path}")

    plt.show()


def plot_combined_ber_ser(results, save_path='combined_ber_ser_plot.png'):
    """
    Vẽ đồ thị kết hợp BER và SER trên cùng một đồ thị

    Args:
        results: Dictionary chứa kết quả mô phỏng
        save_path: Đường dẫn lưu hình ảnh
    """
    ebn0_db = results['ebn0_db']
    ber = results['ber']
    ser = results['ser']

    plt.figure(figsize=(10, 7))

    # Vẽ BER
    plt.semilogy(ebn0_db, ber, 'b-o', linewidth=2.5, markersize=9,
                 label='BER', markerfacecolor='white', markeredgewidth=2)

    # Vẽ SER nếu có dữ liệu
    if any(ser):
        plt.semilogy(ebn0_db, ser, 'r-s', linewidth=2.5, markersize=9,
                     label='SER', markerfacecolor='white', markeredgewidth=2)

    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.xlabel('Eb/N0 (dB)', fontsize=14, fontweight='bold')
    plt.ylabel('Error Rate', fontsize=14, fontweight='bold')
    plt.title('BER & SER vs Eb/N0\n2x2 MIMO-OFDM-STBC, 64-QAM, Rayleigh Channel',
              fontsize=15, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='best')
    plt.xlim([min(ebn0_db), max(ebn0_db)])

    # Thêm lưới phụ
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', alpha=0.3)

    # Thêm thông tin cấu hình
    info_text = "Configuration:\n" \
                "• Antennas: 2 Tx × 2 Rx\n" \
                "• Modulation: 64-QAM\n" \
                "• OFDM: 64 subcarriers\n" \
                "• STBC: Alamouti Code\n" \
                "• Channel: Rayleigh Fading"

    plt.text(0.98, 0.97, info_text,
             transform=plt.gca().transAxes,
             fontsize=10,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Đồ thị kết hợp đã được lưu vào: {save_path}")

    plt.show()


def print_results_table(results):
    """
    In bảng kết quả BER và SER

    Args:
        results: Dictionary chứa kết quả mô phỏng
    """
    ebn0_db = results['ebn0_db']
    ber = results['ber']
    ser = results['ser']

    print("\n" + "=" * 70)
    print("KẾT QUẢ MÔ PHỎNG HỆ THỐNG 2x2 MIMO-OFDM-STBC")
    print("=" * 70)
    print(f"{'Eb/N0 (dB)':<15} {'BER':<20} {'SER':<20}")
    print("-" * 70)

    for i in range(len(ebn0_db)):
        print(f"{ebn0_db[i]:<15} {ber[i]:<20.6e} {ser[i]:<20.6e}")

    print("=" * 70)


if __name__ == '__main__':
    # Load kết quả mô phỏng
    try:
        with open('simulation_results.pkl', 'rb') as f:
            results = pickle.load(f)

        # In bảng kết quả
        print_results_table(results)

        # Vẽ đồ thị
        plot_ber_ser(results)
        plot_combined_ber_ser(results)

    except FileNotFoundError:
        print("Không tìm thấy file 'simulation_results.pkl'")
        print("Vui lòng chạy simulation.py trước!")
