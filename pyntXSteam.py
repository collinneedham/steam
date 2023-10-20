# pyntXSteam - pyXSteam in a pint wrapper
from pyXSteam.XSteam import XSteam

class pyntXSteam(object):

    PROP_UNITS = {
        't': 'K', 'tsat': 'K',
        'p': 'MPa', 'psat': 'MPa', 'pmelt': 'MPa', 'psubl': 'MPa',
        'h': "kJ/kg", 'hV': "kJ/kg", 'hL': "kJ/kg",
        'v': "m**3/kg", 'vV': "m**3/kg", 'vL': "m**3/kg",
        'rho': 'kg/m**3', 'rhoV': 'kg/m**3', 'rhoL': 'kg/m**3',
        's': 'kJ/(kg*C)', 'sV': 'kJ/(kg*C)', 'sL': 'kJ/(kg*C)',
        'u': 'kJ/kg', 'uV': 'kJ/kg', 'uL': 'kJ/kg',
        'Cp': 'kJ/(kg*C)', 'CpV': 'kJ/(kg*C)', 'CpL': 'kJ/(kg*C)',
        'Cv': 'kJ/(kg*C)', 'CvV': 'kJ/(kg*C)', 'CvL': 'kJ/(kg*C)',
        'w': 'm/s', 'wV': 'm/s', 'wL': 'm/s',
        'my': 'N*s/(m**2)',
        'tc': 'W/(m*C)', 'tcV': 'W/(m*C)', 'tcL': 'W/(m*C)',
        'st': 'N/m',
        'x': '',
        'vx': ''
    }

    # initialize XSteam object in m/kg/sec/K/MPa/W units
    def __init__(self, ureg):
        self._xsteam = XSteam(XSteam.UNIT_SYSTEM_BARE)
        self._u = ureg
    
    # parse function name to get input and output properties for conversion
    def __getattr__(self, name):
        def wrapper(*args):
            func = getattr(self._xsteam, name)
            out_prop, in_props = name.split('_', 1)

            # split input props
            if len(in_props) == 1:
                in1 = args[0].to(pyntXSteam.PROP_UNITS[in_props]).magnitude
                out_value = func(in1)
            elif len(in_props) < 5:
                in1 = args[0].to(pyntXSteam.PROP_UNITS[in_props[0]]).magnitude
                in2 = args[1].to(pyntXSteam.PROP_UNITS[in_props[1:]]).magnitude
                out_value = func(in1, in2)
            else:
                raise Exception("Unsupported function")
            
            # return value with units 
            return out_value * self._u(pyntXSteam.PROP_UNITS[out_prop])
        return wrapper


# simple tests
if __name__ == "__main__":
    import pint
    ureg = pint.UnitRegistry()
    ureg.autoconvert_offset_to_baseunit = True
    steam = pyntXSteam(ureg)

    press = 1 * ureg('atm')
    temp = 212 * ureg('degF')
    x = 0.5 * ureg('')
    rho = 1000 * ureg('kg/m**3')

    print(steam.tsat_p(press))
    print(steam.h_px(press, x))
    print(steam.psat_t(temp))
    print(steam.pmelt_t(temp))
