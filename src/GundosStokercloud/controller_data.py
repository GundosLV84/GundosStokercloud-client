import decimal
from enum import Enum


class NotConnectedException(Exception):
    pass


class PowerState(Enum):
    ON = 1
    OFF = 0


class Unit(Enum):
    KWH = 'kwh'
    PERCENT = 'pct'
    DEGREE = 'deg'
    KILO_GRAM = 'kg'
    GRAM = 'g'
    M3HOUR = 'm3/h'
    PASCAL = 'Pa'


class State(Enum):
    POWER = 'state_5'
    HOT_WATER = 'state_7'
    IGNITION_1 = 'state_2'
    IGNITION_2 = 'state_4'
    FAULT_IGNITION = 'state_13'
    OFF = 'state_14'


STATE_BY_VALUE = {key.value: key for key in State}


class Value:
    def __init__(self, value, unit):
        self.value = decimal.Decimal(value)
        self.unit = unit

    def __eq__(self, other):
        if not isinstance(other, Value):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.value == other.value and self.unit == other.unit

    def __repr__(self):
        return "%s %s" % (self.value, self.unit)

def get_from_list_by_key(lst, key, value):
    for itm in lst:
        if itm.get(key) == value:
            return itm

class ControllerData:
    def __init__(self, data):
        if data['notconnected'] != 0:
            raise NotConnectedException("Furnace/boiler not connected to StokerCloud")
        self.data = data

    def get_sub_item(self, submenu, _id):
        return get_from_list_by_key(self.data[submenu], 'id', _id)

    @property
    def alarm(self):
        return {
            0: PowerState.OFF,
            1: PowerState.ON
        }.get(self.data['miscdata'].get('alarm'))

    @property
    def running(self):
        return {
            0: PowerState.OFF,
            1: PowerState.ON
        }.get(self.data['miscdata'].get('running'))

    @property
    def serial_number(self):
        return self.data['serial']

    @property
    def boiler_temperature_current(self):
        return Value(self.get_sub_item('frontdata', 'boilertemp')['value'], Unit.DEGREE)

    @property
    def boiler_temperature_requested(self):
        return Value(self.get_sub_item('frontdata', '-wantedboilertemp')['value'], Unit.DEGREE)

    @property
    def boiler_kwh(self):
        return Value(self.get_sub_item('boilerdata', '5')['value'], Unit.KWH)

    @property
    def state(self):
        return STATE_BY_VALUE.get(self.data['miscdata']['state']['value'])

    @property
    def hotwater_temperature_current(self):
        return Value(self.get_sub_item('frontdata', 'dhw')['value'], Unit.DEGREE)

    @property
    def hotwater_temperature_requested(self):
        return Value(self.get_sub_item('frontdata', 'dhwwanted')['value'], Unit.DEGREE)

    @property
    def consumption_total(self):
        return Value(self.get_sub_item('hopperdata', '4')['value'], Unit.KILO_GRAM)
    
    @property
    def consumption_day(self):
        return Value(self.get_sub_item('hopperdata', '3')['value'], Unit.KILO_GRAM)

    @property
    def boiler_powerPrc(self):
        return Value(self.get_sub_item('boilerdata', '4')['value'], Unit.PERCENT)
    
    @property
    def boiler_returntemp(self):
        return Value(self.get_sub_item('boilerdata', '3')['value'], Unit.DEGREE)
    
    @property
    def boiler_actualo2(self):
        return Value(self.get_sub_item('boilerdata', '12')['value'], Unit.PERCENT)
    
    @property
    def hopper_content(self):
        return Value(self.get_sub_item('frontdata', 'hoppercontent')['value'], Unit.KILO_GRAM)
    
    @property
    def wanted_o2(self):
        return Value(self.get_sub_item('frontdata', 'refoxygen')['value'], Unit.PERCENT)

    @property
    def wanted_air(self):
        return Value(self.get_sub_item('frontdata', 'refair')['value'], Unit.M3HOUR)
    
    @property
    def photosensor(self):
        return Value(self.get_sub_item('boilerdata', '6')['value'], Unit.PERCENT)
    
    @property
    def backpressure(self):
        return STATE_BY_VALUE.get(self.data['miscdata']['backpressure'])
    
    @property
    def exhaust_fan(self):
        return STATE_BY_VALUE.get(self.data['leftoutput']['output-5']['val'])