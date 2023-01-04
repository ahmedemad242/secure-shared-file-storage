"""
FTP Client Presenter
"""
# pylint: disable=C0116
from typing import Union

import tkinter as tk


class FtpClientPresenter:
    """
    FTP Client Presenter
    """

    def connect(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def login(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def displayDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def changeDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def createDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def deleteDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def downloadFile(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def uploadFile(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def deleteFile(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def closeConnection(self, event: Union[tk.EventType, None] = None) -> None:
        pass

    def run(self) -> None:
        pass
