"""
Script vẽ đồ thị so sánh BER/SER thực tế và lý thuyết
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Sử dụng backend không cần GUI
import matplotlib.pyplot as plt
import pickle

from theoretical_performance import calculate_theoretical_curves


def plot_ber_comparison(sim_results, save_path='ber_comparison.png'):
    """
    Vẽ đồ thị so sánh BER thực tế và lý thuyết

    Args:
        sim_results: Dictionary chứa kết quả mô phỏng
        save_path: Đường dẫn lưu hình ảnh
    """
    # Lấy kết quả mô phỏng
    ebn0_sim = np.array(sim_results['ebn0_db'])
    ber_sim = np.array(sim_results['ber'])

    # Tính kết quả lý thuyết
    ebn0_theory = np.arange(0, 26, 0.5)
    theory_results = calculate_theoretical_curves(ebn0_theory)

    # Thay thế BER = 0 bằng giá trị rất nhỏ để hiển thị trên log scale
    ber_sim_plot = [b if b > 0 else 1e-7 for b in ber_sim]

    plt.figure(figsize=(12, 8))

    # Vẽ BER lý thuyết
    plt.semilogy(ebn0_theory, theory_results['ber_rayleigh_div2_simple'],
                 'r--', linewidth=2, label='BER Lý thuyết (Rayleigh + STBC)')

    # Vẽ BER mô phỏng
    plt.semilogy(ebn0_sim, ber_sim_plot, 'b-o', linewidth=2.5, markersize=10,
                 label='BER Mô phỏng (Rayleigh + STBC)',
                 markerfacecolor='white', markeredgewidth=2)

    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.xlabel('Eb/N0 (dB)', fontsize=14, fontweight='bold')
    plt.ylabel('Bit Error Rate (BER)', fontsize=14, fontweight='bold')
    plt.title('So sánh BER: Mô phỏng vs Lý thuyết\n2x2 MIMO-OFDM-STBC, 64-QAM, Rayleigh Channel',
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='best')
    plt.xlim([min(ebn0_sim) - 1, max(ebn0_sim) + 1])
    plt.ylim([1e-7, 1])

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
                "• Channel: Rayleigh Fading + AWGN\n" \
                "• Diversity Order: 2"

    plt.text(0.98, 0.97, info_text,
             transform=plt.gca().transAxes,
             fontsize=10,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Đồ thị so sánh BER đã được lưu vào: {save_path}")

    return save_path


def plot_ser_comparison(sim_results, save_path='ser_comparison.png'):
    """
    Vẽ đồ thị so sánh SER thực tế và lý thuyết

    Args:
        sim_results: Dictionary chứa kết quả mô phỏng
        save_path: Đường dẫn lưu hình ảnh
    """
    # Lấy kết quả mô phỏng
    ebn0_sim = np.array(sim_results['ebn0_db'])
    ser_sim = np.array(sim_results['ser'])

    # Tính kết quả lý thuyết
    ebn0_theory = np.arange(0, 26, 0.5)
    theory_results = calculate_theoretical_curves(ebn0_theory)

    # Thay thế SER = 0 bằng giá trị rất nhỏ
    ser_sim_plot = [s if s > 0 else 1e-7 for s in ser_sim]

    plt.figure(figsize=(12, 8))

    # Vẽ SER lý thuyết
    plt.semilogy(ebn0_theory, theory_results['ser_rayleigh_div2'],
                 'r--', linewidth=2, label='SER Lý thuyết (Rayleigh + STBC)')

    # Vẽ SER mô phỏng
    plt.semilogy(ebn0_sim, ser_sim_plot, 'g-s', linewidth=2.5, markersize=10,
                 label='SER Mô phỏng (Rayleigh + STBC)',
                 markerfacecolor='white', markeredgewidth=2)

    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.xlabel('Eb/N0 (dB)', fontsize=14, fontweight='bold')
    plt.ylabel('Symbol Error Rate (SER)', fontsize=14, fontweight='bold')
    plt.title('So sánh SER: Mô phỏng vs Lý thuyết\n2x2 MIMO-OFDM-STBC, 64-QAM, Rayleigh Channel',
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='best')
    plt.xlim([min(ebn0_sim) - 1, max(ebn0_sim) + 1])
    plt.ylim([1e-7, 1])

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
                "• Channel: Rayleigh Fading + AWGN\n" \
                "• Diversity Order: 2"

    plt.text(0.98, 0.97, info_text,
             transform=plt.gca().transAxes,
             fontsize=10,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Đồ thị so sánh SER đã được lưu vào: {save_path}")

    return save_path


def plot_ber_ser_combined(sim_results, save_path='ber_ser_combined.png'):
    """
    Vẽ đồ thị kết hợp BER và SER trên cùng một đồ thị

    Args:
        sim_results: Dictionary chứa kết quả mô phỏng
        save_path: Đường dẫn lưu hình ảnh
    """
    # Lấy kết quả mô phỏng
    ebn0_sim = np.array(sim_results['ebn0_db'])
    ber_sim = np.array(sim_results['ber'])
    ser_sim = np.array(sim_results['ser'])

    # Tính kết quả lý thuyết
    ebn0_theory = np.arange(0, 26, 0.5)
    theory_results = calculate_theoretical_curves(ebn0_theory)

    # Thay thế 0 bằng giá trị rất nhỏ
    ber_sim_plot = [b if b > 0 else 1e-7 for b in ber_sim]
    ser_sim_plot = [s if s > 0 else 1e-7 for s in ser_sim]

    plt.figure(figsize=(14, 9))

    # Vẽ BER
    plt.semilogy(ebn0_theory, theory_results['ber_rayleigh_div2_simple'],
                 'r--', linewidth=2, alpha=0.7, label='BER Lý thuyết')
    plt.semilogy(ebn0_sim, ber_sim_plot, 'b-o', linewidth=2.5, markersize=10,
                 label='BER Mô phỏng', markerfacecolor='white', markeredgewidth=2)

    # Vẽ SER
    plt.semilogy(ebn0_theory, theory_results['ser_rayleigh_div2'],
                 'm--', linewidth=2, alpha=0.7, label='SER Lý thuyết')
    plt.semilogy(ebn0_sim, ser_sim_plot, 'g-s', linewidth=2.5, markersize=10,
                 label='SER Mô phỏng', markerfacecolor='white', markeredgewidth=2)

    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.xlabel('Eb/N0 (dB)', fontsize=15, fontweight='bold')
    plt.ylabel('Error Rate', fontsize=15, fontweight='bold')
    plt.title('So sánh BER & SER: Mô phỏng vs Lý thuyết\n' +
              '2x2 MIMO-OFDM-STBC, 64-QAM, Rayleigh Channel',
              fontsize=17, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='best', ncol=2)
    plt.xlim([min(ebn0_sim) - 1, max(ebn0_sim) + 1])
    plt.ylim([1e-7, 1])

    # Thêm lưới phụ
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', alpha=0.3)

    # Thêm thông tin cấu hình
    info_text = "Configuration:\n" \
                "• Antennas: 2 Tx × 2 Rx\n" \
                "• Modulation: 64-QAM\n" \
                "• OFDM: 64 subcarriers\n" \
                "• FFT: 64, CP: 16\n" \
                "• STBC: Alamouti\n" \
                "• Channel: Rayleigh + AWGN\n" \
                "• Diversity: 2"

    plt.text(0.02, 0.03, info_text,
             transform=plt.gca().transAxes,
             fontsize=10,
             verticalalignment='bottom',
             horizontalalignment='left',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Đồ thị kết hợp BER & SER đã được lưu vào: {save_path}")

    return save_path


def print_results_table_detailed(sim_results):
    """
    In bảng kết quả chi tiết BER và SER

    Args:
        sim_results: Dictionary chứa kết quả mô phỏng
    """
    ebn0_db = sim_results['ebn0_db']
    ber_sim = sim_results['ber']
    ser_sim = sim_results['ser']

    # Tính lý thuyết
    theory_results = calculate_theoretical_curves(ebn0_db)

    print("\n" + "=" * 90)
    print("KẾT QUẢ MÔ PHỎNG VÀ LÝ THUYẾT - HỆ THỐNG 2x2 MIMO-OFDM-STBC")
    print("=" * 90)
    print(f"{'Eb/N0':>8} │ {'BER (Sim)':>12} │ {'BER (Theory)':>12} │ {'SER (Sim)':>12} │ {'SER (Theory)':>12}")
    print(f"{'(dB)':>8} │ {'':>12} │ {'':>12} │ {'':>12} │ {'':>12}")
    print("-" * 90)

    for i in range(len(ebn0_db)):
        print(f"{ebn0_db[i]:>8.0f} │ {ber_sim[i]:>12.6e} │ {theory_results['ber_rayleigh_div2_simple'][i]:>12.6e} │ "
              f"{ser_sim[i]:>12.6e} │ {theory_results['ser_rayleigh_div2'][i]:>12.6e}")

    print("=" * 90)


if __name__ == '__main__':
    # Load kết quả mô phỏng
    try:
        with open('simulation_results_quick.pkl', 'rb') as f:
            sim_results = pickle.load(f)

        print("\n" + "="*70)
        print("VẼ ĐỒ THỊ SO SÁNH BER/SER MÔ PHỎNG VÀ LÝ THUYẾT")
        print("="*70)

        # In bảng kết quả chi tiết
        print_results_table_detailed(sim_results)

        # Vẽ các đồ thị
        print("\nĐang tạo đồ thị...")
        plot_ber_comparison(sim_results)
        plot_ser_comparison(sim_results)
        plot_ber_ser_combined(sim_results)

        print("\n" + "="*70)
        print("✓ Hoàn tất! Đã tạo 3 đồ thị:")
        print("  1. ber_comparison.png - So sánh BER")
        print("  2. ser_comparison.png - So sánh SER")
        print("  3. ber_ser_combined.png - Đồ thị kết hợp")
        print("="*70)

    except FileNotFoundError:
        print("Không tìm thấy file 'simulation_results_quick.pkl'")
        print("Vui lòng chạy simulation_quick.py trước!")
    except Exception as e:
        print(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()
