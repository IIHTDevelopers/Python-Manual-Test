import random

class Sensor:
    def __init__(self, sensorId):
        self.sensorId = sensorId
        self.status = False

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

class DoorSensorManagementService:
    def __init__(self):
        self.sensors = {}

    def activateSensor(self, sensorId):
        if sensorId in self.sensors:
            self.sensors[sensorId].setStatus(True)
        else:
            print(f"Sensor {sensorId} not found.")

    def deactivateSensor(self, sensorId):
        if sensorId in self.sensors:
            self.sensors[sensorId].setStatus(False)
        else:
            print(f"Sensor {sensorId} not found.")

    def checkSensorStatus(self, sensorId):
        if sensorId in self.sensors:
            return self.sensors[sensorId].getStatus()
        else:
            print(f"Sensor {sensorId} not found.")
            return None

    def addSensor(self, sensor):
        self.sensors[sensor.sensorId] = sensor

class CentralLockingSystem:
    def __init__(self):
        self.sensors = []
        self.alerts = []
        self.vehicleParameters = VehicleParametersRepository()

    def lockAllDoors(self):
        for sensor in self.sensors:
            sensor.setStatus(True)
        print("All doors locked.")

    def unlockAllDoors(self):
        for sensor in self.sensors:
            sensor.setStatus(False)
        print("All doors unlocked.")

    def lockSingleDoor(self, doorId):
        for sensor in self.sensors:
            if sensor.sensorId == doorId:
                sensor.setStatus(True)
                print(f"Door {doorId} locked.")
                return
        print(f"Door {doorId} not found.")

    def unlockSingleDoor(self, doorId):
        for sensor in self.sensors:
            if sensor.sensorId == doorId:
                sensor.setStatus(False)
                print(f"Door {doorId} unlocked.")
                return
        print(f"Door {doorId} not found.")

    def analyzeLockStatus(self):
        for sensor in self.sensors:
            if not sensor.getStatus():
                return False
        return True

    def generateAlerts(self):
        if self.vehicleParameters.getEngineStatus() and not self.analyzeLockStatus():
            alertMessage = "Warning: Engine started but doors are not locked!"
            self.alerts.append(alertMessage)
            print(alertMessage)

class VehicleParametersRepository:
    def __init__(self):
        self.parameters = {}

    def updateParameters(self, vehicleId, parameters):
        self.parameters[vehicleId] = parameters

    def getParameters(self, vehicleId):
        return self.parameters.get(vehicleId, {})

    def getEngineStatus(self):
        for params in self.parameters.values():
            return params.get('engine_status', False)
        return False

class UserInterfaceService:
    @staticmethod
    def displayMenu():
        print(" 0. Quit.")
        print(" 1. Lock all doors.")
        print(" 2. Unlock all doors.")
        print(" 3. Lock single door.")
        print(" 4. Unlock single door.")
        print(" 5. Check lock status.")
        print(" 6. Generate alerts.")

    @staticmethod
    def displayLockStatus(status):
        print("All doors are locked." if status else "Not all doors are locked.")

    @staticmethod
    def displaySystemAlerts(alerts):
        if alerts:
            print("System Alerts:")
            for alert in alerts:
                print(alert)
        else:
            print("No alerts.")

class UserInterfaceController:
    def __init__(self, lockingSystem):
        self.lockingSystem = lockingSystem
        self.uiService = UserInterfaceService()

    def displayMenu(self):
        self.uiService.displayMenu()

    def processUserInput(self, choice):
        if choice == "0":
            print("Exiting program.")
            return False
        elif choice == "1":
            self.lockingSystem.lockAllDoors()
        elif choice == "2":
            self.lockingSystem.unlockAllDoors()
        elif choice == "3":
            doorId = input("Enter the door ID to lock: ")
            self.lockingSystem.lockSingleDoor(doorId)
        elif choice == "4":
            doorId = input("Enter the door ID to unlock: ")
            self.lockingSystem.unlockSingleDoor(doorId)
        elif choice == "5":
            status = self.lockingSystem.analyzeLockStatus()
            self.uiService.displayLockStatus(status)
        elif choice == "6":
            self.lockingSystem.generateAlerts()
            self.uiService.displaySystemAlerts(self.lockingSystem.alerts)
        else:
            print("Invalid choice. Please try again.")
        return True

class ErrorHandlingService:
    @staticmethod
    def handleSensorFailure(sensorId):
        print(f"Error: Sensor {sensorId} has failed.")

    @staticmethod
    def handleCommunicationError(errorMessage):
        print(f"Communication Error: {errorMessage}")

class AlertManagementService:
    def __init__(self):
        self.alertSettings = {}
        self.alerts = []

    def configureAlertSettings(self, alertSettings):
        self.alertSettings = alertSettings

    def sendAlert(self, alertMessage):
        self.alerts.append(alertMessage)
        print(f"Alert sent: {alertMessage}")

    def getAllAlerts(self):
        return self.alerts

    def clearAlerts(self):
        self.alerts.clear()
        print("Alerts cleared.")

def main():
    vehicleParams = VehicleParametersRepository()
    vehicleParams.updateParameters("VH001", {'engine_status': False})
    
    doorSensorManagement = DoorSensorManagementService()
    centralLockingSystem = CentralLockingSystem()
    uiController = UserInterfaceController(centralLockingSystem)

    doorSensor1 = Sensor("DS001")
    doorSensor2 = Sensor("DS002")
    doorSensor3 = Sensor("DS003")
    
    doorSensorManagement.addSensor(doorSensor1)
    doorSensorManagement.addSensor(doorSensor2)
    doorSensorManagement.addSensor(doorSensor3)

    centralLockingSystem.sensors.extend([doorSensor1, doorSensor2, doorSensor3])
    centralLockingSystem.vehicleParameters = vehicleParams

    while True:
        uiController.displayMenu()
        choice = input("Enter your choice: ")
        if not uiController.processUserInput(choice):
            break

if __name__ == "__main__":
    main()