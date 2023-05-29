class Validator:
    def __init__(self, input):
        self.input = input

    def type_validation(self, data_type):
        try:
            data_type(self.input)
            return True
        except ValueError:
            return False

    def range_validator(self, start, end, equal_to_start=False, equal_to_end=False):
        if equal_to_start and equal_to_end:
            if start <= self.input <= end:
                return True
        elif equal_to_start:
            if start <= self.input < end:
                return True
        elif equal_to_end:
            if start < self.input <= end:
                return True
        else:
            if start < self.input < end:
                return True
        return False

    def option_validator(self, options):
        if self.input in options:
            return True
        return False
