"""
Package mô phỏng hệ thống MIMO-OFDM-STBC
"""

__version__ = '1.0.0'
__author__ = 'MIMO-OFDM-STBC Simulation'

from .modulation import qam64_modulate, qam64_demodulate, generate_random_bits
from .ofdm import ofdm_modulate, ofdm_demodulate
from .stbc import alamouti_encode, alamouti_decode
from .channel import (generate_rayleigh_channel, add_awgn,
                      mimo_channel_apply, calculate_snr_from_ebn0)

__all__ = [
    'qam64_modulate',
    'qam64_demodulate',
    'generate_random_bits',
    'ofdm_modulate',
    'ofdm_demodulate',
    'alamouti_encode',
    'alamouti_decode',
    'generate_rayleigh_channel',
    'add_awgn',
    'mimo_channel_apply',
    'calculate_snr_from_ebn0',
]
