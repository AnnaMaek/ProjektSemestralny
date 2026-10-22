SPECYFIKACJA APLIKACJI 

Analiza działań niepożądanych leków z grupy GLP-1

1. Cel aplikacji

Celem aplikacji jest analiza zgłoszeń dotyczących działań niepożądanych leków z grupy GLP-1.

Aplikacja umożliwia przegląd danych, filtrowanie zgłoszeń, obliczanie statystyk, prezentację wyników w formie wykresów, pobieranie raportu w formacie PDF oraz eksport przefiltrowanych danych do pliku CSV.

2. Opis aplikacji

Aplikacja została napisana w języku Python.

Do przetwarzania i analizy danych wykorzystano bibliotekę pandas, natomiast do tworzenia wizualizacji — biblioteki Matplotlib i Seaborn. Interfejs graficzny został wykonany z wykorzystaniem biblioteki Streamlit.

Użytkownik korzysta z aplikacji za pośrednictwem przeglądarki internetowej.

Interfejs składa się z panelu bocznego, w którym znajdują się filtry, oraz głównego obszaru roboczego zawierającego trzy zakładki: "Podsumowanie", "Wizualizacje" i "Dane".

3. Główne funkcjonalności

Aplikacja umożliwia:

- filtrowanie zgłoszeń według substancji czynnej i nazwy handlowej;
- filtrowanie według płci i wieku;
- filtrowanie według powagi działania niepożądanego;
- prezentację podstawowych statystyk dla przefiltrowanych danych;
- wyświetlenie listy najczęściej zgłaszanych działań niepożądanych;
- prezentację danych na wykresach;
- przegląd danych w formie tabeli;
- eksport wybranych danych do pliku CSV;
- generowanie raportu z analizy w formacie PDF.

4. Dane wejściowe

Aplikacja korzysta z pliku CSV zawierającego zgłoszenia działań niepożądanych dla leków z grupy GLP-1.

Dane są wczytywane i przetwarzane przy użyciu biblioteki pandas. 
Źródłem danych jest plik udostępniony w serwisie Kaggle.

5. Filtrowanie danych

Filtry dostępne w panelu bocznym umożliwiają wybór:

- substancji czynnej;
- nazwy handlowej leku;
- płci pacjenta;
- minimalnego i maksymalnego wieku pacjenta;
- powagi działania niepożądanego.

Dodatkowo dostępny jest checkbox pozwalający uwzględnić zgłoszenia, w których nie podano wieku pacjenta.

Wybór substancji czynnej ogranicza listę dostępnych nazw handlowych do preparatów zawierających wybraną substancję. Jeżeli dostępna jest tylko jedna nazwa handlowa, zostaje ona ustawiona automatycznie.

Analogicznie, wybór nazwy handlowej może automatycznie ustawić odpowiadającą jej substancję czynną. Zmiana jednego z tych filtrów na opcję "Wszystkie" powoduje wyzerowanie drugiego, zależnego wyboru.

Minimalny wiek ustawiono na 12 lat, a maksymalny na 120 lat. Wartości te określają zakres dostępny w filtrach aplikacji. Ustawiony wiek minimalny wynika ze wskazań zamieszczonych w Charakterystykach Produktów Leczniczych dla poszczególnych leków.

Plik CSV zawiera zgłoszenia bez podanego wieku pacjenta. Z tego względu udostępniono checkbox umożliwiający uwzględnienie takich rekordów w analizie.

Zastosowanie filtrów wpływa na wyniki prezentowane we wszystkich zakładkach:

- w zakładce "Podsumowanie" — na statystyki i opis wyników;
- w zakładce "Wizualizacje" — na prezentowane wykresy;
- w zakładce "Dane" — na rekordy wyświetlane w tabeli.


6. Zakładka "Podsumowanie"

Zakładka "Podsumowanie" zawiera podstawowe informacje o danych oraz wyniki analizy po zastosowaniu filtrów.

W pierwszej części prezentowane są:

- liczba unikalnych zgłoszeń;
- liczba zgłoszonych działań niepożądanych;
- liczba substancji czynnych, których dotyczą zgłoszenia.

Druga część przedstawia wyniki dla aktualnie przefiltrowanych danych. Na początku wyświetlany jest krótki opis zastosowanych filtrów. 
 
Następnie prezentowane są obliczone statystyki:

- średni wiek pacjentów;
- mediana wieku pacjentów;
- średnia masa ciała;
- liczba działań niepożądanych.

Poniżej znajduje się lista 15 najczęściej występujących działań niepożądanych wraz z liczbą ich wystąpień.

Na końcu zakładki użytkownik może pobrać raport dotyczący przefiltrowanych danych w formacie PDF. Raport jest generowany przy użyciu biblioteki ReportLab. W celu prawidłowego wyświetlania polskich znaków zastosowano odpowiednie czcionki.

7. Zakładka "Wizualizacje"

Zakładka "Wizualizacje" zawiera sześć wykresów:

- Liczba zgłoszeń według substancji czynnej — wykres słupkowy.
- Rozkład wieku pacjentów — histogram.
- Liczba zgłoszeń według płci — wykres słupkowy.
- Zależność wieku i masy ciała — wykres rozrzutu.
- Rozkład masy ciała według płci — wykres pudełkowy.
- 15 najczęściej zgłaszanych działań niepożądanych — wykres słupkowy poziomy.

Wykresy są aktualizowane w zależności od zastosowanych filtrów, dzięki czemu użytkownik może analizować wybrane grupy zgłoszeń.

8. Zakładka "Dane"

Zakładka "Dane" wyświetla tabelę zawierającą rekordy poddawane analizie. Prezentowane dane zależą od ustawień filtrów w panelu bocznym.

Użytkownik może również pobrać przefiltrowane dane do pliku CSV.

9. Ograniczenia aplikacji

Źródłem danych jest plik CSV zawierający zgłoszenia działań niepożądanych dla leków z grupy GLP-1, pobrany z serwisu Kaggle. Wyniki analizy mogą być ograniczone przez jakość i kompletność danych źródłowych. 

W trakcie przygotowywania zbioru usunięto kilka błędnych rekordów zawierających niekompletne lub nieprawidłowe wartości.
Przykładami były zgłoszenia z nierealistyczną masą ciała, wynoszącą 87 ton lub 8 kg. Rekordy te wyłączono z analizy na etapie przygotowania danych. 

Zgłoszenie działania niepożądanego nie oznacza automatycznie, że zostało ono spowodowane przez dany lek. Wyniki przedstawiają analizę dostępnych zgłoszeń i należy je interpretować z uwzględnieniem ograniczeń zbioru danych.