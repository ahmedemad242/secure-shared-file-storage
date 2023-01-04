"""
FTP Client GUI
"""
# pylint: disable=C0116

from typing import Protocol, Union, List

import tkinter as tk
import customtkinter as ctk  # pylint: disable=import-error


class FtpClientPresenter(Protocol):
    """
    FTP Client Presenter
    """

    def connect(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def login(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def displayDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def changeDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def createDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def deleteDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def downloadFile(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def uploadFile(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def deleteFile(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def closeConnection(self, event: Union[tk.EventType, None] = None) -> None:
        ...


class FtpClientGui(ctk.CTk):  # type: ignore # pylint: disable=R0902
    """
    FTP Client GUI
    """

    def __init__(self, presenter: FtpClientPresenter) -> None:  # pylint: disable=R0915
        super().__init__()
        self.title("FTP Client")
        self.geometry(f"{1100}x{600}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sideBarFrame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sideBarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sideBarFrame.grid_rowconfigure(4, weight=1)
        self.nameLabel = ctk.CTkLabel(
            self.sideBarFrame,
            text="Secure FTP\nClient",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearanceModeLabel = ctk.CTkLabel(
            self.sideBarFrame, text="Appearance Mode:", anchor="w"
        )
        self.appearanceModeLabel.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearanceModeOptioneMenu = ctk.CTkOptionMenu(
            self.sideBarFrame,
            values=["Light", "Dark", "System"],
            command=self.changeAppearanceModeEvent,
        )
        self.appearanceModeOptioneMenu.grid(row=6, column=0, padx=20, pady=(10, 30))

        # create server response, and directory list textboxes
        self.textBoxFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.textBoxFrame.grid(row=0, column=1, columnspan=2, sticky="nsew")
        self.textBoxFrame.grid_columnconfigure((0, 1), weight=1)
        self.textBoxFrame.grid_rowconfigure(1, weight=1)

        self.serverResponseLabel = ctk.CTkLabel(self.textBoxFrame, text="Server Response")
        self.serverResponseLabel.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.serverResponseTextbox = ctk.CTkTextbox(self.textBoxFrame, width=250)
        self.serverResponseTextbox.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.directoryListLabel = ctk.CTkLabel(self.textBoxFrame, text="Directory list")
        self.directoryListLabel.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.directoryListTextbox = ctk.CTkTextbox(self.textBoxFrame, width=100)
        self.directoryListTextbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create connect frame
        self.connectFrame = ctk.CTkFrame(self)
        self.connectFrame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.connectLabel = ctk.CTkLabel(master=self.connectFrame, text="Enter Connection Details")
        self.connectLabel.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="n")

        self.ipEntry = ctk.CTkEntry(master=self.connectFrame, placeholder_text="IP address")
        self.ipEntry.grid(row=1, column=2, padx=5, pady=5, sticky="n")

        self.portEntry = ctk.CTkEntry(master=self.connectFrame, placeholder_text="Port number")
        self.portEntry.grid(row=2, column=2, padx=5, pady=10, sticky="n")

        self.connectButton = ctk.CTkButton(
            self.connectFrame, command=presenter.connect, text="Connect"
        )
        self.connectButton.grid(row=3, column=2, padx=5, pady=10, sticky="n")

        # create login frame
        self.loginFrame = ctk.CTkFrame(self)
        self.loginFrame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.loginLabel = ctk.CTkLabel(master=self.loginFrame, text="Enter Login Information")
        self.loginLabel.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="n")

        self.usernameEntry = ctk.CTkEntry(master=self.loginFrame, placeholder_text="Username")
        self.usernameEntry.grid(row=1, column=2, padx=5, pady=5, sticky="n")

        self.passwordEntry = ctk.CTkEntry(master=self.loginFrame, placeholder_text="Password")
        self.passwordEntry.grid(row=2, column=2, padx=5, pady=10, sticky="n")

        self.loginButton = ctk.CTkButton(self.loginFrame, command=presenter.login, text="Login")
        self.loginButton.grid(row=3, column=2, padx=5, pady=10, sticky="n")

        # create control frame

        self.controlFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.controlFrame.grid(
            row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self.controlFrame.grid_columnconfigure((0, 1, 2), weight=1)
        self.controlFrame.grid_rowconfigure(4, weight=1)

        self.mainEntry = ctk.CTkEntry(
            self.controlFrame, placeholder_text="Enter File/Directory name"
        )
        self.mainEntry.grid(
            row=0, column=0, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )

        self.changeDirectoryButton = ctk.CTkButton(
            self.controlFrame, command=presenter.changeDirectory, text="Change Directory"
        )
        self.changeDirectoryButton.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.createDirectoryButton = ctk.CTkButton(
            self.controlFrame, command=presenter.changeDirectory, text="Create Directory"
        )
        self.createDirectoryButton.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        self.deleteDirectoryButton = ctk.CTkButton(
            self.controlFrame, command=presenter.changeDirectory, text="Delete Directory"
        )
        self.deleteDirectoryButton.grid(row=1, column=2, padx=20, pady=10, sticky="nsew")

        self.downloadFileButton = ctk.CTkButton(
            self.controlFrame, command=presenter.changeDirectory, text="Download File"
        )
        self.downloadFileButton.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.uploadFileButton = ctk.CTkButton(
            self.controlFrame, command=presenter.changeDirectory, text="Upload File"
        )
        self.uploadFileButton.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        self.deleteFileButton = ctk.CTkButton(
            self.controlFrame, command=presenter.changeDirectory, text="Delete File"
        )
        self.deleteFileButton.grid(row=2, column=2, padx=20, pady=10, sticky="nsew")

        self.disconnectButton = ctk.CTkButton(
            self.controlFrame, command=presenter.changeDirectory, text="Disconnect"
        )
        self.disconnectButton.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")

        # set default values
        self.serverResponseTextbox.insert(
            "0.0",
            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, \
            sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam \
            erat, sed diam voluptua.\n\n"
            * 20,
        )
        self.directoryListTextbox.insert(
            "0.0",
            "README.mds\nLICENSE\n",
        )
        self.loginButton.configure(state="disabled")
        self.serverResponseTextbox.configure(state="disabled")
        self.directoryListTextbox.configure(state="disabled")
        self.appearanceModeOptioneMenu.set("Dark")

    def changeAppearanceModeEvent(self, appearanceMode: str) -> None:
        ctk.set_appearance_mode(appearanceMode)

    @property
    def mainInput(self) -> str:
        return self.mainEntry.get()  # type: ignore

    @property
    def ipAddress(self) -> str:
        return self.ipEntry.get()  # type: ignore

    @property
    def portNumber(self) -> str:
        return self.portEntry.get()  # type: ignore

    @property
    def username(self) -> str:
        return self.usernameEntry.get()  # type: ignore

    @property
    def ipAddrpasswordess(self) -> str:
        return self.passwordEntry.get()  # type: ignore

    def updateServerResponse(self, response: str) -> None:
        self.serverResponseTextbox.configure(state="normal")
        self.serverResponseTextbox.insert("end", response)
        self.serverResponseTextbox.configure(state="disabled")

    def updateDirectoryResponse(self, dirlist: List[str]) -> None:
        self.directoryListTextbox.configure(state="normal")
        self.directoryListTextbox.delete(1.0, "end")
        for item in dirlist:
            self.directoryListTextbox.insert(0, item)
        self.directoryListTextbox.configure(state="disabled")
