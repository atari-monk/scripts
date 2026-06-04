## Wymagania Skryptu Informacji o Commitach

### Interfejs wiersza poleceń

* Przyjmuje wymagany argument `project_path` wskazujący na katalog docelowy.
* Przyjmuje wymagany argument `description` opisujący zmiany.
* Rozwiązuje podaną ścieżkę projektu do ścieżki bezwzględnej przed przetwarzaniem.

### Walidacja repozytorium

* Wyświetla błąd i kończy działanie, jeśli podana ścieżka nie istnieje.
* Wyświetla błąd i kończy działanie, jeśli podana ścieżka nie jest poprawnym Git repository.
* Używa Git commands do określenia poprawności repozytorium.

### Detekcja zmian Git (Zmiany staged)

* Pobiera staged file changes z repozytorium Git.
* Kategoryzuje zmiany staged na czytelne dla człowieka typy: Added, Modified, Deleted, Renamed i Copied.
* W przypadku nierozpoznanego typu zmiany używa surowej wartości statusu.
* Nie tworzy żadnych wpisów staged-change, gdy nie istnieją zmiany staged.

### Detekcja zmian Git (Zmiany unstaged)

* Pobiera unstaged file changes z repozytorium Git.
* Uwzględnia modyfikacje i usunięcia w unstaged changes.
* Oznacza nieznane lub nierozpoznane typy zmian przy użyciu ich surowego wskaźnika statusu.
* Nie tworzy żadnych wpisów unstaged-change, gdy nie istnieją unstaged changes.

### Wykrywanie nieśledzonych plików

* Pobiera untracked files z repozytorium Git.
* Uwzględnia untracked files w sekcji unstaged changes oznaczone jako “Untracked”.
* Nie wyświetla żadnych wpisów untracked, gdy nie są obecne.

### Generowanie podsumowania Markdown

* Generuje podsumowanie Git changes w formacie Markdown.
* Uwzględnia podany description w wynikach.
* Dzieli treść na sekcje staged changes i unstaged changes.
* Formatuje każdy wpis pliku jako punkt listy z typem zmiany i ścieżką pliku.
* Wyświetla komunikat zastępczy, gdy nie istnieją staged lub unstaged changes.

### Generowanie pliku wyjściowego

* Zapisuje wygenerowane podsumowanie Markdown do `.config/_git-changes-context.md` w katalogu docelowego projektu.
* Tworzy katalog `.config`, jeśli jeszcze nie istnieje.
* Wyświetla lokalizację pliku wyjściowego po zapisaniu.

### Integracja ze schowkiem

* Próbuje skopiować wygenerowane podsumowanie Markdown do systemowego schowka używając `xclip`.
* Wyświetla komunikat o sukcesie, gdy kopiowanie do schowka się powiedzie.
* Wyświetla ostrzeżenie, jeśli funkcjonalność schowka jest niedostępna.

### Obsługa błędów

* Obsługuje nieoczekiwane błędy czasu wykonania w sposób elegancki.
* Wyświetla komunikaty błędów na standardowe wyjście błędów.
* Kończy działanie z niezerowym kodem statusu w przypadku błędu.