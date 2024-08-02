from proxy_db_manager import ProxyDBmanager
from main_proxy import ProxyFilter
from DB.data import list_of_proxies


def man():
    db_manager = ProxyDBmanager()
    filter_manager = ProxyFilter()

    # db_manager.create_table_proxies()
    # filter_manager.get_locations_values()
    # filter_manager.get_proxy_by_country('AR')
    filter_manager.check_proxies(list_of_proxies)


if __name__ == "__main__":
    man()
