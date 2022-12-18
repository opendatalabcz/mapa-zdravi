# mapa-zdravi

Aplikace predikující dostupnost zdravotnické péče v České republice na úrovni lékařských specializací.

Projekt je vytvářen jako diplomová práce na Fakultě informačních technologií ve spolupráci s laboratoří OpenDataLab.

Twitter: [Dostupnost lékařské péče v ČR](https://twitter.com/Lekari_v_CR)

---

## Instalační instrukce

0. Stáhnout [Docker](https://www.docker.com/) a [PostgreSQL](https://www.postgresql.org/download/)
1. Stáhnout projekt
2. `cd src`
3. `docker build -t mapa-zdravi .`
4. `docker run  --network="host" mapa-zdravi`
5. Otevřít v prohlížecí: http://localhost:8080
