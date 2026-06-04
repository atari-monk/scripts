## Dokumentacja skryptu Inicjalizator Struktury

Inicjalizuje strukturę projektu (foldery i pliki) na podstawie konfiguracji JSON.

### Co robi

- Odczytuje plik konfiguracji JSON opisujący strukturę projektu
- Tworzy zestaw folderów i plików w katalogu bazowym
- Zapewnia, że istniejące foldery/pliki nie są tworzone ponownie
- Wyświetla komunikaty o statusie dla każdego utworzonego lub istniejącego elementu

Ten skrypt jest przydatny do szybkiego tworzenia szkieletu układu projektu w spójny i powtarzalny sposób.

### Jak go uruchomić

```bash
powershell -File script.ps1 -ConfigPath path/to/config.json
```

### Wejścia

* Plik konfiguracji JSON przekazany przez `-ConfigPath`
* Przykład struktury JSON:

  * `basePath`: katalog główny projektu
  * `folders`: tablica ścieżek folderów względnych względem `basePath`
  * `files`: tablica ścieżek plików względnych względem `basePath`

Przykład:

* `config.json`

### Wyjścia

* Tworzy foldery w określonym `basePath`
* Tworzy pliki w określonym `basePath`
* Dane wyjściowe konsoli wskazujące:

  * Ścieżki utworzonych folderów/plików
  * Informacje o istniejących folderach/plikach
  * Komunikat zakończenia: `Init project complete`

### Przykład

```bash
powershell -File script.ps1 -ConfigPath .\config.json
```