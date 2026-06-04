## Dokumentacja Skryptu Informacji o Commitach

Generuje uporządkowane podsumowanie Markdown zmian Git w stanie staged, unstaged i untracked dla repozytorium oraz opcjonalnie kopiuje je do schowka.

### Co robi

- Zbiera stan repozytorium Git używając `git diff` i powiązanych poleceń
- Dzieli zmiany na pliki staged, unstaged i untracked
- Konwertuje wynik na czytelny raport Markdown
- Zapisuje raport do lokalnego pliku w repozytorium
- Opcjonalnie kopiuje wynik do schowka używając `xclip`

Ten skrypt jest przydatny do szybkiego generowania podsumowania kontekstu gotowego do commita, szczególnie podczas przygotowywania wiadomości commitów lub przeglądania zmian.

### Jak go uruchomić

```bash
python3 script.py /path/to/repo "Your change description"
```

### Dane wejściowe

* `project_path`: Ścieżka do docelowego repozytorium Git
* `description`: Krótki tekst opisujący zmiany

Opcjonalne zależności:

* `git` (musi być zainstalowany i dostępny w PATH)
* `xclip` (opcjonalnie, dla obsługi schowka w Linux)

### Dane wyjściowe

* Plik Markdown zapisany do:

  ```
  <project_path>/.config/_git-changes-context.md
  ```

* Wyjście terminala:

  * Komunikat o sukcesie z lokalizacją pliku
  * Ostrzeżenie, jeśli brakuje narzędzia schowka
  * Błędy, jeśli ścieżka jest nieprawidłowa lub nie jest repozytorium Git

* Schowek (opcjonalnie):

  * Pełne podsumowanie Markdown skopiowane przez `xclip`

### Przykład

```bash
python3 git_changes.py ~/projects/my-app "Refactored authentication flow and fixed login bug"
```