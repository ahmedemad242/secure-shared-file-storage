"""
This module connects to the FTP server and responsible for all operation on it.
"""
import ftplib


class UnableToConnect(Exception):
    """
    Unable to connect to the server exception.
    """


class NotAuthorized(Exception):
    """
    Unable to connect to the server exception.
    """


class FTPInvalidCommand(Exception):
    """
    Unable to connect to the server exception.
    """


class FTPConnectionModel:
    """
    FTP Connection class is useed to connect to the FTP server.
    responsible for all FTP operations.
    """

    def __init__(self) -> None:
        self.ftp = ftplib.FTP()

    def connectServer(self, ipAddress: str, port: int) -> str:
        """
        Connect to the FTP server.

        Parameters
        ----------
        ipAddress : str
            ip address of the ftp server
        port : int
            port number of the ftp server
        Returns
        -------
        str
            server response
        """

        try:
            return self.ftp.connect(ipAddress, port)
        except UnableToConnect as exc:
            print(exc)
            return "Unable to connect to the server"

    def login(self, username: str, password: str) -> str:
        """
        login to the FTP server.

        Parameters
        ----------
        username : str
            username to login with to the ftp server
        password : str
            password to login with to the ftp server
        Returns
        -------
        str
            server response
        """

        try:
            return self.ftp.login(username, password)
        except NotAuthorized as exc:
            print(exc)
            return "Unable to connect to the server"

    def changeDirectory(self, directoryName: str) -> str:
        """
        Change directory on the FTP client.

        Parameters
        ----------
        directoryName : str
            directoryName to change to
        Returns
        -------
        str
            server response
        """

        try:
            return self.ftp.cwd(directoryName)
        except FTPInvalidCommand as exc:
            print(exc)
            return "Unable to change directory"

    def deleteDirectory(self, directoryName: str) -> str:
        """
        Delete a directory on the FTP client.

        Parameters
        ----------
        directoryName : str
            directoryName to delete
        Returns
        -------
        str
            server response
        """

        try:
            return self.ftp.rmd(directoryName)
        except FTPInvalidCommand as exc:
            print(exc)
            return "Unable to delete directory"

    def createDirectory(self, directoryName: str) -> str:
        """
        Create a directory on the FTP client.

        Parameters
        ----------
        directoryName : str
            directoryName to create
        Returns
        -------
        str
            server response
        """

        try:
            return self.ftp.mkd(directoryName)
        except FTPInvalidCommand as exc:
            print(exc)
            return "Unable to create directory"

    def deleteFile(self, fileName: str) -> str:
        """
        delete a file on the FTP client.

        Parameters
        ----------
        fileName : str
            fileName to delete
        Returns
        -------
        str
            server response
        """

        try:
            return self.ftp.mkd(fileName)
        except FTPInvalidCommand as exc:
            print(exc)
            return "Unable to fileName file"

    def downloadFile(self, fileName: str) -> str:
        """
        download a file from the FTP client.

        Parameters
        ----------
        fileName : str
            fileName to download
        Returns
        -------
        str
            server response
        """

        try:
            with open(fileName, "wb") as downloadedFile:
                return f"Downloading {fileName}...\n" + self.ftp.retrbinary(
                    "RETR " + fileName, downloadedFile.write
                )
        except FTPInvalidCommand as exc:
            print(exc)
            return "Unable to download file"

    def uploadFile(self, fileName: str) -> str:
        """
        upload a file to the FTP client.

        Parameters
        ----------
        fileName : str
            fileName to upload
        Returns
        -------
        str
            server response
        """

        try:
            with open(fileName, "rb") as uploadFile:
                return f"Uploading {fileName}...\n" + self.ftp.storbinary(
                    "STOR " + fileName, uploadFile
                )
        except FTPInvalidCommand as exc:
            print(exc)
            return "Unable to upload file"

    def disconnect(self) -> str:
        """
        Close connection with the FTP server.

        Returns
        -------
        str
            server response
        """

        try:
            return "Closing connection...\n" + self.ftp.quit()
        except FTPInvalidCommand as exc:
            print(exc)
            return "Unable to close connection"
