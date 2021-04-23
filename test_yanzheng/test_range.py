start=0
for end in range(start, 101, 100):
    if not end:
        continue
    print(start, end)
    url = 'https://fapi.lawxp.com/v1/CkeyWord?startid=%s&endid=%s' % (start, end)
    start = end
