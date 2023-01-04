"""
Main module of the application.
"""

from .view import FTPClientGui
from .presenter import FTPClientPresenter
from .model import FTPConnectionModel


def main() -> None:
    """
    Main function of the application.
    """
    view = FTPClientGui()
    model = FTPConnectionModel()
    presenter = FTPClientPresenter(model, view)
    presenter.run()


if __name__ == "__main__":
    main()
