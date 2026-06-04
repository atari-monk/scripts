## Skrypt Inicjalizator Struktury Funkcjonalność 01 - Skrypt

### Cel

Zaimplementuj narzędzie wiersza poleceń, które inicjalizuje strukturę katalogów projektu na podstawie pliku konfiguracyjnego JSON. Narzędzie powinno tworzyć zestaw folderów i plików w określonej ścieżce bazowej, zapewniając idempotentne zachowanie (istniejące pliki/foldery nie są nadpisywane) oraz zapewniać informacje zwrotne w konsoli dla każdej operacji.

### Wymagane zmiany

* Dodaj punkt wejścia CLI, który przyjmuje jeden obowiązkowy parametr: `ConfigPath` (ścieżka do pliku konfiguracyjnego JSON).
* Dodaj logikę ładowania konfiguracji, która:

  * Weryfikuje istnienie pliku konfiguracyjnego.
  * Parsuje JSON do wewnętrznego modelu konfiguracji z:

    * `basePath` (string)
    * `folders` (tablica stringów ścieżek względnych)
    * `files` (tablica stringów ścieżek względnych)
* Dodaj narzędzie do rozwiązywania ścieżek:

  * Połącz `basePath` z każdą względną ścieżką folderu/pliku w pełną ścieżkę systemu plików.
* Dodaj logikę inicjalizacji folderów:

  * Twórz katalogi, jeśli nie istnieją.
  * Pomijaj tworzenie, jeśli już istnieją.
  * Loguj komunikaty statusu do konsoli.
* Dodaj logikę inicjalizacji plików:

  * Twórz pliki, jeśli nie istnieją.
  * Pomijaj tworzenie, jeśli już istnieją.
  * Loguj komunikaty statusu do konsoli.
* Dodaj warstwę orkiestracji (odpowiednik funkcji `main`), która:

  * Ładuje konfigurację
  * Inicjalizuje foldery
  * Inicjalizuje pliki
  * Wypisuje komunikat zakończenia
* Zapewnij, że wszystkie operacje są bezpieczne do ponownego uruchomienia (zachowanie idempotentne).

### Plan implementacji

#### 1. Schemat konfiguracji

Oczekiwana struktura JSON:

```json
{
  "basePath": "string",
  "folders": ["relative/path/one", "relative/path/two"],
  "files": ["relative/file1.txt", "relative/file2.txt"]
}
```

#### 2. Komponenty główne

**Ładowanie konfiguracji**

* Wejście: `ConfigPath`
* Kroki:

  * Sprawdź istnienie pliku
  * Odczytaj całą zawartość pliku
  * Sparsuj JSON
  * Mapuj do struktury wewnętrznej:

    * basePath
    * folders[]
    * files[]
* Obsługa błędów:

  * Rzuć błąd, jeśli plik nie istnieje

**Rozwiązywanie ścieżek**

* Wejście: `basePath`, `relativePath`
* Wyjście: pełna/połączona ścieżka systemu plików
* Zachowanie:

  * Użyj standardowej semantyki łączenia ścieżek (bezpiecznej dla systemu operacyjnego)

**Tworzenie folderów**

* Wejście: pełna ścieżka folderu
* Zachowanie:

  * Jeśli ścieżka nie istnieje jako katalog → utwórz ją
  * Jeśli istnieje → nic nie rób
  * Wypisz:

    * "Utworzono folder: X"
    * lub "Folder już istnieje: X"

**Tworzenie plików**

* Wejście: pełna ścieżka pliku
* Zachowanie:

  * Jeśli plik nie istnieje → utwórz pusty plik
  * Jeśli istnieje → nic nie rób
  * Wypisz:

    * "Utworzono plik: X"
    * lub "Plik już istnieje: X"

#### 3. Przepływ inicjalizacji

1. Sparsuj argument CLI `ConfigPath`
2. Załaduj konfigurację
3. Dla każdego folderu w konfiguracji:

   * Rozwiąż pełną ścieżkę
   * Utwórz folder jeśli potrzebny
4. Dla każdego pliku w konfiguracji:

   * Rozwiąż pełną ścieżkę
   * Utwórz plik jeśli potrzebny
5. Wypisz komunikat zakończenia:

   * "Inicjalizacja projektu zakończona"

#### 4. Zachowanie wykonania

* Musi być uruchamialne jako samodzielny skrypt.
* Musi wspierać wielokrotne uruchomienie bez efektów ubocznych poza tworzeniem brakującej struktury.
* Nie może nadpisywać istniejących plików ani katalogów.

### Kryteria akceptacji

* [ ] Skrypt przyjmuje wymagany argument `ConfigPath` i kończy działanie błędem, jeśli nie został podany.
* [ ] Skrypt waliduje istnienie pliku konfiguracyjnego przed wykonaniem.
* [ ] Konfiguracja JSON jest poprawnie parsowana do `basePath`, `folders` i `files`.
* [ ] Wszystkie ścieżki folderów są tworzone względem `basePath`.
* [ ] Wszystkie ścieżki plików są tworzone względem `basePath`.
* [ ] Istniejące foldery nie są ponownie tworzone ani modyfikowane.
* [ ] Istniejące pliki nie są nadpisywane.
* [ ] Wyjście konsoli jest generowane dla każdej operacji utworzenia/pominięcia.
* [ ] Skrypt wypisuje "Inicjalizacja projektu zakończona" po pomyślnym wykonaniu.
* [ ] Cały proces jest idempotentny przy wielokrotnych uruchomieniach.