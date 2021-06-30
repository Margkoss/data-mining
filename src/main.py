from .lib.app_manager import AppManager


def bootstrap_application():
    AppManager().initialize()
