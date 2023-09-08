# Define here the models for your scraped item
#
# See documentation in = Field()
# https = Field()//docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CollecterItem(Item):
    country = Field()
    company = Field()
    platform = Field() 
    endurance = Field()
    range_ = Field() 
    payload = Field()
    maxspeed = Field()
    altitude = Field()
    mass = Field() 
    width = Field()
    length = Field()

class Object(Item):
    name = Field()
    params = Field()

class Battery(Item):
    I = Field()
    C = Field() 
    formFactor = Field()

class Microcontroller(Item):
    frequency = Field()
    channels = Field()
    I = Field()
    U = Field()
    power = Field()
    channelResolution = Field()
    wirelessProtocol = Field()

class Motor(Item):
    U = Field()
    I = Field()
    R = Field()
    maximumPower = Field()
    battery = Field()
    maxI = Field()
    statorLength = Field()
    statorDiameter = Field()
    valDiameter = Field()
    rotationsNumber = Field()

class MotorController(Item):
    workI = Field()
    maxI = Field()
    energySupport = Field()

class FlightController(Item):
    isBarometer = Field()
    isBlack = Field()
    power = Field()
    proshivka = Field()
    isUSB = Field()
    handler = Field()

class Lidar(Item):
    maxRange = Field() 
    frequency = Field()
    power = Field()

class FlightControllerMicrocontroller(Item):
    frequency = Field()
    flashMemory = Field()
    handler = Field()
    minU = Field()
    maxU = Field()
    numberUARTports = Field()

class Rangefinder(Item): 
    maxRange = Field()
    frequency = Field()
    waveLength = Field()
    power = Field()

class MSS(Item):
    isBattery = Field()
    actionTime = Field()
    plusMinus = Field()

class HandlerPlatform(Item):
    maxSpeed = Field()
    upSpeed = Field()
    downSpeed = Field()
    maxRange = Field()
    maxAltitude = Field()
    energyConsuming = Field()
    payloadMass = Field()
    timeInAir = Field()
    screwsNumber = Field()

class Imager(Item):
    maxRange = Field()
    viewDistance = Field()
    interface = Field()
    U = Field()
    isBattery = Field()
    batteryTime = Field()
    POV = Field()
    zoom = Field()
    defenceClass = Field()
    workTempreture = Field()
    matrixType = Field()

class Copters(Item):
    maxSpeed = Field()
    upSpeed = Field()
    downSpeed = Field()
    maxRange = Field()
    maxAltitude = Field()
    powerConsume = Field()
    payloadMass = Field()
    timeInAir = Field()
    screwNumber = Field()

class CameraRetranslator(Item):
    frequency = Field()
    power = Field()
    channelNumber = Field()
    antennaInput = Field()

class Payload(Item):
    matrix = Field()
    camera = Field()
    zoom = Field()
    megaPixels = Field()
    resolution = Field()
    escort = Field()
    imagerResolution = Field()
    POV = Field()
    imager = Field()
    axisNumber = Field()
    accuracy = Field()
    pitch = Field()
    roll = Field()
    yaw = Field()
    power = Field()
    energySupply = Field()
    I = Field()
    antenna = Field()
    frequrency = Field()
    channelsNumber = Field()

class ControlPanel(Item):
    frequency = Field()
    channelsNumber = Field()
    I = Field()
    power = Field()
    powerTranslations = Field()
    channelResolution = Field()
    wirelessProtocol = Field()
