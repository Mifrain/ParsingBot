from sqlalchemy import insert, select, exists, update, delete

from bot.db.models import Site
from bot.db.base import sync_session

from bot.helpers.schemas import SiteInput

db = sync_session()

class SiteService:

    @staticmethod
    def add_site(site: SiteInput):
        db_site = Site(
            title=site.title,
            url=site.url,
            xpath=site.xpath,
            price=0.0
        )
        db.add(db_site)
        db.commit()
        return 1

    @staticmethod
    def get_sites_without_price():
        query = select(Site).filter_by(price = 0.0)
        result = db.execute(query)
        return result.fetchall()

    @staticmethod
    def get_all_sites():
        query = select(Site.title, Site.price)
        result = db.execute(query)
        return result.fetchall()

    @staticmethod
    def update_price(site_id: int, price: float):
        query = update(Site).filter_by(id = site_id).values(price=price)
        db.execute(query)
        db.commit()
