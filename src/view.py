"""
FTP Client GUI
"""

from typing import Protocol, Union, List, Dict
import tkinter as tk
import customtkinter as ctk


class FTPClientPresenter(Protocol):
    """
    FTP Client Presenter protocol
    """

    # pylint: disable=C0116

    def handleConnect(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def handleLogin(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def handleDisplayDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def handleChangeDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def handleCreateDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def handleDeleteDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def handleDownloadFile(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def handleUploadFile(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def handleDeleteFile(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def handleDisconnect(self, event: Union[tk.EventType, None] = None) -> None:
        ...


class FTPClientGui(ctk.CTk):  # type: ignore # pylint: disable=R0901
    """
    FTP Client GUI
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("FTP Client")
        self.geometry(f"{1100}x{600}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.entryWidgets: Dict[str, ctk.CTkEntry] = {}
        self.loginButton: ctk.CTkButton = None
        self.responseWidgets: Dict[str, ctk.CTkTextbox] = {}

    def buildGUI(self, presenter: FTPClientPresenter) -> None:
        """
        Build the GUI
        """
        self.buildSidebar()
        self.buildResponseSection()
        self.buildControlSection(presenter)
        self.buildConnectSection(presenter)
        self.buildLoginSection(presenter)

    def buildSidebar(self) -> None:
        """
        Build the sidebar frame with widgets
        The sidebar contain the name of the application and the appearance mode option menu
        """
        sideBarFrame = ctk.CTkFrame(self, width=140, corner_radius=0)
        sideBarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sideBarFrame.grid_rowconfigure(4, weight=1)
        nameLabel = ctk.CTkLabel(
            sideBarFrame,
            text="Secure FTP\nClient",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        nameLabel.grid(row=0, column=0, padx=20, pady=(20, 10))
        appearanceModeLabel = ctk.CTkLabel(sideBarFrame, text="Appearance Mode:", anchor="w")
        appearanceModeLabel.grid(row=5, column=0, padx=20, pady=(10, 0))
        appearanceModeOptioneMenu = ctk.CTkOptionMenu(
            sideBarFrame,
            values=["Light", "Dark", "System"],
            command=self.changeAppearanceModeEvent,
        )
        appearanceModeOptioneMenu.grid(row=6, column=0, padx=20, pady=(10, 30))

        appearanceModeOptioneMenu.set("Dark")

    def buildResponseSection(self) -> None:
        """
        Build the response section frame with widgets
        The response section contain the server response and the directory list text boxes
        """
        textBoxFrame = ctk.CTkFrame(self, fg_color="transparent")
        textBoxFrame.grid(row=0, column=1, columnspan=2, sticky="nsew")
        textBoxFrame.grid_columnconfigure((0, 1), weight=1)
        textBoxFrame.grid_rowconfigure(1, weight=1)

        serverResponseLabel = ctk.CTkLabel(textBoxFrame, text="Server Response")
        serverResponseLabel.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        serverResponseTextbox = ctk.CTkTextbox(textBoxFrame, width=250)
        serverResponseTextbox.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        serverResponseTextbox.configure(state="disabled")
        self.responseWidgets["serverResponseTextbox"] = serverResponseTextbox

        directoryListLabel = ctk.CTkLabel(textBoxFrame, text="Directory list")
        directoryListLabel.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        directoryListTextbox = ctk.CTkTextbox(textBoxFrame, width=100)
        directoryListTextbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        directoryListTextbox.configure(state="disabled")
        self.responseWidgets["directoryListTextbox"] = directoryListTextbox

    def buildConnectSection(self, presenter: FTPClientPresenter) -> None:
        """
        Build the connect section frame with widgets
        The connect section contain the connection details entry widgets
        for ip and port, and the connect button

        parameters
        ----------
        presenter: FtpClientPresenter
            The presenter for the ftp client
        """
        connectFrame = ctk.CTkFrame(self)
        connectFrame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        connectLabel = ctk.CTkLabel(master=connectFrame, text="Enter Connection Details")
        connectLabel.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="n")

        ipEntry = ctk.CTkEntry(master=connectFrame, placeholder_text="IP address")
        ipEntry.grid(row=1, column=2, padx=5, pady=5, sticky="n")
        self.entryWidgets["ipEntry"] = ipEntry

        portEntry = ctk.CTkEntry(master=connectFrame, placeholder_text="Port number")
        portEntry.grid(row=2, column=2, padx=5, pady=10, sticky="n")
        self.entryWidgets["portEntry"] = portEntry

        connectButton = ctk.CTkButton(connectFrame, command=presenter.handleConnect, text="Connect")
        connectButton.grid(row=3, column=2, padx=5, pady=10, sticky="n")

    def buildLoginSection(self, presenter: FTPClientPresenter) -> None:
        """
        Build the login section frame with widgets
        The login section contain the login details entry widgets
        for username and password, and the login button

        parameters
        ----------
        presenter: FtpClientPresenter
            The presenter for the ftp client
        """
        loginFrame = ctk.CTkFrame(self)
        loginFrame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        loginLabel = ctk.CTkLabel(master=loginFrame, text="Enter Login Information")
        loginLabel.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="n")

        usernameEntry = ctk.CTkEntry(master=loginFrame, placeholder_text="Username")
        usernameEntry.grid(row=1, column=2, padx=5, pady=5, sticky="n")
        self.entryWidgets["usernameEntry"] = usernameEntry

        passwordEntry = ctk.CTkEntry(master=loginFrame, placeholder_text="Password")
        passwordEntry.grid(row=2, column=2, padx=5, pady=10, sticky="n")
        self.entryWidgets["passwordEntry"] = passwordEntry

        self.loginButton = ctk.CTkButton(loginFrame, command=presenter.handleLogin, text="Login")
        self.loginButton.grid(row=3, column=2, padx=5, pady=10, sticky="n")
        self.loginButton.configure(state="disabled")

    def buildControlSection(self, presenter: FTPClientPresenter) -> None:
        """
        Build the control section frame with widgets
        The control section contain the main entry widget for
        file/directory name, and the contol buttons

        parameters
        ----------
        presenter: FtpClientPresenter
            The presenter for the ftp client
        """
        controlFrame = ctk.CTkFrame(self, fg_color="transparent")
        controlFrame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        controlFrame.grid_columnconfigure((0, 1, 2), weight=1)
        controlFrame.grid_rowconfigure(4, weight=1)

        mainEntry = ctk.CTkEntry(controlFrame, placeholder_text="Enter File/Directory name")
        mainEntry.grid(row=0, column=0, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.entryWidgets["mainEntry"] = mainEntry

        changeDirectoryButton = ctk.CTkButton(
            controlFrame, command=presenter.handleChangeDirectory, text="Change Directory"
        )
        changeDirectoryButton.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        createDirectoryButton = ctk.CTkButton(
            controlFrame, command=presenter.handleCreateDirectory, text="Create Directory"
        )
        createDirectoryButton.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        deleteDirectoryButton = ctk.CTkButton(
            controlFrame, command=presenter.handleDeleteDirectory, text="Delete Directory"
        )
        deleteDirectoryButton.grid(row=1, column=2, padx=20, pady=10, sticky="nsew")

        downloadFileButton = ctk.CTkButton(
            controlFrame, command=presenter.handleDownloadFile, text="Download File"
        )
        downloadFileButton.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        uploadFileButton = ctk.CTkButton(
            controlFrame, command=presenter.handleUploadFile, text="Upload File"
        )
        uploadFileButton.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        deleteFileButton = ctk.CTkButton(
            controlFrame, command=presenter.handleDeleteFile, text="Delete File"
        )
        deleteFileButton.grid(row=2, column=2, padx=20, pady=10, sticky="nsew")

        disconnectButton = ctk.CTkButton(
            controlFrame, command=presenter.handleDisconnect, text="Disconnect"
        )
        disconnectButton.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")

    def changeAppearanceModeEvent(self, appearanceMode: str) -> None:
        """
        Change the appearance mode of the application

        parameters
        ----------
        appearanceMode: str
            The appearance mode to change to (Dark/Light/System)
        """
        ctk.set_appearance_mode(appearanceMode)

    @property
    def mainInput(self) -> str:
        """
        Get the input from the main entry widget

        returns
        -------
        str
            The main input
        """
        return self.entryWidgets["mainEntry"].get()  # type: ignore

    @property
    def ipAddress(self) -> str:
        """
        Get the input from the ip address entry widget

        returns
        -------
        str
            The ip address input
        """
        return self.entryWidgets["ipEntry"].get()  # type: ignore

    @property
    def portNumber(self) -> str:
        """
        Get the input from the port number entry widget

        returns
        -------
        str
            The port number input
        """
        return self.entryWidgets["portEntry"].get()  # type: ignore

    @property
    def username(self) -> str:
        """
        Get the input from the username entry widget

        returns
        -------
        str
            The username input
        """
        return self.entryWidgets["usernameEntry"].get()  # type: ignore

    @property
    def password(self) -> str:
        """
        Get the input from the password entry widget

        returns
        -------
        str
            The password input
        """
        return self.entryWidgets["passwordEntry"].get()  # type: ignore

    def updateServerResponse(self, response: str) -> None:
        """
        Update the server response textbox with the response
        The

        parameters
        ----------
        response: str
            The response to update the textbox with
        """
        self.responseWidgets["serverResponseTextbox"].configure(state="normal")
        self.responseWidgets["serverResponseTextbox"].insert("end", response)
        self.responseWidgets["serverResponseTextbox"].configure(state="disabled")

    def updateDirectoryResponse(self, fileList: List[str]) -> None:
        """
        Update the directory response textbox with the directory list
        The text is replaced with the response

        parameters
        ----------
        fileList: List[str]
            The list of directories/files to update the textbox with
        """
        self.responseWidgets["directoryListTextbox"].configure(state="normal")
        self.responseWidgets["directoryListTextbox"].delete(1.0, "end")
        for file in fileList:
            self.responseWidgets["directoryListTextbox"].insert("end", file)
            self.responseWidgets["directoryListTextbox"].insert("end", "\n")
        self.responseWidgets["directoryListTextbox"].configure(state="disabled")

    def toggleLoginButton(self, state: str) -> None:
        """
        Toggle the login button state

        parameters
        ----------
        state: str
            The state to toggle the login button to
        """
        self.loginButton.configure(state=state)
