# import re

# arr = ['OOAK91', 'ANAM09', 'MSLV11', 'BATH05', 'OOSF147' ]
# arr = 'OOSF147'
# for i in range(len(arr)):
#     trip = re.split("[A-Z]*", arr[i])
#     print(trip)
#     vsl = re.findall("[A-Z]*", arr[i])
#     print(vsl)
# trip = re.split("[A-Z]*", arr)
# print(trip[-1])
# vsl = re.findall("[A-Z]*", arr)
# print(vsl[0])

# s_marks = 'one-two+three#four'
# print(re.split('[-+#]', s_marks))



from datetime import datetime
def convertDateSched(data, opt):
    # ============================================
    # NOT a VIEW
    # support function
    # > converts date string to date object
    # data sample
    # "Wed-26-Feb 17:00"
    # https://www.programiz.com/python-programming/datetime/strptime
    # ============================================

    print('data conversion > {}'.format(data))

    if "full" in opt:
        # splits the date string into date and time and PM/AM
        check = data.split(' ')

        # splits the time string into hour/minute/second
        hora = check[1].split(':')

        # puts the date string back together
        data = str(check[0]) + str(' ') + str(hora[0]) + \
            str(':') + str(hora[1])

        return datetime.strptime(data, '%a-%d-%b %H:%M')
    elif "midway" in opt:
        # splits the date string into date and time and PM/AM
        check = data.split(' ')

        # splits the time string into hour/minute/second
        hora = check[1].split(':')

        # puts the date string back together
        data = str(check[0]) + str(' ') + str(hora[0]) + \
            str(':') + str(hora[1])

        return datetime.strptime(data, '%d-%b %H:%M')
    elif "notime" in opt:
        return datetime.strptime(data, '%a-%d-%b')        


x = "Wed-26-Feb 17:00"
# x = "26-Feb 17:00"
# x = "Wed-26-Feb"
convertDateSched(x, " full")