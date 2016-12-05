from django.conf import settings

import requests

def get_price_choices(voucher_type):
    lst = [('', 'Select Price')]

    prices = requests.get(settings.VOUCHER_VALUES_URL, params={'voucher_type': voucher_type}).json()
    for p in prices['results']:
        lst.append((p, str(p) + ' GHS'))

    return lst

def zeropad(num):
    num = str(num)
    return ('0' * (10 - len(num))) + num

def write_vouchers(voucher_list, _file):
    for v in voucher_list:
        with open(_file, 'a') as f:
            if len(v) == 2:
                f.write(zeropad(v[0]) + ',' + v[1] + '\r\n')
            else:
                f.write(zeropad(v[0]) + ',' + v[1] + ',' + v[2] + '\r\n')

    return f

def send_api_request(url, data):
    get_response = requests.get(url)
    post_response = requests.post(
          url,
          data=data,
          headers={"X-CSRFToken": get_response.cookies['csrftoken']},
          cookies=get_response.cookies
        )

    return post_response.json()
