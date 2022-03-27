# Interface
### Description 
`Interface` creates the interface and its scenes. 
### Syntax  
`interface()`
### Parameters
None 
### Returns  
None

--- 
## initInterface()  
### Description  
`initInterface()` creates the layout for the main interface for Sumo-Scenic.  
### Syntax  
`initInterface()`  
### Parameters  
None  
### Returns  
:`PySimpleGUI.Window`: a scene layout  

---  
## windowLoop()  
### Description  
`windowLoop()` is a loop that catches the user's interactions with the Sumo-Scenic scene.  
### Syntax  
`windowLoop(window)`  
### Parameters  
`window`: PySimpleGUI.Window: a scene layout  
### Returns  
None  

--- 
## sumoConfigWindow()  
### Description  
`sumoConfigWindow()` creates the window layout for the Sumo Configurator scene.  
### Syntax  
`sumoConfigWindow()`  
### Parameters  
None  
### Returns  
:PySimpleGUI.Window: a scene layout  

---  
## sumoConfigLoop()  
### Description  
`sumoConfigLoop()` is a loop that catches the users's interactions with the Sumo Configurator scene.  
### Syntax  
`sumoConfigLoop(window)`  
### Parameters  
`window`: PySimpleGUI.Window: a scene layout  
### Returns  
None  

---  
## browseFileWindow()  
### Description  
`broseFileWindow()` creates a browse file window. Use this over PySimpleGUI.FileBrowse() becuase the "Cancel" button in FileBrowse() closes the entire program instead of taking the user back to the previous scene.  
### Syntax  
`browseFileWindow(file_type)`  
### Parameters  
`file_type`: str: the file type wanted from the user  
### Returns  
:str: full path of file chosen 