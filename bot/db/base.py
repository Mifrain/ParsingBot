from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bot.config import settings


engine = create_engine(settings.DB_URL)
# engine = create_engine("sqlite:///sites.db")

sync_session = sessionmaker(bind=engine)

Base = declarative_base()


# Пример использования
# if __name__ == "__main__":
#     db = SessionLocal()
#     sites = read_excel_to_models(Path("sites.xlsx"))
#     for site in sites:
#         create_site(db, site)
#
#     print(get_all_sites(db))
