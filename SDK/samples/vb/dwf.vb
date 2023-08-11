Imports System.Runtime.InteropServices
Imports System.Text

Module dwf

    Public Const hdwfNone As Integer = 0

    ' device enumeration filters
    Public Const enumfilterAll As Integer            = 0
    Public Const enumfilterType As Integer           = &H8000000
    Public Const enumfilterUSB As Integer            = &H0000001
    Public Const enumfilterNetwork As Integer        = &H0000002
    Public Const enumfilterAXI As Integer            = &H0000004
    Public Const enumfilterRemote As Integer         = &H1000000
    Public Const enumfilterAudio As Integer          = &H2000000
    Public Const enumfilterDemo As Integer           = &H4000000

    ' device ID
    Public Const devidEExplorer As Integer    = 1
    Public Const devidDiscovery As Integer    = 2
    Public Const devidDiscovery2 As Integer   = 3
    Public Const devidDDiscovery As Integer   = 4
    Public Const devidADP3X50 As Integer      = 6
    Public Const devidEclypse As Integer      = 7
    Public Const devidADP5250 As Integer      = 8
    Public Const devidDPS3340 As Integer      = 9

    ' device version
    Public Const devverEExplorerC As Integer     = 2
    Public Const devverEExplorerE As Integer     = 4
    Public Const devverEExplorerF As Integer     = 5
    Public Const devverDiscoveryA As Integer     = 1
    Public Const devverDiscoveryB As Integer     = 2
    Public Const devverDiscoveryC As Integer     = 3

    ' trigger source
    Public Const trigsrcNone As Byte                 = 0
    Public Const trigsrcPC As Byte                   = 1
    Public Const trigsrcDetectorAnalogIn As Byte     = 2
    Public Const trigsrcDetectorDigitalIn As Byte    = 3
    Public Const trigsrcAnalogIn As Byte             = 4
    Public Const trigsrcDigitalIn As Byte            = 5
    Public Const trigsrcDigitalOut As Byte           = 6
    Public Const trigsrcAnalogOut1 As Byte           = 7
    Public Const trigsrcAnalogOut2 As Byte           = 8
    Public Const trigsrcAnalogOut3 As Byte           = 9
    Public Const trigsrcAnalogOut4 As Byte           = 10
    Public Const trigsrcExternal1 As Byte            = 11
    Public Const trigsrcExternal2 As Byte            = 12
    Public Const trigsrcExternal3 As Byte            = 13
    Public Const trigsrcExternal4 As Byte            = 14
    Public Const trigsrcHigh As Byte                 = 15
    Public Const trigsrcLow As Byte                  = 16

    ' instrument states:
    Public Const DwfStateReady As Byte          = 0
    Public Const DwfStateConfig As Byte         = 4
    Public Const DwfStatePrefill As Byte        = 5
    Public Const DwfStateArmed As Byte          = 1
    Public Const DwfStateWait As Byte           = 7
    Public Const DwfStateTriggered As Byte      = 3
    Public Const DwfStateRunning As Byte        = 3
    Public Const DwfStateDone As Byte           = 2

    '
    Public Const DECIAnalogInChannelCount As Integer   = 1
    Public Const DECIAnalogOutChannelCount As Integer   = 2
    Public Const DECIAnalogIOChannelCount As Integer   = 3
    Public Const DECIDigitalInChannelCount As Integer   = 4
    Public Const DECIDigitalOutChannelCount As Integer   = 5
    Public Const DECIDigitalIOChannelCount As Integer   = 6
    Public Const DECIAnalogInBufferSize As Integer   = 7
    Public Const DECIAnalogOutBufferSize As Integer   = 8
    Public Const DECIDigitalInBufferSize As Integer   = 9
    Public Const DECIDigitalOutBufferSize As Integer   = 10

    ' acquisition modes:
    Public Const acqmodeSingle As Integer       = 0
    Public Const acqmodeScanShift As Integer    = 1
    Public Const acqmodeScanScreen As Integer   = 2
    Public Const acqmodeRecord As Integer       = 3
    Public Const acqmodeOvers As Integer        = 4
    Public Const acqmodeSingle1 As Integer      = 5

    ' analog acquisition filter:
    Public Const filterDecimate As Integer   = 0
    Public Const filterAverage As Integer    = 1
    Public Const filterMinMax As Integer     = 2

    ' analog in trigger mode:
    Public Const trigtypeEdge As Integer           = 0
    Public Const trigtypePulse As Integer          = 1
    Public Const trigtypeTransition As Integer     = 2
    Public Const trigtypeWindow As Integer         = 3

    ' trigger slope:
    Public Const DwfTriggerSlopeRise As Integer     = 0
    Public Const DwfTriggerSlopeFall As Integer     = 1
    Public Const DwfTriggerSlopeEither As Integer   = 2

    ' trigger length condition
    Public Const triglenLess As Byte         = 0
    Public Const triglenTimeout As Byte      = 1
    Public Const triglenMore As Byte         = 2

    ' error codes for the functions:
    Public Const dwfercNoErc As Integer = 0        '  No error occurred
    Public Const dwfercUnknownError As Integer = 1        '  API waiting on pending API timed out
    Public Const dwfercApiLockTimeout As Integer = 2        '  API waiting on pending API timed out
    Public Const dwfercAlreadyOpened As Integer = 3        '  Device already opened
    Public Const dwfercNotSupported As Integer = 4        '  Device not supported
    Public Const dwfercInvalidParameter0 As Integer = &H10     '  Invalid parameter sent in API call
    Public Const dwfercInvalidParameter1 As Integer = &H11     '  Invalid parameter sent in API call
    Public Const dwfercInvalidParameter2 As Integer = &H12     '  Invalid parameter sent in API call
    Public Const dwfercInvalidParameter3 As Integer = &H13     '  Invalid parameter sent in API call
    Public Const dwfercInvalidParameter4 As Integer = &H14     '  Invalid parameter sent in API call

    ' analog out signal types
    Public Const funcDC As Byte = 0
    Public Const funcSine As Byte = 1
    Public Const funcSquare As Byte = 2
    Public Const funcTriangle As Byte = 3
    Public Const funcRampUp As Byte = 4
    Public Const funcRampDown As Byte = 5
    Public Const funcNoise As Byte = 6
    Public Const funcPulse As Byte = 7
    Public Const funcTrapezium As Byte = 8
    Public Const funcSinePower As Byte = 9
    Public Const funcCustom As Byte = 30
    Public Const funcPlay As Byte = 31

    ' analog io channel node types
    Public Const analogioEnable As Byte = 1
    Public Const analogioVoltage As Byte = 2
    Public Const analogioCurrent As Byte = 3
    Public Const analogioPower As Byte = 4
    Public Const analogioTemperature As Byte = 5
    Public Const analogioDmm As Byte = 6
    Public Const analogioRange As Byte = 7
    Public Const analogioMeasure As Byte = 8
    Public Const analogioTime As Byte = 9
    Public Const analogioFrequency As Byte = 10
    Public Const analogioResistance As Byte = 11

    Public Const AnalogOutNodeCarrier As Integer = 0
    Public Const AnalogOutNodeFM As Integer = 1
    Public Const AnalogOutNodeAM As Integer = 2

    Public Const DwfAnalogOutModeVoltage As Integer = 0
    Public Const DwfAnalogOutModeCurrent As Integer = 1

    Public Const DwfAnalogOutIdleDisable As Integer = 0
    Public Const DwfAnalogOutIdleOffset As Integer = 1
    Public Const DwfAnalogOutIdleInitial As Integer = 2

    Public Const DwfDigitalInClockSourceInternal As Integer = 0
    Public Const DwfDigitalInClockSourceExternal As Integer = 1

    Public Const DwfDigitalInSampleModeSimple As Integer = 0
    ' alternate samples: noise|sample|noise|sample|...  
    ' where noise is more than 1 transition between 2 samples
    Public Const DwfDigitalInSampleModeNoise As Integer = 1

    Public Const DwfDigitalOutOutputPushPull As Integer = 0
    Public Const DwfDigitalOutOutputOpenDrain As Integer = 1
    Public Const DwfDigitalOutOutputOpenSource As Integer = 2
    Public Const DwfDigitalOutOutputThreeState As Integer = 3 ' for custom and random

    Public Const DwfDigitalOutTypePulse As Integer = 0
    Public Const DwfDigitalOutTypeCustom As Integer = 1
    Public Const DwfDigitalOutTypeRandom As Integer = 2
    Public Const DwfDigitalOutTypeROM As Integer = 3
    Public Const DwfDigitalOutTypeFSM As Integer = 3

    Public Const DwfDigitalOutIdleInit As Integer = 0
    Public Const DwfDigitalOutIdleLow As Integer = 1
    Public Const DwfDigitalOutIdleHigh As Integer = 2
    Public Const DwfDigitalOutIdleZet As Integer = 3

    Public Const DwfAnalogImpedanceImpedance As Integer = 0 ' Ohms
    Public Const DwfAnalogImpedanceImpedancePhase As Integer = 1 ' Radians
    Public Const DwfAnalogImpedanceResistance As Integer = 2 ' Ohms
    Public Const DwfAnalogImpedanceReactance As Integer = 3 ' Ohms
    Public Const DwfAnalogImpedanceAdmittance As Integer = 4 ' Siemen
    Public Const DwfAnalogImpedanceAdmittancePhase As Integer = 5 ' Radians
    Public Const DwfAnalogImpedanceConductance As Integer = 6 ' Siemen
    Public Const DwfAnalogImpedanceSusceptance As Integer = 7 ' Siemen
    Public Const DwfAnalogImpedanceSeriesCapacitance As Integer = 8 ' Farad
    Public Const DwfAnalogImpedanceParallelCapacitance As Integer = 9 ' Farad
    Public Const DwfAnalogImpedanceSeriesInductance As Integer = 10 ' Henry
    Public Const DwfAnalogImpedanceParallelInductance As Integer = 11 ' Henry
    Public Const DwfAnalogImpedanceDissipation As Integer = 12 ' factor
    Public Const DwfAnalogImpedanceQuality As Integer = 13 ' factor
    Public Const DwfAnalogImpedanceVrms As Integer = 14 ' Vrms
    Public Const DwfAnalogImpedanceVreal As Integer = 15 ' V real
    Public Const DwfAnalogImpedanceVimag As Integer = 16 ' V imag
    Public Const DwfAnalogImpedanceIrms As Integer = 17 ' Irms
    Public Const DwfAnalogImpedanceIreal As Integer = 18 ' I real
    Public Const DwfAnalogImpedanceIimag As Integer = 19 ' I imag

    Public Const DwfParamUsbPower As Integer = 2 ' 1 keep the USB power enabled even when AUX is connected, Analog Discovery 2
    Public Const DwfParamLedBrightness As Integer = 3 ' LED brightness 0 ... 100%, Digital Discovery
    Public Const DwfParamOnClose As Integer = 4 ' 0 continue, 1 stop, 2 shutdown
    Public Const DwfParamAudioOut As Integer = 5 ' 0 disable / 1 enable audio output, Analog Discovery 1, 2
    Public Const DwfParamUsbLimit As Integer = 6 ' 0..1000 mA USB power limit, -1 no limit, Analog Discovery 1, 2
    Public Const DwfParamAnalogOut As Integer  = 7 ' 0 disable / 1 enable
    Public Const DwfParamFrequency As Integer  = 8 ' Hz
    Public Const DwfParamExtFreq As Integer  = 9 ' Hz
    Public Const DwfParamClockMode As Integer  = 10 ' 0 internal, 1 output, 2 input, 3 IO

    Public Const DwfWindowRectangular As Integer    = 0
    Public Const DwfWindowTriangular As Integer     = 1
    Public Const DwfWindowHamming As Integer        = 2
    Public Const DwfWindowHann As Integer           = 3
    Public Const DwfWindowCosine As Integer         = 4
    Public Const DwfWindowBlackmanHarris As Integer = 5
    Public Const DwfWindowFlatTop As Integer        = 6
    Public Const DwfWindowKaiser As Integer         = 7

    Public Const DwfAnalogCouplingDC As Integer = 0
    Public Const DwfAnalogCouplingAC As Integer = 1

    ' Macro used to verify if bit is 1 or 0 in given bit field
    ' #define IsBitSet(fs, bit) ((fs & (1<<bit)) != 0)


    ' Error and version APIs:
    <DllImport("dwf.dll", EntryPoint:="FDwfGetLastError", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfGetLastError(ByRef pdwferc As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfGetLastErrorMsg", CallingConvention:=CallingConvention.Cdecl)>
    Function _FDwfGetLastErrorMsg(<MarshalAs(UnmanagedType.LPStr)> ByVal szError As StringBuilder) As Integer
    End Function ' 512

    Function FDwfGetLastErrorMsg(ByRef szError As String) As Integer
        Dim ret As Integer
        Dim sb As StringBuilder = New StringBuilder(512)
        ret = _FDwfGetLastErrorMsg(sb)
        szError = sb.ToString()
        Return ret
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfGetVersion", CallingConvention:=CallingConvention.Cdecl)>
    Function _FDwfGetVersion(<MarshalAs(UnmanagedType.LPStr)> ByVal szVersion As StringBuilder) As Integer
    End Function ' 32
    ' Returns DLL version, for instance: "3.8.5"

    Function FDwfGetVersion(ByRef szVersion As String) As Integer
        Dim ret As Integer
        Dim sb As StringBuilder = New StringBuilder(32)
        ret = _FDwfGetVersion(sb)
        szVersion = sb.ToString()
        Return ret
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfParamSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfParamSet(ByVal param As Integer, ByVal value As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfParamGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfParamGet(ByVal param As Integer, ByRef pvalue As Integer) As Integer
    End Function


    ' DEVICE MANAGMENT FUNCTIONS
    ' Enumeration:
    <DllImport("dwf.dll", EntryPoint:="FDwfEnum", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnum(ByVal enumfilter As Integer, ByRef pcDevice As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumStart", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumStart(ByVal enumfilter As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumStop", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumStop(ByRef pcDevice As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumInfo(ByVal idxDevice As Integer, <MarshalAs(UnmanagedType.LPStr)> szOpt As String) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumDeviceType", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumDeviceType(ByVal idxDevice As Integer, ByRef pDeviceId As Integer, ByRef pDeviceRevision As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumDeviceIsOpened", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumDeviceIsOpened(ByVal idxDevice As Integer, ByRef pfIsUsed As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumUserName", CallingConvention:=CallingConvention.Cdecl)>
    Function _FDwfEnumUserName(ByVal idxDevice As Integer, <MarshalAs(UnmanagedType.LPStr)> ByVal szUserName As StringBuilder) As Integer
    End Function '32

    Function FDwfEnumUserName(ByVal idxDevice As Integer, ByRef szUserName As String) As Integer
        Dim ret As Integer
        Dim sb As StringBuilder = New StringBuilder(32)
        ret = _FDwfEnumUserName(idxDevice, sb)
        szUserName = sb.ToString()
        Return ret
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumDeviceName", CallingConvention:=CallingConvention.Cdecl)>
    Function _FDwfEnumDeviceName(ByVal idxDevice As Integer, <MarshalAs(UnmanagedType.LPStr)> ByVal szUserName As StringBuilder) As Integer
    End Function '32

    Function FDwfEnumDeviceName(ByVal idxDevice As Integer, ByRef szDeviceName As String) As Integer
        Dim ret As Integer
        Dim sb As StringBuilder = New StringBuilder(32)
        ret = _FDwfEnumDeviceName(idxDevice, sb)
        szDeviceName = sb.ToString()
        Return ret
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumSN", CallingConvention:=CallingConvention.Cdecl)>
    Function _FDwfEnumSN(ByVal idxDevice As Integer, <MarshalAs(UnmanagedType.LPStr)> ByVal szSN As StringBuilder) As Integer
    End Function '32

    Function FDwfEnumSN(ByVal idxDevice As Integer, ByRef szSN As String) As Integer
        Dim ret As Integer
        Dim sb As StringBuilder = New StringBuilder(32)
        ret = _FDwfEnumSN(idxDevice, sb)
        szSN = sb.ToString()
        Return ret
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumConfig", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumConfig(ByVal idxDevice As Integer, ByRef pcConfig As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumConfigInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumConfigInfo(ByVal idxConfig As Integer, ByVal info As Integer, ByRef pv As Integer) As Integer
    End Function


    ' Open/Close:
    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceOpen", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceOpen(ByVal idxDevice As Integer, ByRef phdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceOpenEx", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceOpenEx(<MarshalAs(UnmanagedType.LPStr)> szOpt As String, ByRef phdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceConfigOpen", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceConfigOpen(ByVal idxDev As Integer, ByVal idxCfg As Integer, ByRef phdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceClose", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceClose(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceCloseAll", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceCloseAll() As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceAutoConfigureSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceAutoConfigureSet(ByVal hdwf As Integer, ByVal fAutoConfigure As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceAutoConfigureGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceAutoConfigureGet(ByVal hdwf As Integer, ByRef pfAutoConfigure As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceEnableSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceEnableSet(ByVal hdwf As Integer, ByVal fEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceTriggerInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceTriggerInfo(ByVal hdwf As Integer, ByRef pfstrigsrc As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceTriggerSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceTriggerSet(ByVal hdwf As Integer, ByVal idxPin As Integer, ByVal trigsrc As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceTriggerGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceTriggerGet(ByVal hdwf As Integer, ByVal idxPin As Integer, ByRef ptrigsrc As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceTriggerPC", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceTriggerPC(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceTriggerSlopeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceTriggerSlopeInfo(ByVal hdwf As Integer, ByRef pfsslope As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceParamSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceParamSet(ByVal hdwf As Integer, ByVal param As Integer, ByVal value As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDeviceParamGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDeviceParamGet(ByVal hdwf As Integer, ByVal param As Integer, ByRef pvalue As Integer) As Integer
    End Function


    ' ANALOG IN INSTRUMENT FUNCTIONS
    ' Control and status: 
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInConfigure", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInConfigure(ByVal hdwf As Integer, ByVal fReconfigure As Integer, ByVal fStart As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerForce", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerForce(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatus(ByVal hdwf As Integer, ByVal fReadData As Integer, ByRef psts As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusSamplesLeft", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusSamplesLeft(ByVal hdwf As Integer, ByRef pcSamplesLeft As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusSamplesValid", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusSamplesValid(ByVal hdwf As Integer, ByRef pcSamplesValid As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusIndexWrite", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusIndexWrite(ByVal hdwf As Integer, ByRef pidxWrite As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusAutoTriggered", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusAutoTriggered(ByVal hdwf As Integer, ByRef pfAuto As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusData", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusData(ByVal hdwf As Integer, ByVal idxChannel As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdVoltData() As Double, ByVal cdData As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusData2", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusData2(ByVal hdwf As Integer, ByVal idxChannel As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdVoltData() As Double, ByVal idxData As Integer, ByVal cdData As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusData16", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusData16(ByVal hdwf As Integer, ByVal idxChannel As Integer, <MarshalAs(UnmanagedType.LPArray)> rgu16Data() As UShort, ByVal idxData As Integer, ByVal cdData As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusNoise", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusNoise(ByVal hdwf As Integer, ByVal idxChannel As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdMin() As Double, <MarshalAs(UnmanagedType.LPArray)> rgdMax() As Double, ByVal cdData As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusNoise2", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusNoise2(ByVal hdwf As Integer, ByVal idxChannel As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdMin() As Double, <MarshalAs(UnmanagedType.LPArray)> rgdMax() As Double, ByVal idxData As Integer, ByVal cdData As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusSample", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusSample(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pdVoltSample As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusRecord", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusRecord(ByVal hdwf As Integer, ByRef pcdDataAvailable As Integer, ByRef pcdDataLost As Integer, ByRef pcdDataCorrupt As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInRecordLengthSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInRecordLengthSet(ByVal hdwf As Integer, ByVal sLegth As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInRecordLengthGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInRecordLengthGet(ByVal hdwf As Integer, ByRef psLegth As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInStatusTime", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInStatusTime(ByVal hdwf As Integer, ByRef secUtc As UInteger, ByRef tick As UInteger, ByRef ticksPerSecond As UInteger) As Integer
    End Function


    ' Acquisition configuration:
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInFrequencyInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInFrequencyInfo(ByVal hdwf As Integer, ByRef phzMin As Double, ByRef phzMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInFrequencySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInFrequencySet(ByVal hdwf As Integer, ByVal hzFrequency As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInFrequencyGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInFrequencyGet(ByVal hdwf As Integer, ByRef phzFrequency As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInBitsInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInBitsInfo(ByVal hdwf As Integer, ByRef pnBits As Integer) As Integer
    End Function ' Returns the number of ADC bits 

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInBufferSizeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInBufferSizeInfo(ByVal hdwf As Integer, ByRef pnSizeMin As Integer, ByRef pnSizeMax As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInBufferSizeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInBufferSizeSet(ByVal hdwf As Integer, ByVal nSize As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInBufferSizeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInBufferSizeGet(ByVal hdwf As Integer, ByRef pnSize As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInNoiseSizeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInNoiseSizeInfo(ByVal hdwf As Integer, ByRef pnSizeMax As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInNoiseSizeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInNoiseSizeSet(ByVal hdwf As Integer, ByVal nSize As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInNoiseSizeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInNoiseSizeGet(ByVal hdwf As Integer, ByRef pnSize As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInAcquisitionModeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInAcquisitionModeInfo(ByVal hdwf As Integer, ByRef pfsacqmode As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInAcquisitionModeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInAcquisitionModeSet(ByVal hdwf As Integer, ByVal acqmode As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInAcquisitionModeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInAcquisitionModeGet(ByVal hdwf As Integer, ByRef pacqmode As Integer) As Integer
    End Function


    ' Channel configuration:
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelCount", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelCount(ByVal hdwf As Integer, ByRef pcChannel As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelEnableSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelEnableSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal fEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelEnableGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelEnableGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelFilterInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelFilterInfo(ByVal hdwf As Integer, ByRef pfsfilter As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelFilterSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelFilterSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal filter As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelFilterGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelFilterGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfilter As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelRangeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelRangeInfo(ByVal hdwf As Integer, ByRef pvoltsMin As Double, ByRef pvoltsMax As Double, ByRef pnSteps As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelRangeSteps", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelRangeSteps(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgVoltsStep() As Double, ByRef pnSteps As Integer) As Integer ' 32
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelRangeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelRangeSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal voltsRange As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelRangeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelRangeGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pvoltsRange As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelOffsetInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelOffsetInfo(ByVal hdwf As Integer, ByRef pvoltsMin As Double, ByRef pvoltsMax As Double, ByRef pnSteps As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelOffsetSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelOffsetSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal voltOffset As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelOffsetGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelOffsetGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pvoltOffset As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelAttenuationSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelAttenuationSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal xAttenuation As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelAttenuationGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelAttenuationGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pxAttenuation As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelBandwidthSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelBandwidthSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal hz As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelBandwidthGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelBandwidthGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef phz As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelImpedanceSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelImpedanceSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal ohms As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelImpedanceGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelImpedanceGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pohms As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelCouplingInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelCouplingInfo(ByVal hdwf As Integer, ByRef pfscoupling As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelCouplingSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelCouplingSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal coupling As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInChannelCouplingGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInChannelCouplingGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pcoupling As Integer) As Integer
    End Function


    ' Trigger configuration:
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerSourceSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerSourceSet(ByVal hdwf As Integer, ByVal trigsrc As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerSourceGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerSourceGet(ByVal hdwf As Integer, ByRef ptrigsrc As Byte) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerPositionInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerPositionInfo(ByVal hdwf As Integer, ByRef psecMin As Double, ByRef psecMax As Double, ByRef pnSteps As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerPositionSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerPositionSet(ByVal hdwf As Integer, ByVal secPosition As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerPositionGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerPositionGet(ByVal hdwf As Integer, ByRef psecPosition As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerPositionStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerPositionStatus(ByVal hdwf As Integer, ByRef psecPosition As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerAutoTimeoutInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerAutoTimeoutInfo(ByVal hdwf As Integer, ByRef psecMin As Double, ByRef psecMax As Double, ByRef pnSteps As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerAutoTimeoutSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerAutoTimeoutSet(ByVal hdwf As Integer, ByVal secTimeout As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerAutoTimeoutGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerAutoTimeoutGet(ByVal hdwf As Integer, ByRef psecTimeout As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerHoldOffInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerHoldOffInfo(ByVal hdwf As Integer, ByRef psecMin As Double, ByRef psecMax As Double, ByRef pnStep As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerHoldOffSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerHoldOffSet(ByVal hdwf As Integer, ByVal secHoldOff As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerHoldOffGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerHoldOffGet(ByVal hdwf As Integer, ByRef psecHoldOff As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerTypeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerTypeInfo(ByVal hdwf As Integer, ByRef pfstrigtype As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerTypeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerTypeSet(ByVal hdwf As Integer, ByVal trigtype As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerTypeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerTypeGet(ByVal hdwf As Integer, ByRef ptrigtype As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerChannelInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerChannelInfo(ByVal hdwf As Integer, ByRef pidxMin As Integer, ByRef pidxMax As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerChannelSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerChannelSet(ByVal hdwf As Integer, ByVal idxChannel As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerChannelGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerChannelGet(ByVal hdwf As Integer, ByRef pidxChannel As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerFilterInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerFilterInfo(ByVal hdwf As Integer, ByRef pfsfilter As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerFilterSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerFilterSet(ByVal hdwf As Integer, ByVal filter As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerFilterGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerFilterGet(ByVal hdwf As Integer, ByRef pfilter As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerLevelInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerLevelInfo(ByVal hdwf As Integer, ByRef pvoltsMin As Double, ByRef pvoltsMax As Double, ByRef pnSteps As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerLevelSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerLevelSet(ByVal hdwf As Integer, ByVal voltsLevel As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerLevelGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerLevelGet(ByVal hdwf As Integer, ByRef pvoltsLevel As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerHysteresisInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerHysteresisInfo(ByVal hdwf As Integer, ByRef pvoltsMin As Double, ByRef pvoltsMax As Double, ByRef pnSteps As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerHysteresisSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerHysteresisSet(ByVal hdwf As Integer, ByVal voltsLevel As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerHysteresisGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerHysteresisGet(ByVal hdwf As Integer, ByRef pvoltsHysteresis As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerConditionInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerConditionInfo(ByVal hdwf As Integer, ByRef pfstrigcond As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerConditionSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerConditionSet(ByVal hdwf As Integer, ByVal trigcond As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerConditionGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerConditionGet(ByVal hdwf As Integer, ByRef ptrigcond As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerLengthInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerLengthInfo(ByVal hdwf As Integer, ByRef psecMin As Double, ByRef psecMax As Double, ByRef pnSteps As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerLengthSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerLengthSet(ByVal hdwf As Integer, ByVal secLength As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerLengthGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerLengthGet(ByVal hdwf As Integer, ByRef psecLength As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerLengthConditionInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerLengthConditionInfo(ByVal hdwf As Integer, ByRef pfstriglen As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerLengthConditionSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerLengthConditionSet(ByVal hdwf As Integer, ByVal triglen As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerLengthConditionGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerLengthConditionGet(ByVal hdwf As Integer, ByRef ptriglen As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInSamplingSourceSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInSamplingSourceSet(ByVal hdwf As Integer, ByVal trigsrc As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInSamplingSourceGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInSamplingSourceGet(ByVal hdwf As Integer, ByRef ptrigsrc As Byte) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInSamplingSlopeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInSamplingSlopeSet(ByVal hdwf As Integer, ByVal slope As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInSamplingSlopeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInSamplingSlopeGet(ByVal hdwf As Integer, ByRef pslope As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInSamplingDelaySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInSamplingDelaySet(ByVal hdwf As Integer, ByVal sec As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInSamplingDelayGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInSamplingDelayGet(ByVal hdwf As Integer, ByRef psec As Double) As Integer
    End Function



    ' ANALOG OUT INSTRUMENT FUNCTIONS
    ' Configuration:
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutCount", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutCount(ByVal hdwf As Integer, ByRef pcChannel As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutMasterSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutMasterSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idxMaster As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutMasterGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutMasterGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pidxMaster As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutTriggerSourceSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutTriggerSourceSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal trigsrc As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutTriggerSourceGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutTriggerSourceGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef ptrigsrc As Byte) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutTriggerSlopeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutTriggerSlopeSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal slope As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutTriggerSlopeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutTriggerSlopeGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pslope As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRunInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRunInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef psecMin As Double, ByRef psecMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRunSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRunSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal secRun As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRunGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRunGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef psecRun As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRunStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRunStatus(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef psecRun As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutWaitInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutWaitInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef psecMin As Double, ByRef psecMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutWaitSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutWaitSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal secWait As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutWaitGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutWaitGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef psecWait As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRepeatInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRepeatInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pnMin As Integer, ByRef pnMax As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRepeatSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRepeatSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal cRepeat As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRepeatGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRepeatGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pcRepeat As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRepeatStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRepeatStatus(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pcRepeat As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRepeatTriggerSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRepeatTriggerSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal fRepeatTrigger As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutRepeatTriggerGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutRepeatTriggerGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfRepeatTrigger As Integer) As Integer
    End Function


    ' EExplorer channel 3&4 current/voltage limitation
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutLimitationInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutLimitationInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pMin As Double, ByRef pMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutLimitationSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutLimitationSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal limit As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutLimitationGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutLimitationGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef plimit As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutModeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutModeSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal mode As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutModeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutModeGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pmode As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutIdleInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutIdleInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfsidle As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutIdleSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutIdleSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idle As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutIdleGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutIdleGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pidle As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfsnode As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeEnableSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeEnableSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByVal fEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeEnableGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeEnableGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pfEnable As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeFunctionInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeFunctionInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pfsfunc As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeFunctionSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeFunctionSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByVal func As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeFunctionGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeFunctionGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pfunc As Byte) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeFrequencyInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeFrequencyInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef phzMin As Double, ByRef phzMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeFrequencySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeFrequencySet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByVal hzFrequency As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeFrequencyGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeFrequencyGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef phzFrequency As Double) As Integer
    End Function

    ' Carrier Amplitude or Modulation Index 
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeAmplitudeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeAmplitudeInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pMin As Double, ByRef pMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeAmplitudeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeAmplitudeSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByVal vAmplitude As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeAmplitudeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeAmplitudeGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pvAmplitude As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeOffsetInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeOffsetInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pMin As Double, ByRef pMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeOffsetSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeOffsetSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByVal vOffset As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeOffsetGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeOffsetGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pvOffset As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeSymmetryInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeSymmetryInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef ppercentageMin As Double, ByRef ppercentageMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeSymmetrySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeSymmetrySet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByVal percentageSymmetry As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeSymmetryGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeSymmetryGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef ppercentageSymmetry As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodePhaseInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodePhaseInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pdegreeMin As Double, ByRef pdegreeMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodePhaseSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodePhaseSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByVal degreePhase As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodePhaseGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodePhaseGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pdegreePhase As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeDataInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeDataInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef pnSamplesMin As Integer, ByRef pnSamplesMax As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodeDataSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodeDataSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdData() As Double, ByVal cdData As Integer) As Integer
    End Function


    ' needed for EExplorer, not used for ADiscovery
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutCustomAMFMEnableSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutCustomAMFMEnableSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal fEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutCustomAMFMEnableGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutCustomAMFMEnableGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfEnable As Integer) As Integer
    End Function


    ' Control:
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutReset(ByVal hdwf As Integer, ByVal idxChannel As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutConfigure", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutConfigure(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal fStart As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutStatus(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef psts As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodePlayStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodePlayStatus(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, ByRef cdDataFree As Integer, ByRef cdDataLost As Integer, ByRef cdDataCorrupted As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutNodePlayData", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutNodePlayData(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal node As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdData() As Double, ByVal cdData As Integer) As Integer
    End Function



    ' ANALOG IO INSTRUMENT FUNCTIONS
    ' Control:
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOConfigure", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOConfigure(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOStatus(ByVal hdwf As Integer) As Integer
    End Function


    ' Configure:
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOEnableInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOEnableInfo(ByVal hdwf As Integer, ByRef pfSet As Integer, ByRef pfStatus As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOEnableSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOEnableSet(ByVal hdwf As Integer, ByVal fMasterEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOEnableGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOEnableGet(ByVal hdwf As Integer, ByRef pfMasterEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOEnableStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOEnableStatus(ByVal hdwf As Integer, ByRef pfMasterEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelCount", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOChannelCount(ByVal hdwf As Integer, ByRef pnChannel As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelName", CallingConvention:=CallingConvention.Cdecl)>
    Function _FDwfAnalogIOChannelName(ByVal hdwf As Integer, ByVal idxChannel As Integer, <MarshalAs(UnmanagedType.LPStr)> ByVal szName As StringBuilder, <MarshalAs(UnmanagedType.LPStr)> ByVal szLabel As StringBuilder) As Integer
    End Function '32 16

    Function FDwfAnalogIOChannelName(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef szName As String, ByRef szLabel As String) As Integer
        Dim ret As Integer
        Dim sb1 As StringBuilder = New StringBuilder(32)
        Dim sb2 As StringBuilder = New StringBuilder(16)
        ret = _FDwfAnalogIOChannelName(hdwf, idxChannel, sb1, sb2)
        szName = sb1.ToString()
        szLabel = sb2.ToString()
        Return ret
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOChannelInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pnNodes As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelNodeName", CallingConvention:=CallingConvention.Cdecl)>
    Function _FDwfAnalogIOChannelNodeName(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idxNode As Integer, <MarshalAs(UnmanagedType.LPStr)> ByVal szNodeName As StringBuilder, <MarshalAs(UnmanagedType.LPStr)> ByVal szNodeUnits As StringBuilder) As Integer
    End Function '32 16

    Function FDwfAnalogIOChannelNodeName(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idxNode As Integer, ByRef szNodeName As String, ByRef szNodeUnits As String) As Integer
        Dim ret As Integer
        Dim sb1 As StringBuilder = New StringBuilder(32)
        Dim sb2 As StringBuilder = New StringBuilder(16)
        ret = _FDwfAnalogIOChannelNodeName(hdwf, idxChannel, idxNode, sb1, sb2)
        szNodeName = sb1.ToString()
        szNodeUnits = sb2.ToString()
        Return ret
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelNodeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOChannelNodeInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idxNode As Integer, ByRef panalogio As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelNodeSetInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOChannelNodeSetInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idxNode As Integer, ByRef pmin As Double, ByRef pmax As Double, ByRef pnSteps As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelNodeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOChannelNodeSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idxNode As Integer, ByVal value As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelNodeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOChannelNodeGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idxNode As Integer, ByRef pvalue As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelNodeStatusInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOChannelNodeStatusInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idxNode As Integer, ByRef pmin As Double, ByRef pmax As Double, ByRef pnSteps As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogIOChannelNodeStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogIOChannelNodeStatus(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal idxNode As Integer, ByRef pvalue As Double) As Integer
    End Function



    ' DIGITAL IO INSTRUMENT FUNCTIONS
    ' Control:
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOConfigure", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOConfigure(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOStatus(ByVal hdwf As Integer) As Integer
    End Function


    ' Configure:
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputEnableInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputEnableInfo(ByVal hdwf As Integer, ByRef pfsOutputEnableMask As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputEnableSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputEnableSet(ByVal hdwf As Integer, ByVal fsOutputEnable As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputEnableGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputEnableGet(ByVal hdwf As Integer, ByRef pfsOutputEnable As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputInfo(ByVal hdwf As Integer, ByRef pfsOutputMask As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputSet(ByVal hdwf As Integer, ByVal fsOutput As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputGet(ByVal hdwf As Integer, ByRef pfsOutput As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOInputInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOInputInfo(ByVal hdwf As Integer, ByRef pfsInputMask As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOInputStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOInputStatus(ByVal hdwf As Integer, ByRef pfsInput As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputEnableInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputEnableInfo64(ByVal hdwf As Integer, ByRef pfsOutputEnableMask As ULong) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputEnableSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputEnableSet64(ByVal hdwf As Integer, ByVal fsOutputEnable As ULong) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputEnableGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputEnableGet64(ByVal hdwf As Integer, ByRef pfsOutputEnable As ULong) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputInfo64(ByVal hdwf As Integer, ByRef pfsOutputMask As ULong) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputSet64(ByVal hdwf As Integer, ByVal fsOutput As ULong) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOOutputGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOOutputGet64(ByVal hdwf As Integer, ByRef pfsOutput As ULong) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOInputInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOInputInfo64(ByVal hdwf As Integer, ByRef pfsInputMask As ULong) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalIOInputStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalIOInputStatus64(ByVal hdwf As Integer, ByRef pfsInput As ULong) As Integer
    End Function



    ' DIGITAL IN INSTRUMENT FUNCTIONS
    ' Control and status: 
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInConfigure", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInConfigure(ByVal hdwf As Integer, ByVal fReconfigure As Integer, ByVal fStart As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatus(ByVal hdwf As Integer, ByVal fReadData As Integer, ByRef psts As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusSamplesLeft", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusSamplesLeft(ByVal hdwf As Integer, ByRef pcSamplesLeft As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusSamplesValid", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusSamplesValid(ByVal hdwf As Integer, ByRef pcSamplesValid As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusIndexWrite", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusIndexWrite(ByVal hdwf As Integer, ByRef pidxWrite As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusAutoTriggered", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusAutoTriggered(ByVal hdwf As Integer, ByRef pfAuto As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusData", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusData(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As Byte, ByVal countOfDataBytes As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusData2", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusData2(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As Byte, ByVal idxSample As Integer, ByVal countOfDataBytes As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusNoise", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusNoise(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As Byte, ByVal countOfDataBytes As Integer) As Integer
    End Function
    
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusNoise2", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusNoise2(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As Byte, ByVal idxSample As Integer, ByVal countOfDataBytes As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusData", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusDataUShort(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As UShort, ByVal countOfDataBytes As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusData2", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusData2UShort(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As UShort, ByVal idxSample As Integer, ByVal countOfDataBytes As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusNoise", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusNoiseUShort(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As UShort, ByVal countOfDataBytes As Integer) As Integer
    End Function
    
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusNoise2", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusNoise2UShort(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As UShort, ByVal idxSample As Integer, ByVal countOfDataBytes As Integer) As Integer
    End Function    

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusData", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusDataUInteger(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As UInteger, ByVal countOfDataBytes As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusData2", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusData2UInteger(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As UInteger, ByVal idxSample As Integer, ByVal countOfDataBytes As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusNoise", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusNoiseUInteger(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As UInteger, ByVal countOfDataBytes As Integer) As Integer
    End Function
    
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusNoise2", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusNoise2UInteger(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgData() As UInteger, ByVal idxSample As Integer, ByVal countOfDataBytes As Integer) As Integer
    End Function    

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInStatusRecord", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInStatusRecord(ByVal hdwf As Integer, ByRef pcdDataAvailable As Integer, ByRef pcdDataLost As Integer, ByRef pcdDataCorrupt As Integer) As Integer
    End Function


    ' Acquisition configuration:
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInInternalClockInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInInternalClockInfo(ByVal hdwf As Integer, ByRef phzFreq As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInClockSourceInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInClockSourceInfo(ByVal hdwf As Integer, ByRef pfsDwfDigitalInClockSource As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInClockSourceSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInClockSourceSet(ByVal hdwf As Integer, ByVal v As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInClockSourceGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInClockSourceGet(ByVal hdwf As Integer, ByRef pv As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInDividerInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInDividerInfo(ByVal hdwf As Integer, ByRef pdivMax As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInDividerSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInDividerSet(ByVal hdwf As Integer, ByVal div As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInDividerGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInDividerGet(ByVal hdwf As Integer, ByRef pdiv As UInteger) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInBitsInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInBitsInfo(ByVal hdwf As Integer, ByRef pnBits As Integer) As Integer
    End Function
    ' Returns the number of Digital In bits
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInSampleFormatSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInSampleFormatSet(ByVal hdwf As Integer, ByVal nBits As Integer) As Integer
    End Function
    ' valid options 8/16/32
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInSampleFormatGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInSampleFormatGet(ByVal hdwf As Integer, ByRef pnBits As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInInputOrderSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInInputOrderSet(ByVal hdwf As Integer, ByVal fDioFirst As Integer) As Integer
    End Function
    ' for Digital Discovery

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInBufferSizeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInBufferSizeInfo(ByVal hdwf As Integer, ByRef pnSizeMax As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInBufferSizeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInBufferSizeSet(ByVal hdwf As Integer, ByVal nSize As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInBufferSizeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInBufferSizeGet(ByVal hdwf As Integer, ByRef pnSize As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInSampleModeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInSampleModeInfo(ByVal hdwf As Integer, ByRef pfsDwfDigitalInSampleMode As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInSampleModeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInSampleModeSet(ByVal hdwf As Integer, ByVal v As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInSampleModeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInSampleModeGet(ByVal hdwf As Integer, ByRef pv As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInSampleSensibleSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInSampleSensibleSet(ByVal hdwf As Integer, ByVal fs As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInSampleSensibleGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInSampleSensibleGet(ByVal hdwf As Integer, ByRef pfs As UInteger) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInAcquisitionModeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInAcquisitionModeInfo(ByVal hdwf As Integer, ByRef pfsacqmode As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInAcquisitionModeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInAcquisitionModeSet(ByVal hdwf As Integer, ByVal acqmode As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInAcquisitionModeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInAcquisitionModeGet(ByVal hdwf As Integer, ByRef pacqmode As Integer) As Integer
    End Function


    ' Trigger configuration:
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerSourceSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerSourceSet(ByVal hdwf As Integer, ByVal trigsrc As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerSourceGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerSourceGet(ByVal hdwf As Integer, ByRef ptrigsrc As Byte) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerSlopeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerSlopeSet(ByVal hdwf As Integer, ByVal slope As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerSlopeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerSlopeGet(ByVal hdwf As Integer, ByRef pslope As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerPositionInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerPositionInfo(ByVal hdwf As Integer, ByRef pnSamplesAfterTriggerMax As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerPositionSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerPositionSet(ByVal hdwf As Integer, ByVal cSamplesAfterTrigger As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerPositionGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerPositionGet(ByVal hdwf As Integer, ByRef pcSamplesAfterTrigger As UInteger) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerPrefillSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerPrefillSet(ByVal hdwf As Integer, ByVal cSamplesBeforeTrigger As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerPrefillGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerPrefillGet(ByVal hdwf As Integer, ByRef pcSamplesBeforeTrigger As UInteger) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerAutoTimeoutInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerAutoTimeoutInfo(ByVal hdwf As Integer, ByRef psecMin As Double, ByRef psecMax As Double, ByRef pnSteps As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerAutoTimeoutSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerAutoTimeoutSet(ByVal hdwf As Integer, ByVal secTimeout As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerAutoTimeoutGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerAutoTimeoutGet(ByVal hdwf As Integer, ByRef psecTimeout As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerInfo(ByVal hdwf As Integer, ByRef pfsLevelLow As UInteger, ByRef pfsLevelHigh As UInteger, ByRef pfsEdgeRise As UInteger, ByRef pfsEdgeFall As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerSet(ByVal hdwf As Integer, ByVal fsLevelLow As UInteger, ByVal fsLevelHigh As UInteger, ByVal fsEdgeRise As UInteger, ByVal fsEdgeFall As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerGet(ByVal hdwf As Integer, ByRef pfsLevelLow As UInteger, ByRef pfsLevelHigh As UInteger, ByRef pfsEdgeRise As UInteger, ByRef pfsEdgeFall As UInteger) As Integer
    End Function

    ' the logic for trigger bits: Low and High and (Rise or Fall)
    ' bits set in Rise and Fall means any edge

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerResetSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerResetSet(ByVal hdwf As Integer, ByVal fsLevelLow As UInteger, ByVal fsLevelHigh As UInteger, ByVal fsEdgeRise As UInteger, ByVal fsEdgeFall As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerCountSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerCountSet(ByVal hdwf As Integer, ByVal cCount As Integer, ByVal fRestart As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerLengthSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerLengthSet(ByVal hdwf As Integer, ByVal secMin As Double, ByVal secMax As Double, ByVal idxSync As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerMatchSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerMatchSet(ByVal hdwf As Integer, ByVal iPin As Integer, ByVal fsMask As UInteger, ByVal fsValue As UInteger, ByVal cBitStuffing As Integer) As Integer
    End Function



    ' DIGITAL OUT INSTRUMENT FUNCTIONS
    ' Control:
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutConfigure", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutConfigure(ByVal hdwf As Integer, ByVal fStart As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutStatus(ByVal hdwf As Integer, ByRef psts As Byte) As Integer
    End Function


    ' Configuration:
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutInternalClockInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutInternalClockInfo(ByVal hdwf As Integer, ByRef phzFreq As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutTriggerSourceSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutTriggerSourceSet(ByVal hdwf As Integer, ByVal trigsrc As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutTriggerSourceGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutTriggerSourceGet(ByVal hdwf As Integer, ByRef ptrigsrc As Byte) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRunInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRunInfo(ByVal hdwf As Integer, ByRef psecMin As Double, ByRef psecMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRunSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRunSet(ByVal hdwf As Integer, ByVal secRun As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRunGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRunGet(ByVal hdwf As Integer, ByRef psecRun As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRunStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRunStatus(ByVal hdwf As Integer, ByRef psecRun As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutWaitInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutWaitInfo(ByVal hdwf As Integer, ByRef psecMin As Double, ByRef psecMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutWaitSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutWaitSet(ByVal hdwf As Integer, ByVal secWait As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutWaitGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutWaitGet(ByVal hdwf As Integer, ByRef psecWait As Double) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRepeatInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRepeatInfo(ByVal hdwf As Integer, ByRef pnMin As UInteger, ByRef pnMax As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRepeatSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRepeatSet(ByVal hdwf As Integer, ByVal cRepeat As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRepeatGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRepeatGet(ByVal hdwf As Integer, ByRef pcRepeat As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRepeatStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRepeatStatus(ByVal hdwf As Integer, ByRef pcRepeat As UInteger) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutTriggerSlopeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutTriggerSlopeSet(ByVal hdwf As Integer, ByVal slope As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutTriggerSlopeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutTriggerSlopeGet(ByVal hdwf As Integer, ByRef pslope As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRepeatTriggerSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRepeatTriggerSet(ByVal hdwf As Integer, ByVal fRepeatTrigger As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRepeatTriggerGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRepeatTriggerGet(ByVal hdwf As Integer, ByRef pfRepeatTrigger As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutCount", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutCount(ByVal hdwf As Integer, ByRef pcChannel As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutEnableSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutEnableSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal fEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutEnableGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutEnableGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfEnable As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutOutputInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutOutputInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfsDwfDigitalOutOutput As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutOutputSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutOutputSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal v As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutOutputGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutOutputGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pv As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutTypeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutTypeInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfsDwfDigitalOutType As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutTypeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutTypeSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal v As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutTypeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutTypeGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pv As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutIdleInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutIdleInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfsDwfDigitalOutIdle As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutIdleSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutIdleSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal v As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutIdleGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutIdleGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pv As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutDividerInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutDividerInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef vMin As UInteger, ByRef vMax As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutDividerInitSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutDividerInitSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal v As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutDividerInitGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutDividerInitGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pv As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutDividerSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutDividerSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal v As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutDividerGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutDividerGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pv As UInteger) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutCounterInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutCounterInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef vMin As UInteger, ByRef vMax As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutCounterInitSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutCounterInitSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal fHigh As Integer, ByVal v As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutCounterInitGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutCounterInitGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfHigh As Integer, ByRef pv As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutCounterSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutCounterSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal vLow As UInteger, ByVal vHigh As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutCounterGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutCounterGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pvLow As UInteger, ByRef pvHigh As UInteger) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRepetitionInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRepetitionInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef nMax As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRepetitionSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutCounterSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal cRepeat As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutRepetitionGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutRepetitionGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pcRepeat As UInteger) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutDataInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutDataInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pcountOfBitsMax As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutDataSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutDataSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, <MarshalAs(UnmanagedType.LPArray)> rgBits() As Byte, ByVal countOfBits As UInteger) As Integer
    End Function

    ' bits order is lsb first
    ' for TS output the count of bits its the total number of IO|OE bits, it should be an even number
    ' BYTE:   0                 |1     ...
    ' bit:    0 |1 |2 |3 |...|7 |0 |1 |...
    ' sample: IO|OE|IO|OE|...|OE|IO|OE|...


     <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutPlayDataSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutPlayDataSet(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgBits() As Byte, ByVal bitPerSample As UInteger, ByVal countOfBits As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutDataSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutDataSet(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> rgBits() As Byte, ByVal indexOfSample As UInteger, ByVal countOfBits As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutDataSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutDataSet(ByVal hdwf As Integer, ByVal hzRate As Double) As Integer
    End Function

    // UART
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartRateSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartRateSet(ByVal hdwf As Integer, ByVal hz As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartBitsSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartBitsSet(ByVal hdwf As Integer, ByVal cBits As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartParitySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartParitySet(ByVal hdwf As Integer, ByVal parity As Integer) As Integer
    End Function
    ' 0 none, 1 odd, 2 even

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartPolaritySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartPolaritySet(ByVal hdwf As Integer, ByVal parity As Integer) As Integer
    End Function
    ' 0 normal, 1 inverted
    
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartStopSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartStopSet(ByVal hdwf As Integer, ByVal cBit As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartTxSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartTxSet(ByVal hdwf As Integer, ByVal idxChannel As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartRxSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartRxSet(ByVal hdwf As Integer, ByVal idxChannel As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartTx", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartTx(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> szTx() As Byte, ByVal cTx As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalUartRx", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalUartRx(ByVal hdwf As Integer, <MarshalAs(UnmanagedType.LPArray)> szRx() As Byte, ByVal cRx As Integer, ByRef pcRx As Integer, ByRef pParity As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiFrequencySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiFrequencySet(ByVal hdwf As Integer, ByVal hz As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiClockSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiClockSet(ByVal hdwf As Integer, ByVal idxChannel As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiDataSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiDataSet(ByVal hdwf As Integer, ByVal idxDQ As Integer, ByVal idxChannel As Integer) As Integer
    End Function
    ' 0 DQ0_MOSI_SISO, 1 DQ1_MISO, 2 DQ2, 3 DQ3
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiModeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiModeSet(ByVal hdwf As Integer, ByVal iMode As Integer) As Integer
    End Function
    ' bit1 CPOL, bit0 CPHA
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiOrderSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiOrderSet(ByVal hdwf As Integer, ByVal fMSBLSB As Integer) As Integer
    End Function
    ' bit order: 0 MSB first, 1 LSB first

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiSelect", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiSelect(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal level As Integer) As Integer
    End Function
    ' level: 0 low, 1 high, -1 Z

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiWriteRead", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiWriteRead(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, <MarshalAs(UnmanagedType.LPArray)> rgTX() As Byte, ByVal cTX As Integer, <MarshalAs(UnmanagedType.LPArray)> rgRX() As Byte, ByVal cRX As Integer) As Integer
    End Function
    ' cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, ' 1-32 bits / word

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiWriteRead16", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiWriteRead16(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, <MarshalAs(UnmanagedType.LPArray)> rgTX() As UShort, ByVal cTX As Integer, <MarshalAs(UnmanagedType.LPArray)> rgRX() As UShort, ByVal cRX As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiWriteRead32", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiWriteRead32(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, <MarshalAs(UnmanagedType.LPArray)> rgTX() As Integer, ByVal cTX As Integer, <MarshalAs(UnmanagedType.LPArray)> rgRX() As Integer, ByVal cRX As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiRead", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiRead(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, <MarshalAs(UnmanagedType.LPArray)> rgRX() As Byte, ByVal cRX As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiReadOne", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiReadOne(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, ByRef pRX As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiRead16", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiRead16(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, <MarshalAs(UnmanagedType.LPArray)> rgRX() As UShort, ByVal cRX As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiRead32", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiRead32(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, <MarshalAs(UnmanagedType.LPArray)> rgRX() As Integer, ByVal cRX As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiWrite", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiWrite(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, <MarshalAs(UnmanagedType.LPArray)> rgTX() As Byte, ByVal cTX As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiWriteOne", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiWriteOne(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBits As Integer, ByVal vTX As UInteger) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiWrite16", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiWrite16(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, <MarshalAs(UnmanagedType.LPArray)> rgTX() As UShort, ByVal cTX As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalSpiWrite32", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalSpiWrite32(ByVal hdwf As Integer, ByVal cDQ As Integer, ByVal cBitPerWord As Integer, <MarshalAs(UnmanagedType.LPArray)> rgTX() As UInteger, ByVal cTX As Integer) As Integer
    End Function

    // I2C
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cClear", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cClear(ByVal hdwf As Integer, ByRef pfFree As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cStretchSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cStretchSet(ByVal hdwf As Integer, ByVal fEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cRateSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cRateSet(ByVal hdwf As Integer, ByVal hz As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cReadNakSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cReadNakSet(ByVal hdwf As Integer, ByVal fNakLastReadByte As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cSclSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cSclSet(ByVal hdwf As Integer, ByVal idxChannel As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cSdaSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cSdaSet(ByVal hdwf As Integer, ByVal idxChannel As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cWriteRead", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cWriteRead(ByVal hdwf As Integer, ByVal adr8bits As Byte, <MarshalAs(UnmanagedType.LPArray)> rgbTx() As Byte, ByVal cTx As Integer, <MarshalAs(UnmanagedType.LPArray)> rgRx() As Byte, ByVal cRx As Integer, ByRef pNak As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cRead", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cRead(ByVal hdwf As Integer, ByVal adr8bits As Byte, <MarshalAs(UnmanagedType.LPArray)> rgbRx() As Byte, ByVal cRx As Integer, ByRef pNak As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cWrite", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cWrite(ByVal hdwf As Integer, ByVal adr8bits As Byte, <MarshalAs(UnmanagedType.LPArray)> rgbTx() As Byte, ByVal cTx As Integer, ByRef pNak As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cWriteOne", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cWriteOne(ByVal hdwf As Integer, ByVal adr8bits As Byte, ByVal bTx As Byte, ByRef pNak As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cSpyStart", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cSpyStart(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalI2cSpyStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalI2cSpyStatus(ByVal hdwf As Integer, ByRef fStart As Integer, ByRef fStop As Integer, <MarshalAs(UnmanagedType.LPArray)> rgbRx() As Byte, ByRef cData As Integer, ByRef iNak As Integer) As Integer
    End Function

    // CAN
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalCanReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalCanReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalCanRateSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalCanRateSet(ByVal hdwf As Integer, ByVal hz As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalCanPolaritySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalCanPolaritySet(ByVal hdwf As Integer, ByVal fHigh As Integer) As Integer
    End Function
    ' 0 low, 1 high
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalCanTxSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalCanTxSet(ByVal hdwf As Integer, ByVal idxChannel As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalCanRxSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalCanRxSet(ByVal hdwf As Integer, ByVal idxChannel As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalCanTx", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalCanTx(ByVal hdwf As Integer, ByVal vID As Integer, ByVal fExtended As Integer, ByVal fRemote As Integer, ByVal cDLC As Integer, <MarshalAs(UnmanagedType.LPArray)> rgTX() As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalCanRx", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalCanRx(ByVal hdwf As Integer, ByRef pvID As Integer, ByRef pfExtended As Integer, ByRef pfRemote As Integer, ByRef pcDLC As Integer, <MarshalAs(UnmanagedType.LPArray)> rgRX() As Byte, ByVal cRX As Integer, ByRef pvStatus As Integer) As Integer
    End Function

    // Impedance
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceModeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceModeSet(ByVal hdwf As Integer, ByVal mode As Integer) As Integer
    End Function
    ' 0 W1-C1-DUT-C2-R-GND, 1 W1-C1-R-C2-DUT-GND, 8 Impedance Analyzer for AD
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceModeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceModeGet(ByVal hdwf As Integer, ByRef mode As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceReferenceSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceReferenceSet(ByVal hdwf As Integer, ByVal ohms As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceReferenceGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceReferenceGet(ByVal hdwf As Integer, ByRef pohms As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceFrequencySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceFrequencySet(ByVal hdwf As Integer, ByVal hz As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceFrequencyGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceFrequencyGet(ByVal hdwf As Integer, ByRef phz As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceAmplitudeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceAmplitudeSet(ByVal hdwf As Integer, ByVal volts As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceAmplitudeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceAmplitudeGet(ByVal hdwf As Integer, ByRef pvolts As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceOffsetSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceOffsetSet(ByVal hdwf As Integer, ByVal volts As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceOffsetGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceOffsetGet(ByVal hdwf As Integer, ByRef pvolts As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceProbeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceProbeSet(ByVal hdwf As Integer, ByVal ohmRes As Double, ByVal faradCap As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceProbeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceProbeGet(ByVal hdwf As Integer, ByRef pohmRes As Double, ByRef pfaradCap As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedancePeriodSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedancePeriodSet(ByVal hdwf As Integer, ByVal cMinPeriods As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedancePeriodGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedancePeriodGet(ByVal hdwf As Integer, ByRef cMinPeriods As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceCompReset", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceCompReset(ByVal hdwf As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceCompSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceCompSet(ByVal hdwf As Integer, ByVal ohmOpenResistance As Double, ByVal ohmOpenReactance As Double, ByVal ohmShortResistance As Double, ByVal ohmShortReactance As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceCompGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceCompGet(ByVal hdwf As Integer, ByRef pohmOpenResistance As Double, ByRef pohmOpenReactance As Double, ByRef pohmShortResistance As Double, ByRef pohmShortReactance As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceConfigure", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceConfigure(ByVal hdwf As Integer, ByVal fStart As Integer) As Integer
    End Function
    ' 1 start, 0 stop
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceStatus(ByVal hdwf As Integer, ByRef psts As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceStatusInput", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceStatusInput(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pgain As Double, ByRef pradian As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceStatusWarning", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceStatusInput(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pWarning As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogImpedanceStatusMeasure", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogImpedanceStatusMeasure(ByVal hdwf As Integer, ByVal measure As Integer, ByRef pvalue As Double) As Integer
    End Function

    // Miscellaneous
    <DllImport("dwf.dll", EntryPoint:="FDwfSpectrumWindow", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfSpectrumWindow(<MarshalAs(UnmanagedType.LPArray)> rgdWin() As Double, ByVal cdWin As Integer, ByVal vBeta As Double, ByRef vNEBW As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfSpectrumFFT", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfSpectrumFFT(<MarshalAs(UnmanagedType.LPArray)> rgdData() As Double, ByVal cdData As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdBin() As Double, <MarshalAs(UnmanagedType.LPArray)> rgdPhase() As Double, ByVal cdBin As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfSpectrumTransform", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfSpectrumTransform(<MarshalAs(UnmanagedType.LPArray)> rgdData() As Double, ByVal cdData As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdBin() As Double, <MarshalAs(UnmanagedType.LPArray)> rgdPhase() As Double, ByVal cdBin As Integer, ByVal iFirst As Double, ByVal iLast As Double) As Integer
    End Function




    ' OBSOLETE but supported, avoid using the following in new projects:
    Public Const DwfParamKeepOnClose As Byte = 1 ' keep the device running after close, use DwfParamOnClose

    ' use FDwfDigitalInTriggerSourceSet trigsrcAnalogIn
    ' call FDwfDigitalInConfigure before FDwfAnalogInConfigure
    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInMixedSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInMixedSet(ByVal hdwf As Integer, ByVal fEnable As Integer) As Integer
    End Function



    ' use int
    Public Const trigcondRisingPositive As Integer = 0
    Public Const trigcondFallingNegative As Integer = 1

    ' use FDwfDeviceTriggerInfo(hdwf, ptrigsrcInfo) As Integer
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogInTriggerSourceInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogInTriggerSourceInfo(ByVal hdwf As Integer, ByRef pfstrigsrc As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutTriggerSourceInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutTriggerSourceInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfstrigsrc As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalInTriggerSourceInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalInTriggerSourceInfo(ByVal hdwf As Integer, ByRef pfstrigsrc As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfDigitalOutTriggerSourceInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfDigitalOutTriggerSourceInfo(ByVal hdwf As Integer, ByRef pfstrigsrc As Integer) As Integer
    End Function


    ' use BYTE
    Public Const stsRdy As Byte = 0
    Public Const stsArm As Byte = 1
    Public Const stsDone As Byte = 2
    Public Const stsTrig As Byte = 3
    Public Const stsCfg As Byte = 4
    Public Const stsPrefill As Byte = 5
    Public Const stsNotDone As Byte = 6
    Public Const stsTrigDly As Byte = 7
    Public Const stsError As Byte = 8
    Public Const stsBusy As Byte = 9
    Public Const stsStop As Byte = 10


    ' use FDwfAnalogOutNode*
    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutEnableSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutEnableSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal fEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutEnableGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutEnableGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfEnable As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutFunctionInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutFunctionInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfsfunc As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutFunctionSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutFunctionSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal func As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutFunctionGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutFunctionGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pfunc As Byte) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutFrequencyInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutFrequencyInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef phzMin As Double, ByRef phzMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutFrequencySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutFrequencySet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal hzFrequency As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutFrequencyGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutFrequencyGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef phzFrequency As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutAmplitudeInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutAmplitudeInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pvoltsMin As Double, ByRef pvoltsMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutAmplitudeSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutAmplitudeSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal voltsAmplitude As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutAmplitudeGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutAmplitudeGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pvoltsAmplitude As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutOffsetInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutOffsetInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pvoltsMin As Double, ByRef pvoltsMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutOffsetSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutOffsetSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal voltsOffset As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutOffsetGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutOffsetGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pvoltsOffset As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutSymmetryInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutSymmetryInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef ppercentageMin As Double, ByRef ppercentageMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutSymmetrySet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutSymmetrySet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal percentageSymmetry As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutSymmetryGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutSymmetryGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef ppercentageSymmetry As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutPhaseInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutPhaseInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pdegreeMin As Double, ByRef pdegreeMax As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutPhaseSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutPhaseSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByVal degreePhase As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutPhaseGet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutPhaseGet(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pdegreePhase As Double) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutDataInfo", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutDataInfo(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef pnSamplesMin As Integer, ByRef pnSamplesMax As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutDataSet", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutDataSet(ByVal hdwf As Integer, ByVal idxChannel As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdData() As Double, ByVal cdData As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutPlayStatus", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutPlayStatus(ByVal hdwf As Integer, ByVal idxChannel As Integer, ByRef cdDataFree As Integer, ByRef cdDataLost As Integer, ByRef cdDataCorrupted As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfAnalogOutPlayData", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfAnalogOutPlayData(ByVal hdwf As Integer, ByVal idxChannel As Integer, <MarshalAs(UnmanagedType.LPArray)> rgdData() As Double, ByVal cdData As Integer) As Integer
    End Function


    <DllImport("dwf.dll", EntryPoint:="FDwfEnumAnalogInChannels", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumAnalogInChannels(ByVal idxDevice As Integer, ByRef pnChannels As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumAnalogInBufferSize", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumAnalogInBufferSize(ByVal idxDevice As Integer, ByRef pnBufferSize As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumAnalogInBits", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumAnalogInBits(ByVal idxDevice As Integer, ByRef pnBits As Integer) As Integer
    End Function

    <DllImport("dwf.dll", EntryPoint:="FDwfEnumAnalogInFrequency", CallingConvention:=CallingConvention.Cdecl)>
    Function FDwfEnumAnalogInFrequency(ByVal idxDevice As Integer, ByRef phzFrequency As Double) As Integer
    End Function

    Public Const enumfilterEExplorer As Integer      = 1
    Public Const enumfilterDiscovery As Integer      = 2
    Public Const enumfilterDiscovery2 As Integer     = 3
    Public Const enumfilterDDiscovery As Integer     = 4
    Public Const enumfilterSaluki As Integer         = 6


End Module
