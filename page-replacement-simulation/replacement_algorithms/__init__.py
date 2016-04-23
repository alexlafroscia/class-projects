from replacement_algorithms.opt import OptReplacement
from replacement_algorithms.nru import NRUReplacement
from replacement_algorithms.clock import ClockReplacement
from replacement_algorithms.wsc import WSCReplacement


def get_replacement_algorithm(name, *args):
    if name == 'opt':
        return OptReplacement(*args)
    if name == 'nru':
        return NRUReplacement(*args)
    if name == 'clock':
        return ClockReplacement(*args)
    if name == 'work':
        return WSCReplacement(*args)
    raise RuntimeError('Invalid algorithm specified')
