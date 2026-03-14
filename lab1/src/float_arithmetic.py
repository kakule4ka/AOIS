from src.bit_array import BitArray

class IEEE754Arithmetic:
    def float_to_bits(self, val: float) -> BitArray:
        res = BitArray()
        if val == 0.0:
            return res
            
        res.bits[0] = 1 if val < 0 else 0
        val = abs(val)
        
        int_part = int(val)
        frac_part = val - int_part
        
        int_bits = []
        while int_part > 0:
            int_bits.append(int_part % 2)
            int_part //= 2
        int_bits.reverse()
        
        frac_bits = []
        while frac_part > 0 and len(frac_bits) < 150:
            frac_part *= 2
            bit = int(frac_part)
            frac_bits.append(bit)
            frac_part -= bit
            
        if len(int_bits) > 0:
            exp = len(int_bits) - 1
            mantissa = int_bits[1:] + frac_bits
        else:
            exp = -1
            for b in frac_bits:
                if b == 1:
                    break
                exp -= 1
            idx = -exp
            mantissa = frac_bits[idx:] if idx < len(frac_bits) else []
            
        exp_stored = exp + 127
        for i in range(8, 0, -1):
            res.bits[i] = exp_stored % 2
            exp_stored //= 2
            
        for i in range(min(23, len(mantissa))):
            res.bits[9 + i] = mantissa[i]
            
        return res

    def bits_to_float(self, bit_array: BitArray) -> float:
        sign = -1 if bit_array.bits[0] == 1 else 1
        
        exp = 0
        for i in range(1, 9):
            exp = exp * 2 + bit_array.bits[i]
            
        if exp == 0:
            return 0.0
            
        exp -= 127
        mantissa = 1.0
        power = 0.5
        for i in range(9, 32):
            mantissa += bit_array.bits[i] * power
            power /= 2.0
            
        return sign * mantissa * (2 ** exp)

    def _extract(self, b: BitArray):
        s = b.bits[0]
        e = 0
        for i in range(1, 9):
            e = e * 2 + b.bits[i]
        m = [1] + b.bits[9:32] if e > 0 else [0] + b.bits[9:32]
        return s, e, m

    def _pack(self, s, e, m) -> BitArray:
        r = BitArray()
        r.bits[0] = s
        for i in range(8, 0, -1):
            r.bits[i] = e % 2
            e //= 2
        for i in range(23):
            r.bits[9+i] = m[i+1] if i+1 < len(m) else 0
        return r

    def add(self, a: BitArray, b: BitArray) -> BitArray:
        return self._add_sub(a, b, False)

    def subtract(self, a: BitArray, b: BitArray) -> BitArray:
        return self._add_sub(a, b, True)

    def _add_sub(self, a: BitArray, b: BitArray, is_sub: bool) -> BitArray:
        s1, e1, m1 = self._extract(a)
        s2, e2, m2 = self._extract(b)
        
        if is_sub:
            s2 = 1 - s2
            
        if e1 == 0:
            return self._pack(s2, e2, m2)
        if e2 == 0:
            return self._pack(s1, e1, m1)
            
        if e1 < e2:
            s1, s2 = s2, s1
            e1, e2 = e2, e1
            m1, m2 = m2, m1
            
        diff = e1 - e2
        if diff > 24:
            diff = 24
        m2 = [0]*diff + m2[:24-diff]
        
        e_res = e1
        res_m = [0]*25
        
        if s1 == s2:
            s_res = s1
            c = 0
            for i in range(23, -1, -1):
                t = m1[i] + m2[i] + c
                res_m[i+1] = t % 2
                c = t // 2
            res_m[0] = c
            
            if res_m[0] == 1:
                e_res += 1
                m_res = res_m[0:24]
            else:
                m_res = res_m[1:25]
        else:
            c = 0
            for i in range(23, -1, -1):
                d = m1[i] - m2[i] - c
                if d < 0:
                    res_m[i+1] = d + 2
                    c = 1
                else:
                    res_m[i+1] = d
                    c = 0
            res_m[0] = 0
            s_res = s1
            
            if c == 1:
                s_res = s2
                c2 = 1
                for i in range(24, 0, -1):
                    t = 1 - res_m[i] + c2
                    res_m[i] = t % 2
                    c2 = t // 2
                    
            idx = -1
            for i in range(1, 25):
                if res_m[i] == 1:
                    idx = i
                    break
                    
            if idx == -1:
                return BitArray()
                
            shift = idx - 1
            e_res -= shift
            m_res = res_m[idx:] + [0]*shift
            
        return self._pack(s_res, e_res, m_res)

    def multiply(self, a: BitArray, b: BitArray) -> BitArray:
        s1, e1, m1 = self._extract(a)
        s2, e2, m2 = self._extract(b)
        
        s_res = s1 ^ s2
        if e1 == 0 or e2 == 0:
            return self._pack(s_res, 0, [0]*24)
            
        e_res = e1 + e2 - 127
        res_m = [0]*48
        
        for i in range(23, -1, -1):
            if m2[i] == 1:
                c = 0
                for j in range(23, -1, -1):
                    t = res_m[i+j+1] + m1[j] + c
                    res_m[i+j+1] = t % 2
                    c = t // 2
                res_m[i] += c
                
        if res_m[0] == 1:
            e_res += 1
            m_res = res_m[0:24]
        else:
            m_res = res_m[1:25]
            
        return self._pack(s_res, e_res, m_res)

    def divide(self, a: BitArray, b: BitArray) -> BitArray:
        s1, e1, m1 = self._extract(a)
        s2, e2, m2 = self._extract(b)
        
        s_res = s1 ^ s2
        if e2 == 0:
            return BitArray()
        if e1 == 0:
            return self._pack(s_res, 0, [0]*24)
            
        e_res = e1 - e2 + 127
        rem = m1 + [0]*25
        q = []
        
        for _ in range(25):
            greater = True
            for i in range(24):
                if rem[i] > m2[i]:
                    break
                if rem[i] < m2[i]:
                    greater = False
                    break
                    
            if greater:
                q.append(1)
                c = 0
                for i in range(23, -1, -1):
                    diff = rem[i] - m2[i] - c
                    if diff < 0:
                        rem[i] = diff + 2
                        c = 1
                    else:
                        rem[i] = diff
                        c = 0
            else:
                q.append(0)
            rem.pop(0)
            rem.append(0)
            
        if q[0] == 1:
            m_res = q[0:24]
        else:
            e_res -= 1
            m_res = q[1:25]
            
        return self._pack(s_res, e_res, m_res)