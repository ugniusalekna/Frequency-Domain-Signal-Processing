import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

from functions.signal_manipulation import *
from functions.frequency_manipulation import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def plot_signal(sample_rate, signal_data, signal_amplitude, wav_info, title):
    # Obtain and calculate relevant data 
    duration_sec = get_duration_sec(sample_rate, signal_data)
    time_scale, xlabel = get_time_scale(duration_sec)
    duration_scaled = duration_sec * time_scale
    num_channels = wav_info[1]
    text_info = f'Channels: {wav_info[1]}, Audio Duration: {np.round(duration_scaled, 2)} {xlabel}, Sampling Rate: {sample_rate} Hz, Bit Depth: {wav_info[2]} bits'
    
    # Create a figure with multiple subplots based on the number of channels
    fig, axs = plt.subplots(2, num_channels, figsize=(12, 9))
    axs = axs.reshape(-1, num_channels)
    time_axis_signal = get_time_axis(sample_rate, signal_data, time_scale)
    freq_axis_signal = get_freq_axis(sample_rate, signal_amplitude)

    for channel in range(num_channels):        
        # Plot the signal and its amplitude spectrum for every channel
        axs[0, channel].plot(time_axis_signal, signal_data[:, channel], label='Original signal', linewidth=0.4)
        if num_channels > 1:
            axs[0, channel].set_title(f'Channel {channel+1}', fontsize=12)
        axs[0, channel].set_ylabel('Amplitude')
        axs[0, channel].set_xlabel(f'Time ({xlabel})')
        axs[0, channel].set_xlim(-0.05 * duration_scaled, 1.05 * duration_scaled)

        axs[1, channel].plot(freq_axis_signal, signal_amplitude[:, channel], label='Amplitude spectrum', c='#FF4500', linewidth=0.4)
        axs[1, channel].vlines(freq_axis_signal, [0], signal_amplitude[:, channel], color='#FF4500', linewidth=0.5) 
        axs[1, channel].scatter(freq_axis_signal, signal_amplitude[:, channel], color='#FF4500', s=10) 
        axs[1, channel].set_ylabel('Magnitude')
        axs[1, channel].set_xlabel('Frequency (Hz)')
        # axs[1, channel].set_xlim(-10, 5000)

        # Formatting options (scientific notation)
        for row in range(2):
            axs[row, channel].yaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=True))
            axs[row, channel].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
            axs[row, channel].get_yaxis().get_offset_text().set_x(-0.08) 
            axs[row, channel].grid(True)
            axs[row, channel].legend(loc='upper right')

    fig.suptitle(title, fontsize=14)
    fig.text(0.5, 0.03, text_info, fontsize=10, ha='center', va='top', backgroundcolor='white')
    
    # Adjust the layout
    plt.subplots_adjust(left=0.1 if num_channels==1 else 0.085,\
                        right=0.9 if num_channels==1 else 0.98,\
                        top=0.93 if num_channels==1 else 0.9,\
                        bottom=0.11 if num_channels==1 else 0.12,\
                        hspace=0.17 if num_channels==1 else 0.25)
    plt.show(block=False)