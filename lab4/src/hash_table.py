from typing import Any, Optional
from src.models import HashNode
from src.constants import TABLE_SIZE, BASE_ADDRESS, BASE_MULTIPLIER, RUSSIAN_ALPHABET

class HashTable:
    def __init__(self, size: int = TABLE_SIZE):
        self.size = size
        self.table: list[Optional[HashNode]] = [None] * self.size
        self.count = 0

    def _get_v(self, key: str) -> int:
        key_lower = key.lower()
        v = 0
        if len(key_lower) > 0:
            char_index = RUSSIAN_ALPHABET.find(key_lower[0])
            if char_index != -1:
                v += char_index * BASE_MULTIPLIER
        if len(key_lower) > 1:
            char_index = RUSSIAN_ALPHABET.find(key_lower[1])
            if char_index != -1:
                v += char_index
        return v

    def _hash(self, v: int) -> int:
        return (v % self.size) + BASE_ADDRESS

    def create(self, key: str, data: Any) -> bool:
        v = self._get_v(key)
        h = self._hash(v)

        if self.table[h] is None:
            self.table[h] = HashNode(id_key=key, pi_data=data)
            self.count += 1
            return True

        current = self.table[h]
        current.c_flag = 1
        
        while current is not None:
            if current.id_key == key and current.d_flag == 0:
                return False
            if current.p0_next is None:
                break
            current = current.p0_next

        current.t_flag = 0
        current.p0_next = HashNode(id_key=key, pi_data=data)
        self.count += 1
        return True

    def read(self, key: str) -> Optional[Any]:
        v = self._get_v(key)
        h = self._hash(v)
        current = self.table[h]

        while current is not None:
            if current.id_key == key and current.d_flag == 0:
                return current.pi_data
            current = current.p0_next
        return None

    def update(self, key: str, new_data: Any) -> bool:
        v = self._get_v(key)
        h = self._hash(v)
        current = self.table[h]

        while current is not None:
            if current.id_key == key and current.d_flag == 0:
                current.pi_data = new_data
                return True
            current = current.p0_next
        return False

    def delete(self, key: str) -> bool:
        v = self._get_v(key)
        h = self._hash(v)
        current = self.table[h]
        prev = None

        while current is not None:
            if current.id_key == key and current.d_flag == 0:
                current.d_flag = 1
                current.u_flag = 0
                self.count -= 1

                if prev is None:
                    if current.p0_next is None:
                        self.table[h] = None
                    else:
                        self.table[h] = current.p0_next
                        self.table[h].c_flag = 1
                else:
                    prev.p0_next = current.p0_next
                    if prev.p0_next is None:
                        prev.t_flag = 1
                return True
            
            prev = current
            current = current.p0_next
        return False

    def load_factor(self) -> float:
        return self.count / self.size

    def display(self) -> None:
        for i in range(self.size):
            current = self.table[i]
            if current is not None:
                print(f"Index [{i}]:")
                while current is not None:
                    v = self._get_v(current.id_key)
                    h = self._hash(v)
                    print(f"  -> V={v} h={h} ID={current.id_key} "
                          f"C={current.c_flag} U={current.u_flag} T={current.t_flag} "
                          f"L={current.l_flag} D={current.d_flag} Pi='{current.pi_data}'")
                    current = current.p0_next