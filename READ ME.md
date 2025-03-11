# Lego Speed Champions Tracker

## 📄 Projektbeschreibung
Dieses Programm ist ein **Lego Speed Champions Tracker**, mit dem du deine Sammlung von Lego Speed Champions-Sets verwalten kannst. Die Anwendung ermöglicht es dir, Sets zu **hinzufügen**, **bearbeiten**, **löschen**, und **zu filtern**. Zudem werden **Statistiken** zur Sammlung angezeigt und eine **grafische Darstellung** in Form eines Kreisdiagramms zur Verteilung der Marken angeboten.

Die Daten werden in einer JSON-Datei (`lego_speed_champions.json`) gespeichert und können jederzeit aktualisiert werden.

## 📚 Funktionen
### 1. **Hinzufügen & Bearbeiten von Einträgen**
- Neue Lego-Sets können über die Eingabemaske hinzugefügt werden.
- Bereits existierende Sets können durch Auswahl in der Liste bearbeitet werden.
- Änderungen werden in der JSON-Datei gespeichert.

### 2. **Löschen von Einträgen**
- Markiere einen Eintrag in der Liste und drücke auf "Delete", um ihn zu entfernen.
- Das Löschen eines Eintrags ist unwiderruflich.

### 3. **Filterfunktion**
- Filtere die Liste anhand folgender Kriterien:
  - **Marke** (z. B. Ferrari, Porsche, Audi)
  - **Breite** (6 oder 8 Noppen)
  - **Erscheinungsdatum** (z. B. 03.2024)
  - **Teileanzahl** (mit Auswahl ob größer oder kleiner als eine bestimmte Anzahl)
  - **Anzahl der Autos im Set**
  - **Besitzt du das Set?** (Checkbox-Filter)
- Die Filterung erfolgt über Dropdown-Menüs und Eingabefelder.

### 4. **Statistiken**
- Gesamtanzahl an **Teilen** in der Sammlung.
- Gesamtpreis der Sets.
- Gesamtanzahl der **Autos** in der Sammlung.
- Statistiken werden automatisch nach jeder Änderung aktualisiert.

### 5. **Kreisdiagramm der Markenverteilung**
- Zeigt eine grafische Aufteilung der Lego-Sets nach Marke.
- Ermöglicht eine visuelle Analyse der Sammlung.

## 🛠️ Installation & Start
### **Voraussetzungen**
- **Python 3.x** installiert
- **Benötigte Bibliotheken:** `tkinter`, `matplotlib`, `json`, `os`
- Falls `matplotlib` nicht installiert ist, kann es mit folgendem Befehl nachinstalliert werden:
  ```sh
  pip install matplotlib
  ```

### **Start der Anwendung**
1. Stelle sicher, dass sich `speedchampionsTracker.py` und `lego_speed_champions.json` im gleichen Verzeichnis befinden.
2. Öffne ein Terminal und führe das Skript aus:
   ```sh
   python speedchampionsTracker.py
   ```
3. Die Benutzeroberfläche öffnet sich und du kannst deine Lego-Sammlung verwalten.

## 🔧 Technische Details
- **GUI**: Erstellt mit `tkinter`
- **Datenverwaltung**: JSON-Datei als persistenter Speicher
- **Filterung**: Dynamisch über `tkinter`-Widgets
- **Diagramme**: Erstellt mit `matplotlib`
- **Automatische Preisformatierung**: Sucht nach Preisen im `€xx.xx`-Format mit regulären Ausdrücken (`re`-Modul)

## 💡 Hinweise zur Nutzung
- Beim Bearbeiten oder Hinzufügen eines Sets müssen alle Pflichtfelder ausgefüllt werden.
- Die JSON-Datei wird **automatisch aktualisiert**, Änderungen sind nach einem Neustart weiterhin verfügbar.
- Falls Probleme auftreten, überprüfe die **JSON-Datei** auf korrekte Formatierung.

Viel Spaß mit dem Lego Speed Champions Tracker! 🚗💨


