# Mapa zdraví

Aplikace predikující dostupnost zdravotnické péče v České republice na úrovni lékařských specializací.

Projekt je vytvářen jako diplomová práce na Fakultě informačních technologií ve spolupráci s laboratoří OpenDataLab.

Twitter: [Dostupnost lékařské péče v ČR](https://twitter.com/Lekari_v_CR)

Autor: [Jan Garček](https://github.com/garcejan)

---

## Instalační instrukce

0. Stáhnout [Docker](https://www.docker.com/)
1. Stáhnout projekt
2. `$ cd src`
3. `$ docker-compose up -d`
4. `$ docker exec -i <db-container-id> pg_restore --no-owner --no-privileges -d mapa_zdravi_web -U mapazdravi_user < db.bak`
5. Otevřít v prohlížeči: http://localhost:3000

## Poznámky

Pro získání souboru db.bak kontaktujte autora. Jedná se o neveřejnou databázi s údaji vysokých škol, pojišťoven a lékařských komor ČR.
