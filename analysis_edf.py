from scipy.ndimage import gaussian_filter1d
import ecg_plot
import numpy as np
import pyedflib
import wfdb

import curve_analysis
import curve_calculation
import analysis_report


def second_section():
    file_path = 'data/pat00001.edf'
    signals, sample_rates, signal_labels = read_edf_pyedflib(file_path)

    if signals is not None:
        # record = wfdb.rdrecord('data/00001_lr', sampto=1000)
        # ecg = record.p_signal.T
        # sample_rate = record.fs

        ecg = signals
        sample_rate = sample_rates[0]

        second_section_list = list(gaussian_filter1d(ecg[1], 2.5))
        # second_section_list = ecg[1]
        second_section_matrix = [[i, second_section_list[i]] for i in range(len(second_section_list))]

        potential_minimums, maximums = curve_analysis.find_extremes_efd(second_section_matrix, 3)
        minimums = curve_analysis.find_neighbour_minimums(
            maximums,
            3,
            [1],
            potential_minimums,
        )

        # find establish points
        potential_establish_points = curve_analysis.find_establish_points(
            second_section_matrix,
            10,  # !!!!!!!!! small_rectangle_length,
        )
        establish_points = curve_analysis.find_neighbour_minimums(
            maximums,
            3,
            [0, 2],
            potential_establish_points,
        ) + curve_analysis.find_neighbour_maximums(
            minimums,
            5,
            potential_establish_points,
        )
        establish_points.sort()

        # print parameters calculation
        curve_calculation.print_parameters(maximums, establish_points, sample_rate)

        # print report
        analysis_report.print_report(minimums, maximums, establish_points, sample_rate, 10, 0)

        # print(f"Частота дискретизации: {sample_rate}")
    else:
        print("Не удалось прочитать файл.")


def read_edf_pyedflib(file_path):
    """Читает файл EDF с использованием pyEDFlib."""
    try:
        f = pyedflib.EdfReader(file_path)
        n = f.signals_in_file  # Количество каналов
        signal_labels = f.getSignalLabels()  # Получаем названия каналов
        sample_rates = [f.getSampleFrequency(i) for i in range(n)]  # Частота дискретизации для каждого канала
        signals = []
        for i in range(n):
            signals.append(f.readSignal(i))  # Читаем данные сигнала

        # Преобразуем в numpy массивы:
        signals = np.array(signals)
        sample_rates = np.array(sample_rates)

        f.close()
        return signals, sample_rates, signal_labels

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None, None, None


def draw_ecg():
    file_path = 'data/pat00001.edf'
    signals, sample_rates, signal_labels = read_edf_pyedflib(file_path)

    if signals is not None:
        print(signals[1].tolist())
        signals = [gaussian_filter1d(signal, 2.5) for signal in signals]

        lead_index = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        ecg_plot.plot(signals, sample_rate=sample_rates[0], title='ECG', lead_index=lead_index)
        ecg_plot.show()
    else:
        print("Не удалось прочитать файл.")


if __name__ == "__main__":
    # second_section()
    draw_ecg()
