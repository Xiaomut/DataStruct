ip = "10.0.3.193"
num_input = "167969729"

ips = ip.split('.')

num_inputs = [
    str(bin(int(num_input))[2:].rjust(8, '0'))[8 * i:8 * i + 8]
    for i in range(4)
]

ret_ip = []
for i in num_inputs:
    ret_ip.append(int("0b" + i, 2))

ret_ip = '.'.join(ret_ip)

ret_num = ""
for i in ips:
    ret_num += str(int(i, 2))

ret_num = int(ret_num, 10)

print(ret_num)
print(ret_ip)
