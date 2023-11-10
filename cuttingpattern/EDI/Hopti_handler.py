import ctypes

class HOpti_Handler:
    def __init__(self) -> None:
        self.HOpti_DLL = ctypes.WinDLL("C:\HOpti\BIN\\Hopti.dll")

        HOPTI_GetOptiManipulatorHandle = ctypes.WINFUNCTYPE (
                                                        ctypes.c_void_p,
                                                        ctypes.c_char_p,
                                                        ctypes.c_char_p,
                                                    )
        HOPTI_GetOptiManipulatorHandle_Params = ("", "path", ""), ("", "prefix", "")
        self.GetManipulatorHandle = HOPTI_GetOptiManipulatorHandle(
                 ("HOPTI_GetOptiManipulatorHandle", self.HOpti_DLL),
                 HOPTI_GetOptiManipulatorHandle_Params
                )


        HOPTI_ManipulateLayout = ctypes.WINFUNCTYPE (
                                                        ctypes.c_char_p,
                                                        ctypes.c_void_p,
                                                        ctypes.c_char_p,
                                                    )
        HOPTI_ManipulateLayout_Params = ("", "path", ""), ("", "prefix", "")
        self.ManipulateLayout = HOPTI_GetOptiManipulatorHandle(
                 ("HOPTI_ManipulateLayout", self.HOpti_DLL),
                 HOPTI_ManipulateLayout_Params
                )
        
        HOPTI_FreeCuttingCode = ctypes.WINFUNCTYPE (
                                                        None,
                                                        ctypes.c_char_p,
                                                        ctypes.c_char_p,
                                                    )
        HOPTI_FreeCuttingCode_Params = ("", "path", ""), ("", "prefix", "")
        self.FreeCuttingCode = HOPTI_GetOptiManipulatorHandle(
                 ("HOPTI_FreeCuttingCode", self.HOpti_DLL),
                 HOPTI_FreeCuttingCode_Params
                )