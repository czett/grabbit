# grabbit - Ein Shopping-Bewertungstool

**grabbit** ist eine Plattform, auf der Benutzer ihre Einkäufe in verschiedenen Geschäften posten können, um zu zeigen, wie viel sie im Vergleich zum normalen Preis gespart haben. Benutzer können die Geschäfte auf einer interaktiven Karte sehen, Bewertungen hinterlassen und nachsehen, wie andere Einkäufer ähnliche Produkte bewertet haben.

## Features

- **Einkäufe posten:** Benutzer können ihre Einkäufe im Detail posten, einschließlich des bezahlten Preises, des üblichen Preises, der gesparten Abteilungen und eines optionalen Kommentars.
- **Interaktive Karte:** Alle geposteten Einkäufe erscheinen auf einer Karte, die es den Benutzern ermöglicht, zu den jeweiligen Geschäften zu navigieren und die gespeicherten Informationen einzusehen.
- **Bewertungen und Kommentare:** Nutzer können Geschäfte und deren Produkte bewerten, indem sie die Sauberkeit, Vorräte und Privatsphäre bewerten und Kommentare hinterlassen.
- **Store Finder:** Benutzer können über die Karte alle verfügbaren Geschäfte finden, die von anderen Nutzern bewertet wurden. Die Karte zeigt Pins für jedes Geschäft, das eine Bewertung hat.
- **Speichern und Vergleichen:** Ein Klick auf einen Pin führt den Benutzer zur Detailseite des Stores, wo er alle relevanten Informationen und Kommentare einsehen kann.
- **Benutzerprofile:** Jeder Nutzer hat ein Profil, in dem er eine Liste seiner Bewertungen und Einkäufe einsehen kann.
- **Günstige Deals:** Das Tool zeigt den "Multiplikator" für jedes gepostete Produkt, d.h. das Verhältnis zwischen dem bezahlten Preis und dem üblichen Preis, um den Nutzern zu zeigen, wie viel sie im Vergleich zum regulären Preis gespart haben.

## Technische Details

- **Backend:** Das Projekt verwendet Python mit Flask für das Backend, das alle serverseitigen Anfragen verarbeitet, Datenspeicherung und Business-Logik steuert.
- **Datenbank:** Alle Bewertungen, Einkäufe und Geschäfte werden in einer relationalen Datenbank gespeichert (PostgreSQL oder SQLite).
- **Karte:** Die interaktive Karte wird mit Leaflet.js erstellt und nutzt OpenStreetMap-Tiles.
- **User-Authentifizierung:** Nutzer können sich einloggen und ihre Einkäufe sowie Bewertungen verwalten.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.
