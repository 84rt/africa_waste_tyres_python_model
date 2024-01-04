a = 107000
b = 131000
c = 0
x = 0
b_prime = [0, x]
d = 0
e = 920000
g = 0
i = 93400
j = 0
h = 0
m = [0, 0, 0]
k = 29000
l = 0
o = 14400
q = 22700
p = 213000
old_e = e

years = 45
for year in range(years):
    c += a + b
    print(c, a, b)
    # the increase in inputs is after the first year
    a *= 1.045
    b *= 1.045
    print(e)
    g = e * 0.326086957
    l = e * 0.035
    x = e - old_e + g + l - c
    old_e = e
    b_prime = [0, x/2, x]
    h = [x - elem for elem in b_prime]
    print(b_prime, h)
    j = g * (1 - 0.21)

    # add to m from j
    # add to p from i
    # if overflows add to m from i

    m[0] += j-h[0]
    m[1] += j-h[1]
    m[2] += j-h[2]

    # 60% of i will go to p until p is >= 250000 then it it will all go to `m` (though j but we can skip that)
    goes_to_p = i - q - o
    goes_to_i = 0
    if p < 250000:
        if p + goes_to_p < 250000:
            p += goes_to_p
        else:
            goes_to_i = p - 250000 + goes_to_p
            p = 250000
    else:
        goes_to_i = goes_to_p
    m = [elem + goes_to_i for elem in m]
    print(goes_to_p)
    print(p, m)
    print()


    