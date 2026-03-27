from src.bit_array import BitArray

class IntegerArithmetic:
    def add_additional(self, a: BitArray, b: BitArray) -> BitArray:
        r = BitArray()
        c = 0
        for i in range(31, -1, -1):
            t = a.bits[i] + b.bits[i] + c
            r.bits[i] = t % 2
            c = t // 2
        return r

    def subtract_additional(self, a: BitArray, b: BitArray) -> BitArray:
        neg_b = BitArray()
        for i in range(32):
            neg_b.bits[i] = 1 - b.bits[i]
        c = 1
        for i in range(31, -1, -1):
            t = neg_b.bits[i] + c
            neg_b.bits[i] = t % 2
            c = t // 2
        return self.add_additional(a, neg_b)

    def multiply_direct(self, a: BitArray, b: BitArray) -> BitArray:
        r = BitArray()
        r.bits[0] = a.bits[0] ^ b.bits[0]
        m_a = a.bits[1:]
        m_b = b.bits[1:]
        res_m = [0] * 62
        for i in range(30, -1, -1):
            if m_b[i] == 1:
                c = 0
                for j in range(30, -1, -1):
                    idx = i + j + 1
                    t = res_m[idx] + m_a[j] + c
                    res_m[idx] = t % 2
                    c = t // 2
                res_m[i] += c
        for i in range(31):
            r.bits[1 + i] = res_m[31 + i]
        return r

    def divide_fixed(self, a: BitArray, b: BitArray) -> BitArray:
        r = BitArray()
        r.bits[0] = a.bits[0] ^ b.bits[0]
        m_a = a.bits[1:] + [0]*17
        m_b = b.bits[1:]
        rem = [0] * 31
        q = []
        for bit in m_a:
            rem.pop(0)
            rem.append(bit)
            greater_eq = True
            for i in range(31):
                if rem[i] > m_b[i]: 
                    break
                if rem[i] < m_b[i]:
                    greater_eq = False
                    break
            if greater_eq:
                q.append(1)
                c = 0
                for i in range(30, -1, -1):
                    diff = rem[i] - m_b[i] - c
                    if diff < 0:
                        rem[i] = diff + 2
                        c = 1
                    else:
                        rem[i] = diff
                        c = 0
            else:
                q.append(0)
        for i in range(31):
            if len(q) - 31 + i >= 0:
                r.bits[1 + i] = q[len(q) - 31 + i]
        return r