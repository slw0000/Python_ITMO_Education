from get_currency import get_currencies


if __name__ == '__main__':
    # sp_values = input('Введите коды валют через пробел: ')
    # sp_values = sp_values.upper().split()
    sp_values = ['USD', 'EUR', 'GBR']
    currencies = get_currencies(sp_values, url='https://google.com')
    print(currencies)
