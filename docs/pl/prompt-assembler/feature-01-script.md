## Funkcjonalność 01 Skryptu Składacz Promptów - Skrypt

### Cel

Zbuduj narzędzie CLI, które składa końcowy prompt tekstowy poprzez:

* Parsowanie szablonu zawierającego specjalne znaczniki dołączania (`[[key]]`)
* Rozpoznawanie każdego klucza w pliku mapowania JSON
* Rozwijanie każdego klucza w treść jednego lub więcej plików (poprzez ścieżki lub wzorce glob)
* Łączenie wszystkiego w jeden wyjściowy ciąg znaków
* Kopiowanie końcowego wyniku bezpośrednio do schowka systemu (poprzez `xclip`)

System jest zaprojektowany do procesów komponowania promptów, gdzie wielokrotnie używane grupy plików (np. fragmenty kodu, dokumenty, pakiety kontekstu) są dynamicznie wstrzykiwane do szablonu.

---

### Wymagane Zmiany

#### 1. Silnik Parsowania Szablonu

Dodaj logikę do parsowania surowego ciągu szablonu i podziału go na uporządkowane tokeny dwóch typów:

* **Segmenty tekstu dosłownego**
* **Dyrektywy dołączania** w formie `[[key]]`

Zasady:

* `[[key]]` oznacza blok dołączania
* Białe znaki wewnątrz klucza są przycinane
* Jeśli `[[` pojawi się bez odpowiadającego `]]`, zgłoś `ValueError("Unclosed include: missing ']]'")`
* Wynik musi zachować oryginalną kolejność tekstu i dołączeń

Struktura wyjściowa:

```python
list[tuple[bool, str]]
# (is_include, value)
```

Gdzie:

* `is_include = False` → surowy tekst
* `is_include = True` → klucz mapowania

---

#### 2. Rozpoznawanie Pliku Mapowania

Wprowadź plik mapowania JSON o strukturze:

```json
{
  "root": "/base/path",
  "some_key": [
    "path/or/pattern1",
    "path/or/pattern2"
  ]
}
```

Zachowanie:

* `root` określa katalog bazowy dla ścieżek względnych (domyślnie katalog pliku mapowania)
* Każdy klucz mapuje na listę wpisów plików:

  * ścieżki bezwzględne
  * ścieżki względne (rozpoznawane względem root)
  * wzorce glob (obsługuje rekurencyjne dopasowanie `**`)
* Puste lub brakujące listy powinny być ignorowane podczas rozwijania

---

#### 3. System Rozpoznawania Grup Plików

Zaimplementuj funkcję do rozwijania każdego klucza dołączania w blok treści plików.

Dla każdego wpisu mapowania:

* Usuń białe znaki
* Rozpoznaj ścieżkę względem `root`, jeśli nie jest bezwzględna
* Rozwiń wzorce glob przy użyciu `glob(..., recursive=True)`
* Jeśli żaden wzorzec glob nie pasuje:

  * traktuj jako bezpośrednią ścieżkę pliku, jeśli istnieje

Następnie:

* Usuń duplikaty wszystkich dopasowanych plików
* Posortuj je (leksykograficznie według Path)
* Odfiltruj elementy niebędące plikami
* Odczytaj treść plików jako UTF-8

Format wyjściowy na plik:

```
# Plik: <file_path>
<zawartość pliku>
```

Połącz wszystkie bloki plików za pomocą:

```
"\n\n"
```

---

#### 4. Silnik Składania Szablonu

Główna funkcja:

```python
assemble(template_path: Path, mapping_path: Path) -> str
```

Przebieg:

1. Załaduj plik szablonu (UTF-8)
2. Załaduj mapowanie JSON
3. Określ ścieżkę root:

   * mapping["root"] jeśli istnieje
   * w przeciwnym razie katalog pliku mapowania
4. Przetwórz szablon na tokeny
5. Dla każdego tokenu:

   * Jeśli dosłowny → dołącz bezpośrednio
   * Jeśli dołączany:

     * pobierz wpisy mapowania
     * pomiń, jeśli brakujące lub puste
     * rozwiń za pomocą resolvera plików
     * dołącz rozwiniętą treść
6. Zwróć końcowy połączony ciąg znaków (bez dodatkowego separatora między tokenami)

---

#### 5. Interfejs CLI

Dodaj punkt wejścia wiersza poleceń:

```bash
python assemble_prompt.py TEMPLATE MAP
```

Zachowanie:

* Sprawdź liczbę argumentów (musi być równa 2)
* Wywołaj `assemble()`
* Wyślij wynik do schowka za pomocą:

```bash
xclip -selection clipboard
```

poprzez:

```python
subprocess.run(..., input=result, text=True, shell=True, check=True)
```

* Wyświetl potwierdzenie:

```
Copied result to clipboard.
```

* Kody wyjścia:

  * `0` sukces
  * `1` nieprawidłowe użycie

---

#### 6. Obsługa Błędów

* Brakujące argumenty CLI → wyświetl instrukcję na stderr, wyjdź z kodem 1
* Niezamknięte `[[...]]` → zgłoś `ValueError`
* Brakujące pliki → cicho ignorowane, chyba że zostaną rozpoznane przez glob lub sprawdzenie istnienia
* Brakujący klucz mapowania → traktowane jako brak operacji (pomiń dołączenie)

---

### Kryteria Akceptacji

* [ ] Ciągi szablonu zawierające `[[key]]` są poprawnie parsowane na tokeny tekstowe i dołączane w odpowiedniej kolejności
* [ ] Mapowanie JSON poprawnie rozpoznaje klucze dołączania na listy plików
* [ ] Wzorce glob (`*`, `**`) są rozwijane rekurencyjnie
* [ ] Pliki są odduplikowane i posortowane przed odczytem
* [ ] Każdy plik jest poprzedzony prefiksem `# Plik: <path>` w wynikach
* [ ] Treści plików UTF-8 są poprawnie łączone z oddzieleniem pustymi liniami
* [ ] Brakujące lub puste wpisy mapowania są bezpiecznie pomijane
* [ ] Niezamknięte znaczniki dołączania zgłaszają jasny wyjątek
* [ ] CLI poprawnie składa wynik z szablonu i mapowania
* [ ] Końcowy wynik jest kopiowany do schowka za pomocą `xclip`
* [ ] Program kończy działanie z poprawnymi kodami statusu i wyświetla komunikat potwierdzenia