try:
    import PySimpleGUI as sg
except ImportError as e:
    raise ModuleNotFoundError('Sumo scenes require the "pysimplegui" Python package') from e
import os
from scenic.simulators.sumo.simulator import SumoSimulator as sim
from scenic.simulators.sumo.Utilities.config import SUMO as settings

class Interface:

    def __init__(self):
        """Creates the interface for Scenic Sumo integration.
        """
        self.sumo_config = {}
        _window = self.__initInterface()
        self.__windowLoop(_window)

    def __initInterface(self) -> sg.Window:
        """Creates the interface.

        Returns:
            [Window]: Information for the interface
        """
        sg.theme('DarkBlue')

        layout= [   [sg.T('Map File: '), sg.T("", key='map_path'), sg.B('Choose File', key='-Map-')],
                    [sg.T('Scenic File: '), sg.T("", key='scenic_path'),sg.B('Choose File', key='-Scene-')],
                    [sg.B('Run', key='-Run-'), sg.B('Cancel'), sg.B('Sumo Config.', key='-Config-')] 
                ]

        window = sg.Window('Sumo-Scenic', layout, size=(400,100))
        return window
    
    def __windowLoop(self, window):
        """Captures the users inputs.

        Args:
            window ([type]): Contains the information for the interface
        """
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            
            if event == "-Map-":
                map_file = self.__browseFileWindow("map")
                filename = os.path.basename(map_file)
                window['map_path'].update(filename)
            
            if event == "-Scene-":
                scene_file = self.__browseFileWindow("scenic")
                filename = os.path.basename(scene_file)
                window['scenic_path'].update(filename)

            if event == "-Run-":
                sim(map_file, scene_file, self.sumo_config)

            if event == '-Config-':
                sumo_config_window = self.__sumoConfigWindow()
                self.__sumoConfigLoop(sumo_config_window)
                

        window.close()

    def __sumoConfigWindow(self) -> sg.Window:
        """Creates the interface for the sumo configuration window.

        Returns:
            [Window]: A data object holding the layout of the window.
        """
        sg.theme('DarkBlue')
        layout = []

        for dict_key,val in settings.items():
            if type(val) == bool:
                layout += [sg.T(dict_key, size=(20,1)), sg.CB('', default=True, key = dict_key)],
            if type(val) == str or type(val) == int:
                layout += [sg.T(dict_key, size=(20,1)), sg.InputText(val, key = dict_key),],

        layout += [[sg.B('Save'), sg.CButton('Exit'), sg.T('', key='notif')]]
        
        sumo_config_window = sg.Window("Sumo Configurator", layout)

        return sumo_config_window

    def __sumoConfigLoop(self, window):
        """Captures the user's inputs in the sumo configuration window.

        Args:
            window (Window): A data object holding the layout of the window.
        """
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            if event == 'Save':
                self.sumo_config = values
                window['notif'].update("Saved")
    
    def __browseFileWindow(self, file_type : str) -> str:
        """Creates a file browse window.

        Args:
            file_type (str): A description of the file type being chosen.

        Returns:
            str: File of path chosen.
        """

        sg.theme('Dark Blue')

        browse_layout = [ [sg.T("Choose a " + file_type + " file.")],
                        [sg.InputText("file path", key = "-IN-"), sg.FileBrowse('Browse', key = "-File-")],
                        [sg.B("Ok", key = "-OK-"), sg.B("Cancel", key = "-Cancel-")] 
                        ]

        window = sg.Window('Choose File', browse_layout)

        while True:
            event, value = window.read()
            if event == sg.WIN_CLOSED or event == "-Cancel-":
                break

            if event == "-OK-":
                file = value.get("-IN-")
                window.close()
            
            if event == "-File-":
                window["-IN-"].update(value)
        try:
            return file
        except:
            window.close()
            return "No File Path Chosen"
