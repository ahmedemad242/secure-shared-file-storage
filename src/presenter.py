"""
FTP Client Presenter
"""
from __future__ import annotations
from typing import Union, Protocol, List, Callable, Any
from functools import wraps
import tkinter as tk
import os

from src.file_handler.file_cryptographer import FileCryptographer
from .model import FTPConnectionModel, UnableToConnect, NotAuthorized, FTPError


def _newServerResponseEntry(
    func: Callable[[FTPClientPresenter, Union[tk.EventType, None]], None],
) -> Callable[[FTPClientPresenter, Union[tk.EventType, None]], None]:
    @wraps(func)
    def wrapper(self: FTPClientPresenter, *args: Any, **kwargs: Any) -> Any:
        result = func(self, *args, **kwargs)
        self.view.scrollDownServerResponse()
        self.view.updateServerResponse("\n")
        return result

    return wrapper


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
    def key(self) -> str:
        ...

    def updateServerResponse(self, response: str) -> None:
        ...

    def updateDirectoryResponse(self, fileList: List[str]) -> None:
        ...

    def toggleLoginButton(self, state: str) -> None:
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

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """

        try:
            msg = self.model.downloadFile(self.view.mainInput)
            self.view.updateServerResponse(msg)
            self._displayDirectory()
        except FTPError as exp:
            self.view.updateServerResponse(str(exp))

    @_newServerResponseEntry
    def handleUploadFile(self, event: Union[tk.EventType, None] = None) -> None:
        """
        Handle the upload file button being pressed.

        paramters
        ---------
        event: Union[tk.EventType, None]
            The event that triggered the function call.
        """

        try:
            FileCryptographer.encryptFile(self.view.mainInput, bytes(self.view.key, "utf-8"))
            self.model.uploadFile(f"{self.view.mainInput}.enc")
            self.model.uploadFile(f"{self.view.mainInput}.key.enc")
            self.view.updateServerResponse(f"Uploaded file: {self.view.mainInput}")
            os.remove(f"{self.view.mainInput}.enc")
            os.remove(f"{self.view.mainInput}.key.enc")
            self._displayDirectory()
        except (FileNotFoundError, ValueError, FTPError) as exp:
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
