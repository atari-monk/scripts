## Wymagania Skryptu Składacz Promptów

Wyodrębnione z kodu.

### Zachowanie interfejsu wiersza poleceń

- Program musi być uruchamiany z dokładnie dwoma argumentami wiersza poleceń: ścieżką do pliku szablonu oraz ścieżką do pliku mapowania JSON.
- Jeśli wymagane argumenty nie zostaną podane, program musi wypisać komunikat użycia na standardowe wyjście błędów i zakończyć działanie z niezerowym kodem statusu.
- Po poprawnym uruchomieniu program musi przetworzyć pliki szablonu i mapowania oraz wygenerować pojedynczy złożony wynik.
- Po pomyślnym przetworzeniu program musi wypisać komunikat potwierdzający, że wynik został skopiowany do schowka.
- Program musi zakończyć działanie z kodem statusu 0 po pomyślnym zakończeniu.

### Zachowanie parsowania include szablonu

- Program musi traktować wystąpienia `[[key]]` w szablonie jako dyrektywy include.
- Dowolny tekst poza delimitrami `[[...]]` musi być zachowany dokładnie jako literalna zawartość wyjściowa.
- Program musi dzielić szablon na naprzemienne segmenty literalne oraz tokeny include na podstawie znaczników `[[` i `]]`.
- Białe znaki wewnątrz kluczy include muszą być przycinane przed przetwarzaniem.
- Jeśli zostanie znalezione otwarcie `[[` bez odpowiadającego zamknięcia `]]`, program musi zgłosić błąd i zatrzymać wykonanie.
- Nieprawidłowe lub niezamknięte dyrektywy include muszą uniemożliwiać pomyślne złożenie.

### Zachowanie rozwiązywania mapowania

- Każdy klucz include w szablonie musi być rozwiązywany przy użyciu pliku mapowania JSON.
- Jeśli klucz nie występuje w mapowaniu lub mapuje na pustą/listę zawierającą wyłącznie białe znaki, include musi zostać pominięty i nie generować żadnego wyjścia.
- Plik mapowania może definiować katalog `root` używany jako baza do rozwiązywania ścieżek plików.
- Jeśli `root` nie zostanie podany, katalog root musi domyślnie być katalogiem zawierającym plik mapowania.

### Zachowanie rozwiązywania plików i rozwijania grup

- Każdy wpis mapowania musi reprezentować ścieżkę pliku lub wzorzec glob.
- Względne ścieżki plików muszą być rozwiązywane względem skonfigurowanego katalogu root.
- Bezwzględne ścieżki plików muszą być używane bez modyfikacji.
- Wzorce glob muszą być rozwijane rekurencyjnie w celu dopasowania plików systemu plików.
- Jeśli wzorzec glob zwróci dopasowania, wszystkie dopasowane pliki muszą zostać uwzględnione.
- Jeśli nie znaleziono dopasowań glob, program musi traktować wpis jako literalną ścieżkę i uwzględnić go tylko jeśli istnieje.
- Tylko istniejące zwykłe pliki mogą być uwzględniane w wyjściu; katalogi muszą być ignorowane.
- Zduplikowane ścieżki plików muszą być usunięte, tak aby każdy plik był uwzględniony maksymalnie raz.
- Ostateczny zbiór plików musi być posortowany przed uwzględnieniem, aby zapewnić deterministyczne wyjście.

### Zachowanie formatowania zawartości plików

- Każdy dołączony plik musi być poprzedzony linią nagłówka w formacie `# File: <file path>`.
- Pełna zawartość UTF-8 każdego pliku musi być dołączona po jego nagłówku.
- Każdy blok pliku musi być oddzielony od innych bloków dwoma znakami nowej linii.
- Ostateczna rozwinięta zawartość include musi zachowywać oryginalny tekst pliku bez modyfikacji.

### Zachowanie wyjścia składania

- Ostateczne wyjście musi być zbudowane przez konkatenację literalnych segmentów szablonu oraz rozwiniętej zawartości include w kolejności.
- Bloki include muszą być w całości zastępowane przez ich rozwiązaną zawartość plików.
- Literalne segmenty tekstu z szablonu muszą pozostać niezmienione w końcowym wyniku.
- Ostateczny złożony ciąg musi być pojedynczym, ciągłym wynikiem tekstowym.

### Zachowanie wyjścia do schowka

- Po złożeniu ostatecznego wyniku program musi skopiować rezultat do systemowego schowka używając `xclip` z opcją `-selection clipboard`.
- Złożony tekst musi być przekazany do polecenia schowka przez standardowe wejście.
- Operacja schowka musi być wykonana jako polecenie powłoki i musi zakończyć się powodzeniem, aby program mógł zakończyć działanie.
- Jeśli operacja schowka się nie powiedzie, program musi zakończyć działanie z niezerowym kodem wyjścia.

### Zachowanie obsługi błędów

- Brak zamykających delimiterów include musi zgłosić błąd runtime i zatrzymać wykonanie.
- Niepowodzenie polecenia schowka musi spowodować zakończenie programu błędem.
- Nieprawidłowe użycie wiersza poleceń musi skutkować komunikatem błędu i niezerowym kodem wyjścia.