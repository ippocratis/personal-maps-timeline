Fork of https://github.com/Rundiz/personal-maps-timeline but in docker.
All credits to @Rundiz

**Install**                               
                                                                                                                                                     
- Clone this repo 

-  Place your google timeline backup .json files in personal-maps-timeline dir.

- Run `docker compose up build -d`                                                      When the php,db and nginx containers are up and running:
                                                             
- Create the db and tables `docker exec -it db mariadb -uroot -pexample  personal_location_history < personal-maps-timeline/mariadb-structure.sql`

- Run `docker exec -it php composer update`

- Import timeline json files to db `docker exec -it php /var/www/html/import-json-to-db.php`

To retrieve place names instead of raw coords run
- `docker exec -it php php /var/www/html/retrieve-place-detail.php`

If you don't have or don't want to use a google api you can use nominatim reverse geocode and osm 

`docker exec -it php php /var/www/html/retrieve-place-detail-osm.php`

Visit localhost:8765 or the ip address of you local machine e.g. 192.168.1.24:8765
