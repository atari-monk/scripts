## Skrypt Informacji o Commitach Funkcjonalność 01 - Skrypt

### Cel

Zbuduj narzędzie CLI, które inspektuje lokalne repozytorium Git i generuje czytelne dla człowieka podsumowanie w formacie Markdown stanu katalogu roboczego (zmiany w stagingu, zmiany niezatwierdzone oraz pliki nieśledzone). Narzędzie zapisuje podsumowanie do lokalnego pliku projektu oraz opcjonalnie kopiuje je do systemowego schowka.

---

### Zmiany wymagane

- Dodaj punkt wejścia CLI (`main`), który przyjmuje:
  - `project_path` (ścieżka do repozytorium Git)
  - `description` (opis zmian w formie swobodnego tekstu)

- Dodaj abstrakcję wykonywania Git:
  - Zaimplementuj helper do uruchamiania poleceń Git przez `subprocess.Popen`
  - Musi wspierać:
    - przechwytywanie stdout/stderr
    - zwracanie kodu wyjścia
    - wykonywanie poleceń w określonym katalogu repozytorium

- Dodaj walidację repozytorium:
  - Sprawdź, czy ścieżka istnieje na dysku
  - Sprawdź, czy jest to repozytorium Git używając `git rev-parse --git-dir`

- Zaimplementuj funkcje zbierania zmian:
  - **Zmiany w stagingu**
    - Użyj `git diff --cached --name-status`
    - Parsuj linie wyjściowe w formacie:
      - `<status>\t<filepath>`
    - Mapowanie statusów:
      - `A → Dodane`
      - `M → Zmodyfikowane`
      - `D → Usunięte`
      - `R → Zmienione nazwy`
      - `C → Skopiowane`
  - **Zmiany niezatwierdzone**
    - Użyj `git diff --name-status`
    - Mapowanie statusów:
      - `M → Zmodyfikowane`
      - `D → Usunięte`
  - **Pliki nieśledzone**
    - Użyj `git ls-files --others --exclude-standard`
    - Podziel wynik na listę ścieżek plików

- Zaimplementuj generator Markdown:
  - Struktura wyjścia:
    - Tytuł: `# Git Changes Context`
    - Sekcja opisu
    - Sekcja zmian w stagingu (lista punktowana lub „Brak zmian w stagingu”)
    - Sekcja zmian niezatwierdzonych
      - Połącz zmodyfikowane/usunięte pliki niezatwierdzone z plikami nieśledzonymi oznaczonymi jako `Nieśledzone`
  - Format każdego elementu:
    - `**<ChangeType>**: \`filepath\``

- Zaimplementuj zapis do pliku:
  - Utwórz katalog: `<project_path>/.config/`
  - Zapisz plik wyjściowy:
    - `<project_path>/.config/_git-changes-context.md`
  - Nadpisz istniejący plik, jeśli występuje
  - Wypisz potwierdzenie z ścieżką pliku

- Zaimplementuj obsługę schowka:
  - Spróbuj skopiować finalny Markdown używając `xclip -selection clipboard`
  - Jeśli się powiedzie: wypisz komunikat o sukcesie
  - Jeśli `xclip` nie jest dostępny: wypisz ostrzeżenie na stderr (niekrytyczne)

- Dodaj solidną obsługę błędów:
  - Zakończ działanie z kodem różnym od zera w przypadku:
    - nieprawidłowej ścieżki
    - repozytorium nie-Git
    - nieoczekiwanych błędów wykonania
  - Wypisz błędy na stderr

---

### Kryteria akceptacji

- [ ] Uruchomienie CLI z poprawną ścieżką do repozytorium Git generuje podsumowanie zmian repozytorium w formacie Markdown
- [ ] Pliki w stagingu, niezatwierdzone i nieśledzone są poprawnie kategoryzowane i wyświetlane
- [ ] Plik wyjściowy jest tworzony w `.config/_git-changes-context.md` wewnątrz repozytorium docelowego
- [ ] Podsumowanie zawiera opis podany przez użytkownika
- [ ] Narzędzie poprawnie mapuje kody statusów Git na czytelne etykiety
- [ ] Narzędzie poprawnie obsługuje puste zestawy zmian
- [ ] Narzędzie próbuje skopiować wynik do schowka używając `xclip`
- [ ] Brak `xclip` nie powoduje awarii programu
- [ ] Nieprawidłowe ścieżki lub katalogi niebędące repozytorium Git powodują poprawne zakończenie z komunikatem błędu