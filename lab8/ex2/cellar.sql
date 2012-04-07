PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "wine" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT ,
  "name" varchar(45) DEFAULT NULL,
  "year" varchar(45) DEFAULT NULL,
  "grapes" varchar(45) DEFAULT NULL,
  "country" varchar(45) DEFAULT NULL,
  "region" varchar(45) DEFAULT NULL,
  "description" blob,
  "picture" varchar(256) DEFAULT NULL
);
INSERT INTO "wine" VALUES(1,'CHATEAU DE SAINT COSME','2009','Grenache / Syrah','France','Southern Rhone / Gigondas','The aromas of fruit and spice give one a hint of the light drinkability of this lovely wine, which makes an excellent complement to fish dishes.','saint_cosme.jpg');
INSERT INTO "wine" VALUES(2,'LAN RIOJA CRIANZA','2006','Tempranillo','Spain','Rioja','A resurgence of interest in boutique vineyards has opened the door for this excellent foray into the dessert wine market. Light and bouncy, with a hint of black truffle, this wine will not fail to tickle the taste buds.','lan_rioja.jpg');
INSERT INTO "wine" VALUES(3,'MARGERUM SYBARITE','2010','Sauvignon Blanc','USA','California Central Cosat','The cache of a fine Cabernet in ones wine cellar can now be replaced with a childishly playful wine bubbling over with tempting tastes of
black cherry and licorice. This is a taste sure to transport you back in time.','margerum.jpg');
INSERT INTO "wine" VALUES(4,'OWEN ROE "EX UMBRIS"','2009','Syrah','USA','Washington','A one-two punch of black pepper and jalapeno will send your senses reeling, as the orange essence snaps you back to reality. Don''t miss
this award-winning taste sensation.','ex_umbris.jpg');
INSERT INTO "wine" VALUES(5,'REX HILL','2009','Pinot Noir','USA','Oregon','One cannot doubt that this will be the wine served at the Hollywood award shows, because it has undeniable star power. Be the first to catch
the debut that everyone will be talking about tomorrow.','rex_hill.jpg');
INSERT INTO "wine" VALUES(6,'VITICCIO CLASSICO RISERVA','2007','Sangiovese Merlot','Italy','Tuscany','Though soft and rounded in texture, the body of this wine is full and rich and oh-so-appealing. This delivery is even more impressive when one takes note of the tender tannins that leave the taste buds wholly satisfied.','viticcio.jpg');
INSERT INTO "wine" VALUES(7,'CHATEAU LE DOYENNE','2005','Merlot','France','Bordeaux','Though dense and chewy, this wine does not overpower with its finely balanced depth and structure. It is a truly luxurious experience for the
senses.','le_doyenne.jpg');
INSERT INTO "wine" VALUES(8,'DOMAINE DU BOUSCAT','2009','Merlot','France','Bordeaux','The light golden color of this wine belies the bright flavor it holds. A true summer wine, it begs for a picnic lunch in a sun-soaked vineyard.','bouscat.jpg');
INSERT INTO "wine" VALUES(9,'BLOCK NINE','2009','Pinot Noir','USA','California','With hints of ginger and spice, this wine makes an excellent complement to light appetizer and dessert fare for a holiday gathering.','block_nine.jpg');
INSERT INTO "wine" VALUES(10,'DOMAINE SERENE','2007','Pinot Noir','USA','Oregon','Though subtle in its complexities, this wine is sure to please a wide range of enthusiasts. Notes of pomegranate will delight as the nutty finish completes the picture of a fine sipping experience.','domaine_serene.jpg');
INSERT INTO "wine" VALUES(11,'BODEGA LURTON','2011','Pinot Gris','Argentina','Mendoza','Solid notes of black currant blended with a light citrus make this wine an easy pour for varied palates.','bodega_lurton.jpg');
INSERT INTO "wine" VALUES(12,'LES MORIZOTTES','2009','Chardonnay','France','Burgundy','Breaking the mold of the classics, this offering will surprise and undoubtedly get tongues wagging with the hints of coffee and tobacco in
perfect alignment with more traditional notes. Breaking the mold of the classics, this offering will surprise and
undoubtedly get tongues wagging with the hints of coffee and tobacco in
perfect alignment with more traditional notes. Sure to please the late-night crowd with the slight jolt of adrenaline it brings.','morizottes.jpg');
COMMIT;