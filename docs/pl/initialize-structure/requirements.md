## Wymagania Skryptu Inicjalizator Struktury

### Wywołanie skryptu i dane wejściowe

* Wymaga obowiązkowego parametru `ConfigPath` określającego ścieżkę do pliku konfiguracyjnego.
* Przyjmuje ścieżkę do pliku konfiguracyjnego i używa jej jako jedynego wejścia do sterowania całym zachowaniem inicjalizacji.

### Ładowanie i walidacja konfiguracji

* Odczytuje plik konfiguracyjny JSON z podanej ścieżki.
* Zgłasza błąd, gdy plik konfiguracyjny nie istnieje.
* Wyodrębnia bazową ścieżkę, listę ścieżek folderów oraz listę ścieżek plików z konfiguracji.

### Rozwiązywanie ścieżek

* Rozwiązuje wszystkie ścieżki folderów i plików względem skonfigurowanej ścieżki bazowej.

### Zachowanie tworzenia katalogów

* Tworzy każdy folder zdefiniowany w konfiguracji, jeśli jeszcze nie istnieje.
* Nie modyfikuje istniejących folderów, gdy już istnieją.
* Wyświetla komunikat informujący o utworzeniu folderu.
* Wyświetla komunikat informujący, gdy folder już istnieje.

### Zachowanie tworzenia plików

* Tworzy każdy plik zdefiniowany w konfiguracji, jeśli jeszcze nie istnieje.
* Nie modyfikuje istniejących plików, gdy już istnieją.
* Wyświetla komunikat informujący o utworzeniu pliku.
* Wyświetla komunikat informujący, gdy plik już istnieje.

### Przepływ wykonania i zakończenie

* Inicjalizuje wszystkie foldery przed utworzeniem jakichkolwiek plików.
* Przetwarza wszystkie skonfigurowane foldery i pliki dokładnie jeden raz podczas każdego wykonania.
* Wyświetla komunikat zakończenia po pomyślnym zakończeniu inicjalizacji projektu.