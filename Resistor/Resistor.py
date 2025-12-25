import random
class Resistor:
    @staticmethod
    def invoke(params={}):
        results=[]
        #Force current, measure voltage
        forcedCurrent = params["source_i_ma_A"]
        measuredVoltage = random.gauss(forcedCurrent*1e3, 10)
        resMeas = measuredVoltage/forcedCurrent
        results.append(1e-3*resMeas) #Append the results

        forcedCurrent = params["source_i_ma_B"]
        measuredVoltage = random.gauss(forcedCurrent*1e3, 10)
        resMeas = measuredVoltage/forcedCurrent
        results.append(1e-3*resMeas) #Append the results

        forcedCurrent = params["source_i_ma_C"]
        measuredVoltage = random.gauss(forcedCurrent*1e3, 10)
        resMeas = measuredVoltage/forcedCurrent
        results.append(1e-3*resMeas) #Append the results

        #Shutdown
        forcedCurrent=0.0
        return results