SPECYFIKACJA APLIKACJI 

Analiza działań niepożądanych leków z grupy GLP-1

1. Cel aplikacji

Celem aplikacji jest analiza zgłoszeń dotyczących działań niepożądanych leków z grupy GLP-1.
Aplikacja umożliwia przegląd danych, filtrowanie zgłoszeń, obliczanie statystyk, prezentacje wyników w formie wykresów, pobranie raportu w formacie PDF oraz przefitrowanych danych w formacie CSV.

2. Opis aplikacji

Aplikacja została napisana w języku Python. Dane są przetwarzane przy pomocy bibliotek pandas, matplotlib, seaborn. GUI zostało wykonane z wykorzystaniem biblioteki Streamlit. 
Użytkownik korzysta z aplikacji przez interfejs w przeglądarce internetowej. 
Aplikacja posiada pasek boczny gdzie są dostępne filtry.
W głównym oknie są trzy zakładki: podsumowanie, wizualizacje i dane. 

3. Główne funkcjonalności

Aplikacja umożliwia:
- filtrowanie zgłoszeń według substancji czynnej
- filtrowanie według nazwy handlowej
- filtrowanie według płci i wieku
- filtrowanie według powagi działania niepożądanego
- prezentację podstawowych statystyk dla przfiltrowanych danych
- utworzenie listy najczęsciej zgłaszanych działań niepożadanych dla wybranej grupy pacjentów
- prezentację danych na wykresach
- przegląd danych w formie tabeli
- eksport wybranych wyników do pliku CSV
- generowanie raportu analizy w formacie PDF

4. Dane wejściowe

Aplikacja korzysta z załączonego pliku csv zawierającego zgłoszenia działań niepożadanych.
Dane z pliku zostały wczytane i przetworzane przy pomocy biblioteki pandas. 

5. Filtrowanie danych

Filtry dostępne w panelu bocznym umożliwiają ustalenie takich parametrów jak:
- substancja chemiczna
- nazwa handlowa leku
- płeć
- wiek minimalny oraz wiek maksymalny 
- checbox pozwala uwzględnić zgłoszenia bez podanego wieku pacjenta
- powaga działania niepożądanego

Wybór substancji chemicznej ogranicza wybór nazwy handlowej do preparatów zawierających wybraną substancję. Jeśli jest tylko jedna możliwość do wyboru, to zostaje ona ustawiona automatycznie. Podobny schemat działa w drugą stronę, gdzie wybór nazwy handlowej automatycznie ustawia pasującą do niej nazwę substancji chemicznej. Zmiana jednego z wymienionych filtrów na "wszystkie" powoduje wyzerowanie drugiego zależnego wyboru. 

Wiek minimalny został ustawiony na 12 lat, ponieważ analizowane leki są przeznaczone dla pacjentów powyżej 12 roku życia. 
Wiek maksymalny ustawiono na 120 lat.

Plik CSV zawierał zgłoszenia bez podanego wieku pacjenta, stąd checkbox umożliwiający dodanie takich zgłoszeń do analizy. 

Filtrowanie danych wpływa na wyniki prezentowane w zakładkach aplikacji: statystyki i opis w zakładce "podsumowanie", wykresy w zakładce "wizualizacje" oraz prezentowane w tabeli dane, w zakładce "dane". 

6. Zakładka "Podsumowanie"

Część pierwsza wyświetla podstawowe informacje dotyczące liczby unikalnych zgłoszeń, liczby zgłoszonych działań niepożadanych oraz ilości substancji czynnych, których dotyczą te zgłoszenia.

Cześć druga opisuje wynik filtrowania. 
Na wstępie jest krótki opis zastosowanych filtrów. 
Następnie prezentowane są obliczone statyski: średni wiek, mediana wieku, średnia masa ciała oraz liczba działań niepożądanych. 
Poniżej znajduje się lista 15 najczęściej występujących działań niepożadanych wraz z liczbą wystapień.

Na końcu jest możliwość pobrania raportu dotyczącego przefiltrowanych danych w formacie PDF.  Raport PDF tworzony jest przy użyciu biblioteki ReportLab. Do obsługi polskich znaków zostały zainstalowane odpowiednie czcionki.

7. Zakładka "Wizualizacje"

Aplikacja wyświetla 6 wykresów:
    1) Liczba zgłoszeń według substancji czynnej  - wykres słupkowy
    2) Rozkład wieku pacjetów - histogram
    3) Liczba zgłoszeń według płci - wykres słupkowy
    4) Zależność wieku i masy ciała - wykres rozrzutu
    5) Rozkład masy ciała według płci - wykres pudełkowy    
    6) 15 najczęściej zgłaszanych działań niepożądanych - wykres słupkowy poziomy
Wykresy są aktualizowane w zależności od zastosowanych filtrów. 

8. Zakładka "Dane"

Wyświetla tabelę CSV na której prowadzona jest analiza. Wyświetlane dane zależne są od wybranych filtrów. 
Można pobrać przefiltrowane dane do pliku CSV. 
