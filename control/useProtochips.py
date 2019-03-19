
from pywinauto.application import Application as app

class UseProtochips:

    def connectToProtochips(username):
        protoConnect = app(backend="win32").connect(path=r"C:\\Users\\Protochips\\Desktop\\Aduro V 2.2.4\\Release\\Aduro.exe")
        protoMainWindow = protoConnect['Protochips: Aduro 500 V2.2.4']

        protoMainWindow.Edit6.set_text(username)
        protoMainWindow['I Agree'].click()

        return protoMainWindow

    def chipSetup(protoMainWindow,chipType,expTemplate,measMode):

        protoMainWindow['Chip TypeComboBox'].select(chipType)

        protoMainWindow['Experiment TemplateComboBox'].select(expTemplate)
        protoMainWindow['Measurement ModeComboBox'].select(measMode)

    def channelSetup(protoMainWindow,voltageFunc,voltageMode):

        protoMainWindow['Channel A Setup'].click()
        protoMainWindow['FunctionComboBox'].select(voltageFunc)
        protoMainWindow['ModeComboBox'].select(voltageMode)


    def waveformGen(protoMainWindow,numSteps)

#%%


proto = autoProto.connectToProtochips('Abinash')

autoProto.chipSetup(proto,'Electrical','Electrical DC Voltage Bias','Normal')

autoProto.channelSetup(proto,'VoltageSource','Waveform')

proto['ModeButton2'].click()

proto['ModeComboBox'].select('Waveform')

protoMainWindow.print_control_identifiers()



app.Kill_()
