    def ReadVoltage(self):
            """
            Read raw values and convert them to voltages for middle (M) and left (L) LDR sensors.
            """
            """
            IMPLEMENTATION:
             - define GPIO-pins
             - set correct sequence for GPIO-pins
             - remove and rename ADC-pins definitions
             - rename variables dependent on LDR-readings in the rest of the code
            """
            
            # LDR activation pins
            adc_activation_pins=[Pin(22,Pin.OUT),Pin(19,Pin.OUT),Pin(18,Pin.OUT)]
            
            # LDR activation sequence
            LDR_number=[
                [?,?,?],
                [?,?,?],
                [?,?,?],
                [?,?,?],
                [?,?,?]
                ]
            
            step_sequence[step]
            
            def set_combination(combination):
                for pin in range(len(adc_activation_pins)):
                    adc_activation_pins[pin].value(sequence[pin])
            
            # LDR left far
            set_combination(sequence[0])
            raw_valueL2 = self.adc.read_u16()
            self.voltageL2 = raw_valueL2 * 3.3 / 65535
            
            # LDR left close
            set_combination(sequence[1])
            raw_valueL1 = self.adc.read_u16()
            self.voltageL1 = raw_valueL1 * 3.3 / 65535
            
            # LDR middle
            set_combination(sequence[2])
            raw_valueM = self.adc.read_u16()
            self.voltageM = raw_valueM * 3.3 / 65535
            
            # LDR right close
            set_combination(sequence[3])
            raw_valueR1 = self.adc.read_u16()
            self.voltageR1 = raw_valueR1 * 3.3 / 65535
            
            # LDR right far
            set_combination(sequence[4])
            raw_valueR2 = self.adc.read_u16()
            self.voltageR2 = raw_valueR2 * 3.3 / 65535