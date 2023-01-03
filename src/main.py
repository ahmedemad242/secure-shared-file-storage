"""
Main module of the application.
"""
from view import FtpClientGui  # pylint: disable=no-name-in-module,import-error
from presenter import FtpClientPresenter  # pylint: disable=import-error


def main() -> None:
    """
    Main function of the application.
    """
    view = FtpClientGui()
    presenter = FtpClientPresenter()
    view.initGUi(presenter)
    view.mainloop()


if __name__ == "__main__":
    main()
