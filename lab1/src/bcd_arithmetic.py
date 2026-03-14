from src.bit_array import BitArray

class Excess3BCDArithmetic:
    def decimal_to_excess3(self, val: int) -> BitArray:
        r = BitArray()
        r.bits[0] = 1 if val < 0 else 0
        v_str = str(abs(val)).zfill(7)
        idx = 31
        
        for char in reversed(v_str):
            d = int(char) + 3
            for _ in range(4):
                r.bits[idx] = d % 2
                d //= 2
                idx -= 1
                
        return r

    def excess3_to_decimal(self, b: BitArray) -> int:
        v_str = ""
        for i in range(31, 3, -4):
            group = b.bits[i-3:i+1]
            d = group[0]*8 + group[1]*4 + group[2]*2 + group[3]
            if d >= 3:
                v_str = str(d - 3) + v_str
                
        res = int(v_str) if v_str else 0
        return -res if b.bits[0] == 1 else res

    def add(self, a: BitArray, b: BitArray) -> BitArray:
        r = BitArray()
        c = 0
        
        for i in range(31, 3, -4):
            group_a = a.bits[i-3:i+1]
            group_b = b.bits[i-3:i+1]
            s = [0]*4
            lc = c
            
            for j in range(3, -1, -1):
                t = group_a[j] + group_b[j] + lc
                s[j] = t % 2
                lc = t // 2
                
            if lc == 1:
                corr = [0, 0, 1, 1]
                cc = 0
                for j in range(3, -1, -1):
                    t = s[j] + corr[j] + cc
                    r.bits[i-3+j] = t % 2
                    cc = t // 2
                c = 1
            else:
                corr = [1, 1, 0, 1]
                cc = 0
                for j in range(3, -1, -1):
                    t = s[j] + corr[j] + cc
                    r.bits[i-3+j] = t % 2
                    cc = t // 2
                c = 0
                
        r.bits[0] = a.bits[0]
        return r