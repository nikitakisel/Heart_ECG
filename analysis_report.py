def print_report(minimums, maximums, establish_points, scale, small_rectangle_length, axis):
    # Анализ сердечного ритма и проводимости
    interval_r_r1 = (maximums[4][0] - maximums[1][0]) / scale  # Значение первого интервала R-R
    interval_r_r2 = (maximums[7][0] - maximums[4][0]) / scale
    interval_r_r_average = (interval_r_r1 + interval_r_r2) / 2

    # Это среднее значение интервала R-R в одном отведении
    percent_10_from_interval_r_r_average = interval_r_r_average / 10
    print(f'\n{percent_10_from_interval_r_r_average}')

    # Находим десять процентов от среднего значения интервала R-R
    difference_interval_r_r1_r_r2 = interval_r_r1 - interval_r_r2

    if difference_interval_r_r1_r_r2 < 0:
        positive_value = difference_interval_r_r1_r_r2 * (-1)
        if positive_value <= interval_r_r_average:
            print('Ритм правильный регулярный')
        else:
            print('Ритм неправильный(нерегулярный)')
    else:
        if difference_interval_r_r1_r_r2 < interval_r_r_average:
            print('Ритм правильный регулярный')
        else:
            print('Ритм неправильный(нерегулярный)')

    # Подсчет числа сердечных сокращений
    heart_rate = 60 / interval_r_r_average
    print(heart_rate)

    # Определение положения электрической оси сердца во фронтальной плоскости

    # Оценка функций проводимости
    length_of_tooth_p = establish_points[1][0] - establish_points[0][0]  # Длина зубца Р
    if length_of_tooth_p <= 0.1:
        print('Длина зубца P находится в допустимом диапозоне')
    else:
        print('Длина зубца P не находится в допустимом диапозоне ')

    # Длительность интервалов P-Q(R) во втором стандартном отведении
    interval_duration_pqr = minimums[1][0] - establish_points[0][0]
    if 0.12 <= interval_duration_pqr <= 0.2:
        print('Длительность интервала P-Q(R) находится в допустимом диапозоне(норма)')
    else:
        print('Длительность интервала P-Q(R)не находится в допустимом диапозоне(патология)')

    # Длительность желудочкового комплекса QRS
    ventricular_qrs_complex_duration = establish_points[3][0] - establish_points[2][0]
    if 0.06 <= ventricular_qrs_complex_duration <= 0.1:
        print('Длительность желудочкового комплекса QRS находится в допустимом диапозоне(норма)')
    else:
        print('Длительность желудочкового комплекса QRS не находится в допустимом диапозоне(патология)')

    # Интервал внутреннего отклонения в грудных отведениях V1 и V6
    internal_deviation_interval_v1 = 1
    internal_deviation_interval_v6 = 1
    if internal_deviation_interval_v1 <= 0.03:
        print('Интервал внутреннего отклонения в грудном отведении V1 находится в диапозоне нормы')
    else:
        print('Интервал внутреннего отклонения в грудном отведении V1 не находится в диапозоне нормы')

    if internal_deviation_interval_v6 <= 0.05:
        print('Интервал внутреннего отклонения в грудном отведении V6 находится в диапозоне нормы')
    else:
        print('Интервал внутреннего отклонения в грудном отведении V6 не находится в диапозоне нормы')

    # Анализ предсердного зубца P
    wave_amplitude_P = (max(establish_points[0][1], establish_points[2][1]) - maximums[0][1]) / small_rectangle_length  # Амплитуда зубца P
    if wave_amplitude_P <= 2.5:
        print('Амплитуда зубца P находится в диапозоне нормы')
    else:
        print('Амплитуда зубца P не находится в диапозоне нормы')

    # Полярность зубца P

    # Форма зубца P

    # Анализ желудочкового комплекса QRST

    # Амплитуда и продолжительность зубца Q
    wave_amplitud_Q = 3  # Значение амплитуды зубца Q
    length_of_tooth_Q = 2  # Значение продолжительности зубца Q

    if wave_amplitud_Q <= 0.03:
        print('Амплитуда зубца Q находится в диапозоне нормы')
    else:
        print('Амплитуда зубца Q не находится в диапозоне нормы')

    if length_of_tooth_Q <= 0.04:
        print('Продолжителность зубца Q находится в диапозоне нормы')
    else:
        print('Продолжителность зубца Q не находится в диапозоне нормы')

    # Амплитуда зубца R
    wave_amplitude_R = (axis - maximums[1][1]) / small_rectangle_length  # Значение амплитуды зубца R
    if 6 <= wave_amplitude_R <= 16:
        print('Амплитуда зубца R находится в диапозоне нормы')
    else:
        print('Амплитуда зубца R не находится в диапозоне нормы')

    # Амплитуда зубца S
    wave_amplitude_s = 1  # Значение амплитуды зубца S

    if 0 <= wave_amplitude_s <= 6:
        print('Амплитуда зубца S находится в диапозоне нормы')
    else:
        print('Амплитуда зубца S не находится в диапозоне нормы')

    # Анализ сегмента RS-T

    # Положительное (+) или отрицательное (-) отклонение точки соединения j от изоэлектрической линии

    # Смещение сегмента RS-T на расстояние 0.08 сек вправо от точки соединения j

    # Форма смещения сегмента RS-T

    # Полярность зубца T

    # Форма зубца T

    # Амплитуда зубца T
    wave_amplitude_t = (max(establish_points[4][1], establish_points[5][1]) - maximums[2][1]) / small_rectangle_length  # Значение амплитуды зубца Т

    if wave_amplitude_t <= 6:
        print('Амплитуда зубца T находится в диапозоне нормы')
    else:
        print('Амплитуда зубца T не находится в диапозоне нормы')

    # Анализ интервала Q-T
    interval_QT = (establish_points[5][0] - establish_points[2][0]) / scale  # Значение интервала Q-T
    interval_QT *= 1000  # Перевод секунд в микросекунды

    interval_QTC = interval_QT / (interval_r_r1 ** 0.5)

    if 360 <= interval_QTC <= 440:
        print(interval_QTC, 'Нормальная продолжительность корригированного интервала')
    elif 340 <= interval_QTC <= 359:
        print(interval_QTC, 'Пограничное значение корригированного интервала')
    elif 441 <= interval_QTC <= 460:
        print(interval_QTC, 'Пограничное значение корригированного интервала')
    elif interval_QTC < 340:
        print(interval_QTC, 'Корригированный интервал QT укорочен')
    else:
        # interval_QTC > 460
        print(interval_QTC, 'Корригированный интервал QT удлинен')
