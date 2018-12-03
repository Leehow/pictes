def ctti(row_label):
    if row_label == 'button':
        return 1
    elif row_label == 'checkbox':
        return 2
    elif row_label == 'checkbox_c':
        return 3
    elif row_label == 'input_text':
        return 4
    elif row_label == 'textarea':
        return 5
    elif row_label == 'input_psw':
        return 6
    elif row_label == 'input_radio':
        return 7
    elif row_label == 'input_radio_c':
        return 8
    elif row_label == 'link':
        return 9
    elif row_label == 'select':
        return 10
    elif row_label == 'textblock':
        return 11
    elif row_label == 'tab':
        return 12
    elif row_label == 'tab_list':
        return 13
    elif row_label == 'datepicker':
        return 14
    else:
        None

