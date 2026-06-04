## Dokumentacja Skryptu Składacz Promptów

Składacz szablonów, który rozwija tokeny include na zawartości plików i kopiuje wynik do schowka.

### Co robi

- Czyta plik szablonu zawierający specjalne znaczniki include w formie `[[key]]`
- Ładuje plik mapowania JSON, który definiuje, które pliki należą do każdego klucza
- Rozwiązuje ścieżki plików (w tym wzorce glob) względem konfigurowalnego katalogu głównego
- Zastępuje każdy `[[key]]` w szablonie połączoną zawartością pasujących plików
- Kopiuje końcowy złożony wynik do schowka systemowego za pomocą `xclip`

Ten skrypt jest zwykle używany do budowania pakietów promptów lub dokumentów z wielu plików źródłowych w powtarzalny sposób.

### Jak go uruchomić

```bash
python assemble_prompt.py TEMPLATE MAP
```

> Wymaga zainstalowanego `xclip` dostępnego w ścieżce systemowej PATH.

### Wejścia

- `TEMPLATE`
  - Ścieżka do pliku szablonu tekstowego
  - Zawiera zwykły tekst i znaczniki include, takie jak `[[section_name]]`

- `MAP`
  - Ścieżka do pliku mapowania JSON
  - Przykład struktury:
    ```json
    {
      "root": "./base_dir",
      "section_name": [
        "file1.txt",
        "dir/*.md"
      ]
    }
    ```

  - Pola:
    - `root` (opcjonalne): katalog bazowy do rozwiązywania ścieżek względnych
    - klucze: odpowiadają znacznikom include w szablonie
    - wartości: lista ścieżek plików lub wzorców glob

### Wyjścia

- Końcowy złożony tekst jest:
  - Wypisywany do schowka systemowego (przez `xclip -selection clipboard`)
  - Nie zapisywany na dysku, chyba że zostanie przekierowany zewnętrznie
- Wyjście terminala:
  - `Copied result to clipboard.` w przypadku powodzenia

### Przykład

```bash
python assemble_prompt.py prompt_template.txt mapping.json
```