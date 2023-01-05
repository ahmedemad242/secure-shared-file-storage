"""
FTP Client Presenter
"""
from __future__ import annotations
from typing import Union, Protocol, List, Callable, Any
from functools import wraps

import tkinter as tk
import platform
import os
import subprocess

from src.file_handler.file_cryptographer import FileCryptographer
from .model import FTPConnectionModel, UnableToConnect, NotAuthorized, FTPError


def _newServerResponseEntry(
    func: Callable[[FTPClientPresenter, Any], Any],
) -> Callable[[FTPClientPresenter, Any], Any]:
    @wraps(func)
    def wrapper(self: FTPClientPresenter, *args: Any, **kwargs: Any) -> Any:
        result = func(self, *args, **kwargs)
        self.view.scrollDownServerResponse()
        self.view.updateServerResponse("\n")
        return result

    return wrapper


def _openExplorer(filePath: str) -> None:
    # pylint: disable=R1732
    """
    Open the file explorer to select a file.

    paramters
    ---------
    filePath: str
        The path to the file.
    """

    if platform.system() == "Windows":
        subprocess.Popen(["explorer", "/select,", filePath])
    else:
        subprocess.Popen(["xdg-open", filePath])


class FTPClientGui(Protocol):
    """
    View Protocol
    """

    # pylint: disable=C0116

    def buildGUI(self, presenter: FTPClientPresenter) -> None:
        ...

    @property
    def mainInput(self) -> str:
        ...

    @property
    def ipAddress(self) -> str:
        ...

    @property
    def portNumber(self) -> str:
        ...

    @property
    def username(self) -> str:
        ...

    @property
    def password(self) -> str:
        ...

    @property
    def rsaKey(self) -> str:
        ...

    @property
    def encryptedKeyFilePath(self) -> str:
        ...

    def updateServerResponse(self, response: str) -> None:
        ...

    def updateDirectoryResponse(self, fileList: List[str]) -> None:
        ...

    def toggleLoginButton(self, state: str) -> None:
        ...

    def toggleControlButtons(self, state: str) -> None:
        ...

    def scrollDownServerResponse(self) -> None:
        ...

    def mainloop(self) -> None:
        ...


class FTPClientPresenter:
    """
    FTP Client Presenter
    """

    # pylint: disable=W0613

    def __init__(self, model: FTPConnectionModel, view: FTPClientGui) -> None:
        self.model = model
        self.view = view

    @_newServerResponseEntry
    def handleConnect(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the connect button being pressed.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """
        try:
            msg = self.model.connect(
                self.view.ipAddress,
                int(self.view.portNumber),
            )
            self.view.updateServerResponse(msg)
            self.view.toggleLoginButton("normal")

        except UnableToConnect as exp:
            self.view.updateServerResponse(str(exp))
        except ValueError:
            self.view.updateServerResponse("Port number must be an integer")

    @_newServerResponseEntry
    def handleLogin(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the login button being pressed.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """
        try:
            msg = self.model.login(
                self.view.username,
                self.view.password,
            )
            self.view.updateServerResponse(msg)
            self.view.toggleControlButtons("normal")
            self._displayDirectory()
        except NotAuthorized as exp:
            self.view.updateServerResponse(str(exp))

    @_newServerResponseEntry
    def handleChangeDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the change directory button being pressed.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """
        try:
            msg = self.model.changeDirectory(self.view.mainInput)
            self.view.updateServerResponse(msg)
            self._displayDirectory()
        except FTPError as exp:
            self.view.updateServerResponse(str(exp))

    @_newServerResponseEntry
    def handleCreateDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the create directory button being pressed.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """
        try:
            msg = self.model.createDirectory(self.view.mainInput)
            self.view.updateServerResponse(msg)
            self._displayDirectory()
        except FTPError as exp:
            self.view.updateServerResponse(str(exp))

    @_newServerResponseEntry
    def handleDeleteDirectory(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the delete directory button being pressed.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """

        try:
            msg = self.model.deleteDirectory(self.view.mainInput)
            self.view.updateServerResponse(msg)
            self._displayDirectory()
        except FTPError as exp:
            self.view.updateServerResponse(str(exp))

    @_newServerResponseEntry
    def handleDownloadFile(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the download file button being pressed.

        Here we save the files to disk then remove them, the reason behind this is that
        the ftplib requires a file to be saved to disk.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """
        rsaKey = self.view.rsaKey
        encryptedKeyFilePath = self.view.mainInput + ".key.enc"
        encryptedFilePath = self.view.mainInput + ".enc"

        try:
            self.model.downloadFile(encryptedFilePath)
            if self.view.encryptedKeyFilePath == "":
                self.model.downloadFile(encryptedKeyFilePath)
            else:
                encryptedKeyFilePath = self.view.encryptedKeyFilePath

            FileCryptographer.decryptFile(
                encryptedFilePath, encryptedKeyFilePath, bytes(rsaKey, "utf-8")
            )

            os.remove(encryptedFilePath)
            if self.view.encryptedKeyFilePath == "":
                os.remove(encryptedKeyFilePath)

            decryptedFilePath = f"{os.getcwd()}/{self.view.mainInput}.dec"
            _openExplorer(decryptedFilePath)

            self.view.updateServerResponse("Downloaded and decrypted file: " + self.view.mainInput)

        except (FileNotFoundError, TypeError, ValueError, FTPError) as exp:
            self.view.updateServerResponse(str(exp))

    @_newServerResponseEntry
    def handleUploadFile(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the upload file button being pressed.

        Here we encrypt the file and then upload it to the server. The reason we save the encrypted
        to disk and then remove it is because the way the ftplib works.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """

        try:
            FileCryptographer.encryptFile(self.view.mainInput, bytes(self.view.rsaKey, "utf-8"))
            self.model.uploadFile(f"{self.view.mainInput}.enc")
            self.model.uploadFile(f"{self.view.mainInput}.key.enc")
            self.view.updateServerResponse(f"Uploaded file: {self.view.mainInput}")
            os.remove(f"{self.view.mainInput}.enc")
            os.remove(f"{self.view.mainInput}.key.enc")

            _openExplorer(os.getcwd())
            self._displayDirectory()
        except (FileNotFoundError, TypeError, ValueError, FTPError) as exp:
            self.view.updateServerResponse(str(exp))

    @_newServerResponseEntry
    def handleDeleteFile(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the delete file button being pressed.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """

        try:
            self.model.deleteFile(self.view.mainInput + ".enc")
            self.model.deleteFile(self.view.mainInput + ".key.enc")
            self.view.updateServerResponse(f"Deleted file: {self.view.mainInput}")
            self._displayDirectory()
        except FTPError as exp:
            self.view.updateServerResponse(str(exp))

    @_newServerResponseEntry
    def handleDisconnect(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the disconnect button being pressed.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """

        try:
            msg = self.model.disconnect()
            self.view.updateServerResponse(msg)
            self.view.toggleLoginButton("disabled")
            self.view.toggleControlButtons("disabled")
        except FTPError as exp:
            self.view.updateServerResponse(str(exp))

        self.view.updateServerResponse("\n")

    def _displayDirectory(self) -> None:
        """
        display directory in directory list response text box.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """

        fileList = self.model.displayDirectory()
        fileList = [fileName.replace(".enc", "") for fileName in fileList if ".key" not in fileName]
        self.view.updateDirectoryResponse(fileList)

    def run(self) -> None:
        """
        Run the application.
        """
        self.view.buildGUI(self)
        self.view.mainloop()
