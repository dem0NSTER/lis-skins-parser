from tools.drivers import SteamDriver, LisSkinsDriver


def main(steam=True):
    if steam:
        cookies_updater = SteamDriver()
        cookies_updater.update_cookies()
    else:
        cookies_updater = LisSkinsDriver()
        cookies_updater.update_cookies()



main()
