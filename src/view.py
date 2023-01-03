"""
FTP Client GUI
"""
# pylint: disable=C0116

from typing import Protocol, Union

import tkinter as tk


class FtpClientPresenter(Protocol):
    """
    FTP Client Presenter
    """

    def connectServer(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def loginServer(self, event: Union[tk.EventType, None] = None) -> None:
        ...

    def displayDir(self, event: Union[tk.EventType, None] = None) -> None:
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


class FtpClientGui(tk.Tk):  # pylint: disable=R0902
    """
    FTP Client GUI
    """

    def __init__(self, presenter: FtpClientPresenter) -> None:
        super().__init__()
        self.title("FTP Client")
        self.geometry(f"{920}x{600}")

        self.sideBar = tk.Frame(self, width=140)

        # Connect
        self.ipLabel = tk.Label(text="IP Address")
        self.ipEntry = tk.Entry()
        self.portLabel = tk.Label(text="Port")
        self.portEntry = tk.Entry()
        self.connectButton = tk.Button(text="Connect", command=presenter.connectServer)

        # Login
        self.loginLabel = tk.Label(text="Username")
        self.loginEntry = tk.Entry()
        self.passLabel = tk.Label(text="Password")
        self.passEntry = tk.Entry()
        self.loginButton = tk.Button(text="Login", command=presenter.loginServer)

        # Server response text box
        self.serverMsgLabel = tk.Label(text="Server response:")
        self.serverMsgText = tk.Text(width=40)

        # Directory listing
        self.directoryLabel = tk.Label(text="Directory listing:")
        self.directoryListBox = tk.Listbox(width=10)

        # Options
        self.inputLabel = tk.Label(self.sideBar, text="Input")
        self.inputEnrty = tk.Entry(self.sideBar)
        self.changeDirectoryButton = tk.Button(
            self.sideBar, text="Change Directory", command=presenter.changeDirectory, width=15
        )
        self.createDirectoryButton = tk.Button(
            self.sideBar, text="Create Directory", command=presenter.createDirectory, width=15
        )
        self.deleteDirectoryButton = tk.Button(
            text="Delete Directory", command=presenter.deleteDirectory, width=15
        )
        self.deleteFileButton = tk.Button(
            text="Delete File", command=presenter.deleteFile, width=15
        )
        self.downloadFileButton = tk.Button(
            text="Download File", command=presenter.downloadFile, width=15
        )
        self.uploadFileButton = tk.Button(
            text="Upload File", command=presenter.uploadFile, width=15
        )
        self.disconnectButton = tk.Button(
            text="Disconnect", command=presenter.closeConnection, width=15
        )

        self.ipLabel.grid(row=0, column=0)
        self.ipEntry.grid(row=0, column=1)
        self.portLabel.grid(row=1, column=0)
        self.portEntry.grid(row=1, column=1)
        self.connectButton.grid(row=2, column=1, sticky="nesw")

        self.loginLabel.grid(row=0, column=2)
        self.loginEntry.grid(row=0, column=3)
        self.passLabel.grid(row=1, column=2)
        self.passEntry.grid(row=1, column=3)
        self.loginButton.grid(row=2, column=3, sticky="nesw")

        self.sideBar.grid(row=0, column=5, rowspan=4, sticky="nsew")

        self.serverMsgLabel.grid(row=3, column=0)
        self.serverMsgText.grid(row=4, column=0, columnspan=3, rowspan=5, sticky="nsew")

        self.directoryLabel.grid(row=3, column=3)
        self.directoryListBox.grid(row=4, column=3, columnspan=2, rowspan=5, sticky="nsew")

        self.inputLabel.grid(row=0, column=0)
        self.inputEnrty.grid(row=1)
        # self.changeDirectoryButton.grid(row=7, column=0, columnspan=5)
        # self.createDirectoryButton.grid(row=8, column=0, columnspan=5)
        # self.deleteDirectoryButton.grid(row=9, column=0, columnspan=5)
        # self.deleteFileButton.grid(row=10, column=0, columnspan=5)
        # self.downloadFileButton.grid(row=11, column=0, columnspan=5)
        # self.uploadFileButton.grid(row=12, column=0, columnspan=5)
        # self.disconnectButton.grid(row=13, column=0, columnspan=5)
