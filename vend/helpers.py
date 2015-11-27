import requests

def zeropad(num):
    num = str(num)
    return ('0' * (10 - len(num))) + num

def write_vouchers(voucher_list, _file):
    print voucher_list
    for v in voucher_list:
        with open(_file, 'a') as f:
            f.write(zeropad(v[0]) + ',' + v[1] + '\n')

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
