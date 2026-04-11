from typing import Any, Optional

class HashNode:
    def __init__(self, id_key: str, pi_data: Any):
        self.id_key = id_key
        self.pi_data = pi_data
        self.c_flag = 0
        self.u_flag = 1
        self.t_flag = 1
        self.l_flag = 0
        self.d_flag = 0
        self.p0_next: Optional['HashNode'] = None